import {
  OtamainPageParams,
  OtamainPageListGetResultModel,
  OtamainListItem,
} from './model/otamainModel';
import { defHttp } from '/@/utils/http/axios';
import { ErrorMessageMode } from '/#/axios';
import {
  OtaversionPageListGetResultModel,
  OtaversionParams,
} from '/@/api/demo/model/otaversionModel';

enum Api {
  otaDetail = '/device/otamain/querybyid',
  updateOtamain = '/device/otamain/updatejson',
  setOtamainType = '/device/otamain/settype',
  setOtamainUpdateType = '/device/otamain/setupdatetype',
  GetAllOtamainList = '/device/otamain/queryweb',
  OtamainDelete = '/device/otamain/delete',
  otaversionList = '/device/otaversion/querybyotaid',
}
//OTA详情
export const getOtamainDetail = (ota_id: number) =>
  defHttp.get({ url: Api.otaDetail, params: { ota_id } });

//OTA查询版本列表
export function getOtaversionList(
  params: OtaversionParams | undefined,
  mode: ErrorMessageMode = 'modal',
) {
  const data = defHttp.get<OtaversionPageListGetResultModel>(
    {
      url: Api.otaversionList,
      params,
    },
    {
      errorMessageMode: mode,
    },
  );
  return data;
}
//APP列表
export function getOtamainList(
  params: OtamainPageParams | undefined,
  mode: ErrorMessageMode = 'modal',
) {
  const data = defHttp.get<OtamainPageListGetResultModel>(
    {
      url: Api.GetAllOtamainList,
      params,
    },
    {
      errorMessageMode: mode,
    },
  );
  return data;
}

export const setOtamainType = (id: number, ota_type: number) =>
  defHttp.post({ url: Api.setOtamainType, params: { id, ota_type } });

export const setOtamainUpdateType = (id: number, ota_update_type: number) =>
  defHttp.post({ url: Api.setOtamainUpdateType, params: { id, ota_update_type } });

export const delOtamain = (id: number) =>
  defHttp.delete({ url: Api.OtamainDelete, params: { id } });

/**
 * @description: 新增/修改APP分类详情
 */
export function updateOtamain(params: {}, mode: ErrorMessageMode = 'modal') {
  return defHttp.post<OtamainListItem>(
    {
      url: Api.updateOtamain,
      params,
    },
    {
      errorMessageMode: mode,
      //isReturnNativeResponse: true,
    },
  );
}
