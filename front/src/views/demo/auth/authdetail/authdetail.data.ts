import { BasicColumn } from '/@/components/Table';
import { FormSchema } from '/@/components/Table';
import { uploadApi } from '/@/api/sys/upload';
import { h } from 'vue';
import { Img } from '/@/components/Img';
import { Switch } from 'ant-design-vue';
import { useMessage } from '/@/hooks/web/useMessage';
import { setAuthdetailType } from '/@/api/demo/authdetail';

export const columns: BasicColumn[] = [
  {
    title: '权限名称',
    dataIndex: 'detail_name',
    width: 160,
  },
  {
    title: '权限编号',
    dataIndex: 'detail_code',
    width: 120,
  },
  {
    title: '授权名称',
    dataIndex: 'class_name',
    width: 260,
  },
  {
    title: '是否默认',
    dataIndex: 'detail_type',
    width: 120,
    customRender: ({ record }) => {
      if (!Reflect.has(record, 'pendingStatus')) {
        record.pendingStatus = false;
      }
      return h(Switch, {
        checked: record.detail_type === 1,
        checkedChildren: '默认属性',
        unCheckedChildren: '特殊属性',
        loading: record.pendingStatus,
        onChange(checked: boolean) {
          record.pendingStatus = true;
          const newType = checked ? 1 : 0;
          const { createMessage } = useMessage();
          //setRoleStatus(record.id, newStatus)
          setAuthdetailType(record.id, newType)
            .then(() => {
              record.detail_type = newType;
              createMessage.success('成功设置权限属性');
              //location.reload();
              // @ts-ignore
              //const [reload] = useTable;
              //reload();
            })
            .catch(() => {
              createMessage.error('设置权限属性失败');
            })
            .finally(() => {
              record.pendingStatus = false;
            });
        },
      });
    },
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
    title: '权限描述',
    dataIndex: 'detail_desc',
    width: 260,
  },
  {
    title: '权限备注',
    dataIndex: 'detail_remark',
    width: 260,
  },
  {
    title: '创建时间',
    dataIndex: 'gmt_create',
    width: 180,
  },
];

export const searchFormSchema: FormSchema[] = [
  {
    field: 'detail_name',
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

// @ts-ignore
export const authdetailFormSchema: FormSchema[] = [
  {
    field: 'id',
    label: '自增编号',
    required: false,
    component: 'Input',
    dynamicDisabled: true,
  },
  {
    field: 'detail_name',
    label: '权限名称',
    required: true,
    component: 'Input',
  },
  {
    field: 'detail_code',
    label: '权限编号',
    component: 'Input',
    required: true,
  },
  {
    field: 'detail_image',
    label: '权限图标',
    required: false,
    component: 'Upload',
    componentProps: {
      api: uploadApi,
    },
  },
  {
    field: 'detail_type',
    label: '是否默认属性',
    required: true,
    component: 'RadioButtonGroup',
    defaultValue: 0,
    componentProps: {
      options: [
        { label: '默认属性', value: 0 },
        { label: '特殊属性', value: 1 },
      ],
    },
  },
  {
    field: 'detail_desc',
    label: '权限描述',
    component: 'InputTextArea',
  },
  {
    field: 'detail_remark',
    label: '权限备注',
    component: 'InputTextArea',
  },
];
