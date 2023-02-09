import { BasicColumn } from '/@/components/Table';
import { FormSchema } from '/@/components/Table';
import { uploadApi } from '/@/api/sys/upload';
import { h } from 'vue';
import { Img } from '/@/components/Img';

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
    title: '授权图标',
    dataIndex: 'class_image',
    width: 120,
    customRender: ({ record }) => {
      // @ts-ignore
      return h(Img, { src: record.class_image, imgwidth: '80' });
    },
  },
  {
    title: '授权描述',
    dataIndex: 'class_desc',
  },
  {
    title: '备注',
    dataIndex: 'class_remark',
  },
  {
    title: '创建时间',
    dataIndex: 'gmt_create',
    width: 180,
  },
];

export const searchFormSchema: FormSchema[] = [
  {
    field: 'class_name',
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

export const authFormSchema: FormSchema[] = [
  {
    field: 'id',
    label: '自增编号',
    required: false,
    component: 'Input',
    dynamicDisabled: true,
  },
  {
    field: 'class_name',
    label: '授权名称',
    required: true,
    component: 'Input',
  },
  {
    field: 'class_code',
    label: '授权编号',
    required: true,
    component: 'Input',
  },
  {
    field: 'class_image',
    label: '授权图标',
    required: false,
    component: 'Upload',
    componentProps: {
      api: uploadApi,
    },
  },
  {
    label: '授权描述',
    field: 'class_desc',
    component: 'InputTextArea',
  },
  {
    label: '授权备注',
    field: 'class_remark',
    component: 'InputTextArea',
  },
];
