import { BasicColumn } from '/@/components/Table';
import { FormSchema } from '/@/components/Table';
import { uploadApi } from '/@/api/sys/upload';
import { h } from 'vue';
import { Img } from '/@/components/Img';
import { Switch } from 'ant-design-vue';
import { useMessage } from '/@/hooks/web/useMessage';
import { setAppType, setAppUpdateType } from '/@/api/demo/app';

export const columns: BasicColumn[] = [
  {
    title: 'APP名称',
    dataIndex: 'app_name',
    width: 120,
  },
  {
    title: 'APP编号',
    dataIndex: 'app_code',
    width: 120,
  },
  {
    title: '所属分类',
    dataIndex: 'class_name',
    width: 120,
  },
  {
    title: 'APP图标',
    dataIndex: 'app_image',
    width: 120,
    customRender: ({ record }) => {
      // @ts-ignore
      return h(Img, { src: record.app_image, imgwidth: '80' });
    },
  },
  {
    title: 'APP包名',
    dataIndex: 'app_package',
    width: 180,
  },
  {
    title: 'APP属性',
    dataIndex: 'app_type',
    width: 120,
    customRender: ({ record }) => {
      if (!Reflect.has(record, 'pendingStatus')) {
        record.pendingStatus = false;
      }
      return h(Switch, {
        checked: record.app_type === 1,
        checkedChildren: '内置应用',
        unCheckedChildren: '应用市场',
        loading: record.pendingStatus,
        onChange(checked: boolean) {
          record.pendingStatus = true;
          const newType = checked ? 1 : 0;
          const { createMessage } = useMessage();
          //setRoleStatus(record.id, newStatus)
          setAppType(record.id, newType)
            .then(() => {
              record.app_type = newType;
              createMessage.success(`已成功修改APP属性`);
            })
            .catch(() => {
              createMessage.error('修改APP属性失败');
            })
            .finally(() => {
              record.pendingStatus = false;
            });
        },
      });
    },
  },
  {
    title: '更新属性',
    dataIndex: 'app_update_type',
    width: 120,
    customRender: ({ record }) => {
      if (!Reflect.has(record, 'pendingStatus')) {
        record.pendingStatus = false;
      }
      return h(Switch, {
        checked: record.app_update_type === 1,
        checkedChildren: '强制更新',
        unCheckedChildren: '非强制更新',
        loading: record.pendingStatus,
        onChange(checked: boolean) {
          record.pendingStatus = true;
          const newType = checked ? 1 : 0;
          const { createMessage } = useMessage();
          //setRoleStatus(record.id, newStatus)
          setAppUpdateType(record.id, newType)
            .then(() => {
              record.app_update_type = newType;
              createMessage.success(`已成功修改更新属性`);
            })
            .catch(() => {
              createMessage.error('修改更新属性失败');
            })
            .finally(() => {
              record.pendingStatus = false;
            });
        },
      });
    },
  },
  {
    title: 'APP简介',
    dataIndex: 'app_info',
    width: 120,
  },
  {
    title: 'APP评分',
    dataIndex: 'app_score',
    width: 120,
  },
  {
    title: '下载次数',
    dataIndex: 'app_download_amount',
    width: 120,
  },
  {
    title: '开发公司',
    dataIndex: 'app_company',
    width: 120,
  },
  {
    title: 'APP描述',
    dataIndex: 'app_desc',
  },
  {
    title: '备注',
    dataIndex: 'app_remark',
  },
  {
    title: '创建时间',
    dataIndex: 'gmt_create',
    width: 180,
  },
];

export const searchFormSchema: FormSchema[] = [
  {
    field: 'app_name',
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

export const appFormSchema: FormSchema[] = [
  {
    field: 'id',
    label: '自增编号',
    required: false,
    component: 'Input',
    dynamicDisabled: true,
  },
  {
    field: 'app_name',
    label: 'APP名称',
    required: true,
    component: 'Input',
  },
  {
    field: 'app_code',
    label: 'APP编号',
    required: true,
    component: 'Input',
  },
  {
    field: 'app_package',
    label: 'APP包名',
    required: true,
    component: 'Input',
  },
  {
    field: 'class_name',
    label: '所属分类',
    component: 'TreeSelect',
    componentProps: {
      fieldNames: {
        label: 'class_name',
        key: 'app_class_id',
        value: 'app_class_id',
      },
      getPopupContainer: () => document.body,
    },
    required: true,
  },
  {
    field: 'app_image',
    label: 'APP图标',
    required: false,
    component: 'Upload',
    componentProps: {
      api: uploadApi,
    },
  },
  {
    field: 'app_type',
    label: 'APP属性',
    required: true,
    component: 'RadioButtonGroup',
    defaultValue: 0,
    componentProps: {
      options: [
        { label: '应用市场', value: 0 },
        { label: '内置应用', value: 1 },
      ],
    },
  },
  {
    field: 'app_update_type',
    label: '更新属性',
    required: true,
    component: 'RadioButtonGroup',
    defaultValue: 0,
    componentProps: {
      options: [
        { label: '非强制更新', value: 0 },
        { label: '强制更新', value: 1 },
      ],
    },
  },
  {
    label: 'APP简介',
    field: 'app_info',
    component: 'InputTextArea',
  },
  {
    label: 'APP评分',
    field: 'app_score',
    component: 'Input',
  },
  {
    label: 'APP下载次数',
    field: 'app_download_amount',
    component: 'Input',
  },
  {
    label: 'APP开发公司',
    field: 'app_company',
    component: 'Input',
  },
  {
    label: 'APP描述',
    field: 'app_desc',
    component: 'InputTextArea',
  },
  {
    label: 'APP备注',
    field: 'app_remark',
    component: 'InputTextArea',
  },
];
