//import { getAllRoleList, isProductExist } from '/@/api/demo/system';
import { BasicColumn } from '/@/components/Table';
import { FormSchema } from '/@/components/Table';
import { uploadApi } from '/@/api/sys/upload';
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
    title: '所属项目',
    dataIndex: 'pro_name',
    width: 120,
  },
  {
    title: '设备类型图标',
    dataIndex: 'prod_image',
    width: 120,
    customRender: ({ record }) => {
      // @ts-ignore
      return h(Img, { src: record.prod_image, imgwidth: '80' });
    },
  },
  {
    title: '创建时间',
    dataIndex: 'gmt_create',
    width: 180,
  },
  {
    title: '备注',
    dataIndex: 'prod_remark',
  },
];

export const searchFormSchema: FormSchema[] = [
  {
    field: 'prod_name',
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

export const productFormSchema: FormSchema[] = [
  {
    field: 'id',
    label: '自增编号',
    required: false,
    component: 'Input',
    dynamicDisabled: true,
  },
  {
    field: 'prod_name',
    label: '设备类型名称',
    required: true,
    component: 'Input',
  },
  {
    field: 'prod_code',
    label: '设备类型编号',
    required: true,
    component: 'Input',
  },
  {
    field: 'pro_name',
    label: '所属项目',
    component: 'TreeSelect',
    componentProps: {
      fieldNames: {
        label: 'pro_name',
        key: 'project_id',
        value: 'project_id',
      },
      getPopupContainer: () => document.body,
    },
    required: true,
  },
  {
    field: 'prod_image',
    label: '设备类型图标',
    required: false,
    component: 'Upload',
    componentProps: {
      api: uploadApi,
    },
  },
  {
    label: '备注',
    field: 'prod_remark',
    component: 'InputTextArea',
  },
  /*{
    field: 'prod_name',
    label: '设备类型名称',
    component: 'Input',
    helpMessage: ['本字段演示异步验证', '不能输入带有admin的设备类型名称'],
    rules: [
      {
        required: true,
        message: '请输入设备类型名称',
      },
      {
        validator(_, value) {
          return new Promise((resolve, reject) => {
            isProductExist(value)
              .then(() => resolve())
              .catch((err) => {
                reject(err.message || '验证失败');
              });
          });
        },
      },
    ],
  },*/
  /*{
    label: '角色',
    field: 'role',
    component: 'ApiSelect',
    componentProps: {
      api: getAllRoleList,
      labelField: 'roleName',
      valueField: 'roleValue',
    },
    required: true,
  },*/
];
