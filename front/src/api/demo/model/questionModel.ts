import { BasicPageParams, BasicFetchResult } from '/@/api/model/baseModel';

export type QuestionParams = {
  questionid?: string;
};

export type QuestionPageParams = BasicPageParams & QuestionParams;

export interface QuestionListItem {
  id: number;
  title: string;
  seq: number;
  isopen: string;
}

/**
 * @description: Request list return value
 */

export type QuestionPageListGetResultModel = BasicFetchResult<QuestionListItem>;

export type QuestionListGetResultModel = QuestionListItem[];
