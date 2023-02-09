import { BasicPageParams, BasicFetchResult } from '/@/api/model/baseModel';

export type ExceluploadParams = {
  upload_id: number;
  device_id: number;
};

export type ExceluploadPageParams = BasicPageParams & ExceluploadParams;

export interface ExceluploadListItem {
  id: number;
  upload_id: number;
  excel_name: string;
  gmt_create: string;
}

export interface ExceluploadUpdateItem {
  id: number;
  upload_id: number;
  device_id: number;
}
/**
 * @description: Request list return value
 */

export type ExceluploadPageListGetResultModel = BasicFetchResult<ExceluploadListItem>;

export type ExceluploadListGetResultModel = ExceluploadListItem[];
