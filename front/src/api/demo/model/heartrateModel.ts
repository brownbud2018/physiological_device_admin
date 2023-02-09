import { BasicPageParams, BasicFetchResult } from '/@/api/model/baseModel';

export type HeartrateParams = {
  dmuserid?: string;
};

export type HeartratePageParams = BasicPageParams & HeartrateParams;

export interface HeartrateListItem {
  id: number;
  dmuserid: number;
  dmusername: string;
  heartrateurl: string;
  heartrate: string;
  conclusionid: number;
  conclusion: string;
  hintid: number;
  hint: string;
  suggestid: number;
  suggest: string;
  createtime: string;
}

/**
 * @description: Request list return value
 */

export type HeartratePageListGetResultModel = BasicFetchResult<HeartrateListItem>;

export type HeartrateListGetResultModel = HeartrateListItem[];
