import { BasicPageParams, BasicFetchResult } from '/@/api/model/baseModel';

export type DeviceParams = {
  name?: string;
  device_level?: string;
};

export type DevicePageParams = BasicPageParams & DeviceParams;

export interface DeviceListItem {
  id: number;
  device_code: string;
  name: string;
  device_ota: number;
  ota_name: string;
  version: string;
  product_id: number;
  prod_name: string;
  address: string;
  image: string;
  is_active: number;
  device_level: number;
  device_auth_class_id: number;
  gmt_create: string;
}

/**
 * @description: Request list return value
 */

export type DevicePageListGetResultModel = BasicFetchResult<DeviceListItem>;
