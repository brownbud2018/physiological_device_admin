import { RolePageParams, RolePageListGetResultModel, RoleListItem } from './model/roleModel';
import { defHttp } from '/@/utils/http/axios';
import { ErrorMessageMode } from '/#/axios';
import { AccessPageListGetResultModel } from "/@/api/demo/model/accessModel";

enum Api {
  updateRole = '/role/updatejson',
  setRoleType = '/role/settype',
  RolePageList = '/role',
  GetAllRoleList = '/role/queryweb',
  RoleDelete = '/role/delete',
  accessroleList = '/access/qtree1',
}

/**
 * @description: 项目列表
 */
export function getRoleList(params: RolePageParams | undefined, mode: ErrorMessageMode = 'modal') {
  const data = defHttp.get<RolePageListGetResultModel>(
    {
      url: Api.GetAllRoleList,
      params,
    },
    {
      errorMessageMode: mode,
    },
  );
  return data;
}

/**
 * @description: Access列表
 */
export const getAccessRoleList = (role_id: number) =>
  defHttp.get<AccessPageListGetResultModel>({ url: Api.accessroleList, params: { role_id } });

export const getAccessRoleList1 = () =>
  defHttp.get<AccessPageListGetResultModel>({ url: Api.accessroleList });

export const setRoleType = (id: number, role_status: number) =>
  defHttp.post({ url: Api.setRoleType, params: { id, role_status } });

export const delRoleType = (id: number) => defHttp.delete({ url: Api.RoleDelete, params: { id } });

/**
 * @description: 新增/修改项目详情
 */
export function updateRole(params: {}, mode: ErrorMessageMode = 'modal') {
  //console.log(params);
  return defHttp.post<RoleListItem>(
    {
      url: Api.updateRole,
      params,
    },
    {
      errorMessageMode: mode,
      isReturnNativeResponse: true,
    },
  );
}
