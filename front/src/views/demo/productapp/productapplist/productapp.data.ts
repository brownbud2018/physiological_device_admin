import { BasicColumn } from '/@/components/Table';
import { FormSchema } from '/@/components/Table';

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
    title: 'APP名称',
    dataIndex: 'app_name',
    width: 120,
  },
  {
    title: 'APP编号',
    dataIndex: 'app_code',
    width: 120,
  },
];

export const searchFormSchema: FormSchema[] = [
  {
    field: 'productapp_name',
    label: '名称/编号：',
    component: 'Input',
    colProps: { span: 8 },
  },
];

export const productappFormSchema: FormSchema[] = [
  {
    field: 'id',
    label: '自增编号',
    required: false,
    component: 'Input',
    dynamicDisabled: true,
  },
  {
    field: 'prod_id',
    label: '设备类型',
    component: 'TreeSelect',
    componentProps: {
      fieldNames: {
        label: 'prod_name',
        key: 'prod_id',
        value: 'prod_id',
      },
      getPopupContainer: () => document.body,
    },
    required: true,
  },
  {
    field: 'app_pro_id',
    label: 'APP',
    component: 'TreeSelect',
    componentProps: {
      fieldNames: {
        label: 'app_name',
        key: 'app_pro_id',
        value: 'app_pro_id',
      },
      getPopupContainer: () => document.body,
    },
    required: true,
  },
];
