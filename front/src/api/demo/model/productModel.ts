import { BasicPageParams, BasicFetchResult } from '/@/api/model/baseModel';

export type ProductParams = {
  prod_name?: string;
  prod_image?: string;
  prod_remark?: string;
};

export type logParams = {
  prod_id: number;
  prod_code?: string;
  prod_name?: string;
  device_code?: string;
  name?: string;
  log_code?: string;
};

export type ProductPageParams = BasicPageParams & ProductParams;

export type LogPageParams = BasicPageParams & logParams;

export interface ProductListItem {
  id: number;
  prod_name: string;
  prod_code: string;
  pro_image: string;
  project_id: number;
  prod_remark: string;
  gmt_create: string;
}

export interface LogListItem {
  device_code: string;
  device_id: number;
  gmt_create: string;
  id: number;
  log_code: string;
  log_image: string;
  device_name: string;
  prod_code: string;
  prod_name: string;
}

/**
 * @description: Request list return value
 */

export type ProductPageListGetResultModel = BasicFetchResult<ProductListItem>;

export type LogPageListGetResultModel = BasicFetchResult<LogListItem>;

export type ProductListGetResultModel = ProductListItem[];
