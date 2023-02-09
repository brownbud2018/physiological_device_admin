import {
  DevicePageParams,
  DevicePageListGetResultModel,
  DeviceListItem,
} from './model/deviceModel';
import { defHttp } from '/@/utils/http/axios';
import { ErrorMessageMode } from '/#/axios';
import { LogPageListGetResultModel, LogPageParams } from '/@/api/demo/model/productModel';
import { OtamainListItem, OtamainPageListGetResultModel } from '/@/api/demo/model/otamainModel';

enum Api {
  getProductList = '/device/product/qtree',
  getOTAList = '/device/otamain/qtree',
  getAuthList = '/device/authclass/qtree',
  IsDeviceExist = '/device/device/deviceexist',
  IsNewDeviceExist = '/device/device/devicenewexist',
  projectDetail = '/device/product/querybyid',
  logList = '/device/devicelog/querybyprodid',
  deviceLogList = '/device/devicelog/querybydeviceid',
  updateDevice = '/device/device/updatejson',
  setDeviceType = '/device/device/settype',
  setDevicePwd = '/device/device/changepwd',
  deleteDevice = '/device/device/delete',
  GetAllDeviceList = '/device/device/queryweb',
  deviceDetail = '/device/device/querybyid',
  provinceList = '/device/device/queryprovince',
  cityList = '/device/device/querycity',
  provinceCityList = '/device/device/queryprovincecity',
}

export const isDeviceExist1 = (device_code: string) =>
  defHttp.post(
    { url: Api.IsNewDeviceExist, params: { device_code } },
    { errorMessageMode: 'none' },
  );

export const isDeviceExist = (id: number, device_code: string) =>
  defHttp.post(
    { url: Api.IsDeviceExist, params: { id, device_code } },
    { errorMessageMode: 'none' },
  );
//device列表
export function getDeviceList(
  params: DevicePageParams | undefined,
  mode: ErrorMessageMode = 'modal',
) {
  const data = defHttp.get<DevicePageListGetResultModel>(
    {
      url: Api.GetAllDeviceList,
      params,
    },
    {
      errorMessageMode: mode,
    },
  );
  return data;
}
//device详情
export const getDeviceDetail = (device_id: number) =>
  defHttp.get({ url: Api.deviceDetail, params: { device_id } });
/**
 * @description: 项目列表+设备类型子表，Tree
 */
export const getProductTreeList = (params?: DeviceListItem) =>
  defHttp.get<DevicePageListGetResultModel>({ url: Api.getProductList, params });
/**
 * @description: OTA，Tree
 */
export const getOTATreeList = (params?: OtamainListItem) =>
  defHttp.get<OtamainPageListGetResultModel>({ url: Api.getOTAList, params });
/**
 * @description: OTA，Tree
 */
export const getAuthTreeList = (params?: OtamainListItem) =>
  defHttp.get<OtamainPageListGetResultModel>({ url: Api.getAuthList, params });

//设备类型查询日志列表
export function getLogList(params: LogPageParams | undefined, mode: ErrorMessageMode = 'modal') {
  const data = defHttp.get<LogPageListGetResultModel>(
    {
      url: Api.logList,
      params,
    },
    {
      errorMessageMode: mode,
    },
  );
  return data;
}

//Device_id查询日志列表
export function getDeviceLogList(
  params: LogPageParams | undefined,
  mode: ErrorMessageMode = 'modal',
) {
  const data = defHttp.get<LogPageListGetResultModel>(
    {
      url: Api.deviceLogList,
      params,
    },
    {
      errorMessageMode: mode,
    },
  );
  return data;
}
export const setDeviceType = (id: number, is_active: number) =>
  defHttp.post({ url: Api.setDeviceType, params: { id, is_active } });

export const setDevicePwd = (id: number, hashed_password: string) =>
  defHttp.post({ url: Api.setDevicePwd, params: { id, hashed_password } });

export const delDeviceType = (id: number) =>
  defHttp.delete({ url: Api.deleteDevice, params: { id } });

/**
 * @description: 新增/修改Device详情
 */
export function updateDevice(params: {}, mode: ErrorMessageMode = 'modal') {
  //console.log(params);
  return defHttp.post<DeviceListItem>(
    {
      url: Api.updateDevice,
      params,
    },
    {
      errorMessageMode: mode,
      isReturnNativeResponse: true,
    },
  );
}
//省份列表
export const getProvinceList = () => defHttp.get({ url: Api.provinceList });
//城市列表
export const getCityList = () => defHttp.get({ url: Api.cityList });
//省份+城市列表
export const getProvinceCityList = () => defHttp.get({ url: Api.provinceCityList });
