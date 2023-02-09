import { AdminPageParams, AdminPageListGetResultModel, AdminListItem } from './model/adminModel';
import { defHttp } from '/@/utils/http/axios';
import { ErrorMessageMode } from '/#/axios';
import { OtamainListItem, OtamainPageListGetResultModel } from '/@/api/demo/model/otamainModel';

enum Api {
  getAdminList = '/admin/qtree',
  getRoleList = '/role/qtree',
  getDocList = '/professors/qtree',
  getOTAList = '/otamain/qtree',
  getAuthList = '/authclass/qtree',
  IsAdminExist = '/admin/adminexist',
  IsNewAdminExist = '/admin/adminnewexist',
  projectDetail = '/role/querybyid',
  updateAdmin = '/admin/updatejson',
  setAdminType = '/admin/settype',
  setAdminType1 = '/admin/settype1',
  setAdminPwd = '/admin/changepwd',
  deleteAdmin = '/admin/delete',
  GetAllAdminList = '/admin/queryweb',
  adminDetail = '/admin/querybyid',
}

export const isAdminExist1 = (admin_code: string) =>
  defHttp.post({ url: Api.IsNewAdminExist, params: { admin_code } }, { errorMessageMode: 'none' });

export const isAdminExist = (id: number, admin_code: string) =>
  defHttp.post({ url: Api.IsAdminExist, params: { id, admin_code } }, { errorMessageMode: 'none' });
//admin列表
export function getAdminList(
  params: AdminPageParams | undefined,
  mode: ErrorMessageMode = 'modal',
) {
  const data = defHttp.get<AdminPageListGetResultModel>(
    {
      url: Api.GetAllAdminList,
      params,
    },
    {
      errorMessageMode: mode,
    },
  );
  return data;
}
//admin详情
export const getAdminDetail = (admin_id: number) =>
  defHttp.get({ url: Api.adminDetail, params: { admin_id } });
/**
 * @description: 管理员列表，Tree
 */
export const getAdminTreeList = (params?: AdminListItem) =>
  defHttp.get<AdminPageListGetResultModel>({ url: Api.getAdminList, params });
/**
 * @description: 角色列表，Tree
 */
export const getRoleTreeList = (params?: AdminListItem) =>
  defHttp.get<AdminPageListGetResultModel>({ url: Api.getRoleList, params });
/**
 * @description: 医生列表，Tree
 */
export const getDocTreeList = (params?: AdminListItem) =>
  defHttp.get<AdminPageListGetResultModel>({ url: Api.getDocList, params });
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

export const setAdminType = (id: number, is_active: number) =>
  defHttp.post({ url: Api.setAdminType, params: { id, is_active } });

export const setAdminType1 = (id: number, user_type: number) =>
  defHttp.post({ url: Api.setAdminType1, params: { id, user_type } });

export const setAdminPwd = (id: number, hashed_password: string) =>
  defHttp.post({ url: Api.setAdminPwd, params: { id, hashed_password } });

export const delAdminType = (id: number) =>
  defHttp.delete({ url: Api.deleteAdmin, params: { id } });

/**
 * @description: 新增/修改Admin详情
 */
export function updateAdmin(params: {}, mode: ErrorMessageMode = 'modal') {
  //console.log(params);
  return defHttp.post<AdminListItem>(
    {
      url: Api.updateAdmin,
      params,
    },
    {
      errorMessageMode: mode,
      isReturnNativeResponse: true,
    },
  );
}
