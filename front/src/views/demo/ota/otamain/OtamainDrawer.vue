<template>
  <BasicDrawer
    v-bind="$attrs"
    @register="registerDrawer"
    showFooter
    :title="getTitle"
    width="500px"
    @ok="handleSubmit"
  >
    <BasicForm @register="registerForm" />
  </BasicDrawer>
</template>
<script lang="ts">
  import { defineComponent, ref, computed, unref } from 'vue';
  import { BasicForm, useForm } from '/@/components/Form/index';
  import { otaFormSchema } from './otamain.data';
  import { BasicDrawer, useDrawerInner } from '/@/components/Drawer';
  import { updateOtamain } from '/@/api/demo/otamain';

  //components: BasicTree
  export default defineComponent({
    name: 'OtamainDrawer',
    components: { BasicDrawer, BasicForm },
    emits: ['success', 'register'],
    setup(_, { emit }) {
      const isUpdate = ref(true);

      const [registerForm, { resetFields, setFieldsValue, validate }] = useForm({
        labelWidth: 90,
        schemas: otaFormSchema,
        showActionButtonGroup: false,
      });

      const [registerDrawer, { setDrawerProps, closeDrawer }] = useDrawerInner(async (data) => {
        resetFields();
        setDrawerProps({ confirmLoading: false });
        isUpdate.value = !!data?.isUpdate;

        //修改传递给编辑页面的data.record数据，把image从字符串改成数组
        //因为Upload组件，它的value值，必须是数组，无奈啊。。。
        const datachange: any[] = [];
        for (const key in data.record) {
          type KeyType = keyof typeof data.record;
          const initialValue = data.record[key as KeyType];
          if (key === 'ota_image') {
            datachange[key as KeyType] = [initialValue]; //加个[]改成数组
          } else {
            datachange[key as KeyType] = initialValue;
          }
        }
        //console.log(datachange);
        if (unref(isUpdate)) {
          setFieldsValue({
            ...datachange, //data.record改成datachange
          });
        }
      });

      const getTitle = computed(() => (!unref(isUpdate) ? '新增OTA' : '编辑OTA'));

      async function handleSubmit() {
        try {
          const values = await validate();
          setDrawerProps({ confirmLoading: true });
          //把image的值，从数组，转成字符串，唉
          const datachange = {};
          for (const key in values) {
            type KeyType = keyof typeof values;
            const initialValue = values[key as KeyType];
            switch (key) {
              case 'ota_image':
                if (initialValue != undefined) {
                  datachange[key] = initialValue[0]; //把上传的图片地址，从数组转成字符串
                } else {
                  datachange[key] = '';
                }
                break;
              case 'id':
                if (initialValue === 0 || initialValue === undefined) {
                  datachange[key] = 0;
                } else {
                  datachange[key] = initialValue;
                }
                break;
              case 'ota_type':
                if (initialValue === 0 || initialValue === undefined) {
                  datachange[key] = 0;
                } else {
                  datachange[key] = 1;
                }
                break;
              case 'ota_update_type':
                if (initialValue === 0 || initialValue === undefined) {
                  datachange[key] = 0;
                } else {
                  datachange[key] = 1;
                }
                break;
              default:
                datachange[key] = initialValue;
                break;
            }
          }
          // TODO custom api
          //console.log('datachange', datachange);
          const dataUpdate = await updateOtamain(datachange, 'none');
          if (dataUpdate) {
            closeDrawer();
          }
          emit('success');
        } finally {
          setDrawerProps({ confirmLoading: false });
        }
      }

      return {
        registerDrawer,
        registerForm,
        getTitle,
        handleSubmit,
      };
    },
  });
</script>
