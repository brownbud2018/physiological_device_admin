import { BasicPageParams, BasicFetchResult } from '/@/api/model/baseModel';

export type MedicalRecordParams = {
  dmuserid?: string;
};

export type MedicalRecordPageParams = BasicPageParams & MedicalRecordParams;

export interface MedicalRecordListItem {
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

export type MedicalRecordPageListGetResultModel = BasicFetchResult<MedicalRecordListItem>;

export type MedicalRecordListGetResultModel = MedicalRecordListItem[];
