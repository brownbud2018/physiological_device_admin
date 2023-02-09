import { BasicPageParams, BasicFetchResult } from '/@/api/model/baseModel';

export type ProductotaParams = {
  ota_v_name?: string;
  ota_v_code?: string;
};

export type ProductotaPageParams = BasicPageParams & ProductotaParams;

export interface ProductotaListItem {
  id: number;
  prod_code: string;
  prod_name: string;
  ota_v_code: string;
  ota_v_name: string;
  ota_v_image: string;
  ota_v_file: string;
  ota_main_id: number;
  ota_name: string;
  ota_v_default: number;
  ota_v_remark: string;
  gmt_create: string;
}

/**
 * @description: Request list return value
 */

export type ProductotaPageListGetResultModel = BasicFetchResult<ProductotaListItem>;
