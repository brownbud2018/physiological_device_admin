import { BasicColumn, FormSchema } from '/@/components/Table';
import { h } from 'vue';
import { Img } from '/@/components/Img';

export const columns: BasicColumn[] = [
  {
    title: '权限编号',
    dataIndex: 'detail_code',
    width: 120,
  },
  {
    title: '权限名称',
    dataIndex: 'detail_name',
    width: 180,
  },
  {
    title: '权限图标',
    dataIndex: 'detail_image',
    width: 120,
    customRender: ({ record }) => {
      // @ts-ignore
      return h(Img, { src: record.detail_image, imgwidth: '80' });
    },
  },
  {
    title: '默认权限',
    dataIndex: 'detail_type',
    width: 120,
    customRender: ({ record }) => {
      // @ts-ignore
      if (record.detail_type === 1) {
        return '默认权限';
      } else {
        return '特殊权限';
      }
    },
  },
  {
    title: '备注',
    dataIndex: 'detail_remark',
  },
  {
    title: '创建时间',
    dataIndex: 'gmt_create',
    width: 180,
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
