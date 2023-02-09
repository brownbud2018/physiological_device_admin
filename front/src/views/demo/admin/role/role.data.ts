import { BasicColumn } from '/@/components/Table';
import { FormSchema } from '/@/components/Table';
import { h } from 'vue';
import { Switch } from 'ant-design-vue';
import { setRoleType } from '/@/api/demo/role';
import { useMessage } from '/@/hooks/web/useMessage';
//列表
//
export const columns: BasicColumn[] = [
  {
    title: '角色名称',
    dataIndex: 'role_name',
    width: 200,
  },
  {
    title: '角色启用状态',
    dataIndex: 'role_status',
    width: 120,
    customRender: ({ record }) => {
      if (!Reflect.has(record, 'pendingStatus')) {
        record.pendingStatus = false;
      }
      return h(Switch, {
        checked: record.role_status === 1,
        checkedChildren: '已启用',
        unCheckedChildren: '已禁用',
        loading: record.pendingStatus,
        onChange(checked: boolean) {
          record.pendingStatus = true;
          const newType = checked ? 1 : 0;
          const { createMessage } = useMessage();
          //setRoleStatus(record.id, newStatus)
          setRoleType(record.id, newType)
            .then(() => {
              record.role_status = newType;
              createMessage.success(`已成功修改角色状态`);
            })
            .catch(() => {
              createMessage.error('修改角色状态');
            })
            .finally(() => {
              record.pendingStatus = false;
            });
        },
      });
    },
  },
  {
    title: '描述',
    dataIndex: 'role_desc',
  },
  {
    title: '创建时间',
    dataIndex: 'gmt_create',
    width: 180,
  },
];
//搜索
export const searchFormSchema: FormSchema[] = [
  {
    field: 'role_name',
    label: '角色名称',
    component: 'Input',
    colProps: { span: 8 },
  },
  {
    field: 'role_status',
    label: '角色启用',
    component: 'Select',
    componentProps: {
      options: [
        { label: '已禁用', value: '0' },
        { label: '已启用', value: '1' },
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
    field: 'role_name',
    label: '角色名称',
    required: true,
    component: 'Input',
  },
  {
    field: 'role_status',
    label: '角色启用',
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
    field: 'role_desc',
    label: '角色描述',
    component: 'InputTextArea',
  },
  {
    label: ' ',
    field: 'menu',
    slot: 'menu',
    component: 'Input',
  },
];
