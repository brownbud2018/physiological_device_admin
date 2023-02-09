import { BasicPageParams, BasicFetchResult } from '/@/api/model/baseModel';

export type ProductappParams = {
  prod_id: number;
  app_id: number;
};

export type ProductappPageParams = BasicPageParams & ProductappParams;

export interface ProductappListItem {
  id: number;
  prod_name: string;
  app_name: string;
  gmt_create: string;
}

export interface ProductappUpdateItem {
  id: number;
  prod_id: number;
  app_id: number;
}
/**
 * @description: Request list return value
 */

export type ProductappPageListGetResultModel = BasicFetchResult<ProductappListItem>;

export type ProductappListGetResultModel = ProductappListItem[];
