import {
  ProductPageParams,
  ProductPageListGetResultModel,
  ProductListItem,
  LogPageListGetResultModel,
  LogPageParams,
} from './model/productModel';
import { defHttp } from '/@/utils/http/axios';
import { ErrorMessageMode } from '/#/axios';
import { ProjectListGetResultModel, ProjectListItem } from '/@/api/demo/model/projectModel';

enum Api {
  projectList = '/device/project/qtree',
  projectDetail = '/device/product/querybyid',
  logList = '/device/devicelog/querybyprodid',
  updateProduct = '/device/product/updatejson',
  setProductType = '/device/product/settype',
  GetAllProductList = '/device/product/queryweb',
  ProductDelete = '/device/product/delete',
}

/**
 * @description: 项目列表
 */
export const getProjectList = (params?: ProjectListItem) =>
  defHttp.get<ProjectListGetResultModel>({ url: Api.projectList, params });

//设备类型列表
export function getProductList(
  params: ProductPageParams | undefined,
  mode: ErrorMessageMode = 'modal',
) {
  const data = defHttp.get<ProductPageListGetResultModel>(
    {
      url: Api.GetAllProductList,
      params,
    },
    {
      errorMessageMode: mode,
    },
  );
  return data;
}
//设备类型详情
export const getProductDetail = (prod_id: number) =>
  defHttp.get({ url: Api.projectDetail, params: { prod_id } });

//设备类型查询日志列表
export function getLogList(params: LogPageParams | undefined, mode: ErrorMessageMode = 'modal') {
  const data = defHttp.get<LogPageListGetResultModel>(
    {
      url: Api.logList,
      params,
    },
    {
      errorMessageMode: mode,
    },
  );
  return data;
}
export const setProductType = (id: number, pro_type: number) =>
  defHttp.post({ url: Api.setProductType, params: { id, pro_type } });

export const delProductType = (id: number) =>
  defHttp.delete({ url: Api.ProductDelete, params: { id } });

/**
 * @description: 新增/修改项目详情
 */
export function updateProduct(params: {}, mode: ErrorMessageMode = 'modal') {
  //console.log(params);
  return defHttp.post<ProductListItem>(
    {
      url: Api.updateProduct,
      params,
    },
    {
      errorMessageMode: mode,
      isReturnNativeResponse: true,
    },
  );
}
