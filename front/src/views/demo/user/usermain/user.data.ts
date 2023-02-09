//import { getAllRoleList, isDeviceExist } from '/@/api/demo/system';
import { BasicColumn } from '/@/components/Table';
import { FormSchema } from '/@/components/Table';
//import { uploadApi } from '/@/api/sys/upload';
import { h } from 'vue';
import { Httpimg } from '/@/components/Httpimg';
//import { Switch } from 'ant-design-vue';
//import { useMessage } from '/@/hooks/web/useMessage';
//import { setDeviceType } from '/@/api/demo/user';

export const columns: BasicColumn[] = [
  {
    title: '用户姓名',
    dataIndex: 'name',
    width: 180,
  },
  {
    title: '串号',
    dataIndex: 'deviceid',
    width: 180,
  },
  {
    title: '设备名',
    dataIndex: 'devicename',
    width: 180,
  },
  {
    title: '测量次数',
    dataIndex: 'getnumber',
    //sorter: true,
    children: [
      {
        title: '血糖',
        dataIndex: 'bloodsugarcount',
        width: 80,
      },
      {
        title: '血压',
        dataIndex: 'bloodpressurecount',
        width: 80,
      },
      {
        title: '心率',
        dataIndex: 'heartratecount',
        width: 80,
      },
      {
        title: '血氧',
        dataIndex: 'bloodoxygencount',
        width: 80,
      },
      {
        title: '体温',
        dataIndex: 'temperaturecount',
        width: 80,
      },
    ],
  },
  {
    title: '用户头像',
    dataIndex: 'headicon',
    width: 120,
    customRender: ({ record }) => {
      if (record.headicon != null && record.headicon != '') {
        // @ts-ignore
        return h(Httpimg, {
          src: 'https://pic.luckystar.com.cn/' + record.headicon + '.jpg',
          imgwidth: '80',
        });
      } else {
        return h(Httpimg, {
          src: '/resource/img/nohead.jpg',
          imgwidth: '80',
        });
      }
    },
  },
  {
    title: '手机号码',
    dataIndex: 'phone',
    width: 120,
  },
  {
    title: '年龄',
    dataIndex: 'age',
    width: 80,
  },
  {
    title: '性别',
    dataIndex: 'sex',
    width: 100,
    customRender: ({ record }) => {
      if (record.sex === '0') {
        return '男';
      } else if (record.sex === '1') {
        return '女';
      } else {
        return '未知';
      }
    },
  },
  {
    title: '身份证号码',
    dataIndex: 'idcard',
    width: 180,
  },
  {
    title: '身高',
    dataIndex: 'height',
    width: 80,
  },
  {
    title: '体重',
    dataIndex: 'weight',
    width: 80,
  },
  {
    title: '城市编号',
    dataIndex: 'cityid',
    width: 80,
  },
  {
    title: '城市名称',
    dataIndex: 'cityname',
    width: 80,
  },
  {
    title: '血型',
    dataIndex: 'bloodtypename',
    width: 80,
  },
  {
    title: '药物过敏史',
    dataIndex: 'allergyname',
    width: 80,
  },
  {
    title: '既往病史',
    dataIndex: 'medicalname',
    width: 100,
  },
  {
    title: '遗传史',
    dataIndex: 'geneticname',
    width: 100,
  },
  {
    title: '健康说明',
    dataIndex: 'descr',
    width: 120,
  },
  {
    title: '创建时间',
    dataIndex: 'createtime',
    width: 180,
  },
];

export const searchFormSchema: FormSchema[] = [
  {
    field: 'user_name',
    label: '姓名',
    component: 'Input',
    colProps: { span: 8 },
  },
  {
    field: 'deviceId',
    label: '串号',
    component: 'Input',
    colProps: { span: 8 },
  },
  {
    field: 'deviceidlength',
    label: '串号长度',
    component: 'Input',
    colProps: { span: 8 },
  },
];

// @ts-ignore
export const userFormSchema: FormSchema[] = [
  {
    field: 'id',
    label: '自增编号',
    required: false,
    component: 'Input',
    dynamicDisabled: true,
  },
  {
    field: 'name',
    label: '用户姓名',
    required: true,
    component: 'Input',
  },
  {
    field: 'deviceid',
    label: '串号',
    required: true,
    component: 'Input',
  },
  {
    field: 'headicon',
    label: '用户头像',
    required: false,
    component: 'Input',
  },
  {
    field: 'phone',
    label: '手机号码',
    required: false,
    component: 'Input',
  },
  {
    field: 'age',
    label: '年龄',
    required: false,
    component: 'Input',
  },
  {
    field: 'sex',
    label: '性别',
    required: false,
    component: 'RadioButtonGroup',
    defaultValue: 0,
    componentProps: {
      options: [
        { label: '男', value: 0 },
        { label: '女', value: 1 },
      ],
    },
  },
  {
    field: 'idcard',
    label: '身份证号码',
    required: false,
    component: 'Input',
  },
  {
    field: 'height',
    label: '身高',
    required: false,
    component: 'Input',
  },
  {
    field: 'weight',
    label: '体重',
    required: false,
    component: 'Input',
  },
  {
    field: 'cityid',
    label: '城市编号',
    required: false,
    component: 'Input',
  },
  {
    field: 'cityname',
    label: '城市名称',
    required: false,
    component: 'Input',
  },
  {
    field: 'bloodtypename',
    label: '血型',
    component: 'TreeSelect',
    componentProps: {
      fieldNames: {
        label: 'bloodtypename',
        key: 'bloodtypeid',
        value: 'bloodtypeid',
      },
      getPopupContainer: () => document.body,
    },
    required: false,
  },
  {
    field: 'allergyname',
    label: '药物过敏史',
    component: 'TreeSelect',
    componentProps: {
      fieldNames: {
        label: 'allergyname',
        key: 'allergyid',
        value: 'allergyid',
      },
      getPopupContainer: () => document.body,
    },
    required: false,
  },
  {
    field: 'medicalname',
    label: '既往病史',
    component: 'TreeSelect',
    componentProps: {
      fieldNames: {
        label: 'medicalname',
        key: 'medicalid',
        value: 'medicalid',
      },
      getPopupContainer: () => document.body,
    },
    required: false,
  },
  {
    field: 'geneticname',
    label: '遗传史',
    component: 'TreeSelect',
    componentProps: {
      fieldNames: {
        label: 'geneticname',
        key: 'geneticid',
        value: 'geneticid',
      },
      getPopupContainer: () => document.body,
    },
    required: false,
  },
  {
    field: 'descr',
    label: '健康说明',
    required: false,
    component: 'InputTextArea',
  },
];
