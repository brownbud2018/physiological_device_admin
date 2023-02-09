import { BasicColumn } from '/@/components/Table';
import { FormSchema } from '/@/components/Table';
import { uploadApi } from '/@/api/sys/upload';
import { h } from 'vue';
import { Img } from '/@/components/Img';
import { Switch } from 'ant-design-vue';
import { useMessage } from '/@/hooks/web/useMessage';
import { setOtaversionType } from '/@/api/demo/otaversion';

export const columns: BasicColumn[] = [
  {
    title: 'OTA版本名称',
    dataIndex: 'ota_v_name',
    width: 180,
  },
  {
    title: 'OTA版本编号',
    dataIndex: 'ota_v_code',
    width: 120,
  },
  {
    title: 'OTA名称',
    dataIndex: 'ota_name',
    width: 160,
  },
  {
    title: 'OTA版本MD5',
    dataIndex: 'ota_v_md5',
    width: 260,
  },
  {
    title: '是否默认',
    dataIndex: 'ota_v_default',
    width: 120,
    customRender: ({ record }) => {
      if (!Reflect.has(record, 'pendingStatus')) {
        record.pendingStatus = false;
      }
      return h(Switch, {
        checked: record.ota_v_default === 1,
        checkedChildren: '默认版本',
        unCheckedChildren: '非默认版本',
        loading: record.pendingStatus,
        onChange(checked: boolean) {
          record.pendingStatus = true;
          const newType = checked ? 1 : 0;
          const { createMessage } = useMessage();
          //setRoleStatus(record.id, newStatus)
          setOtaversionType(record.id, newType)
            .then(() => {
              record.ota_v_default = newType;
              createMessage.success('成功设置默认版本');
              location.reload();
              // @ts-ignore
              //const [reload] = useTable;
              //reload();
            })
            .catch(() => {
              createMessage.error('设置默认版本失败');
            })
            .finally(() => {
              record.pendingStatus = false;
            });
        },
      });
    },
  },
  {
    title: 'OTA版本图标',
    dataIndex: 'ota_v_image',
    width: 120,
    customRender: ({ record }) => {
      // @ts-ignore
      return h(Img, { src: record.ota_v_image, imgwidth: '80' });
    },
  },
  {
    title: 'OTA版本文件地址',
    dataIndex: 'ota_v_file',
    width: 260,
  },
  {
    title: 'OTA版本备注',
    dataIndex: 'ota_v_remark',
    width: 260,
  },
  {
    title: '创建时间',
    dataIndex: 'gmt_create',
    width: 180,
  },
];

export const searchFormSchema: FormSchema[] = [
  {
    field: 'otaversion_name',
    label: '名称/编号/备注',
    component: 'Input',
    colProps: { span: 8 },
  },
  /*{
    field: 'nickname',
    label: '昵称',
    component: 'Input',
    colProps: { span: 8 },
  },*/
];

// @ts-ignore
export const otaversionFormSchema: FormSchema[] = [
  {
    field: 'id',
    label: '自增编号',
    required: false,
    component: 'Input',
    dynamicDisabled: true,
  },
  {
    field: 'ota_v_name',
    label: 'OTA版本名称',
    required: true,
    component: 'Input',
  },
  {
    field: 'ota_v_code',
    label: 'OTA版本编号',
    component: 'Input',
    required: true,
  },
  {
    field: 'ota_v_md5',
    label: 'OTA版本MD5',
    component: 'Input',
    required: true,
  },
  {
    field: 'ota_name',
    label: '所属OTA',
    component: 'TreeSelect',
    componentProps: {
      fieldNames: {
        label: 'ota_name',
        key: 'ota_main_id',
        value: 'ota_main_id',
      },
      getPopupContainer: () => document.body,
    },
    required: true,
  },
  {
    field: 'ota_v_image',
    label: 'OTA版本图标',
    required: false,
    component: 'Upload',
    componentProps: {
      api: uploadApi,
    },
  },
  {
    field: 'ota_v_file',
    label: '安装文件',
    required: true,
    component: 'UploadBig',
  },
  {
    field: 'ota_v_default',
    label: '是否默认版本',
    required: true,
    component: 'RadioButtonGroup',
    defaultValue: 0,
    componentProps: {
      options: [
        { label: '非默认版本', value: 0 },
        { label: '默认版本', value: 1 },
      ],
    },
  },
  {
    field: 'ota_v_remark',
    label: 'OTA版本备注',
    component: 'InputTextArea',
  },
];
