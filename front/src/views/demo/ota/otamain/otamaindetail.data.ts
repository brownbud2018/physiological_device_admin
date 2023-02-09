import { BasicColumn, FormSchema } from '/@/components/Table';
import { h } from 'vue';
import { Img } from '/@/components/Img';

export const columns: BasicColumn[] = [
  {
    title: '版本编号',
    dataIndex: 'ota_v_code',
    width: 120,
  },
  {
    title: '版本名称',
    dataIndex: 'ota_v_name',
    width: 180,
  },
  {
    title: '版本图标',
    dataIndex: 'ota_v_image',
    width: 120,
    customRender: ({ record }) => {
      // @ts-ignore
      return h(Img, { src: record.ota_v_image, imgwidth: '80' });
    },
  },
  {
    title: '文件地址',
    dataIndex: 'ota_v_file',
    width: 280,
  },
  {
    title: 'OTA名称',
    dataIndex: 'ota_name',
    width: 120,
  },
  {
    title: '默认版本',
    dataIndex: 'ota_v_default',
    width: 120,
    customRender: ({ record }) => {
      // @ts-ignore
      if (record.ota_v_default === 1) {
        return '默认版本';
      } else {
        return '历史版本';
      }
    },
  },
  {
    title: '备注',
    dataIndex: 'ota_v_remark',
  },
  {
    title: '创建时间',
    dataIndex: 'gmt_create',
    width: 180,
  },
];

export const searchFormSchema: FormSchema[] = [
  {
    field: 'search_name',
    label: '名称/编号',
    component: 'Input',
    colProps: { span: 8 },
  },
];
