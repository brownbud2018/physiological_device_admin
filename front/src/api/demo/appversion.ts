import {
  AppversionPageParams,
  AppversionPageListGetResultModel,
  AppversionListItem,
} from './model/appversionModel';
import { defHttp } from '/@/utils/http/axios';
import { ErrorMessageMode } from '/#/axios';
import { VersionPageListGetResultModel, VersionPageParams } from '/@/api/demo/model/appModel';
import { OtamainListItem, OtamainPageListGetResultModel } from '/@/api/demo/model/otamainModel';

enum Api {
  getAppproList = '/device/apppro/qtree',
  getOTAList = '/device/otamain/qtree',
  IsAppversionExist = '/device/appversion/deviceexist',
  IsNewAppversionExist = '/device/appversion/devicenewexist',
  appclassDetail = '/device/apppro/querybyid',
  logList = '/device/devicelog/querybyprodid',
  deviceLogList = '/device/devicelog/querybydeviceid',
  updateAppversion = '/device/appversion/updatejson',
  setAppversionType = '/device/appversion/settype',
  setAppversionPwd = '/device/appversion/changepwd',
  deleteAppversion = '/device/appversion/delete',
  GetAllAppversionList = '/device/appversion/queryweb',
  appversionDetail = '/device/appversion/querybyid',
}

export const isAppversionExist1 = (device_code: string) =>
  defHttp.post(
    { url: Api.IsNewAppversionExist, params: { device_code } },
    { errorMessageMode: 'none' },
  );

export const isAppversionExist = (id: number, device_code: string) =>
  defHttp.post(
    { url: Api.IsAppversionExist, params: { id, device_code } },
    { errorMessageMode: 'none' },
  );
//device列表
export function getAppversionList(
  params: AppversionPageParams | undefined,
  mode: ErrorMessageMode = 'modal',
) {
  const data = defHttp.get<AppversionPageListGetResultModel>(
    {
      url: Api.GetAllAppversionList,
      params,
    },
    {
      errorMessageMode: mode,
    },
  );
  return data;
}
//device详情
export const getAppversionDetail = (device_id: number) =>
  defHttp.get({ url: Api.appversionDetail, params: { device_id } });
/**
 * @description: 项目列表+设备类型子表，Tree
 */
export const getAppproTreeList = (params?: AppversionListItem) =>
  defHttp.get<AppversionPageListGetResultModel>({ url: Api.getAppproList, params });
/**
 * @description: OTA，Tree
 */
export const getOTATreeList = (params?: OtamainListItem) =>
  defHttp.get<OtamainPageListGetResultModel>({ url: Api.getOTAList, params });

//设备类型查询日志列表
export function getLogList(
  params: VersionPageParams | undefined,
  mode: ErrorMessageMode = 'modal',
) {
  const data = defHttp.get<VersionPageListGetResultModel>(
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

//Appversion_id查询日志列表
export function getAppversionLogList(
  params: VersionPageParams | undefined,
  mode: ErrorMessageMode = 'modal',
) {
  const data = defHttp.get<VersionPageListGetResultModel>(
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
export const setAppversionType = (id: number, app_v_default: number) =>
  defHttp.post({ url: Api.setAppversionType, params: { id, app_v_default } });

export const delAppversionType = (id: number) =>
  defHttp.delete({ url: Api.deleteAppversion, params: { id } });

/**
 * @description: 新增/修改Appversion详情
 */
export function updateAppversion(params: {}, mode: ErrorMessageMode = 'modal') {
  //console.log(params);
  return defHttp.post<AppversionListItem>(
    {
      url: Api.updateAppversion,
      params,
    },
    {
      errorMessageMode: mode,
      isReturnNativeResponse: true,
    },
  );
}
