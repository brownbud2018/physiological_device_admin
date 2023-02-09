import {
  AuthaboutParams,
  AuthaboutPageListGetResultModel,
  AuthaboutUpdateItem,
} from './model/authaboutModel';
import { defHttp } from '/@/utils/http/axios';
import { ErrorMessageMode } from '/#/axios';
import {
  AuthclassPageListGetResultModel,
  AuthclassListItem,
} from '/@/api/demo/model/authclassModel';
import { AuthdetailPageListGetResultModel, AuthdetailListItem } from './model/authdetailModel';

enum Api {
  authclassList = '/device/authclass/qtree',
  authdetailList = '/device/authdetail/qtree',
  GetAllAuthaboutList = '/device/authclassanddetail/queryweb',
  AuthaboutDelete = '/device/authclassanddetail/delete',
  updateAuthabout = '/device/authclassanddetail/updatejson',
}

/**
 * @description: 授权列表
 */
export const getAuthclassList = (params?: AuthclassListItem) =>
  defHttp.get<AuthclassPageListGetResultModel>({ url: Api.authclassList, params });
/**
 * @description: Authdetail列表
 */
export const getAuthdetailList = (params?: AuthdetailListItem) =>
  defHttp.get<AuthdetailPageListGetResultModel>({ url: Api.authdetailList, params });

//设备关联Authdetail列表
export function getAuthaboutList(
  params: AuthaboutParams | undefined,
  mode: ErrorMessageMode = 'modal',
) {
  const data = defHttp.get<AuthaboutPageListGetResultModel>(
    {
      url: Api.GetAllAuthaboutList,
      params,
    },
    {
      errorMessageMode: mode,
    },
  );
  return data;
}

export const delAuthabout = (id: number) =>
  defHttp.delete({ url: Api.AuthaboutDelete, params: { id } });

/**
 * @description: 新增/修改关联
 */
export function updateAuthabout(params: {}, mode: ErrorMessageMode = 'modal') {
  return defHttp.post<AuthaboutUpdateItem>(
    {
      url: Api.updateAuthabout,
      params,
    },
    {
      errorMessageMode: mode,
      //isReturnNativeResponse: true,
    },
  );
}
