import { BasicPageParams, BasicFetchResult } from '/@/api/model/baseModel';

export type AuthclassParams = {
  class_name?: string;
  class_code?: string;
};

export type AuthclassPageParams = BasicPageParams & AuthclassParams;

export interface AuthclassListItem {
  id: number;
  class_code: string;
  class_name: string;
  class_image: string;
  class_remark: string;
  gmt_create: string;
}

/**
 * @description: Request list return value
 */

export type AuthclassPageListGetResultModel = BasicFetchResult<AuthclassListItem>;
