<template>
  <BasicModal v-bind="$attrs" @register="registerModal" :title="getTitle" @ok="handleSubmit">
    <BasicForm @register="registerForm" />
  </BasicModal>
</template>
<script lang="ts">
  import { defineComponent, ref, computed, unref } from 'vue';
  import { BasicModal, useModalInner } from '/@/components/Modal';
  import { BasicForm, useForm } from '/@/components/Form/index';
  import { adminFormSchema } from './admin.data';
  import { getDocTreeList, getRoleTreeList, isAdminExist, isAdminExist1 } from '/@/api/demo/admin';
  import { updateAdmin } from '/@/api/demo/admin';
  import { useMessage } from '../../../../hooks/web/useMessage';

  export default defineComponent({
    name: 'AdminModal',
    components: { BasicModal, BasicForm },
    emits: ['success', 'register'],
    setup(_, { emit }) {
      const isUpdate = ref(true);
      const rowId = ref('');

      const [registerForm, { setFieldsValue, updateSchema, resetFields, validate }] = useForm({
        labelWidth: 100,
        schemas: adminFormSchema,
        showActionButtonGroup: false,
        actionColOptions: {
          span: 23,
        },
      });

      const [registerModal, { setModalProps, closeModal }] = useModalInner(async (data) => {
        resetFields();
        setModalProps({ confirmLoading: false });
        isUpdate.value = !!data?.isUpdate;
        let defaultstr = '请选择角色';
        let defaultid = 0;
        let defaultstr1 = '请选择医生';
        let defaultid1 = 0;
        //编辑->传递的prop数据获取
        if (unref(isUpdate)) {
          rowId.value = data.record.id;
          defaultstr = data.record.role_name;
          defaultid = data.record.role_id;
          defaultstr1 = data.record.professor_name;
          defaultid1 = data.record.professor_id;
          //把图片字段从字符串转数组，Upload组件才能识别
          const datachange = {};
          for (const key in data.record) {
            type KeyType = keyof typeof data.record;
            const initialValue = data.record[key as KeyType];
            switch (key) {
              case 'image':
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
          //编辑
          updateSchema([
            {
              field: 'is_active',
              label: '是否启用',
              required: true,
              component: 'RadioButtonGroup',
              defaultValue: data.record.is_active,
              componentProps: {
                options: [
                  { label: '已禁用', value: 0 },
                  { label: '已启用', value: 1 },
                ],
              },
            },
            {
              field: 'user_type',
              label: '是否超级管理员',
              required: true,
              component: 'RadioButtonGroup',
              defaultValue: data.record.user_type,
              componentProps: {
                options: [
                  { label: '普通管理员', value: 0 },
                  { label: '超级管理员', value: 1 },
                ],
              },
            },
            {
              field: 'name',
              label: '管理员账号',
              component: 'Input',
              rules: [
                {
                  required: true,
                  message: '管理员账号已存在',
                  validator: async (_, value) => {
                    return new Promise((resolve, reject) => {
                      isAdminExist(data.record.id, value)
                        .then(() => resolve())
                        .catch((err) => {
                          reject(err.message || '验证失败');
                        });
                    });
                  },
                  trigger: 'blur',
                },
              ],
            },
          ]);
        } else {
          //新增
          updateSchema([
            {
              field: 'name',
              label: '管理员账号',
              component: 'Input',
              rules: [
                {
                  required: true,
                  message: '管理员账号已存在',
                  validator: async (_, value) => {
                    return new Promise((resolve, reject) => {
                      isAdminExist1(value)
                        .then(() => resolve())
                        .catch((err) => {
                          reject(err.message || '验证失败');
                        });
                    });
                  },
                  trigger: 'blur',
                },
              ],
            },
          ]);
        }
        const treeData0 = await getRoleTreeList();
        let treeData = treeData0.data;

        updateSchema([
          {
            field: 'role_name',
            defaultValue: {
              label: defaultstr,
              key: defaultid,
              value: defaultid,
            },
            componentProps: { treeData },
          },
        ]);
        const treeData1 = await getDocTreeList();
        treeData = treeData1.data;
        updateSchema([
          {
            field: 'professor_name',
            defaultValue: {
              label: defaultstr1,
              key: defaultid1,
              value: defaultid1,
            },
            componentProps: { treeData },
          },
        ]);
      });

      const getTitle = computed(() => (!unref(isUpdate) ? '新增管理员' : '编辑管理员'));

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
              case 'image':
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
              case 'role_name':
                if (initialValue.value === undefined) {
                  datachange['role_id'] = initialValue;
                } else {
                  datachange['role_id'] = initialValue.value;
                }
                break;
              case 'professor_name':
                if (initialValue.value === undefined) {
                  datachange['professor_id'] = initialValue;
                } else {
                  datachange['professor_id'] = initialValue.value;
                }
                break;
              default:
                datachange[key] = initialValue;
                break;
            }
          }
          const { createMessage } = useMessage();
          if (datachange.role_id === 0) {
            createMessage.error('必须选择一个所属角色!');
          } else {
            setModalProps({ confirmLoading: true });
            // TODO custom api
            const dataUpdate = await updateAdmin(datachange, 'none');
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
