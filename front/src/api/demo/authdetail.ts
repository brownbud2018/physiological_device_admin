import {
  AuthdetailPageParams,
  AuthdetailPageListGetResultModel,
  AuthdetailListItem,
} from './model/authdetailModel';
import { defHttp } from '/@/utils/http/axios';
import { ErrorMessageMode } from '/#/axios';
import {
  AuthclassListItem,
  AuthclassPageListGetResultModel,
} from '/@/api/demo/model/authclassModel';

enum Api {
  getAuthclassList = '/device/authclass/qtree',
  getAuthList = '/device/authclass/qtree',
  updateAuthdetail = '/device/authdetail/updatejson',
  setAuthdetailType = '/device/authdetail/settype',
  deleteAuthdetail = '/device/authdetail/delete',
  GetAllAuthdetailList = '/device/authdetail/queryweb',
  authdetailDetail = '/device/authdetail/querybyid',
}
//权限列表
export function getAuthdetailList(
  params: AuthdetailPageParams | undefined,
  mode: ErrorMessageMode = 'modal',
) {
  const data = defHttp.get<AuthdetailPageListGetResultModel>(
    {
      url: Api.GetAllAuthdetailList,
      params,
    },
    {
      errorMessageMode: mode,
    },
  );
  return data;
}
//device详情
export const getAuthdetailDetail = (device_id: number) =>
  defHttp.get({ url: Api.authdetailDetail, params: { device_id } });
/**
 * @description: AuthTree
 */
export const getAuthclassTreeList = (params?: AuthdetailListItem) =>
  defHttp.get<AuthdetailPageListGetResultModel>({ url: Api.getAuthclassList, params });
/**
 * @description: Auth，Tree
 */
export const getAuthTreeList = (params?: AuthclassListItem) =>
  defHttp.get<AuthclassPageListGetResultModel>({ url: Api.getAuthList, params });

export const setAuthdetailType = (id: number, detail_type: number) =>
  defHttp.post({ url: Api.setAuthdetailType, params: { id, detail_type } });

export const delAuthdetail = (id: number) =>
  defHttp.delete({ url: Api.deleteAuthdetail, params: { id } });

/**
 * @description: 新增/修改Authdetail详情
 */
export function updateAuthdetail(params: {}, mode: ErrorMessageMode = 'modal') {
  //console.log(params);
  return defHttp.post<AuthdetailListItem>(
    {
      url: Api.updateAuthdetail,
      params,
    },
    {
      errorMessageMode: mode,
      //isReturnNativeResponse: true,
    },
  );
}
