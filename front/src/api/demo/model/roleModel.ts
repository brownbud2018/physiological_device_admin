import { BasicPageParams, BasicFetchResult } from '/@/api/model/baseModel';

export type RoleParams = {
  role_name?: string;
  role_status?: string;
};

export type RolePageParams = BasicPageParams & RoleParams;

export interface RoleListItem {
  id: number;
  role_name: string;
  role_status: number;
  role_desc: string;
  gmt_create: string;
}

/**
 * @description: Request list return value
 */

export type RolePageListGetResultModel = BasicFetchResult<RoleListItem>;

export type RoleListGetResultModel = BasicFetchResult<RoleListItem>;
