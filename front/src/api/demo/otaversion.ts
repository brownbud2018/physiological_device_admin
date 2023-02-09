import {
  OtaversionPageParams,
  OtaversionPageListGetResultModel,
  OtaversionListItem,
} from './model/otaversionModel';
import { defHttp } from '/@/utils/http/axios';
import { ErrorMessageMode } from '/#/axios';
import { OtamainListItem, OtamainPageListGetResultModel } from '/@/api/demo/model/otamainModel';

enum Api {
  getOtamainList = '/device/otamain/qtree',
  getOTAList = '/device/otamain/qtree',
  IsNewOtaversionExist = '/device/otaversion/devicenewexist',
  updateOtaversion = '/device/otaversion/updatejson',
  setOtaversionType = '/device/otaversion/settype',
  deleteOtaversion = '/device/otaversion/delete',
  GetAllOtaversionList = '/device/otaversion/queryweb',
  otaversionDetail = '/device/otaversion/querybyid',
}
//OTA列表
export function getOtaversionList(
  params: OtaversionPageParams | undefined,
  mode: ErrorMessageMode = 'modal',
) {
  const data = defHttp.get<OtaversionPageListGetResultModel>(
    {
      url: Api.GetAllOtaversionList,
      params,
    },
    {
      errorMessageMode: mode,
    },
  );
  return data;
}
//device详情
export const getOtaversionDetail = (device_id: number) =>
  defHttp.get({ url: Api.otaversionDetail, params: { device_id } });
/**
 * @description: OTATree
 */
export const getOtaTreeList = (params?: OtaversionListItem) =>
  defHttp.get<OtaversionPageListGetResultModel>({ url: Api.getOtamainList, params });
/**
 * @description: OTA，Tree
 */
export const getOTATreeList = (params?: OtamainListItem) =>
  defHttp.get<OtamainPageListGetResultModel>({ url: Api.getOTAList, params });

export const setOtaversionType = (id: number, ota_v_default: number) =>
  defHttp.post({ url: Api.setOtaversionType, params: { id, ota_v_default } });

export const delOtaversion = (id: number) =>
  defHttp.delete({ url: Api.deleteOtaversion, params: { id } });

/**
 * @description: 新增/修改Otaversion详情
 */
export function updateOtaversion(params: {}, mode: ErrorMessageMode = 'modal') {
  //console.log(params);
  return defHttp.post<OtaversionListItem>(
    {
      url: Api.updateOtaversion,
      params,
    },
    {
      errorMessageMode: mode,
      //isReturnNativeResponse: true,
    },
  );
}
