import {
  ExceluploadPageListGetResultModel,
  ExceluploadParams,
  ExceluploadUpdateItem,
} from './model/exceluploadModel';
import { defHttp } from '/@/utils/http/axios';
import { ErrorMessageMode } from '/#/axios';

enum Api {
  GetAllExceluploadList = '/device/excelupload/queryweb',
  setExceluploadType = '/device/excelupload/settype',
  updateExcelupload = '/device/excelupload/updatejson',
  ExceluploadDelete = '/device/excelupload/delete',
  ExceluploadDetail = '/device/excelupload/querybyid',
  setExceluploadImport = '/device/excelupload/setimport',
}

/**
 * @description: 项目列表
 */
export function getExceluploadList(
  params: ExceluploadParams | undefined,
  mode: ErrorMessageMode = 'modal',
) {
  const data = defHttp.get<ExceluploadPageListGetResultModel>(
    {
      url: Api.GetAllExceluploadList,
      params,
    },
    {
      errorMessageMode: mode,
    },
  );
  return data;
}
//上传详情
export const getExceluploadDetail = (excel_id: number) =>
  defHttp.get({ url: Api.ExceluploadDetail, params: { excel_id } });
/**
 * @description: 新增/修改Excel
 */
export function updateExcelupload(params: {}, mode: ErrorMessageMode = 'modal') {
  return defHttp.post<ExceluploadUpdateItem>(
    {
      url: Api.updateExcelupload,
      params,
    },
    {
      errorMessageMode: mode,
      //isReturnNativeResponse: true,
    },
  );
}

export const setExceluploadType = (id: number, is_import: number) =>
  defHttp.post({ url: Api.setExceluploadType, params: { id, is_import } });

export const delExcelupload = (id: number) =>
  defHttp.delete({ url: Api.ExceluploadDelete, params: { id } });

//执行导入
export const setExcelImport = (id: number) =>
  defHttp.post({ url: Api.setExceluploadImport, params: { id } });
