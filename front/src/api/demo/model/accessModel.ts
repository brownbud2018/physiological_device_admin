import { BasicPageParams, BasicFetchResult } from '/@/api/model/baseModel';

export type AccessParams = {
  access_code?: string;
  access_name?: string;
  access_image?: string;
  access_desc?: string;
  access_remark?: string;
};

export type AccessPageParams = BasicPageParams & AccessParams;

export interface AccessListItem {
  id: number;
  access_code: string;
  access_name: string;
  access_image: string;
  parent_id: number;
  is_check: number;
  is_menu: number;
  access_desc: string;
  access_remark: string;
  sort_order: number;
  gmt_create: string;
}

/**
 * @description: Request list return value
 */

export type AccessPageListGetResultModel = BasicFetchResult<AccessListItem>;

export type AccessListGetResultModel = AccessListItem[];
