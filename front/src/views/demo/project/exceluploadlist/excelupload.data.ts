import { BasicColumn } from '/@/components/Table';
import { FormSchema } from '/@/components/Table';
import { uploadApi } from '/@/api/sys/upload';
import { h } from 'vue';
import { Img } from '/@/components/Img';
//列表
export const columns: BasicColumn[] = [
  {
    title: '上传名称',
    dataIndex: 'excel_name',
    width: 200,
  },
  {
    title: '上传编号',
    dataIndex: 'excel_code',
    width: 120,
  },
  {
    title: '上传地址',
    dataIndex: 'excel_address',
    width: 220,
  },
  {
    title: '是否导入',
    dataIndex: 'is_import',
    width: 100,
    customRender: ({ record }) => {
      if (record.is_import === 1) {
        return '已导入';
      } else {
        return '未导入';
      }
    },
  },
  {
    title: 'Device名称',
    dataIndex: 'name',
    width: 120,
  },
  {
    title: 'Device密码',
    dataIndex: 'hashed_password',
    width: 120,
  },
  {
    title: '所属设备类型',
    dataIndex: 'prod_name',
    width: 120,
  },
  {
    title: 'Device版本',
    dataIndex: 'version',
    width: 120,
  },
  {
    title: '所属OTA',
    dataIndex: 'ota_name',
    width: 180,
  },
  {
    title: '等级权限',
    dataIndex: 'device_level',
    width: 120,
    customRender: ({ record }) => {
      if (record.device_level === 0) {
        return '普通等级';
      }
      if (record.device_level === 1) {
        return '授权等级';
      }
      if (record.device_level === 2) {
        return 'VIP等级';
      } else {
        return '未知等级';
      }
    },
  },
  {
    title: '授权类',
    dataIndex: 'class_name',
    width: 180,
  },
  {
    title: '是否激活',
    dataIndex: 'is_active',
    width: 120,
    customRender: ({ record }) => {
      if (record.is_active === 1) {
        return '已激活';
      } else {
        return '未激活';
      }
    },
  },
  {
    title: 'device图标',
    dataIndex: 'image',
    width: 120,
    customRender: ({ record }) => {
      // @ts-ignore
      return h(Img, { src: record.image, imgwidth: '80' });
    },
  },
  {
    title: '创建时间',
    dataIndex: 'gmt_create',
    width: 180,
  },
  {
    title: '备注',
    dataIndex: 'excel_remark',
  },
];
//搜索
export const searchFormSchema: FormSchema[] = [
  {
    field: 'search_name',
    label: '上传名称',
    component: 'Input',
    colProps: { span: 8 },
  },
  {
    field: 'is_import',
    label: '上传是否导入',
    component: 'Select',
    componentProps: {
      options: [
        { label: '未导入', value: '0' },
        { label: '已导入', value: '1' },
      ],
    },
    colProps: { span: 8 },
  },
];
//新增/修改弹出编辑界面，绑定字段
export const formSchema: FormSchema[] = [
  {
    field: 'id',
    label: '自增编号',
    required: false,
    component: 'Input',
    dynamicDisabled: true,
  },
  {
    field: 'excel_name',
    label: '上传名称',
    required: true,
    component: 'Input',
  },
  {
    field: 'excel_code',
    label: '上传编号',
    required: true,
    component: 'Input',
  },
  {
    field: 'excel_address',
    label: '上传地址',
    required: false,
    component: 'Upload',
    componentProps: {
      api: uploadApi,
    },
  },
  {
    field: 'name',
    label: 'device名称',
    required: true,
    component: 'Input',
  },
  {
    field: 'hashed_password',
    label: 'device密码',
    required: true,
    component: 'InputPassword',
  },
  {
    field: 'version',
    label: 'device版本',
    required: false,
    component: 'Input',
  },
  {
    field: 'prod_name',
    label: '所属设备类型',
    component: 'TreeSelect',
    componentProps: {
      fieldNames: {
        label: 'prod_name',
        key: 'product_id',
        value: 'product_id',
      },
      getPopupContainer: () => document.body,
    },
    required: true,
  },
  {
    field: 'ota_name',
    label: '所属OTA',
    component: 'TreeSelect',
    componentProps: {
      fieldNames: {
        label: 'ota_name',
        key: 'device_ota',
        value: 'device_ota',
      },
      getPopupContainer: () => document.body,
    },
    required: true,
  },
  {
    field: 'class_name',
    label: '所属授权类',
    component: 'TreeSelect',
    componentProps: {
      fieldNames: {
        label: 'class_name',
        key: 'device_auth_class_id',
        value: 'device_auth_class_id',
      },
      getPopupContainer: () => document.body,
    },
    required: true,
  },
  {
    field: 'image',
    label: 'device图标',
    required: false,
    component: 'Upload',
    componentProps: {
      api: uploadApi,
    },
  },
  {
    field: 'is_active',
    label: '是否激活',
    required: true,
    component: 'RadioButtonGroup',
    defaultValue: 0,
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
    defaultValue: 0,
    componentProps: {
      options: [
        { label: '普通等级', value: 0 },
        { label: '授权等级', value: 1 },
        { label: 'VIP等级', value: 2 },
      ],
    },
  },
  {
    label: '地址',
    field: 'address',
    component: 'InputTextArea',
  },
  {
    field: 'excel_remark',
    label: '上传备注',
    component: 'InputTextArea',
  },
];
