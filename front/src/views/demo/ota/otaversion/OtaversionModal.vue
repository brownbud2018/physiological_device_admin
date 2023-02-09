<template>
  <BasicModal v-bind="$attrs" @register="registerModal" :title="getTitle" @ok="handleSubmit">
    <BasicForm @register="registerForm" />
  </BasicModal>
</template>
<script lang="ts">
  import { defineComponent, ref, computed, unref } from 'vue';
  import { BasicModal, useModalInner } from '/@/components/Modal';
  import { BasicForm, useForm } from '/@/components/Form/index';
  import { otaversionFormSchema } from './otaversion.data';
  import { getOTATreeList, updateOtaversion } from '/@/api/demo/otaversion';
  import { useMessage } from '/@/hooks/web/useMessage';

  export default defineComponent({
    name: 'OtaversionModal',
    components: { BasicModal, BasicForm },
    emits: ['success', 'register'],
    setup(_, { emit }) {
      const isUpdate = ref(true);
      const rowId = ref('');

      const [registerForm, { setFieldsValue, updateSchema, resetFields, validate }] = useForm({
        labelWidth: 100,
        schemas: otaversionFormSchema,
        showActionButtonGroup: false,
        actionColOptions: {
          span: 23,
        },
      });

      const [registerModal, { setModalProps, closeModal }] = useModalInner(async (data) => {
        resetFields();
        setModalProps({ confirmLoading: false });
        isUpdate.value = !!data?.isUpdate;
        let defaultstr = '请选择所属OTA';
        let defaultid = 0;
        //编辑->传递的prop数据获取
        if (unref(isUpdate)) {
          rowId.value = data.record.id;
          defaultstr = data.record.ota_name;
          defaultid = data.record.ota_main_id;
          //把图片字段从字符串转数组，Upload组件才能识别
          const datachange = {};
          for (const key in data.record) {
            type KeyType = keyof typeof data.record;
            const initialValue = data.record[key as KeyType];
            switch (key) {
              case 'ota_v_image':
                if (initialValue != undefined) {
                  datachange[key] = [initialValue]; //把地址，从字符串转成数组
                } else {
                  datachange[key] = '';
                }
                break;
              case 'ota_v_file':
                if (initialValue != undefined) {
                  datachange[key] = initialValue;
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
              default:
                datachange[key] = initialValue;
                break;
            }
          }
          const datachangePops = new Proxy(datachange, {});
          setFieldsValue({
            ...datachangePops,
          });
        }

        if (unref(isUpdate)) {
          //编辑
          updateSchema([
            {
              field: 'ota_v_default',
              label: '是否默认',
              required: true,
              component: 'RadioButtonGroup',
              defaultValue: data.record.ota_v_default,
              componentProps: {
                options: [
                  { label: '非默认版本', value: 0 },
                  { label: '默认版本', value: 1 },
                ],
              },
            },
            {
              field: 'ota_v_code',
              label: 'OTA版本编号',
              component: 'Input',
            },
          ]);
        } else {
          //新增
          updateSchema([
            {
              field: 'ota_v_code',
              label: 'OTA版本编号',
              component: 'Input',
            },
          ]);
        }
        const treeData0 = await getOTATreeList();
        let treeData = treeData0.data;

        updateSchema([
          {
            field: 'ota_name',
            defaultValue: {
              label: defaultstr,
              key: defaultid,
              value: defaultid,
            },
            componentProps: { treeData },
          },
        ]);
      });

      const getTitle = computed(() => (!unref(isUpdate) ? '新增OTA版本' : '编辑OTA版本'));

      async function handleSubmit() {
        try {
          const values = await validate();
          setModalProps({ confirmLoading: true });
          //把image的值，从数组，转成字符串，唉
          const datachange = {};
          for (const key in values) {
            type KeyType = keyof typeof values;
            const initialValue = values[key as KeyType];
            switch (key) {
              case 'ota_v_image':
                if (initialValue != undefined) {
                  datachange[key] = initialValue[0]; //把上传的图片地址，从数组转成字符串
                } else {
                  datachange[key] = '';
                }
                break;
              case 'ota_v_file':
                if (initialValue != undefined) {
                  datachange[key] = initialValue;
                } else {
                  datachange[key] = '';
                }
                break;
              case 'id':
                if (initialValue === 0 || initialValue === undefined || initialValue === '') {
                  datachange[key] = 0;
                } else {
                  datachange[key] = initialValue;
                }
                break;
              case 'ota_name':
                if (initialValue.value === undefined) {
                  datachange['ota_main_id'] = initialValue;
                } else {
                  datachange['ota_main_id'] = initialValue.value;
                }
                break;
              default:
                datachange[key] = initialValue;
                break;
            }
          }
          const { createMessage } = useMessage();
          if (datachange.ota_main_id === 0) {
            createMessage.error('必须选择一个所属OTA!');
          } else {
            setModalProps({ confirmLoading: true });
            // TODO custom api
            const dataUpdate = await updateOtaversion(datachange, 'none');
            closeModal();
          }
          emit('success', { isUpdate: unref(isUpdate), values: { ...values, id: rowId.value } });
        } finally {
          setModalProps({ confirmLoading: false });
        }
      }

      return { registerModal, registerForm, getTitle, handleSubmit };
    },
  });
</script>
