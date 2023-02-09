import { BasicColumn } from '/@/components/Table';
import { FormSchema } from '/@/components/Table';
import { timestampToDate1 } from '/@/utils/dateUtil';
import { h } from 'vue';
import { Img } from '/@/components/Img';
import { uploadApi } from "/@/api/sys/upload";
//列表
//
export const columns: BasicColumn[] = [
  {
    title: '医生名称',
    dataIndex: 'professor_name',
    width: 200,
  },
  {
    title: '医生性别',
    dataIndex: 'sex',
    width: 120,
    customRender: ({ record }) => {
      if (record.sex == 0) {
        return '女';
      } else {
        return '男';
      }
    },
  },
  {
    title: '来源',
    dataIndex: 'fromcat',
  },
  {
    title: '主治分类',
    dataIndex: 'cat_name',
  },
  {
    title: '头像',
    dataIndex: 'avatar',
    width: 120,
    customRender: ({ record }) => {
      // @ts-ignore
      return h(Img, { src: record.avatar, imgwidth: '80' });
    },
  },
  {
    title: '邮箱',
    dataIndex: 'email',
    width: 180,
  },
  {
    title: '电话',
    dataIndex: 'phone',
    width: 150,
  },
  {
    title: '职称',
    dataIndex: 'title',
  },
  {
    title: '擅长领域',
    dataIndex: 'expert',
    width: 180,
  },
  {
    title: '专家简介',
    dataIndex: 'resume',
    width: 180,
  },
  {
    title: '创建时间',
    dataIndex: 'reg_time',
    width: 180,
    customRender: ({ record }) => {
      if (record.reg_time == 0) {
        return '外站';
      } else {
        return timestampToDate1(record.reg_time);
      }
    },
  },
];
//搜索
export const searchFormSchema: FormSchema[] = [
  {
    field: 'professor_name',
    label: '医生名称',
    component: 'Input',
    colProps: { span: 8 },
  },
  {
    field: 'sex',
    label: '医生性别',
    component: 'Select',
    componentProps: {
      options: [
        { label: '女', value: '0' },
        { label: '男', value: '1' },
      ],
    },
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
    field: 'professor_name',
    label: '医生名称',
    required: true,
    component: 'Input',
  },
  {
    field: 'cat_name',
    label: '主治分类',
    component: 'TreeSelect',
    componentProps: {
      fieldNames: {
        label: 'cat_name',
        key: 'cat_id',
        value: 'cat_id',
      },
      getPopupContainer: () => document.body,
    },
    required: true,
  },
  {
    field: 'email',
    label: 'email',
    required: true,
    component: 'Input',
  },
  {
    field: 'sex',
    label: '医生性别',
    required: true,
    component: 'RadioButtonGroup',
    defaultValue: 0,
    componentProps: {
      options: [
        { label: '女', value: 0 },
        { label: '男', value: 1 },
      ],
    },
  },
  {
    field: 'title',
    label: '职称',
    required: true,
    component: 'Input',
  },
  {
    field: 'avatar',
    label: '头像',
    required: true,
    component: 'Upload',
    componentProps: {
      api: uploadApi,
    },
  },
  {
    field: 'phone',
    label: '电话',
    required: true,
    component: 'Input',
  },
  {
    field: 'expert',
    label: '擅长领域',
    required: true,
    component: 'InputTextArea',
  },
  {
    field: 'resume',
    label: '专家简介',
    required: true,
    component: 'InputTextArea',
  },
];
