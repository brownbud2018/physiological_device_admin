<template>
  <BasicDrawer
    v-bind="$attrs"
    @register="registerDrawer"
    showFooter
    :title="getTitle"
    width="50%"
    @ok="handleSubmit"
  >
    <BasicForm @register="registerForm" />
  </BasicDrawer>
</template>
<script lang="ts">
  import { defineComponent, ref, computed, unref } from 'vue';
  import { BasicForm, useForm } from '/@/components/Form/index';
  import { accessFormSchema } from './access.data';
  import { BasicDrawer, useDrawerInner } from '/@/components/Drawer';

  import { getAccessTreeList, isAccessExist, isAccessExist1, updateAccess } from '/@/api/demo/access';

  export default defineComponent({
    name: 'AccessDrawer',
    components: { BasicDrawer, BasicForm },
    emits: ['success', 'register'],
    setup(_, { emit }) {
      const isUpdate = ref(true);
      const rowId = ref('');

      const [registerForm, { resetFields, setFieldsValue, updateSchema, validate }] = useForm({
        labelWidth: 100,
        schemas: accessFormSchema,
        showActionButtonGroup: false,
        baseColProps: { lg: 12, md: 24 },
      });

      const [registerDrawer, { setDrawerProps, closeDrawer }] = useDrawerInner(async (data) => {
        resetFields();
        setDrawerProps({ confirmLoading: false });
        isUpdate.value = !!data?.isUpdate;
        let defaultstr = '顶层权限';
        let defaultid = 0;

        if (unref(isUpdate)) {
          rowId.value = data.record.id;
          if (data.record.parent_id != 0) {
            defaultstr = data.record.parent_name;
            defaultid = data.record.parent_id;
          }
          setFieldsValue({
            ...data.record,
          });
        }
        if (unref(isUpdate)) {
          //编辑
          updateSchema([
            {
              field: 'is_check',
              label: '是否验证权限',
              required: true,
              component: 'RadioButtonGroup',
              defaultValue: data.record.is_check,
              componentProps: {
                options: [
                  { label: '不验证', value: 0 },
                  { label: '需验证', value: 1 },
                ],
              },
            },
            {
              field: 'is_menu',
              label: '是否菜单',
              required: true,
              component: 'RadioButtonGroup',
              defaultValue: data.record.is_menu,
              componentProps: {
                options: [
                  { label: '否', value: 0 },
                  { label: '是', value: 1 },
                ],
              },
            },
            {
              field: 'access_code',
              label: '权限编号',
              component: 'Input',
              rules: [
                {
                  required: true,
                  message: '权限编号已存在',
                  validator: async (_, value) => {
                    return new Promise((resolve, reject) => {
                      isAccessExist(data.record.id, value)
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
              field: 'access_code',
              label: '权限编号',
              component: 'Input',
              rules: [
                {
                  required: true,
                  message: '权限编号已存在',
                  validator: async (_, value) => {
                    return new Promise((resolve, reject) => {
                      isAccessExist1(value)
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

        const treeData0 = await getAccessTreeList();
        let treeData = treeData0.data;
        updateSchema([
          {
            field: 'parent_name',
            defaultValue: {
              label: defaultstr,
              key: defaultid,
              value: defaultid,
            },
            componentProps: { treeData },
          },
        ]);
      });

      const getTitle = computed(() => (!unref(isUpdate) ? '新增权限1' : '编辑权限1'));

      async function handleSubmit() {
        try {
          const values = await validate();
          const datachange = {};
          for (const key in values) {
            type KeyType = keyof typeof values;
            const initialValue = values[key as KeyType];
            switch (key) {
              /*case 'access_image':
                if (initialValue != undefined) {
                  datachange[key] = initialValue[0]; //把上传的图片地址，从数组转成字符串
                } else {
                  datachange[key] = '';
                }
                break;*/
              case 'id':
                if (initialValue === 0 || initialValue === undefined || initialValue === '') {
                  datachange[key] = 0;
                } else {
                  datachange[key] = initialValue;
                }
                break;
              case 'parent_name':
                if (initialValue.value === undefined) {
                  datachange['parent_id'] = initialValue;
                } else {
                  datachange['parent_id'] = initialValue.value;
                }
                break;
              default:
                datachange[key] = initialValue;
                break;
            }
          }
          setDrawerProps({ confirmLoading: true });
          // TODO custom api
          //console.log('datachange', datachange);
          const dataUpdate = await updateAccess(datachange, 'none');
          closeDrawer();
          emit('success');
        } finally {
          setDrawerProps({ confirmLoading: false });
        }
      }

      return { registerDrawer, registerForm, getTitle, handleSubmit };
    },
  });
</script>
