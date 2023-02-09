import { BasicPageParams, BasicFetchResult } from '/@/api/model/baseModel';

export type AppclassParams = {
  class_name?: string;
  class_type?: string;
};

export type AppclassPageParams = BasicPageParams & AppclassParams;

export interface AppclassListItem {
  id: number;
  class_name: string;
  class_code: string;
  class_type: number;
  class_image: string;
  class_remark: string;
  gmt_create: string;
}

/**
 * @description: Request list return value
 */

export type AppclassPageListGetResultModel = BasicFetchResult<AppclassListItem>;

export type AppclassListGetResultModel = BasicFetchResult<AppclassListItem>;
