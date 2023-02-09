import { BasicPageParams, BasicFetchResult } from '/@/api/model/baseModel';

export type AppParams = {
  app_code?: string;
  app_name?: string;
  app_image?: string;
  app_remark?: string;
};

export type versionParams = {
  app_pro_id: number;
  app_v_code?: string;
  app_v_name?: string;
  app_v_default?: number;
  app_v_remark?: string;
  id?: number;
};

export type AppPageParams = BasicPageParams & AppParams;

export type VersionPageParams = BasicPageParams & versionParams;

export interface AppListItem {
  id: number;
  app_name: string;
  app_code: string;
  app_image: string;
  app_class_id: number;
  app_remark: string;
  gmt_create: string;
}

export interface VersionListItem {
  app_pro_id: number;
  app_v_code?: string;
  app_v_name?: string;
  app_v_default?: number;
  app_v_remark?: string;
  id?: number;
}

/**
 * @description: Request list return value
 */

export type AppPageListGetResultModel = BasicFetchResult<AppListItem>;

export type VersionPageListGetResultModel = BasicFetchResult<VersionListItem>;

export type AppListGetResultModel = AppListItem[];
