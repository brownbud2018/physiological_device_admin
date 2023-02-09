import { BasicColumn } from '/@/components/Table';
import { FormSchema } from '/@/components/Table';

export const columns: BasicColumn[] = [
  {
    title: '授权名称',
    dataIndex: 'class_name',
    width: 120,
  },
  {
    title: '授权编号',
    dataIndex: 'class_code',
    width: 120,
  },
  {
    title: '权限名称',
    dataIndex: 'detail_name',
    width: 120,
  },
  {
    title: '权限编号',
    dataIndex: 'detail_code',
    width: 120,
  },
];

// @ts-ignore
export const searchFormSchema: FormSchema[] = [
  {
    field: 'auth_name',
    label: '名称/编号：',
    component: 'Input',
    colProps: { span: 8 },
  },
];

export const authaboutFormSchema: FormSchema[] = [
  {
    field: 'id',
    label: '自增编号',
    required: false,
    component: 'Input',
    dynamicDisabled: true,
  },
  {
    field: 'class_id',
    label: '授权',
    component: 'TreeSelect',
    componentProps: {
      fieldNames: {
        label: 'class_name',
        key: 'class_id',
        value: 'class_id',
      },
      getPopupContainer: () => document.body,
    },
    required: true,
  },
  {
    field: 'detail_id',
    label: '权限',
    component: 'TreeSelect',
    componentProps: {
      fieldNames: {
        label: 'detail_name',
        key: 'detail_id',
        value: 'detail_id',
      },
      getPopupContainer: () => document.body,
    },
    required: true,
  },
];
