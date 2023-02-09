import { BasicColumn } from '/@/components/Table';
import { FormSchema } from '/@/components/Table';
import { h } from 'vue';
import { Switch } from 'ant-design-vue';
//import { setRoleStatus } from '/@/api/demo/system';
import { setProjectType } from '/@/api/demo/project';
import { useMessage } from '/@/hooks/web/useMessage';
import { uploadApi } from '/@/api/sys/upload';
import { Img } from '/@/components/Img';
//列表
export const columns: BasicColumn[] = [
  {
    title: '项目名称',
    dataIndex: 'pro_name',
    width: 200,
  },
  {
    title: '项目编号',
    dataIndex: 'pro_code',
    width: 180,
  },
  {
    title: '项目图标',
    dataIndex: 'pro_image',
    width: 120,
    customRender: ({ record }) => {
      // @ts-ignore
      return h(Img, { src: record.pro_image, imgwidth: '80' });
    },
  },
  {
    title: '项目类型',
    dataIndex: 'pro_type',
    width: 120,
    customRender: ({ record }) => {
      if (!Reflect.has(record, 'pendingStatus')) {
        record.pendingStatus = false;
      }
      return h(Switch, {
        checked: record.pro_type === 1,
        checkedChildren: '正式项目',
        unCheckedChildren: '测试项目',
        loading: record.pendingStatus,
        onChange(checked: boolean) {
          record.pendingStatus = true;
          const newType = checked ? 1 : 0;
          const { createMessage } = useMessage();
          //setRoleStatus(record.id, newStatus)
          setProjectType(record.id, newType)
            .then(() => {
              record.pro_type = newType;
              createMessage.success(`已成功修改项目类型`);
            })
            .catch(() => {
              createMessage.error('修改项目类型失败');
            })
            .finally(() => {
              record.pendingStatus = false;
            });
        },
      });
    },
  },
  {
    title: '创建时间',
    dataIndex: 'gmt_create',
    width: 180,
  },
  {
    title: '备注',
    dataIndex: 'pro_remark',
  },
];
//搜索
export const searchFormSchema: FormSchema[] = [
  {
    field: 'pro_name',
    label: '项目名称',
    component: 'Input',
    colProps: { span: 8 },
  },
  {
    field: 'pro_type',
    label: '项目类型',
    component: 'Select',
    componentProps: {
      options: [
        { label: '测试项目', value: '0' },
        { label: '正式项目', value: '1' },
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
    field: 'pro_name',
    label: '项目名称',
    required: true,
    component: 'Input',
  },
  {
    field: 'pro_code',
    label: '项目编号',
    required: true,
    component: 'Input',
  },
  {
    field: 'pro_image',
    label: '项目图标',
    required: false,
    component: 'Upload',
    componentProps: {
      api: uploadApi,
    },
  },
  {
    field: 'pro_type',
    label: '项目类型',
    required: true,
    component: 'RadioButtonGroup',
    defaultValue: 0,
    componentProps: {
      options: [
        { label: '测试项目', value: 0 },
        { label: '正式项目', value: 1 },
      ],
    },
  },
  {
    field: 'pro_remark',
    label: '项目备注',
    component: 'InputTextArea',
  },
];
