import { BasicColumn } from '/@/components/Table';
import { FormSchema } from '/@/components/Table';
import { uploadApi } from '/@/api/sys/upload';
import { h } from 'vue';
import { Httpimg } from '/@/components/Httpimg';
import { HttpUrl } from '/@/components/HttpUrl';

export const columns: BasicColumn[] = [
  {
    title: '设备编号',
    dataIndex: 'device_id',
    width: 180,
    customRender: ({ record }) => {
      if (record.device_id != null && record.device_id != '') {
        // @ts-ignore
        return h(HttpUrl, {
          src: '/#/user/userconsulting_detail/' + record.id,
          atext: record.device_id,
          alttext: record.device_id,
        });
      } else {
        return h(HttpUrl, {
          src: '/#/user/userconsulting_detail/' + record.id,
          atext: record.device_id,
          alttext: record.device_id,
        });
      }
    },
  },
  {
    title: '咨询用户',
    dataIndex: 'username',
    width: 180,
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
    title: '医生姓名',
    dataIndex: 'professor_name',
    width: 120,
  },
  {
    title: '咨询内容',
    dataIndex: 'content',
    width: 320,
    customRender: ({ record }) => {
      if (record.device_id != null && record.device_id != '') {
        // @ts-ignore
        return h(HttpUrl, {
          src: '/#/user/userconsulting_detail/' + record.id,
          atext: record.content,
          alttext: record.content,
        });
      } else {
        return h(HttpUrl, {
          src: '/#/user/userconsulting_detail/' + record.id,
          atext: record.content,
          alttext: record.content,
        });
      }
    },
  },
  {
    //状态（0待医生接入，1待医生回复，2医生已回复，5完结）
    title: '咨询状态',
    dataIndex: 'status',
    width: 120,
    customRender: ({ record }) => {
      switch (record.status) {
        case 0:
          return '待医生接入';
        case 1:
          return '待医生回复';
        case 2:
          return '医生已回复';
        case 5:
          switch (record.close_type) {
            case 1:
              return '医生关闭';
            case 2:
              return '用户关闭';
            case 3:
              return '超过24小时自动关闭';
            case 4:
              return '20次回复后自动关闭';
            default:
              return '已关闭';
          }
        default:
          return '待医生接入';
      }
    },
  },
  {
    //咨询类型（10健康辅导，20付费咨询）
    title: '咨询属性',
    dataIndex: 'type',
    width: 120,
    customRender: ({ record }) => {
      switch (record.type) {
        case 10:
          return '健康辅导';
        case 20:
          return '付费咨询';
        default:
          return '默认';
      }
    },
  },
  {
    title: '咨询金额',
    dataIndex: 'price',
    width: 120,
  },
  {
    title: '是否付款',
    dataIndex: 'is_payed',
    width: 120,
    customRender: ({ record }) => {
      switch (record.is_payed) {
        case 0:
          switch (record.type) {
            case 10:
              return '免费';
            case 20:
              return '未付款';
            default:
              return '默认';
          }
        case 1:
          switch (record.type) {
            case 10:
              return '免费';
            case 20:
              return '已付款';
            default:
              return '默认';
          }
        default:
          return record.is_payed;
      }
    },
  },
  {
    title: '咨询时间',
    dataIndex: 'add_time',
    width: 120,
    customRender: ({ record }) => {
      const date = new Date((record.add_time + 28800) * 1000);
      const year = date.getFullYear();
      const month = date.getMonth() + 1 < 10 ? '0' + (date.getMonth() + 1) : date.getMonth() + 1;
      const day = date.getDate() < 10 ? '0' + date.getDate() : date.getDate();
      const hour = date.getHours() < 10 ? '0' + date.getHours() : date.getHours();
      const minute = date.getMinutes() < 10 ? '0' + date.getMinutes() : date.getMinutes();
      const second = date.getSeconds() < 10 ? '0' + date.getSeconds() : date.getSeconds();
      const str = `${year}-${month}-${day} ${hour}:${minute}:${second}`;
      return str;
    },
  },
];

export const searchFormSchema: FormSchema[] = [
  {
    field: 'content',
    label: '编号/姓名/内容',
    component: 'Input',
    colProps: { span: 8 },
  },
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
    label: '咨询名称',
    required: true,
    component: 'Input',
  },
  {
    field: 'ota_code',
    label: '咨询编号',
    required: true,
    component: 'Input',
  },
  {
    field: 'ota_package',
    label: '咨询包名',
    required: true,
    component: 'Input',
  },
  {
    field: 'ota_image',
    label: '咨询图标',
    required: false,
    component: 'Upload',
    componentProps: {
      api: uploadApi,
    },
  },
  {
    field: 'ota_type',
    label: '咨询属性',
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
    label: '咨询简介',
    field: 'ota_info',
    component: 'InputTextArea',
  },
  {
    label: '咨询评分',
    field: 'ota_score',
    component: 'Input',
  },
  {
    label: '咨询下载次数',
    field: 'ota_download_amount',
    component: 'Input',
  },
  {
    label: '咨询开发公司',
    field: 'ota_company',
    component: 'Input',
  },
  {
    label: '咨询描述',
    field: 'ota_desc',
    component: 'InputTextArea',
  },
  {
    label: '咨询备注',
    field: 'ota_remark',
    component: 'InputTextArea',
  },
];
