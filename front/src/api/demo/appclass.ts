import {
  AppclassPageParams,
  AppclassPageListGetResultModel,
  AppclassListItem,
} from './model/appclassModel';
import { defHttp } from '/@/utils/http/axios';
import { ErrorMessageMode } from '/#/axios';

enum Api {
  updateAppclass = '/device/appclass/updatejson',
  setAppclassType = '/device/appclass/settype',
  AppclassPageList = '/device/appclass',
  GetAllAppclassList = '/device/appclass/queryweb',
  AppclassDelete = '/device/appclass/delete',
}

/**
 * @description: APP类别列表
 */
export function getAppclassList(
  params: AppclassPageParams | undefined,
  mode: ErrorMessageMode = 'modal',
) {
  const data = defHttp.get<AppclassPageListGetResultModel>(
    {
      url: Api.GetAllAppclassList,
      params,
    },
    {
      errorMessageMode: mode,
    },
  );
  return data;
}

export const setAppclassType = (id: number, class_type: number) =>
  defHttp.post({ url: Api.setAppclassType, params: { id, class_type } });

export const delAppclassType = (id: number) =>
  defHttp.delete({ url: Api.AppclassDelete, params: { id } });

/**
 * @description: 新增/修改APP类别详情
 */
export function updateAppclass(params: {}, mode: ErrorMessageMode = 'modal') {
  //console.log(params);
  return defHttp.post<AppclassListItem>(
    {
      url: Api.updateAppclass,
      params,
    },
    {
      errorMessageMode: mode,
      isReturnNativeResponse: true,
    },
  );
}
