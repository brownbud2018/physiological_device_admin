<template>
  <BasicModal v-bind="$attrs" @register="registerModal" :title="getTitle" @ok="handleSubmit">
    <BasicForm @register="registerForm" />
  </BasicModal>
</template>
<script lang="ts">
  import { defineComponent, ref, computed, unref } from 'vue';
  import { BasicModal, useModalInner } from '/@/components/Modal';
  import { BasicForm, useForm } from '/@/components/Form/index';
  import { authaboutFormSchema } from './authabout.data';
  import { getAuthdetailList, getAuthclassList, updateAuthabout } from '/@/api/demo/authabout';
  import { useMessage } from '/@/hooks/web/useMessage';

  export default defineComponent({
    name: 'AuthaboutModal',
    components: { BasicModal, BasicForm },
    emits: ['success', 'register'],
    setup(_, { emit }) {
      const isUpdate = ref(true);
      const rowId = ref('');

      const [registerForm, { setFieldsValue, updateSchema, resetFields, validate }] = useForm({
        labelWidth: 100,
        schemas: authaboutFormSchema,
        showActionButtonGroup: false,
        actionColOptions: {
          span: 23,
        },
      });

      const [registerModal, { setModalProps, closeModal }] = useModalInner(async (data) => {
        resetFields();
        setModalProps({ confirmLoading: false });
        isUpdate.value = !!data?.isUpdate;
        let defaultstr = '请选择所属授权';
        let defaultid = 0;
        let defaultstr1 = '请选择所属权限';
        let defaultid1 = 0;
        //编辑->传递的prop数据获取
        if (unref(isUpdate)) {
          rowId.value = data.record.id;
          defaultstr = data.record.class_name;
          defaultid = data.record.class_id;
          defaultstr1 = data.record.detail_name;
          defaultid1 = data.record.detail_id;
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
          const treeData0 = await getAuthclassList();
          let treeData = treeData0.data;
          updateSchema([
            {
              field: 'class_id',
              defaultValue: {
                label: defaultstr,
                key: defaultid,
                value: defaultid,
              },
              componentProps: { treeData },
            },
          ]);
          const treeData1 = await getAuthdetailList();
          treeData = treeData1.data;
          updateSchema([
            {
              field: 'detail_id',
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
          const treeData0 = await getAuthclassList();
          let treeData = treeData0.data;
          updateSchema([
            {
              field: 'class_id',
              defaultValue: {
                label: defaultstr,
                key: defaultid,
                value: defaultstr,
              },
              componentProps: { treeData },
            },
          ]);
          const treeData1 = await getAuthdetailList();
          treeData = treeData1.data;
          updateSchema([
            {
              field: 'detail_id',
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

      const getTitle = computed(() => (!unref(isUpdate) ? '新增授权关联权限' : '编辑授权关联权限'));

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
              case 'class_id':
                if (initialValue.value === undefined) {
                  datachange['class_id'] = initialValue;
                } else {
                  datachange['class_id'] = initialValue.value;
                }
                break;
              case 'detail_id':
                if (initialValue.value === undefined) {
                  datachange['detail_id'] = initialValue;
                } else {
                  datachange['detail_id'] = initialValue.value;
                }
                break;
              default:
                datachange[key] = initialValue;
                break;
            }
          }
          const { createMessage } = useMessage();
          if (datachange.class_id === 0) {
            createMessage.error('必须选择一个所属授权!');
          } else {
            if (datachange.detail_id === 0) {
              createMessage.error('必须选择一个权限!');
            } else {
              // TODO custom api
              //console.log('datachange', datachange);
              const dataUpdate = await updateAuthabout(datachange, 'none');
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
