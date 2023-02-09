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
  import { formSchema } from './excelupload.data';
  import { BasicDrawer, useDrawerInner } from '/@/components/Drawer';
  import { updateExcelupload } from '/@/api/demo/excelupload';
  import { getAuthTreeList, getOTATreeList, getProductTreeList } from '/@/api/demo/device';
  import { uploadApi } from '../../../../api/sys/upload';

  //components: BasicTree
  export default defineComponent({
    name: 'ExceluploadDrawer',
    components: { BasicDrawer, BasicForm },
    emits: ['success', 'register'],
    setup(_, { emit }) {
      const isUpdate = ref(true);
      const rowId = ref('');

      const [registerForm, { resetFields, updateSchema, setFieldsValue, validate }] = useForm({
        labelWidth: 90,
        schemas: formSchema,
        showActionButtonGroup: false,
      });

      const [registerDrawer, { setDrawerProps, closeDrawer }] = useDrawerInner(async (data) => {
        resetFields();
        setDrawerProps({ confirmLoading: false });
        isUpdate.value = !!data?.isUpdate;
        let defaultstr = '请选择所属项目';
        let defaultid = 0;
        let defaultotastr = '请在此选择所属OTA';
        let defaultotaid = 0;
        let defaultauthstr = '请选择所属授权类';
        let defaultauthid = 0;
        let activeData = 0;
        let levelData = 0;
        //编辑->传递的prop数据获取
        if (unref(isUpdate)) {
          rowId.value = data.record.id;
          defaultstr = data.record.prod_name;
          defaultid = data.record.product_id;
          defaultotastr = data.record.ota_name;
          defaultotaid = data.record.device_ota;
          defaultauthstr = data.record.class_name;
          defaultauthid = data.record.device_auth_class_id;
          activeData = data.record.is_active;
          levelData = data.record.device_level;
          //修改传递给编辑页面的data.record数据，把image从字符串改成数组
          //因为Upload组件，它的value值，必须是数组，无奈啊。。。
          const datachange: any[] = [];
          for (const key in data.record) {
            type KeyType = keyof typeof data.record;
            const initialValue = data.record[key as KeyType];
            switch (key) {
              case 'excel_address':
                if (initialValue != undefined) {
                  datachange[key] = [initialValue]; //把地址，从字符串转成数组
                } else {
                  datachange[key] = '';
                }
                break;
              case 'is_active':
                if (initialValue != undefined) {
                  datachange[key] = initialValue; //是否激活
                } else {
                  datachange[key] = 0;
                }
                break;
              case 'device_level':
                if (initialValue != undefined) {
                  datachange[key] = initialValue; //是否激活
                } else {
                  datachange[key] = 0;
                }
                break;
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
          //console.log(datachange);
          setFieldsValue({
            ...datachange,
          });
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

        updateSchema([
          {
            field: 'is_active',
            defaultValue: activeData,
          },
          {
            field: 'device_level',
            defaultValue: levelData,
          },
        ]);
      });

      const getTitle = computed(() => (!unref(isUpdate) ? '新增上传Excel' : '编辑上传Excel'));

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
              case 'excel_address':
                if (initialValue != undefined) {
                  datachange[key] = initialValue[0]; //把上传的图片地址，从数组转成字符串
                } else {
                  datachange[key] = '';
                }
                break;
              case 'image':
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
              case 'is_import':
                if (initialValue === 0 || initialValue === undefined) {
                  datachange[key] = 0;
                } else {
                  datachange[key] = 1;
                }
                break;
              case 'is_active':
                if (initialValue === 0 || initialValue === undefined) {
                  datachange[key] = 0;
                } else {
                  datachange[key] = 1;
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
          // TODO custom api
          //console.log('datachange', datachange);
          const dataUpdate = await updateExcelupload(datachange, 'none');
          //console.log('dataUpdate', dataUpdate);
          closeDrawer();
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
