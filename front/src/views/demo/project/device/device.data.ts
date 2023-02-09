//import { getAllRoleList, isDeviceExist } from '/@/api/demo/system';
import { BasicColumn } from '/@/components/Table';
import { FormSchema } from '/@/components/Table';
import { uploadApi } from '/@/api/sys/upload';
import { h } from 'vue';
import { Img } from '/@/components/Img';
import { Switch } from 'ant-design-vue';
import { useMessage } from '/@/hooks/web/useMessage';
import { getProvinceCityList, getProvinceList, setDeviceType } from "/@/api/demo/device";

export const columns: BasicColumn[] = [
  {
    title: '设备类型名称',
    dataIndex: 'prod_name',
    width: 180,
  },
  {
    title: 'Device编号',
    dataIndex: 'device_code',
    width: 180,
  },
  {
    title: 'Device名称',
    dataIndex: 'name',
    width: 180,
  },
  {
    title: 'Device版本',
    dataIndex: 'version',
    width: 100,
  },
  {
    title: '所属OTA',
    dataIndex: 'ota_name',
    width: 120,
  },
  {
    title: '等级权限',
    dataIndex: 'device_level',
    width: 100,
    customRender: ({ record }) => {
      if (record.device_level === 0) {
        return '普通等级';
      }
      if (record.device_level === 1) {
        return '授权等级';
      }
      if (record.device_level === 2) {
        return 'VIP等级';
      } else {
        return '未知等级';
      }
    },
  },
  {
    title: '授权类',
    dataIndex: 'class_name',
    width: 180,
  },
  /*
  `class_id` int(11) DEFAULT NULL COMMENT 'device对应授权类属性ID：例如
  1.V7EN项目授权类1【测试样机】，
  2.V7EN项目授权类2【客户样机】，
  3.V7CN项目授权类1【第一批试产机器】
  4.【等级4】*/
  {
    title: '是否激活',
    dataIndex: 'is_active',
    width: 120,
    customRender: ({ record }) => {
      if (!Reflect.has(record, 'pendingStatus')) {
        record.pendingStatus = false;
      }
      return h(Switch, {
        checked: record.is_active === 1,
        checkedChildren: '已激活',
        unCheckedChildren: '未激活',
        loading: record.pendingStatus,
        onChange(checked: boolean) {
          record.pendingStatus = true;
          const newType = checked ? 1 : 0;
          const { createMessage } = useMessage();
          //setRoleStatus(record.id, newStatus)
          setDeviceType(record.id, newType)
            .then(() => {
              record.is_active = newType;
              createMessage.success('成功激活');
            })
            .catch(() => {
              createMessage.error('激活失败');
            })
            .finally(() => {
              record.pendingStatus = false;
            });
        },
      });
    },
  },
  {
    title: 'device图标',
    dataIndex: 'image',
    width: 120,
    customRender: ({ record }) => {
      // @ts-ignore
      return h(Img, { src: record.image, imgwidth: '80' });
    },
  },
  {
    title: '省份',
    dataIndex: 'province',
    width: 120,
  },
  {
    title: '城市',
    dataIndex: 'city',
    width: 120,
  },
  {
    title: '创建时间',
    dataIndex: 'gmt_create',
    width: 180,
  },
];

export const searchFormSchema: FormSchema[] = [
  {
    field: 'device_name',
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
let provincesdata = [];
let citiesdata = {};
const openPages = async () => {
  let provincecityInfo = {};
  provincecityInfo = await getProvinceCityList();
  provincesdata = provincecityInfo['data']['province'];
  const citiesOptionsData = {
    guangdong: [
      {
        label: '珠海市',
        value: '1',
        key: '1',
      },
      {
        label: '深圳市',
        value: '2',
        key: '2',
      },
      {
        label: '广州市',
        value: '3',
        key: '3',
      },
    ],
    jiangsu: [
      {
        label: '南京市',
        value: '1',
        key: '1',
      },
      {
        label: '无锡市',
        value: '2',
        key: '2',
      },
      {
        label: '苏州市',
        value: '3',
        key: '3',
      },
    ],
  };
  citiesdata = provincecityInfo['data']['city'];
};
openPages();
/*
const provincesOptions = [
  {
    id: 'guangdong',
    label: '广东省',
    value: '1',
    key: '1',
  },
  {
    id: 'jiangsu',
    label: '江苏省',
    value: '2',
    key: '2',
  },
];
const citiesOptionsData = {
  guangdong: [
    {
      label: '珠海市',
      value: '1',
      key: '1',
    },
    {
      label: '深圳市',
      value: '2',
      key: '2',
    },
    {
      label: '广州市',
      value: '3',
      key: '3',
    },
  ],
  jiangsu: [
    {
      label: '南京市',
      value: '1',
      key: '1',
    },
    {
      label: '无锡市',
      value: '2',
      key: '2',
    },
    {
      label: '苏州市',
      value: '3',
      key: '3',
    },
  ],
};*/
// @ts-ignore
// @ts-ignore
// @ts-ignore
export const deviceFormSchema: FormSchema[] = [
  {
    field: 'id',
    label: '自增编号',
    required: false,
    component: 'Input',
    dynamicDisabled: true,
  },
  {
    field: 'name',
    label: 'device名称',
    required: true,
    component: 'Input',
  },
  {
    field: 'device_code',
    label: 'device编号',
    component: 'Input',
    rules: [
      {
        required: true,
        message: 'device编号已存在',
      },
    ],
  },
  /*{
    field: 'hashed_password',
    label: 'device密码',
    required: true,
    component: 'InputPassword',
  },*/
  {
    field: 'version',
    label: 'device版本',
    required: false,
    component: 'Input',
  },
  {
    field: 'prod_name',
    label: '所属设备类型',
    component: 'TreeSelect',
    componentProps: {
      fieldNames: {
        label: 'prod_name',
        key: 'product_id',
        value: 'product_id',
      },
      getPopupContainer: () => document.body,
    },
    required: true,
  },
  {
    field: 'ota_name',
    label: '所属OTA',
    component: 'TreeSelect',
    componentProps: {
      fieldNames: {
        label: 'ota_name',
        key: 'device_ota',
        value: 'device_ota',
      },
      getPopupContainer: () => document.body,
    },
    required: true,
  },
  {
    field: 'class_name',
    label: '所属授权类',
    component: 'TreeSelect',
    componentProps: {
      fieldNames: {
        label: 'class_name',
        key: 'device_auth_class_id',
        value: 'device_auth_class_id',
      },
      getPopupContainer: () => document.body,
    },
    required: true,
  },
  {
    field: 'image',
    label: 'device图标',
    required: false,
    component: 'Upload',
    componentProps: {
      api: uploadApi,
    },
  },
  {
    field: 'is_active',
    label: '是否激活',
    required: true,
    component: 'RadioButtonGroup',
    defaultValue: 0,
    componentProps: {
      options: [
        { label: '未激活', value: 0 },
        { label: '已激活', value: 1 },
      ],
    },
  },
  {
    field: 'device_level',
    label: '等级权限',
    required: true,
    component: 'RadioButtonGroup',
    defaultValue: 0,
    componentProps: {
      options: [
        { label: '普通等级', value: 0 },
        { label: '授权等级', value: 1 },
        { label: 'VIP等级', value: 2 },
      ],
    },
  },
  {
    field: 'provinceid',
    component: 'Select',
    label: '省份',
    colProps: {
      span: 8,
    },
    componentProps: ({ formModel, formActionType }) => {
      return {
        options: provincesdata,
        placeholder: '请选择省份',
        onChange: (e: any) => {
          let citiesOptions = citiesdata[e];
          if (e === undefined) {
            citiesOptions = [];
          }
          formModel.cityid = undefined; //  reset city value
          const { updateSchema } = formActionType;
          updateSchema({
            field: 'cityid',
            componentProps: {
              options: citiesOptions,
            },
          });
        },
      };
    },
  },
  {
    field: 'cityid',
    component: 'Select',
    label: '城市',
    colProps: {
      span: 8,
    },
    componentProps: ({ formModel }) => {
      if (formModel.provinceid != '' && formModel.provinceid != undefined) {
        return {
          options: citiesdata[formModel.provinceid],
          placeholder: '请选择城市',
        };
      } else {
        return {
          options: [],
          placeholder: '请选择城市',
        };
      }
    },
  },
  {
    label: '地址',
    field: 'address',
    component: 'InputTextArea',
  },
];
