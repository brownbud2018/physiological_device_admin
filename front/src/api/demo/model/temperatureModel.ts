import { BasicPageParams, BasicFetchResult } from '/@/api/model/baseModel';

export type TemperatureParams = {
  dmuserid?: string;
};

export type TemperaturePageParams = BasicPageParams & TemperatureParams;

export interface TemperatureListItem {
  id: number;
  dmuserid: number;
  dmusername: string;
  temperature: string;
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

export type TemperaturePageListGetResultModel = BasicFetchResult<TemperatureListItem>;

export type TemperatureListGetResultModel = TemperatureListItem[];
