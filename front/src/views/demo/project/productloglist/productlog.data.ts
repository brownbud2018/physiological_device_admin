import { BasicColumn } from '/@/components/Table';
import { FormSchema } from '/@/components/Table';

export const columns: BasicColumn[] = [
  {
    title: 'LOG编号',
    dataIndex: 'log_code',
    width: 120,
  },
  {
    title: 'Device编号',
    dataIndex: 'device_code',
    width: 120,
  },
  {
    title: 'Device名称',
    dataIndex: 'device_name',
    width: 120,
  },
  {
    title: '创建时间',
    dataIndex: 'gmt_create',
    width: 180,
  },
];

export const searchFormSchema: FormSchema[] = [
  {
    field: 'log_name',
    label: '名称/编号：',
    component: 'Input',
    colProps: { span: 8 },
  },
];

export const productlogFormSchema: FormSchema[] = [
  {
    field: 'id',
    label: '自增编号',
    required: false,
    component: 'Input',
    dynamicDisabled: true,
  },
  {
    field: 'log_code',
    label: 'LOG编号',
    required: false,
    component: 'Input',
  },
  {
    field: 'device_id',
    label: 'Device',
    component: 'TreeSelect',
    componentProps: {
      fieldNames: {
        label: 'device_name',
        key: 'device_id',
        value: 'device_id',
      },
      getPopupContainer: () => document.body,
    },
    required: true,
  },
];
