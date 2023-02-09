import {
  AdminauthParams,
  AdminauthPageListGetResultModel,
  AdminauthUpdateItem,
} from './model/adminauthModel';
import { defHttp } from '/@/utils/http/axios';
import { ErrorMessageMode } from '/#/axios';
import { AdminPageListGetResultModel, AdminListItem } from '/@/api/demo/model/adminModel';
import { AuthclassPageListGetResultModel, AuthclassListItem } from './model/authclassModel';

enum Api {
  adminList = '/admin/qtree',
  authclassList = '/device/authclass/qtree',
  GetAllAdminauthList = '/adminauth/queryweb',
  AdminauthDelete = '/adminauth/delete',
  updateAdminauth = '/adminauth/updatejson',
}

/**
 * @description: 管理员列表
 */
export const getAdminList = (params?: AdminListItem) =>
  defHttp.get<AdminPageListGetResultModel>({ url: Api.adminList, params });
/**
 * @description: 授权列表
 */
export const getAuthclassList = (params?: AuthclassListItem) =>
  defHttp.get<AuthclassPageListGetResultModel>({ url: Api.authclassList, params });

//管理员关联授权列表
export function getAdminauthList(
  params: AdminauthParams | undefined,
  mode: ErrorMessageMode = 'modal',
) {
  const data = defHttp.get<AdminauthPageListGetResultModel>(
    {
      url: Api.GetAllAdminauthList,
      params,
    },
    {
      errorMessageMode: mode,
    },
  );
  return data;
}

export const delAdminauth = (id: number) =>
  defHttp.delete({ url: Api.AdminauthDelete, params: { id } });

/**
 * @description: 新增/修改关联
 */
export function updateAdminauth(params: {}, mode: ErrorMessageMode = 'modal') {
  return defHttp.post<AdminauthUpdateItem>(
    {
      url: Api.updateAdminauth,
      params,
    },
    {
      errorMessageMode: mode,
      //isReturnNativeResponse: true,
    },
  );
}
