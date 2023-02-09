import {
  ProjectPageParams,
  ProjectPageListGetResultModel,
  ProjectListItem,
} from './model/projectModel';
import { defHttp } from '/@/utils/http/axios';
import { ErrorMessageMode } from '/#/axios';

enum Api {
  updateProject = '/device/project/updatejson',
  setProjectType = '/device/project/settype',
  ProjectPageList = '/device/project',
  GetAllProjectList = '/device/project/queryweb',
  ProjectDelete = '/device/project/delete',
}

/**
 * @description: 项目列表
 */
export function getProjectList(
  params: ProjectPageParams | undefined,
  mode: ErrorMessageMode = 'modal',
) {
  const data = defHttp.get<ProjectPageListGetResultModel>(
    {
      url: Api.GetAllProjectList,
      params,
    },
    {
      errorMessageMode: mode,
    },
  );
  return data;
}

export const setProjectType = (id: number, pro_type: number) =>
  defHttp.post({ url: Api.setProjectType, params: { id, pro_type } });

export const delProjectType = (id: number) =>
  defHttp.delete({ url: Api.ProjectDelete, params: { id } });

/**
 * @description: 新增/修改项目详情
 */
export function updateProject(params: {}, mode: ErrorMessageMode = 'modal') {
  //console.log(params);
  return defHttp.post<ProjectListItem>(
    {
      url: Api.updateProject,
      params,
    },
    {
      errorMessageMode: mode,
      isReturnNativeResponse: true,
    },
  );
}
