<template>
  <BasicModal v-bind="$attrs" @register="registerModal" :title="getTitle" @ok="handleSubmit">
    <BasicForm @register="registerForm" />
  </BasicModal>
</template>
<script lang="ts">
  import { defineComponent, ref, computed, unref } from 'vue';
  import { BasicModal, useModalInner } from '/@/components/Modal';
  import { BasicForm, useForm } from '/@/components/Form/index';
  import { authdetailFormSchema } from './authdetail.data';
  import { updateAuthdetail } from '/@/api/demo/authdetail';

  export default defineComponent({
    name: 'AuthdetailModal',
    components: { BasicModal, BasicForm },
    emits: ['success', 'register'],
    setup(_, { emit }) {
      const isUpdate = ref(true);
      const rowId = ref('');

      const [registerForm, { setFieldsValue, updateSchema, resetFields, validate }] = useForm({
        labelWidth: 100,
        schemas: authdetailFormSchema,
        showActionButtonGroup: false,
        actionColOptions: {
          span: 23,
        },
      });

      const [registerModal, { setModalProps, closeModal }] = useModalInner(async (data) => {
        resetFields();
        setModalProps({ confirmLoading: false });
        isUpdate.value = !!data?.isUpdate;
        //编辑->传递的prop数据获取
        if (unref(isUpdate)) {
          rowId.value = data.record.id;
          //把图片字段从字符串转数组，Upload组件才能识别
          const datachange = {};
          for (const key in data.record) {
            type KeyType = keyof typeof data.record;
            const initialValue = data.record[key as KeyType];
            switch (key) {
              case 'detail_image':
                if (initialValue != undefined) {
                  datachange[key] = [initialValue]; //把地址，从字符串转成数组
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
          //console.log('编辑', isUpdate);
          //编辑
          updateSchema([
            {
              field: 'detail_type',
              label: '是否默认',
              required: true,
              component: 'RadioButtonGroup',
              defaultValue: data.record.detail_type,
              componentProps: {
                options: [
                  { label: '默认属性', value: 0 },
                  { label: '特殊属性', value: 1 },
                ],
              },
            },
            {
              field: 'detail_code',
              label: '权限编号',
              component: 'Input',
            },
          ]);
        } else {
          //新增
          updateSchema([
            {
              field: 'detail_code',
              label: '权限编号',
              component: 'Input',
            },
          ]);
        }
      });

      const getTitle = computed(() => (!unref(isUpdate) ? '新增权限' : '编辑权限'));

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
              case 'detail_image':
                if (initialValue != undefined) {
                  datachange[key] = initialValue[0]; //把上传的图片地址，从数组转成字符串
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
              default:
                datachange[key] = initialValue;
                break;
            }
          }
          setModalProps({ confirmLoading: true });
          // TODO custom api
          const dataUpdate = await updateAuthdetail(datachange, 'none');
          if (dataUpdate) {
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
