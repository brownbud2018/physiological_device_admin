import { BasicColumn } from '/@/components/Table';
import { FormSchema } from '/@/components/Table';
export const columns: BasicColumn[] = [
  {
    title: '日志编号',
    dataIndex: 'log_code',
    width: 120,
  },
  {
    title: '日志地址',
    dataIndex: 'log_image',
    width: 180,
  },
  {
    title: '创建时间',
    dataIndex: 'gmt_create',
    width: 180,
  },
  {
    title: 'device编号',
    dataIndex: 'device_code',
    width: 120,
  },
  {
    title: 'device名称',
    dataIndex: 'name',
    width: 120,
  },
];

export const searchFormSchema: FormSchema[] = [
  {
    field: 'search_name',
    label: '名称/编号',
    component: 'Input',
    colProps: { span: 8 },
  },
];
