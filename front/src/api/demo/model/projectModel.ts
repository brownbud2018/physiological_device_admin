import { BasicPageParams, BasicFetchResult } from '/@/api/model/baseModel';

export type ProjectParams = {
  pro_name?: string;
  pro_type?: string;
};

export type ProjectPageParams = BasicPageParams & ProjectParams;

export interface ProjectListItem {
  id: number;
  pro_name: string;
  pro_code: string;
  pro_type: number;
  pro_image: string;
  pro_remark: string;
  gmt_create: string;
}

/**
 * @description: Request list return value
 */

export type ProjectPageListGetResultModel = BasicFetchResult<ProjectListItem>;

export type ProjectListGetResultModel = BasicFetchResult<ProjectListItem>;
