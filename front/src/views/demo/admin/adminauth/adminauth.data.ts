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
    title: '管理员昵称',
    dataIndex: 'nickname',
    width: 120,
  },
  {
    title: '管理员编号',
    dataIndex: 'name',
    width: 120,
  },
];

// @ts-ignore
export const searchFormSchema: FormSchema[] = [
  {
    field: 'class_name',
    label: '名称/编号：',
    component: 'Input',
    colProps: { span: 8 },
  },
];

export const adminauthFormSchema: FormSchema[] = [
  {
    field: 'id',
    label: '自增编号',
    required: false,
    component: 'Input',
    dynamicDisabled: true,
  },
  {
    field: 'admin_id',
    label: '管理员',
    component: 'TreeSelect',
    componentProps: {
      fieldNames: {
        label: 'nickname',
        key: 'admin_id',
        value: 'admin_id',
      },
      getPopupContainer: () => document.body,
    },
    required: true,
  },
  {
    field: 'auth_class_id',
    label: '授权',
    component: 'TreeSelect',
    componentProps: {
      fieldNames: {
        label: 'class_name',
        key: 'auth_class_id',
        value: 'auth_class_id',
      },
      getPopupContainer: () => document.body,
    },
    required: true,
  },
];
