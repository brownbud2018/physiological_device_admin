import { BasicPageParams, BasicFetchResult } from '/@/api/model/baseModel';

export type AuthaboutParams = {
  prod_id: number;
  app_id: number;
};

export type AuthaboutPageParams = BasicPageParams & AuthaboutParams;

export interface AuthaboutListItem {
  id: number;
  prod_name: string;
  app_name: string;
  gmt_create: string;
}

export interface AuthaboutUpdateItem {
  id: number;
  prod_id: number;
  app_id: number;
}
/**
 * @description: Request list return value
 */

export type AuthaboutPageListGetResultModel = BasicFetchResult<AuthaboutListItem>;

export type AuthaboutListGetResultModel = AuthaboutListItem[];
