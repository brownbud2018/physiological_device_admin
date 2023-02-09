import { BasicColumn } from '/@/components/Table';
import { FormSchema } from '/@/components/Table';
import { uploadApi } from '/@/api/sys/upload';
import { h } from 'vue';
import { Img } from '/@/components/Img';
import { Switch } from 'ant-design-vue';
import { useMessage } from '/@/hooks/web/useMessage';
import { setOtamainType, setOtamainUpdateType } from '/@/api/demo/otamain';

export const columns: BasicColumn[] = [
  {
    title: 'OTA名称',
    dataIndex: 'ota_name',
    width: 180,
  },
  {
    title: 'OTA编号',
    dataIndex: 'ota_code',
    width: 120,
  },
  {
    title: 'OTA图标',
    dataIndex: 'ota_image',
    width: 120,
    customRender: ({ record }) => {
      // @ts-ignore
      return h(Img, { src: record.ota_image, imgwidth: '80' });
    },
  },
  {
    title: 'OTA包名',
    dataIndex: 'ota_package',
    width: 120,
  },
  {
    title: 'OTA属性',
    dataIndex: 'ota_type',
    width: 120,
    customRender: ({ record }) => {
      if (!Reflect.has(record, 'pendingStatus')) {
        record.pendingStatus = false;
      }
      return h(Switch, {
        checked: record.ota_type === 1,
        checkedChildren: '内置应用',
        unCheckedChildren: '应用市场',
        loading: record.pendingStatus,
        onChange(checked: boolean) {
          record.pendingStatus = true;
          const newType = checked ? 1 : 0;
          const { createMessage } = useMessage();
          //setRoleStatus(record.id, newStatus)
          setOtamainType(record.id, newType)
            .then(() => {
              record.ota_type = newType;
              createMessage.success(`已成功修改OTA属性`);
            })
            .catch(() => {
              createMessage.error('修改OTA属性失败');
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
    dataIndex: 'ota_update_type',
    width: 120,
    customRender: ({ record }) => {
      if (!Reflect.has(record, 'pendingStatus')) {
        record.pendingStatus = false;
      }
      return h(Switch, {
        checked: record.ota_update_type === 1,
        checkedChildren: '强制更新',
        unCheckedChildren: '非强制更新',
        loading: record.pendingStatus,
        onChange(checked: boolean) {
          record.pendingStatus = true;
          const newType = checked ? 1 : 0;
          const { createMessage } = useMessage();
          //setRoleStatus(record.id, newStatus)
          setOtamainUpdateType(record.id, newType)
            .then(() => {
              record.ota_update_type = newType;
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
    title: 'OTA简介',
    dataIndex: 'ota_info',
    width: 120,
  },
  {
    title: 'OTA评分',
    dataIndex: 'ota_score',
    width: 120,
  },
  {
    title: '下载次数',
    dataIndex: 'ota_download_amount',
    width: 120,
  },
  {
    title: '开发公司',
    dataIndex: 'ota_company',
    width: 120,
  },
  {
    title: 'OTA描述',
    dataIndex: 'ota_desc',
  },
  {
    title: '备注',
    dataIndex: 'ota_remark',
  },
  {
    title: '创建时间',
    dataIndex: 'gmt_create',
    width: 180,
  },
];

export const searchFormSchema: FormSchema[] = [
  {
    field: 'ota_name',
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

export const otaFormSchema: FormSchema[] = [
  {
    field: 'id',
    label: '自增编号',
    required: false,
    component: 'Input',
    dynamicDisabled: true,
  },
  {
    field: 'ota_name',
    label: 'OTA名称',
    required: true,
    component: 'Input',
  },
  {
    field: 'ota_code',
    label: 'OTA编号',
    required: true,
    component: 'Input',
  },
  {
    field: 'ota_package',
    label: 'OTA包名',
    required: true,
    component: 'Input',
  },
  {
    field: 'ota_image',
    label: 'OTA图标',
    required: false,
    component: 'Upload',
    componentProps: {
      api: uploadApi,
    },
  },
  {
    field: 'ota_type',
    label: 'OTA属性',
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
    field: 'ota_update_type',
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
    label: 'OTA简介',
    field: 'ota_info',
    component: 'InputTextArea',
  },
  {
    label: 'OTA评分',
    field: 'ota_score',
    component: 'Input',
  },
  {
    label: 'OTA下载次数',
    field: 'ota_download_amount',
    component: 'Input',
  },
  {
    label: 'OTA开发公司',
    field: 'ota_company',
    component: 'Input',
  },
  {
    label: 'OTA描述',
    field: 'ota_desc',
    component: 'InputTextArea',
  },
  {
    label: 'OTA备注',
    field: 'ota_remark',
    component: 'InputTextArea',
  },
];
