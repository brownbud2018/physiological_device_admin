<template>
  <BasicModal v-bind="$attrs" @register="registerModal" :title="getTitle" @ok="handleSubmit">
    <BasicForm @register="registerForm" />
  </BasicModal>
</template>
<script lang="ts">
  import { defineComponent, ref, computed, unref } from 'vue';
  import { BasicModal, useModalInner } from '/@/components/Modal';
  import { BasicForm, useForm } from '/@/components/Form/index';
  import { productappFormSchema } from './productapp.data';
  import { getAPPList, getProductList, updateProductapp } from '/@/api/demo/productapp';
  import { useMessage } from '../../../../hooks/web/useMessage';

  export default defineComponent({
    name: 'ProductappModal',
    components: { BasicModal, BasicForm },
    emits: ['success', 'register'],
    setup(_, { emit }) {
      const isUpdate = ref(true);
      const rowId = ref('');

      const [registerForm, { setFieldsValue, updateSchema, resetFields, validate }] = useForm({
        labelWidth: 100,
        schemas: productappFormSchema,
        showActionButtonGroup: false,
        actionColOptions: {
          span: 23,
        },
      });

      const [registerModal, { setModalProps, closeModal }] = useModalInner(async (data) => {
        resetFields();
        setModalProps({ confirmLoading: false });
        isUpdate.value = !!data?.isUpdate;
        let defaultstr = '请选择所属设备类型';
        let defaultid = 0;
        let defaultstr1 = '请选择所属APP';
        let defaultid1 = 0;
        //编辑->传递的prop数据获取
        if (unref(isUpdate)) {
          rowId.value = data.record.id;
          defaultstr = data.record.prod_name;
          defaultid = data.record.prod_id;
          defaultstr1 = data.record.app_name;
          defaultid1 = data.record.app_pro_id;
          const datachange = {};
          for (const key in data.record) {
            type KeyType = keyof typeof data.record;
            const initialValue = data.record[key as KeyType];
            switch (key) {
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

        //console.log(treeData);
        if (unref(isUpdate)) {
          //编辑
          const treeData0 = await getProductList();
          let treeData = treeData0.data;
          updateSchema([
            {
              field: 'prod_id',
              defaultValue: {
                label: defaultstr,
                key: defaultid,
                value: defaultid,
              },
              componentProps: { treeData },
            },
          ]);
          const treeData1 = await getAPPList();
          treeData = treeData1.data;
          updateSchema([
            {
              field: 'app_pro_id',
              defaultValue: {
                label: defaultstr1,
                key: defaultid1,
                value: defaultid1,
              },
              componentProps: { treeData },
            },
          ]);
        } else {
          //新增
          const treeData0 = await getProductList();
          let treeData = treeData0.data;
          updateSchema([
            {
              field: 'prod_id',
              defaultValue: {
                label: defaultstr,
                key: defaultid,
                value: defaultstr,
              },
              componentProps: { treeData },
            },
          ]);
          const treeData1 = await getAPPList();
          treeData = treeData1.data;
          updateSchema([
            {
              field: 'app_pro_id',
              defaultValue: {
                label: defaultstr1,
                key: defaultid1,
                value: defaultstr1,
              },
              componentProps: { treeData },
            },
          ]);
        }
      });

      const getTitle = computed(() => (!unref(isUpdate) ? '新增设备关联APP' : '编辑设备关联APP'));

      async function handleSubmit() {
        try {
          const values = await validate();
          //console.log('values', values);
          setModalProps({ confirmLoading: true });
          const datachange = {};
          for (const key in values) {
            type KeyType = keyof typeof values;
            const initialValue = values[key as KeyType];
            switch (key) {
              case 'id':
                if (initialValue === 0 || initialValue === undefined || initialValue === '') {
                  datachange[key] = 0;
                } else {
                  datachange[key] = initialValue;
                }
                break;
              case 'prod_id':
                if (initialValue.value === undefined) {
                  datachange['prod_id'] = initialValue;
                } else {
                  datachange['prod_id'] = initialValue.value;
                }
                break;
              case 'app_pro_id':
                if (initialValue.value === undefined) {
                  datachange['app_pro_id'] = initialValue;
                } else {
                  datachange['app_pro_id'] = initialValue.value;
                }
                break;
              default:
                datachange[key] = initialValue;
                break;
            }
          }
          const { createMessage } = useMessage();
          if (datachange.prod_id === 0) {
            createMessage.error('必须选择一个所属设备类型!');
          } else {
            if (datachange.app_pro_id === 0) {
              createMessage.error('必须选择一个APP!');
            } else {
              // TODO custom api
              //console.log('datachange', datachange);
              const dataUpdate = await updateProductapp(datachange, 'none');
              if (dataUpdate) {
                closeModal();
              }
            }
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
