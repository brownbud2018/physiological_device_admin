<template>
  <BasicModal v-bind="$attrs" @register="registerModal" :title="getTitle" @ok="handleSubmit">
    <BasicForm @register="registerForm" />
  </BasicModal>
</template>
<script lang="ts">
  import { defineComponent, ref, computed, unref } from 'vue';
  import { BasicModal, useModalInner } from '/@/components/Modal';
  import { BasicForm, useForm } from '/@/components/Form/index';
  import { formSchema } from './professors.data';
  import { getCatList, updateProfessors } from '/@/api/demo/professors';
  import { useMessage } from '/@/hooks/web/useMessage';

  export default defineComponent({
    name: 'ProfessorsModal',
    components: { BasicModal, BasicForm },
    emits: ['success', 'register'],
    setup(_, { emit }) {
      const isUpdate = ref(true);
      const rowId = ref('');

      const [registerForm, { setFieldsValue, updateSchema, resetFields, validate }] = useForm({
        labelWidth: 100,
        schemas: formSchema,
        showActionButtonGroup: false,
        actionColOptions: {
          span: 23,
        },
      });

      const [registerModal, { setModalProps, closeModal }] = useModalInner(async (data) => {
        resetFields();
        setModalProps({ confirmLoading: false });
        isUpdate.value = !!data?.isUpdate;
        let defaultstr = '请选择所属主治分类';
        let defaultid = 0;
        //编辑->传递的prop数据获取
        if (unref(isUpdate)) {
          rowId.value = data.record.id;
          defaultstr = data.record.cat_name;
          defaultid = data.record.cat_id;
          //把图片字段从字符串转数组，Upload组件才能识别
          const datachange = {};
          for (const key in data.record) {
            type KeyType = keyof typeof data.record;
            const initialValue = data.record[key as KeyType];
            switch (key) {
              case 'avatar':
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
          //console.log(datachangePops);
          setFieldsValue({
            ...datachangePops,
          });
        }

        const treeData0 = await getCatList();
        const treeData = treeData0.data;
        //console.log(data);
        updateSchema([
          /*{
            field: 'pwd',
            show: !unref(isUpdate),
          },*/
          {
            field: 'cat_name',
            defaultValue: {
              label: defaultstr,
              key: defaultid,
              value: defaultid,
            },
            componentProps: { treeData },
          },
          {
            field: 'sex',
            label: '医生性别',
            required: true,
            component: 'RadioButtonGroup',
            defaultValue: data.record.sex,
            componentProps: {
              options: [
                { label: '女', value: 0 },
                { label: '男', value: 1 },
              ],
            },
          },
        ]);
      });

      const getTitle = computed(() => (!unref(isUpdate) ? '新增医生' : '编辑医生'));

      async function handleSubmit() {
        try {
          const values = await validate();
          //console.log('values', values);
          setModalProps({ confirmLoading: true });
          //把image的值，从数组，转成字符串，唉
          const datachange = {};
          for (const key in values) {
            type KeyType = keyof typeof values;
            const initialValue = values[key as KeyType];
            switch (key) {
              case 'avatar':
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
              case 'cat_name':
                if (initialValue.value === undefined) {
                  datachange['cat_id'] = initialValue;
                } else {
                  datachange['cat_id'] = initialValue.value;
                }
                break;
              default:
                datachange[key] = initialValue;
                break;
            }
          }
          const { createMessage } = useMessage();
          if (datachange.cat_id === 0) {
            createMessage.error('必须选择一个所属项目!');
          } else {
            // TODO custom api
            //console.log('datachange', datachange);
            const dataUpdate = await updateProfessors(datachange, 'none');
            //console.log('dataUpdate', dataUpdate);
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
