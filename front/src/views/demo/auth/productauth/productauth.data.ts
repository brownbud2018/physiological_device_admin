import { BasicColumn } from '/@/components/Table';
import { FormSchema } from '/@/components/Table';
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
    title: '授权名称',
    dataIndex: 'class_name',
    width: 180,
  },
  {
    title: '授权编号',
    dataIndex: 'class_code',
    width: 120,
  },
  {
    title: '授权图标',
    dataIndex: 'class_image',
    width: 120,
    customRender: ({ record }) => {
      // @ts-ignore
      return h(Img, { src: record.class_image, imgwidth: '80' });
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
    field: 'auth_name',
    label: '授权名称/编号',
    component: 'Input',
    colProps: { span: 8 },
  },
];
