// @ts-ignore
import {
  AuthclassPageParams,
  AuthclassPageListGetResultModel,
  AuthclassListItem,
} from '/@/api/demo/model/authclassModel';
import { defHttp } from '/@/utils/http/axios';
import { ErrorMessageMode } from '/#/axios';
import { AuthdetailPageListGetResultModel, AuthdetailParams } from './model/authdetailModel';

enum Api {
  classDetail = '/device/authclass/querybyid',
  updateAuthclass = '/device/authclass/updatejson',
  setAuthclassType = '/device/authclass/settype',
  setAuthclassUpdateType = '/device/authclass/setupdatetype',
  GetAllAuthclassList = '/device/authclass/queryweb',
  AuthclassDelete = '/device/authclass/delete',
  authaboutList = '/device/authclassanddetail/querydetailbyclassid',
}
//OTA详情
export const getAuthclassDetail = (class_id: number) =>
  defHttp.get({ url: Api.classDetail, params: { class_id } });

//OTA查询版本列表
export function getAuthdetailList(
  params: AuthdetailParams | undefined,
  mode: ErrorMessageMode = 'modal',
) {
  const data = defHttp.get<AuthdetailPageListGetResultModel>(
    {
      url: Api.authaboutList,
      params,
    },
    {
      errorMessageMode: mode,
    },
  );
  return data;
}
//APP列表
export function getAuthclassList(
  params: AuthclassPageParams | undefined,
  mode: ErrorMessageMode = 'modal',
) {
  const data = defHttp.get<AuthclassPageListGetResultModel>(
    {
      url: Api.GetAllAuthclassList,
      params,
    },
    {
      errorMessageMode: mode,
    },
  );
  return data;
}

export const setAuthclassType = (id: number, class_type: number) =>
  defHttp.post({ url: Api.setAuthclassType, params: { id, class_type } });

export const setAuthclassUpdateType = (id: number, class_update_type: number) =>
  defHttp.post({ url: Api.setAuthclassUpdateType, params: { id, class_update_type } });

export const delAuthclass = (id: number) =>
  defHttp.delete({ url: Api.AuthclassDelete, params: { id } });

/**
 * @description: 新增/修改APP分类详情
 */
export function updateAuthclass(params: {}, mode: ErrorMessageMode = 'modal') {
  return defHttp.post<AuthclassListItem>(
    {
      url: Api.updateAuthclass,
      params,
    },
    {
      errorMessageMode: mode,
      //isReturnNativeResponse: true,
    },
  );
}
