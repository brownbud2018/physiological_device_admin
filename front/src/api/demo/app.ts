import {
  AppPageParams,
  AppPageListGetResultModel,
  AppListItem,
  VersionPageListGetResultModel,
  versionParams,
} from './model/appModel';
import { defHttp } from '/@/utils/http/axios';
import { ErrorMessageMode } from '/#/axios';
import { AppclassListGetResultModel, AppclassListItem } from '/@/api/demo/model/appclassModel';

enum Api {
  appclassList = '/device/appclass/qtree',
  appclassDetail = '/device/apppro/querybyid',
  versionList = '/device/appversion/querybyappid',
  updateApp = '/device/apppro/updatejson',
  setAppType = '/device/apppro/settype',
  setAppUpdateType = '/device/apppro/setupdatetype',
  GetAllAppList = '/device/apppro/queryweb',
  AppDelete = '/device/apppro/delete',
}

/**
 * @description: APP分类列表
 */
export const getAppclassList = (params?: AppclassListItem) =>
  defHttp.get<AppclassListGetResultModel>({ url: Api.appclassList, params });

//APP列表
export function getAppList(params: AppPageParams | undefined, mode: ErrorMessageMode = 'modal') {
  const data = defHttp.get<AppPageListGetResultModel>(
    {
      url: Api.GetAllAppList,
      params,
    },
    {
      errorMessageMode: mode,
    },
  );
  return data;
}
//APP详情
export const getAppDetail = (app_id: number) =>
  defHttp.get({ url: Api.appclassDetail, params: { app_id } });

//APP查询日志列表
export function getVersionList(
  params: versionParams | undefined,
  mode: ErrorMessageMode = 'modal',
) {
  const data = defHttp.get<VersionPageListGetResultModel>(
    {
      url: Api.versionList,
      params,
    },
    {
      errorMessageMode: mode,
    },
  );
  return data;
}
export const setAppType = (id: number, app_type: number) =>
  defHttp.post({ url: Api.setAppType, params: { id, app_type } });

export const setAppUpdateType = (id: number, app_update_type: number) =>
  defHttp.post({ url: Api.setAppUpdateType, params: { id, app_update_type } });

export const delAppType = (id: number) => defHttp.delete({ url: Api.AppDelete, params: { id } });

/**
 * @description: 新增/修改APP分类详情
 */
export function updateApp(params: {}, mode: ErrorMessageMode = 'modal') {
  //console.log(params);
  return defHttp.post<AppListItem>(
    {
      url: Api.updateApp,
      params,
    },
    {
      errorMessageMode: mode,
      isReturnNativeResponse: true,
    },
  );
}
