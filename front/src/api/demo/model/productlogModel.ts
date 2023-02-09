import { BasicPageParams, BasicFetchResult } from '/@/api/model/baseModel';

export type ProductlogParams = {
  prod_id: number;
  device_id: number;
};

export type ProductlogPageParams = BasicPageParams & ProductlogParams;

export interface ProductlogListItem {
  id: number;
  prod_name: string;
  name: string;
  gmt_create: string;
}

export interface ProductlogUpdateItem {
  id: number;
  prod_id: number;
  device_id: number;
}
/**
 * @description: Request list return value
 */

export type ProductlogPageListGetResultModel = BasicFetchResult<ProductlogListItem>;

export type ProductlogListGetResultModel = ProductlogListItem[];
