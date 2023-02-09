import { BasicColumn } from '/@/components/Table';
import { FormSchema } from '/@/components/Table';
import { uploadApi } from '/@/api/sys/upload';
import { h } from 'vue';
import { Img } from '/@/components/Img';

export const columns: BasicColumn[] = [
  {
    title: '设备类型名称',
    dataIndex: 'prod_name',
    width: 120,
  },
  {
    title: '设备类型编号',
    dataIndex: 'prod_code',
    width: 120,
  },
  {
    title: 'OTA名称',
    dataIndex: 'ota_name',
    width: 180,
  },
  {
    title: 'OTA编号',
    dataIndex: 'ota_code',
    width: 120,
  },
  {
    title: 'OTA图标',
    dataIndex: 'ota_image',
    width: 120,
    customRender: ({ record }) => {
      // @ts-ignore
      return h(Img, { src: record.ota_image, imgwidth: '80' });
    },
  },
  {
    title: 'OTA包名',
    dataIndex: 'ota_package',
    width: 260,
  },
  {
    title: 'OTA属性',
    dataIndex: 'ota_type',
    width: 120,
    customRender: ({ record }) => {
      if (record.ota_type == 0) {
        return '非内置应用';
      } else {
        return '内置应用';
      }
    },
  },
  {
    title: 'OTA更新属性',
    dataIndex: 'ota_update_type',
    width: 120,
    customRender: ({ record }) => {
      if (record.ota_update_type == 0) {
        return '非强制更新';
      } else {
        return '强制更新';
      }
    },
  },
  {
    title: '创建时间',
    dataIndex: 'gmt_create',
    width: 180,
  },
];

export const searchFormSchema: FormSchema[] = [
  {
    field: 'prod_name',
    label: '设备名称/编号/备注',
    component: 'Input',
    colProps: { span: 8 },
  },
  {
    field: 'ota_name',
    label: 'OTA名称/编号/备注',
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
export const productotaFormSchema: FormSchema[] = [
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
    component: 'Upload',
    componentProps: {
      api: uploadApi,
    },
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
