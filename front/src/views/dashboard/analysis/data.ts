export interface GrowCardItem {
  img: string;
  title: string;
  value: number;
  total: number;
  color: string;
  action: string;
}
export const growCardList: GrowCardItem[] = [
  {
    title: '设备数',
    img: 'visit-count|svg',
    value: 0,
    total: 0,
    color: 'green',
    action: '合计',
  },
  {
    title: '用户数',
    img: 'total-sales|svg',
    value: 0,
    total: 0,
    color: 'blue',
    action: '合计',
  },
  {
    title: '检测数',
    img: 'download-count|svg',
    value: 0,
    total: 0,
    color: 'orange',
    action: '合计',
  },
  {
    title: '超标数',
    img: 'transaction|svg',
    value: 0,
    total: 0,
    color: 'purple',
    action: '合计',
  },
];
