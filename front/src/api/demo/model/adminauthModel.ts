import { BasicPageParams, BasicFetchResult } from '/@/api/model/baseModel';

export type AdminauthParams = {
  admin_id: number;
  auth_class_id: number;
};

export type AdminauthPageParams = BasicPageParams & AdminauthParams;

export interface AdminauthListItem {
  id: number;
  nickname: string;
  class_name: string;
  gmt_create: string;
}

export interface AdminauthUpdateItem {
  id: number;
  admin_id: number;
  auth_class_id: number;
}
/**
 * @description: Request list return value
 */

export type AdminauthPageListGetResultModel = BasicFetchResult<AdminauthListItem>;

export type AdminauthListGetResultModel = AdminauthListItem[];
