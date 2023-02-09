import { BasicPageParams, BasicFetchResult } from '/@/api/model/baseModel';

export type ProductstatisticsParams = {
  prod_id: number;
  device_id: number;
};

export type ProductstatisticsPageParams = BasicPageParams & ProductstatisticsParams;

export interface ProductstatisticsListItem {
  id: number;
  prod_name: string;
  name: string;
  gmt_create: string;
}

export interface ProductstatisticsUpdateItem {
  id: number;
  prod_id: number;
  device_id: number;
}
/**
 * @description: Request list return value
 */

export type ProductstatisticsPageListGetResultModel = BasicFetchResult<ProductstatisticsListItem>;

export type ProductstatisticsListGetResultModel = ProductstatisticsListItem[];
