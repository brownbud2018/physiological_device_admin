<template>
  <BasicModal v-bind="$attrs" @register="registerModal" :title="getTitle" @ok="handleSubmit">
    <BasicForm @register="registerForm" />
  </BasicModal>
</template>
<script lang="ts">
  import { defineComponent, ref, computed, unref } from 'vue';
  import { BasicModal, useModalInner } from '/@/components/Modal';
  import { BasicForm, useForm } from '/@/components/Form/index';
  import { userFormSchema } from './user.data';
  import {
    getMedicalTreeList,
    getAllergyTreeList,
    getBloodtypeTreeList,
    getGeneticTreeList,
    updateUser,
  } from '/@/api/demo/user';

  export default defineComponent({
    name: 'UserModal',
    components: { BasicModal, BasicForm },
    emits: ['success', 'register'],
    setup(_, { emit }) {
      const isUpdate = ref(true);
      const rowId = ref('');

      const [registerForm, { setFieldsValue, updateSchema, resetFields, validate }] = useForm({
        labelWidth: 100,
        schemas: userFormSchema,
        showActionButtonGroup: false,
        actionColOptions: {
          span: 23,
        },
      });

      const [registerModal, { setModalProps, closeModal }] = useModalInner(async (data) => {
        resetFields();
        setModalProps({ confirmLoading: false });
        isUpdate.value = !!data?.isUpdate;
        let str1 = '请选择血型';
        let id1 = 0;
        let str2 = '请选择药物过敏史';
        let id2 = 0;
        let str3 = '请选择既往病史';
        let id3 = 0;
        let str4 = '请选择遗传史';
        let id4 = 0;
        //编辑->传递的prop数据获取
        if (unref(isUpdate)) {
          rowId.value = data.record.id;
          str1 =
            data.record.bloodtypename == null || data.record.bloodtypename == ''
              ? '请选择血型'
              : data.record.bloodtypename;
          id1 = data.record.bloodtypeid;
          str2 =
            data.record.allergyname == null || data.record.allergyname == ''
              ? '请选择药物过敏史'
              : data.record.allergyname;
          id2 = data.record.allergyid;
          str3 =
            data.record.medicalname == null || data.record.medicalname == ''
              ? '请选择既往病史'
              : data.record.medicalname;
          id3 = data.record.medicalid;
          str4 =
            data.record.geneticname == null || data.record.geneticname == ''
              ? '请选择遗传史'
              : data.record.geneticname;
          id4 = data.record.geneticid;
          //把图片字段从字符串转数组，Upload组件才能识别
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
              case 'sex':
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
              field: 'sex',
              label: '性别',
              required: true,
              component: 'RadioButtonGroup',
              defaultValue: parseInt(data.record.sex),
              componentProps: {
                options: [
                  { label: '男', value: 0 },
                  { label: '女', value: 1 },
                ],
              },
            },
          ]);
        }
        const treeData0 = await getBloodtypeTreeList();
        let treeData = treeData0.data;
        updateSchema([
          {
            field: 'bloodtypename',
            defaultValue: {
              label: str1,
              key: id1,
              value: id1,
            },
            componentProps: { treeData },
          },
        ]);
        const treeData00 = await getAllergyTreeList();
        treeData = treeData00.data;
        updateSchema([
          {
            field: 'allergyname',
            defaultValue: {
              label: str2,
              key: id2,
              value: id2,
            },
            componentProps: { treeData },
          },
        ]);
        const treeData11 = await getMedicalTreeList();
        treeData = treeData11.data;
        updateSchema([
          {
            field: 'medicalname',
            defaultValue: {
              label: str3,
              key: id3,
              value: id3,
            },
            componentProps: { treeData },
          },
        ]);
        const treeData22 = await getGeneticTreeList();
        treeData = treeData22.data;
        updateSchema([
          {
            field: 'geneticname',
            defaultValue: {
              label: str4,
              key: id4,
              value: id4,
            },
            componentProps: { treeData },
          },
        ]);
      });

      const getTitle = computed(() => (!unref(isUpdate) ? '新增User' : '编辑User'));

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
              case 'id':
                if (
                  initialValue === 0 ||
                  initialValue === undefined ||
                  initialValue === null ||
                  initialValue === ''
                ) {
                  datachange[key] = 0;
                } else {
                  datachange[key] = initialValue;
                }
                break;
              case 'cityid':
                if (initialValue === 0 || initialValue === undefined || initialValue === '') {
                  datachange[key] = 0;
                } else {
                  datachange[key] = initialValue;
                }
                break;
              case 'cityname':
                if (initialValue === undefined || initialValue === null || initialValue === '') {
                  datachange[key] = '';
                } else {
                  datachange[key] = initialValue;
                }
                break;
              case 'bloodtypename':
                if (initialValue === undefined || initialValue === null || initialValue === '') {
                  datachange['bloodtypeid'] = 0;
                } else {
                  if (initialValue.value === undefined || initialValue.value === null || initialValue.value === 0) {
                    if (initialValue.value === 0) {
                      datachange['bloodtypeid'] = 0;
                    } else {
                      datachange['bloodtypeid'] = initialValue;
                    }
                  } else {
                    datachange['bloodtypeid'] = initialValue.value;
                  }
                }
                break;
              case 'allergyname':
                if (initialValue === undefined || initialValue === null || initialValue === '') {
                  datachange['allergyid'] = 0;
                } else {
                  if (initialValue.value === undefined || initialValue.value === null || initialValue.value === 0) {
                    if (initialValue.value === 0) {
                      datachange['allergyid'] = 0;
                    } else {
                      datachange['allergyid'] = initialValue;
                    }
                  } else {
                    datachange['allergyid'] = initialValue.value;
                  }
                }
                break;
              case 'medicalname':
                if (initialValue === undefined || initialValue === null || initialValue === '') {
                  datachange['medicalid'] = 0;
                } else {
                  if (initialValue.value === undefined || initialValue.value === null || initialValue.value === 0) {
                    if (initialValue.value === 0) {
                      datachange['medicalid'] = 0;
                    } else {
                      datachange['medicalid'] = initialValue;
                    }
                  } else {
                    datachange['medicalid'] = initialValue.value;
                  }
                }
                break;
              case 'geneticname':
                if (initialValue === undefined || initialValue === null || initialValue === '') {
                  datachange['geneticid'] = 0;
                } else {
                  if (initialValue.value === undefined || initialValue.value === null || initialValue.value === 0) {
                    if (initialValue.value === 0) {
                      datachange['geneticid'] = 0;
                    } else {
                      datachange['geneticid'] = initialValue;
                    }
                  } else {
                    datachange['geneticid'] = initialValue.value;
                  }
                }
                break;
              default:
                if (initialValue === undefined || initialValue === null) {
                  datachange[key] = '';
                } else {
                  datachange[key] = initialValue;
                }
                break;
            }
          }
          //console.log(datachange);
          //const { createMessage } = useMessage();
          setModalProps({ confirmLoading: true });
          const dataUpdate = await updateUser(datachange, 'none');
          closeModal();
          /*if (datachange.product_id === 0) {
            createMessage.error('必须选择一个所属设备类型!');
          } else {
            if (datachange.user_ota === 0) {
              createMessage.error('必须选择一个所属OTA!');
            } else {
              // TODO custom api
            }
          }*/
          emit('success', { isUpdate: unref(isUpdate), values: { ...values, id: rowId.value } });
        } finally {
          setModalProps({ confirmLoading: false });
        }
      }

      return { registerModal, registerForm, getTitle, handleSubmit };
    },
  });
</script>
