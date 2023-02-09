import { BasicPageParams, BasicFetchResult } from '/@/api/model/baseModel';

export type AppversionParams = {
  app_v_name?: string;
  app_v_code?: string;
};

export type AppversionPageParams = BasicPageParams & AppversionParams;

export interface AppversionListItem {
  id: number;
  app_v_code: string;
  app_v_name: string;
  app_v_image: string;
  app_v_file: string;
  app_pro_id: number;
  app_name: string;
  app_v_default: number;
  app_v_remark: string;
  gmt_create: string;
}

/**
 * @description: Request list return value
 */

export type AppversionPageListGetResultModel = BasicFetchResult<AppversionListItem>;
