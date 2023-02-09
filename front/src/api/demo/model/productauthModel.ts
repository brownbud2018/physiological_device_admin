import { BasicPageParams, BasicFetchResult } from '/@/api/model/baseModel';

export type ProductauthParams = {
  detail_name?: string;
  detail_code?: string;
};

export type ProductauthPageParams = BasicPageParams & ProductauthParams;

export interface ProductauthListItem {
  id: number;
  prod_code: string;
  prod_name: string;
  detail_code: string;
  detail_name: string;
  detail_image: string;
  detail_file: string;
  class_id: number;
  class_name: string;
  detail_default: number;
  detail_remark: string;
  gmt_create: string;
}

/**
 * @description: Request list return value
 */

export type ProductauthPageListGetResultModel = BasicFetchResult<ProductauthListItem>;
