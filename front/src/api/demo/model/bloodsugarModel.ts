import { BasicPageParams, BasicFetchResult } from '/@/api/model/baseModel';

export type BloodsugarParams = {
  dmuserid?: string;
};

export type BloodsugarPageParams = BasicPageParams & BloodsugarParams;

export interface BloodsugarListItem {
  id: number;
  dmuserid: number;
  dmusername: string;
  pmbg: string;
  pbg: string;
  conclusionid: number;
  conclusion: string;
  hintid: number;
  hint: string;
  suggestid: number;
  suggest: string;
  type: string;
  createtime: string;
}

/**
 * @description: Request list return value
 */

export type BloodsugarPageListGetResultModel = BasicFetchResult<BloodsugarListItem>;

export type BloodsugarListGetResultModel = BloodsugarListItem[];
