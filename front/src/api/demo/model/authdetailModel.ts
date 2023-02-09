import { BasicPageParams, BasicFetchResult } from '/@/api/model/baseModel';

export type AuthdetailParams = {
  detail_name?: string;
  detail_code?: string;
};

export type AuthdetailPageParams = BasicPageParams & AuthdetailParams;

export interface AuthdetailListItem {
  id: number;
  detail_code: string;
  detail_name: string;
  detail_image: string;
  detail_file: string;
  detail_default: number;
  detail_remark: string;
  gmt_create: string;
}

/**
 * @description: Request list return value
 */

export type AuthdetailPageListGetResultModel = BasicFetchResult<AuthdetailListItem>;
