import { BasicPageParams, BasicFetchResult } from '/@/api/model/baseModel';

export type UserconsultingParams = {
  content?: string;
};

export type UserconsultingPageParams = BasicPageParams & UserconsultingParams;

export interface UserconsultingListItem {
  id: number;
  device_id: string;
  type: number;
  leaguer_id: number;
  content: string;
  image: string;
  doctor_type: number;
  doctor_id: number;
  status: number;
  price: number;
  is_payed: number;
  payed_time: string;
  payed_type: string;
  add_time: string;
}

/**
 * @description: Request list return value
 */

export type UserconsultingPageListGetResultModel = BasicFetchResult<UserconsultingListItem>;
