export interface BasicPageParams {
  pageIndex: number;
  pageSize: number;
}

export interface BasicFetchResult<T> {
  dataList: T[];
  count: number;
}
