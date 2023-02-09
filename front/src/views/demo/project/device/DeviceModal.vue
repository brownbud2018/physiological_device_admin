<template>
  <BasicModal v-bind="$attrs" @register="registerModal" :title="getTitle" @ok="handleSubmit">
    <BasicForm @register="registerForm" />
  </BasicModal>
</template>
<script lang="ts">
  import { defineComponent, ref, computed, unref } from 'vue';
  import { BasicModal, useModalInner } from '/@/components/Modal';
  import { BasicForm, useForm } from '/@/components/Form/index';
  import { deviceFormSchema } from './device.data';
  import {
    getAuthTreeList,
    getOTATreeList,
    getProductTreeList,
    isDeviceExist,
    isDeviceExist1,
  } from '/@/api/demo/device';
  import { updateDevice } from '/@/api/demo/device';
  import { useMessage } from '/@/hooks/web/useMessage';

  export default defineComponent({
    name: 'DeviceModal',
    components: { BasicModal, BasicForm },
    emits: ['success', 'register'],
    setup(_, { emit }) {
      const isUpdate = ref(true);
      const rowId = ref('');

      const [registerForm, { setFieldsValue, updateSchema, resetFields, validate }] = useForm({
        labelWidth: 100,
        schemas: deviceFormSchema,
        showActionButtonGroup: false,
        actionColOptions: {
          span: 23,
        },
      });

      const [registerModal, { setModalProps, closeModal }] = useModalInner(async (data) => {
        resetFields();
        setModalProps({ confirmLoading: false });
        isUpdate.value = !!data?.isUpdate;
        let defaultstr = '请选择所属项目';
        let defaultid = 0;
        let defaultotastr = '请在此选择所属OTA';
        let defaultotaid = 0;
        let defaultauthstr = '请选择所属授权类';
        let defaultauthid = 0;
        //编辑->传递的prop数据获取
        if (unref(isUpdate)) {
          rowId.value = data.record.id;
          defaultstr = data.record.prod_name;
          defaultid = data.record.product_id;
          defaultotastr = data.record.ota_name;
          defaultotaid = data.record.device_ota;
          defaultauthstr = data.record.class_name;
          defaultauthid = data.record.device_auth_class_id;
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
          //console.log('编辑', isUpdate);
          //编辑
          updateSchema([
            {
              field: 'is_active',
              label: '是否激活',
              required: true,
              component: 'RadioButtonGroup',
              defaultValue: data.record.is_active,
              componentProps: {
                options: [
                  { label: '未激活', value: 0 },
                  { label: '已激活', value: 1 },
                ],
              },
            },
            {
              field: 'device_level',
              label: '等级权限',
              required: true,
              component: 'RadioButtonGroup',
              defaultValue: data.record.device_level,
              componentProps: {
                options: [
                  { label: '普通等级', value: 0 },
                  { label: '授权等级', value: 1 },
                  { label: 'VIP等级', value: 2 },
                ],
              },
            },
            {
              field: 'device_code',
              label: 'device编号',
              component: 'Input',
              rules: [
                {
                  required: true,
                  message: 'device编号已存在',
                  validator: async (_, value) => {
                    return new Promise((resolve, reject) => {
                      isDeviceExist(data.record.id, value)
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
              field: 'device_code',
              label: 'device编号',
              component: 'Input',
              rules: [
                {
                  required: true,
                  message: 'device编号已存在',
                  validator: async (_, value) => {
                    return new Promise((resolve, reject) => {
                      isDeviceExist1(value)
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
        const treeData0 = await getProductTreeList();
        let treeData = treeData0.data;

        updateSchema([
          {
            field: 'prod_name',
            defaultValue: {
              label: defaultstr,
              key: defaultid,
              value: defaultid,
            },
            componentProps: { treeData },
          },
        ]);
        const treeData00 = await getOTATreeList();
        treeData = treeData00.data;
        updateSchema([
          {
            field: 'ota_name',
            defaultValue: {
              label: defaultotastr,
              key: defaultotaid,
              value: defaultotaid,
            },
            componentProps: { treeData },
          },
        ]);
        const treeData11 = await getAuthTreeList();
        treeData = treeData11.data;
        updateSchema([
          {
            field: 'class_name',
            defaultValue: {
              label: defaultauthstr,
              key: defaultauthid,
              value: defaultauthid,
            },
            componentProps: { treeData },
          },
        ]);
      });

      const getTitle = computed(() => (!unref(isUpdate) ? '新增Device' : '编辑Device'));

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
              case 'prod_name':
                if (initialValue.value === undefined) {
                  datachange['product_id'] = initialValue;
                } else {
                  datachange['product_id'] = initialValue.value;
                }
                break;
              case 'ota_name':
                if (initialValue.value === undefined) {
                  datachange['device_ota'] = initialValue;
                } else {
                  datachange['device_ota'] = initialValue.value;
                }
                break;
              case 'class_name':
                if (initialValue.value === undefined) {
                  datachange['device_auth_class_id'] = initialValue;
                } else {
                  datachange['device_auth_class_id'] = initialValue.value;
                }
                break;
              default:
                datachange[key] = initialValue;
                break;
            }
          }
          const { createMessage } = useMessage();
          if (datachange.product_id === 0) {
            createMessage.error('必须选择一个所属设备类型!');
          } else {
            if (datachange.device_ota === 0) {
              createMessage.error('必须选择一个所属OTA!');
            } else {
              setModalProps({ confirmLoading: true });
              // TODO custom api
              const dataUpdate = await updateDevice(datachange, 'none');
              closeModal();
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
