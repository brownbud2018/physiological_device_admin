import { BasicPageParams, BasicFetchResult } from '/@/api/model/baseModel';

export type BloodpressureParams = {
  dmuserid?: string;
};

export type BloodpressurePageParams = BasicPageParams & BloodpressureParams;

export interface BloodpressureListItem {
  id: number;
  dmuserid: number;
  dmusername: string;
  dbp: string;
  sbp: string;
  conclusionid: number;
  conclusion: string;
  hintid: number;
  hint: string;
  suggestid: number;
  suggest: string;
  typeid: string;
  createtime: string;
}

/**
 * @description: Request list return value
 */

export type BloodpressurePageListGetResultModel = BasicFetchResult<BloodpressureListItem>;

export type BloodpressureListGetResultModel = BloodpressureListItem[];
