import { BasicPageParams, BasicFetchResult } from '/@/api/model/baseModel';

export type UploadBigParams = {
  file_name?: string;
};

export type UploadBigPageParams = BasicPageParams & UploadBigParams;

export interface UploadBigItem {
  file: string;
  chunknumber: string;
  identifier: string;
}

export interface UploadBigMergeItem {
  identifier: string;
  filename: string;
  chunkstar: number;
}

export interface UploadBigDelItem {
  identifier: string;
  chunkstar: number;
}

/**
 * @description: Request list return value
 */

export type UploadBigGetResultModel = BasicFetchResult<UploadBigItem>;
