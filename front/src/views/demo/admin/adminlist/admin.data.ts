//import { getAllRoleList, isAdminExist } from '/@/api/demo/system';
// @ts-ignore
import { setAdminType, setAdminType1 } from '/@/api/demo/admin';
import { BasicColumn, FormSchema } from '/@/components/Table';
import { uploadApi } from '/@/api/sys/upload';
import { h } from 'vue';
import { Img } from '/@/components/Img';
import { Switch } from 'ant-design-vue';
import { useMessage } from '/@/hooks/web/useMessage';

export const columns: BasicColumn[] = [
  {
    title: '角色名称',
    dataIndex: 'role_name',
    width: 120,
  },
  {
    title: '管理员用户名',
    dataIndex: 'name',
    width: 120,
  },
  {
    title: '管理员昵称',
    dataIndex: 'nickname',
    width: 120,
  },
  {
    title: '最后登录地址',
    dataIndex: 'address',
    width: 120,
  },
  {
    title: '是否禁用',
    dataIndex: 'is_active',
    width: 120,
    customRender: ({ record }) => {
      if (!Reflect.has(record, 'pendingStatus')) {
        record.pendingStatus = false;
      }
      return h(Switch, {
        checked: record.is_active === 1,
        checkedChildren: '已启用',
        unCheckedChildren: '已禁用',
        loading: record.pendingStatus,
        onChange(checked: boolean) {
          record.pendingStatus = true;
          const newType = checked ? 1 : 0;
          const { createMessage } = useMessage();
          //setRoleStatus(record.id, newStatus)
          setAdminType(record.id, newType)
            .then(() => {
              record.is_active = newType;
              createMessage.success('成功设置启用/禁用');
            })
            .catch(() => {
              createMessage.error('启用/禁用失败');
            })
            .finally(() => {
              record.pendingStatus = false;
            });
        },
      });
    },
  },
  {
    title: '是否超级管理员',
    dataIndex: 'user_type',
    width: 120,
    customRender: ({ record }) => {
      if (!Reflect.has(record, 'pendingStatus')) {
        record.pendingStatus = false;
      }
      return h(Switch, {
        checked: record.user_type === 1,
        checkedChildren: '是',
        unCheckedChildren: '否',
        loading: record.pendingStatus,
        onChange(checked: boolean) {
          record.pendingStatus = true;
          const newType = checked ? 1 : 0;
          const { createMessage } = useMessage();
          //setRoleStatus(record.id, newStatus)
          setAdminType1(record.id, newType)
            .then(() => {
              record.user_type = newType;
              createMessage.success('成功设置超级管理员');
            })
            .catch(() => {
              createMessage.error('设置超级管理员失败');
            })
            .finally(() => {
              record.pendingStatus = false;
            });
        },
      });
    },
  },
  {
    title: '管理员头像',
    dataIndex: 'image',
    width: 120,
    customRender: ({ record }) => {
      // @ts-ignore
      return h(Img, { src: record.image, imgwidth: '80' });
    },
  },
  {
    title: '关联医生姓名',
    dataIndex: 'professor_name',
    width: 100,
  },
  {
    title: '创建时间',
    dataIndex: 'gmt_create',
    width: 180,
  },
];

export const searchFormSchema: FormSchema[] = [
  {
    field: 'admin_name',
    label: '管理员名称',
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
export const adminFormSchema: FormSchema[] = [
  {
    field: 'id',
    label: '自增编号',
    required: false,
    component: 'Input',
    dynamicDisabled: true,
  },
  {
    field: 'name',
    label: '管理员用户名',
    component: 'Input',
    rules: [
      {
        required: true,
        message: '用户名已存在',
      },
    ],
  },
  {
    label: '管理员昵称',
    field: 'nickname',
    component: 'InputTextArea',
  },
  {
    field: 'role_name',
    label: '所属角色',
    component: 'TreeSelect',
    componentProps: {
      fieldNames: {
        label: 'role_name',
        key: 'role_id',
        value: 'role_id',
      },
      getPopupContainer: () => document.body,
    },
    required: true,
  },
  {
    field: 'professor_name',
    label: '所属医生',
    component: 'TreeSelect',
    componentProps: {
      fieldNames: {
        label: 'professor_name',
        key: 'professor_id',
        value: 'professor_id',
      },
      getPopupContainer: () => document.body,
    },
    required: true,
  },
  {
    field: 'image',
    label: 'admin图标',
    required: false,
    component: 'Upload',
    componentProps: {
      api: uploadApi,
    },
  },
  {
    field: 'is_active',
    label: '是否启用',
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
    field: 'user_type',
    label: '超级管理员',
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
    label: '地址',
    field: 'address',
    component: 'InputTextArea',
  },
];
