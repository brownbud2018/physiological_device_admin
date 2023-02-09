import { BasicColumn } from '/@/components/Table';
import { FormSchema } from '/@/components/Table';

export const columns: BasicColumn[] = [
  {
    title: '统计编号',
    dataIndex: 'stat_code',
    width: 120,
  },
  {
    title: '统计名称',
    dataIndex: 'stat_name',
    width: 260,
  },
  {
    title: '设备编号',
    dataIndex: 'prod_code',
    width: 120,
  },
  {
    title: '设备名称',
    dataIndex: 'prod_name',
    width: 120,
  },
  {
    title: '统计次数',
    dataIndex: 'stat_num',
    width: 120,
  },
  {
    title: '备注',
    dataIndex: 'remark',
    width: 120,
  },
];

export const searchFormSchema: FormSchema[] = [
  {
    field: 'stat_name',
    label: '名称/编号：',
    component: 'Input',
    colProps: { span: 8 },
  },
];
