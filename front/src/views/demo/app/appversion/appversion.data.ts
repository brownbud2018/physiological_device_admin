import { BasicColumn } from '/@/components/Table';
import { FormSchema } from '/@/components/Table';
import { uploadApi } from '/@/api/sys/upload';
import { h } from 'vue';
import { Img } from '/@/components/Img';
import { Switch } from 'ant-design-vue';
import { useMessage } from '/@/hooks/web/useMessage';
import { setAppversionType } from '/@/api/demo/appversion';

export const columns: BasicColumn[] = [
  {
    title: 'APP版本名称',
    dataIndex: 'app_v_name',
    width: 120,
  },
  {
    title: 'APP版本编号',
    dataIndex: 'app_v_code',
    width: 120,
  },
  {
    title: 'APP名称',
    dataIndex: 'app_name',
    width: 120,
  },
  {
    title: '是否默认',
    dataIndex: 'app_v_default',
    width: 120,
    customRender: ({ record }) => {
      if (!Reflect.has(record, 'pendingStatus')) {
        record.pendingStatus = false;
      }
      return h(Switch, {
        checked: record.app_v_default === 1,
        checkedChildren: '默认版本',
        unCheckedChildren: '非默认版本',
        loading: record.pendingStatus,
        onChange(checked: boolean) {
          record.pendingStatus = true;
          const newType = checked ? 1 : 0;
          const { createMessage } = useMessage();
          //setRoleStatus(record.id, newStatus)
          setAppversionType(record.id, newType)
            .then(() => {
              record.app_v_default = newType;
              createMessage.success('成功设置默认版本');
              location.reload();
              // @ts-ignore
              //const [reload] = useTable;
              //reload();
            })
            .catch(() => {
              createMessage.error('设置默认版本失败');
            })
            .finally(() => {
              record.pendingStatus = false;
            });
        },
      });
    },
  },
  {
    title: 'APP版本图标',
    dataIndex: 'app_v_image',
    width: 120,
    customRender: ({ record }) => {
      // @ts-ignore
      return h(Img, { src: record.app_v_image, imgwidth: '80' });
    },
  },
  {
    title: 'APP版本文件地址',
    dataIndex: 'app_v_file',
    width: 260,
  },
  {
    title: 'APP版本备注',
    dataIndex: 'app_v_remark',
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
    field: 'appversion_name',
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
export const appversionFormSchema: FormSchema[] = [
  {
    field: 'id',
    label: '自增编号',
    required: false,
    component: 'Input',
    dynamicDisabled: true,
  },
  {
    field: 'app_v_name',
    label: 'APP版本名称',
    required: true,
    component: 'Input',
  },
  {
    field: 'app_v_code',
    label: 'APP版本编号',
    component: 'Input',
    required: true,
  },
  {
    field: 'app_name',
    label: '所属APP',
    component: 'TreeSelect',
    componentProps: {
      fieldNames: {
        label: 'app_name',
        key: 'app_pro_id',
        value: 'app_pro_id',
      },
      getPopupContainer: () => document.body,
    },
    required: true,
  },
  {
    field: 'app_v_image',
    label: 'APP版本图标',
    required: false,
    component: 'Upload',
    componentProps: {
      api: uploadApi,
    },
  },
  {
    field: 'app_v_file',
    label: '安装文件',
    required: true,
    component: 'UploadBig',
  },
  {
    field: 'app_v_default',
    label: '是否默认版本',
    required: true,
    component: 'RadioButtonGroup',
    defaultValue: 0,
    componentProps: {
      options: [
        { label: '非默认版本', value: 0 },
        { label: '默认版本', value: 1 },
      ],
    },
  },
  {
    field: 'app_v_remark',
    label: 'APP版本备注',
    component: 'InputTextArea',
  },
];
