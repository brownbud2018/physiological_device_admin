import { BasicColumn, FormSchema } from '/@/components/Table';
import { h } from 'vue';
import { Img } from '/@/components/Img';

export const columns: BasicColumn[] = [
  {
    title: '上传编号',
    dataIndex: 'excel_code',
    width: 120,
  },
  {
    title: '上传名称',
    dataIndex: 'excel_name',
    width: 180,
  },
  {
    title: '上传地址',
    dataIndex: 'excel_address',
    width: 180,
  },
  {
    title: '是否已导入',
    dataIndex: 'is_import',
    width: 120,
    customRender: ({ record }) => {
      // @ts-ignore
      if (record.excel_type === 1) {
        return '已导入';
      } else {
        return '未导入';
      }
    },
  },
  {
    title: '备注',
    dataIndex: 'excel_remark',
  },
  {
    title: '上传时间',
    dataIndex: 'gmt_create',
    width: 180,
  },
  {
    title: 'device图标',
    dataIndex: 'image',
    width: 120,
    customRender: ({ record }) => {
      // @ts-ignore
      return h(Img, { src: record.excel_image, imgwidth: '80' });
    },
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

export const tableFormExcel: BasicColumn[] = [
  {
    title: 'Device编号',
    dataIndex: 'dataSource',
    width: 120,
  },
];

export const refundExcelTableData: any[] = [
  {
    dataSource: 'device编号',
  },
];
