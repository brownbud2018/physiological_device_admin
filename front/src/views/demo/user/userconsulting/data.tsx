import { BasicColumn } from '/@/components/Table';
import { FormSchema } from '/@/components/Table';
import { DescItem } from '/@/components/Description/index';

export const columns: BasicColumn[] = [
  {
    title: '用户ID',
    dataIndex: 'dmuserid',
    width: 120,
  },
  {
    title: '用户名',
    dataIndex: 'dmusername',
    width: 180,
  },
  {
    title: '餐前血糖',
    dataIndex: 'pmbg',
    width: 120,
  },
  {
    title: '餐后血糖',
    dataIndex: 'pbg',
    width: 120,
  },
  {
    title: '结论',
    dataIndex: 'conclusion',
    width: 120,
  },
  {
    title: '测量时间',
    dataIndex: 'createtime',
    width: 180,
  },
];

export const columnspressure: BasicColumn[] = [
  {
    title: '用户ID',
    dataIndex: 'dmuserid',
    width: 120,
  },
  {
    title: '用户名',
    dataIndex: 'dmusername',
    width: 120,
  },
  {
    title: '舒张压',
    dataIndex: 'dbp',
    width: 100,
  },
  {
    title: '收缩压',
    dataIndex: 'sbp',
    width: 100,
  },
  {
    title: '结论',
    dataIndex: 'conclusion',
    width: 220,
  },
  {
    title: '测量时间',
    dataIndex: 'createtime',
    width: 180,
  },
];

export const columnsheartrate: BasicColumn[] = [
  {
    title: '用户ID',
    dataIndex: 'dmuserid',
    width: 120,
  },
  {
    title: '用户名',
    dataIndex: 'dmusername',
    width: 180,
  },
  {
    title: '心率值',
    dataIndex: 'heartrate',
    width: 120,
  },
  {
    title: '结论',
    dataIndex: 'conclusion',
    width: 120,
  },
  {
    title: '测量时间',
    dataIndex: 'createtime',
    width: 180,
  },
];

export const columnsbloodoxygen: BasicColumn[] = [
  {
    title: '用户ID',
    dataIndex: 'dmuserid',
    width: 120,
  },
  {
    title: '用户名',
    dataIndex: 'dmusername',
    width: 120,
  },
  {
    title: '血氧饱和度',
    dataIndex: 'spo',
    width: 120,
  },
  {
    title: '脉率',
    dataIndex: 'pulse',
    width: 120,
  },
  {
    title: '结论',
    dataIndex: 'conclusion',
    width: 180,
  },
  {
    title: '测量时间',
    dataIndex: 'createtime',
    width: 180,
  },
];

export const columnstemperature: BasicColumn[] = [
  {
    title: '用户ID',
    dataIndex: 'dmuserid',
    width: 120,
  },
  {
    title: '用户名',
    dataIndex: 'dmusername',
    width: 180,
  },
  {
    title: '体温',
    dataIndex: 'temperature',
    width: 120,
  },
  {
    title: '结论',
    dataIndex: 'conclusion',
    width: 120,
  },
  {
    title: '测量时间',
    dataIndex: 'createtime',
    width: 180,
  },
];

export const columnsmedicalrecord: BasicColumn[] = [
  {
    title: '用户ID',
    dataIndex: 'dmuserid',
    width: 120,
  },
  {
    title: '用户名',
    dataIndex: 'dmusername',
    width: 180,
  },
  {
    title: '检测项目',
    dataIndex: 'recordname',
    width: 120,
  },
  {
    title: '描述',
    dataIndex: 'descr',
    width: 220,
  },
  {
    title: '上传时间',
    dataIndex: 'createtime',
    width: 180,
  },
];

export const columnsquestion: BasicColumn[] = [
  {
    title: '用户ID',
    dataIndex: 'userid',
    width: 120,
  },
  {
    title: '用户名',
    dataIndex: 'dmusername',
    width: 180,
  },
  {
    title: '问卷标题',
    dataIndex: 'questionname',
    width: 120,
  },
  {
    title: '填写时间',
    dataIndex: 'createtime',
    width: 180,
  },
];

export const columnsphysique: BasicColumn[] = [
  {
    title: '用户ID',
    dataIndex: 'dmuserid',
    width: 120,
  },
  {
    title: '用户名',
    dataIndex: 'dmusername',
    width: 180,
  },
  {
    title: '结论',
    dataIndex: 'hint',
    width: 120,
  },
  {
    title: '填写时间',
    dataIndex: 'createtime',
    width: 180,
  },
];

export const personSchema: DescItem[] = [
  {
    field: 'b1',
    label: '用户姓名',
  },
  {
    field: 'b2',
    label: '联系电话',
  },
  {
    field: 'b3',
    label: '年龄',
  },
  {
    field: 'b4',
    label: '性别',
  },
  {
    field: 'b5',
    label: '身高',
  },
  {
    field: 'b6',
    label: '体重',
  },
];

export const personData = {
  b1: '测试用户',
  b2: '18866668888',
  b3: '40岁',
  b4: '男',
  b5: '174cm',
  b6: '70Kg',
};

export const userDetailData = {
  b1: '1',
  b2: '测试用户',
  b3: '18866668888',
  b4: '40岁',
  b5: '男',
  b6: '174cm',
  b7: '70Kg',
  b8: '测试串号',
  b9: '测试设备',
  b10: '666666666666666666',
  b11: '320100',
  b12: '南京市',
  b13: 'A型',
  b14: '无',
  b15: '无',
  b16: '无',
  b17: '健康说明',
  b18: '2022-08-16 09:05:32',
  b19: '广东省',
  b20: '深圳市',
};

export const userDetailSchema: DescItem[] = [
  {
    field: 'b1',
    label: '用户ID',
  },
  {
    field: 'b2',
    label: '用户姓名',
  },
  {
    field: 'b3',
    label: '联系电话',
  },
  {
    field: 'b4',
    label: '年龄',
  },
  {
    field: 'b5',
    label: '性别',
  },
  {
    field: 'b6',
    label: '身高',
  },
  {
    field: 'b7',
    label: '体重',
  },
  {
    field: 'b8',
    label: '设备串号',
  },
  {
    field: 'b9',
    label: '设备名称',
  },
  {
    field: 'b10',
    label: '身份证号码',
  },
  {
    field: 'b11',
    label: '城市编号',
  },
  {
    field: 'b12',
    label: '城市名称',
  },
  {
    field: 'b13',
    label: '血型',
  },
  {
    field: 'b14',
    label: '药物过敏史',
  },
  {
    field: 'b15',
    label: '既往病史',
  },
  {
    field: 'b16',
    label: '遗传史',
  },
  {
    field: 'b17',
    label: '健康说明',
  },
  {
    field: 'b18',
    label: '创建时间',
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

export interface ListItem {
  title: string;
  icon: string;
  color?: string;
}

export interface TabItem {
  key: string;
  name: string;
  component: string;
}

<span class="iconify" data-icon="jam:codepen-circle" data-inline="false"></span>;

export const achieveList: TabItem[] = [
  {
    key: '1',
    name: '咨询',
    component: 'UserDetailHead',
  },
  {
    key: '2',
    name: '血糖',
    component: 'Application',
  },
  {
    key: '3',
    name: '血压',
    component: 'Project',
  },
  {
    key: '4',
    name: '心率',
    component: 'Project',
  },
  {
    key: '5',
    name: '血氧',
    component: 'Project',
  },
  {
    key: '6',
    name: '体温',
    component: 'Project',
  },
  {
    key: '7',
    name: '病历',
    component: 'Project',
  },
  {
    key: '8',
    name: '问卷',
    component: 'Project',
  },
  {
    key: '9',
    name: '体质辨识',
    component: 'Project',
  },
];

export const actions: any[] = [
  { icon: 'clarity:star-line', text: '156', color: '#018ffb' },
  { icon: 'bx:bxs-like', text: '156', color: '#459ae8' },
  { icon: 'bx:bxs-message-dots', text: '2', color: '#42d27d' },
];

export const applicationList = (() => {
  const result: any[] = [];
  for (let i = 0; i < 8; i++) {
    result.push({
      title: 'Vben Admin',
      icon: 'emojione-monotone:letter-a',
      color: '#1890ff',
      active: '100',
      new: '1,799',
      download: 'bx:bx-download',
    });
  }
  return result;
})();

export const projectList = (() => {
  const result: any[] = [];
  for (let i = 0; i < 8; i++) {
    result.push({
      title: 'Vben Admin',
      content: '基于Vue Next, TypeScript, Ant Design实现的一套完整的企业级后台管理系统。',
    });
  }
  return result;
})();

// @ts-ignore
export const messageFrom: FormSchema[] = [
  {
    field: 'id',
    label: '自增编号',
    required: false,
    component: 'Input',
    dynamicDisabled: true,
  },
];
