import {
  ProductappParams,
  ProductappPageListGetResultModel,
  ProductappUpdateItem
} from './model/productappModel';
import { defHttp } from '/@/utils/http/axios';
import { ErrorMessageMode } from '/#/axios';
import { ProductListGetResultModel, ProductListItem } from '/@/api/demo/model/productModel';
import { AppListGetResultModel, AppListItem } from '/@/api/demo/model/appModel';

enum Api {
  productList = '/device/product/qtree',
  appList = '/device/apppro/qtree',
  GetAllProductappList = '/device/productapp/queryweb',
  ProductappDelete = '/device/productapp/delete',
  updateProductapp = '/device/productapp/updatejson',
}

/**
 * @description: 设备类型列表
 */
export const getProductList = (params?: ProductListItem) =>
  defHttp.get<ProductListGetResultModel>({ url: Api.productList, params });
/**
 * @description: APP列表
 */
export const getAPPList = (params?: AppListItem) =>
  defHttp.get<AppListGetResultModel>({ url: Api.appList, params });

//设备关联APP列表
export function getProductappList(
  params: ProductappParams | undefined,
  mode: ErrorMessageMode = 'modal',
) {
  const data = defHttp.get<ProductappPageListGetResultModel>(
    {
      url: Api.GetAllProductappList,
      params,
    },
    {
      errorMessageMode: mode,
    },
  );
  return data;
}

export const delProductapp = (id: number) =>
  defHttp.delete({ url: Api.ProductappDelete, params: { id } });

/**
 * @description: 新增/修改关联
 */
export function updateProductapp(params: {}, mode: ErrorMessageMode = 'modal') {
  return defHttp.post<ProductappUpdateItem>(
    {
      url: Api.updateProductapp,
      params,
    },
    {
      errorMessageMode: mode,
      //isReturnNativeResponse: true,
    },
  );
}
