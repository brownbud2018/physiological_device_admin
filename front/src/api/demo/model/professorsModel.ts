import { BasicPageParams, BasicFetchResult } from '/@/api/model/baseModel';

export type ProfessorsParams = {
  pro_name?: string;
  pro_type?: string;
};

export type ProfessorsPageParams = BasicPageParams & ProfessorsParams;

export interface ProfessorsListItem {
  id: number;
  pro_name: string;
  pro_code: string;
  pro_type: number;
  pro_image: string;
  pro_remark: string;
  gmt_create: string;
}

export interface CatListItem {
  cat_id: number;
  cat_name: string;
  cat_type: string;
  keywords: number;
  cat_desc: string;
  sort_order: string;
  show_in_nav: string;
  parent_id: number;
}

/**
 * @description: Request list return value
 */

export type ProfessorsPageListGetResultModel = BasicFetchResult<ProfessorsListItem>;

export type ProfessorsListGetResultModel = BasicFetchResult<ProfessorsListItem>;
