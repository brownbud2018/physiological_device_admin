//import { getAllRoleList, isAccessExist } from '/@/api/demo/system';
// @ts-ignore
import { setAccessType, setAccessType1 } from '/@/api/demo/access';
import { BasicColumn, FormSchema } from '/@/components/Table';
//import { uploadApi } from '/@/api/sys/upload';
import { h } from 'vue';
//import { Img } from '/@/components/Img';
import { Switch } from 'ant-design-vue';
import { useMessage } from '/@/hooks/web/useMessage';
import { Icon } from '/@/components/Icon';

export const columns: BasicColumn[] = [
  {
    title: '权限编号',
    dataIndex: 'access_code',
    width: 240,
    align: 'left',
  },
  {
    title: '权限名称',
    dataIndex: 'access_name',
    width: 120,
  },
  {
    title: '图标',
    dataIndex: 'menu_icon',
    width: 50,
    customRender: ({ record }) => {
      return h(Icon, { icon: record.menu_icon });
    },
  },
  {
    title: '目录',
    dataIndex: 'access_path',
    width: 180,
  },
  {
    title: '详细路径',
    dataIndex: 'access_redirect',
    width: 180,
  },
  {
    title: '是否验证',
    dataIndex: 'is_check',
    width: 120,
    customRender: ({ record }) => {
      if (!Reflect.has(record, 'pendingStatus')) {
        record.pendingStatus = false;
      }
      return h(Switch, {
        checked: record.is_check === 1,
        checkedChildren: '是',
        unCheckedChildren: '否',
        loading: record.pendingStatus,
        onChange(checked: boolean) {
          record.pendingStatus = true;
          const newType = checked ? 1 : 0;
          const { createMessage } = useMessage();
          //setRoleStatus(record.id, newStatus)
          setAccessType(record.id, newType)
            .then(() => {
              record.is_check = newType;
              createMessage.success('成功设置验证');
            })
            .catch(() => {
              createMessage.error('设置验证失败');
            })
            .finally(() => {
              record.pendingStatus = false;
            });
        },
      });
    },
  },
  {
    title: '是否菜单',
    dataIndex: 'is_menu',
    width: 120,
    customRender: ({ record }) => {
      if (!Reflect.has(record, 'pendingStatus')) {
        record.pendingStatus = false;
      }
      return h(Switch, {
        checked: record.is_menu === 1,
        checkedChildren: '是',
        unCheckedChildren: '否',
        loading: record.pendingStatus,
        onChange(checked: boolean) {
          record.pendingStatus = true;
          const newType = checked ? 1 : 0;
          const { createMessage } = useMessage();
          //setRoleStatus(record.id, newStatus)
          setAccessType1(record.id, newType)
            .then(() => {
              record.is_menu = newType;
              createMessage.success('成功设置菜单');
            })
            .catch(() => {
              createMessage.error('启用菜单失败');
            })
            .finally(() => {
              record.pendingStatus = false;
            });
        },
      });
    },
  },
  {
    title: '父权限名称',
    dataIndex: 'parent_name',
    width: 120,
  },
  {
    title: '权限排序',
    dataIndex: 'sort_order',
    width: 120,
  },
  {
    title: '权限描述',
    dataIndex: 'access_desc',
    width: 120,
  },
  {
    title: '权限备注',
    dataIndex: 'access_remark',
    width: 120,
  },
  {
    title: '创建时间',
    dataIndex: 'gmt_create',
    width: 180,
  },
  /*{
    title: '路由',
    dataIndex: 'access_component',
    width: 120,
  },
  {
    title: '权限头像',
    dataIndex: 'access_image',
    width: 120,
    customRender: ({ record }) => {
      // @ts-ignore
      return h(Img, { src: record.access_image, imgwidth: '80' });
    },
  },*/
];

export const searchFormSchema: FormSchema[] = [
  {
    field: 'access_name',
    label: '权限名称',
    component: 'Input',
    colProps: { span: 8 },
  },
  {
    field: 'is_check',
    label: '是否验证权限',
    component: 'Select',
    componentProps: {
      options: [
        { label: '不验证', value: '0' },
        { label: '需验证', value: '1' },
      ],
    },
    colProps: { span: 8 },
  },
];

// @ts-ignore
export const accessFormSchema: FormSchema[] = [
  {
    field: 'id',
    label: '自增编号',
    required: false,
    component: 'Input',
    dynamicDisabled: true,
  },
  {
    label: '权限编号',
    field: 'access_code',
    component: 'Input',
  },
  {
    label: '权限名称',
    field: 'access_name',
    component: 'Input',
  },
  {
    label: '权限目录',
    field: 'access_path',
    component: 'Input',
  },
  {
    label: '详细路径',
    field: 'access_redirect',
    component: 'Input',
  },
  {
    label: '权限排序',
    field: 'sort_order',
    component: 'Input',
  },
  {
    field: 'menu_icon',
    label: '权限图标',
    component: 'Input',
  },
  {
    field: 'parent_name',
    label: '所属父权限',
    component: 'TreeSelect',
    componentProps: {
      fieldNames: {
        label: 'access_name',
        key: 'access_id',
        value: 'access_id',
      },
      getPopupContainer: () => document.body,
    },
  },
  {
    field: 'is_check',
    label: '是否验证',
    required: true,
    component: 'RadioButtonGroup',
    defaultValue: 0,
    componentProps: {
      options: [
        { label: '已禁用', value: 0 },
        { label: '已启用', value: 1 },
      ],
    },
  },
  {
    field: 'is_menu',
    label: '是否菜单',
    required: true,
    component: 'RadioButtonGroup',
    defaultValue: 0,
    componentProps: {
      options: [
        { label: '否', value: 0 },
        { label: '是', value: 1 },
      ],
    },
  },
  {
    label: '描述',
    field: 'access_desc',
    component: 'InputTextArea',
  },
  {
    label: '备注',
    field: 'access_remark',
    component: 'InputTextArea',
  },
  /*{
    label: '权限路由',
    field: 'access_component',
    component: 'Input',
  },
  {
    field: 'access_image',
    label: '权限头像',
    required: false,
    component: 'Upload',
    componentProps: {
      api: uploadApi,
    },
  },*/
];
