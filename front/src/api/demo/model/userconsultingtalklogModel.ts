import { BasicPageParams, BasicFetchResult } from '/@/api/model/baseModel';

export type UserconsultingtalklogParams = {
  name?: string;
};

export type UserconsultingtalklogPageParams = BasicPageParams & UserconsultingtalklogParams;

export interface UserconsultingtalklogListItem {
  id: number;
  consulting_id: string;
  reply_type: number;
  reply_uid: number;
  content_type: number;
  status: number;
  content: string;
  add_time: string;
}

/**
 * @description: Request list return value
 */

export type UserconsultingtalklogPageListGetResultModel = BasicFetchResult<UserconsultingtalklogListItem>;
