import { BasicPageParams, BasicFetchResult } from '/@/api/model/baseModel';

export type AdminParams = {
  name?: string;
  is_active?: number;
  user_type?: number;
};

export type AdminPageParams = BasicPageParams & AdminParams;

export interface AdminListItem {
  id: number;
  name: string;
  address: string;
  image: string;
  is_active: number;
  user_type: number;
  gmt_create: string;
}

/**
 * @description: Request list return value
 */

export type AdminPageListGetResultModel = BasicFetchResult<AdminListItem>;
