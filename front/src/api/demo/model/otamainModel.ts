import { BasicPageParams, BasicFetchResult } from '/@/api/model/baseModel';

export type OtamainParams = {
  name?: string;
  otamain_level?: string;
};

export type OtamainPageParams = BasicPageParams & OtamainParams;

export interface OtamainListItem {
  id: number;
  ota_code: string;
  ota_name: string;
  ota_image: string;
  ota_package: string;
  ota_type: number;
  ota_update_type: number;
  ota_info: string;
  ota_score: number;
  ota_download_amount: string;
  ota_company: string;
  ota_desc: string;
  ota_remark: string;
  gmt_create: string;
}

/**
 * @description: Request list return value
 */

export type OtamainPageListGetResultModel = BasicFetchResult<OtamainListItem>;
