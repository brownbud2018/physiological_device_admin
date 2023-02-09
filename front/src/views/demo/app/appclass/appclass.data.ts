import { BasicColumn } from '/@/components/Table';
import { FormSchema } from '/@/components/Table';
import { h } from 'vue';
import { uploadApi } from '/@/api/sys/upload';
import { Img } from '/@/components/Img';
//列表
export const columns: BasicColumn[] = [
  {
    title: '分类名称',
    dataIndex: 'class_name',
    width: 200,
  },
  {
    title: '分类编号',
    dataIndex: 'class_code',
    width: 180,
  },
  {
    title: '分类图标',
    dataIndex: 'class_image',
    width: 120,
    customRender: ({ record }) => {
      // @ts-ignore
      return h(Img, { src: record.class_image, imgwidth: '80' });
    },
  },
  {
    title: '分类描述',
    dataIndex: 'class_desc',
    width: 180,
  },
  {
    title: '创建时间',
    dataIndex: 'gmt_create',
    width: 180,
  },
  {
    title: '备注',
    dataIndex: 'class_remark',
  },
];
//搜索
export const searchFormSchema: FormSchema[] = [
  {
    field: 'class_name',
    label: '名称/编号/描述/备注',
    component: 'Input',
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
    field: 'class_name',
    label: '分类名称',
    required: true,
    component: 'Input',
  },
  {
    field: 'class_code',
    label: '分类编号',
    required: true,
    component: 'Input',
  },
  {
    field: 'class_image',
    label: '分类图标',
    required: false,
    component: 'Upload',
    componentProps: {
      api: uploadApi,
    },
  },
  {
    field: 'class_desc',
    label: '分类描述',
    component: 'InputTextArea',
  },
  {
    field: 'class_remark',
    label: '分类备注',
    component: 'InputTextArea',
  },
];
