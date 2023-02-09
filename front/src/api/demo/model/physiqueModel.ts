import { BasicPageParams, BasicFetchResult } from '/@/api/model/baseModel';

export type PhysiqueParams = {
  dmuserid?: string;
};

export type PhysiquePageParams = BasicPageParams & PhysiqueParams;

export interface PhysiqueListItem {
  id: number;
  dmuserid: number;
  dmusername: string;
  physique: string;
  conclusion: string;
  hint: string;
  createtime: string;
}

/**
 * @description: Request list return value
 */

export type PhysiquePageListGetResultModel = BasicFetchResult<PhysiqueListItem>;

export type PhysiqueListGetResultModel = PhysiqueListItem[];
