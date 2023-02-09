import { BasicPageParams, BasicFetchResult } from '/@/api/model/baseModel';

export type BloodoxygenParams = {
  dmuserid?: string;
};

export type BloodoxygenPageParams = BasicPageParams & BloodoxygenParams;

export interface BloodoxygenListItem {
  id: number;
  dmuserid: number;
  dmusername: string;
  spo: string;
  pulse: string;
  bloodoxygenurl: string;
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

export type BloodoxygenPageListGetResultModel = BasicFetchResult<BloodoxygenListItem>;

export type BloodoxygenListGetResultModel = BloodoxygenListItem[];
