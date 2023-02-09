import {
  ProfessorsPageParams,
  ProfessorsPageListGetResultModel,
  ProfessorsListItem,
  ProfessorsListGetResultModel, CatListItem
} from "./model/professorsModel";
import { defHttp } from '/@/utils/http/axios';
import { ErrorMessageMode } from '/#/axios';

enum Api {
  catList = '/professors/catqtree',
  updateProfessors = '/professors/updatejson',
  GetAllProfessorsList = '/professors/queryweb',
  ProfessorsDelete = '/professors/delete',
}

/**
 * @description: 主治分类列表
 */
export const getCatList = (params?: CatListItem) =>
  defHttp.get<ProfessorsListGetResultModel>({ url: Api.catList, params });
/**
 * @description: 医生列表
 */
export function getProfessorsList(
  params: ProfessorsPageParams | undefined,
  mode: ErrorMessageMode = 'modal',
) {
  const data = defHttp.get<ProfessorsPageListGetResultModel>(
    {
      url: Api.GetAllProfessorsList,
      params,
    },
    {
      errorMessageMode: mode,
    },
  );
  return data;
}

export const delProfessorsType = (id: number) =>
  defHttp.delete({ url: Api.ProfessorsDelete, params: { id } });

/**
 * @description: 新增/修改医生详情
 */
export function updateProfessors(params: {}, mode: ErrorMessageMode = 'modal') {
  //console.log(params);
  return defHttp.post<ProfessorsListItem>(
    {
      url: Api.updateProfessors,
      params,
    },
    {
      errorMessageMode: mode,
      isReturnNativeResponse: true,
    },
  );
}
