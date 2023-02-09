import {
  AccessPageParams,
  AccessPageListGetResultModel,
  AccessListItem,
} from './model/accessModel';
import { defHttp } from '/@/utils/http/axios';
import { ErrorMessageMode } from '/#/axios';

enum Api {
  updateAccess = '/access/updatejson',
  setAccessType = '/access/settype',
  setAccessType1 = '/access/settype1',
  AccessPageList = '/access',
  GetAllAccessList = '/access/queryweb',
  AccessDelete = '/access/delete',
  getAccessList = '/access/qtree',
  IsAccessExist = '/access/accessexist',
  IsNewAccessExist = '/access/accessnewexist',
}

/**
 * @description: 项目列表
 */
export function getAccessList(
  params: AccessPageParams | undefined,
  mode: ErrorMessageMode = 'modal',
) {
  const data = defHttp.get<AccessPageListGetResultModel>(
    {
      url: Api.GetAllAccessList,
      params,
    },
    {
      errorMessageMode: mode,
    },
  );
  return data;
}

export const setAccessType = (id: number, is_check: number) =>
  defHttp.post({ url: Api.setAccessType, params: { id, is_check } });

export const setAccessType1 = (id: number, is_menu: number) =>
  defHttp.post({ url: Api.setAccessType1, params: { id, is_menu } });

export const delAccessType = (id: number) =>
  defHttp.delete({ url: Api.AccessDelete, params: { id } });

/**
 * @description: 新增/修改项目详情
 */
export function updateAccess(params: {}, mode: ErrorMessageMode = 'modal') {
  //console.log(params);
  return defHttp.post<AccessListItem>(
    {
      url: Api.updateAccess,
      params,
    },
    {
      errorMessageMode: mode,
      isReturnNativeResponse: true,
    },
  );
}

/**
 * @description: 项目列表+设备类型子表，Tree
 */
export const getAccessTreeList = (params?: AccessListItem) =>
  defHttp.get<AccessPageListGetResultModel>({ url: Api.getAccessList, params });

export const isAccessExist1 = (access_code: string) =>
  defHttp.post(
    { url: Api.IsNewAccessExist, params: { access_code } },
    { errorMessageMode: 'none' },
  );

export const isAccessExist = (id: number, access_code: string) =>
  defHttp.post(
    { url: Api.IsAccessExist, params: { id, access_code } },
    { errorMessageMode: 'none' },
  );
