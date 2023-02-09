import {
  ProductotaPageParams,
  ProductotaPageListGetResultModel,
  ProductotaListItem,
} from './model/productotaModel';
import { defHttp } from '/@/utils/http/axios';
import { ErrorMessageMode } from '/#/axios';

enum Api {
  getProductList = '/device/product/qtree',
  GetAllProductotaList = '/device/product/queryproductota',
}
//OTA列表
export function getProductotaList(
  params: ProductotaPageParams | undefined,
  mode: ErrorMessageMode = 'modal',
) {
  const data = defHttp.get<ProductotaPageListGetResultModel>(
    {
      url: Api.GetAllProductotaList,
      params,
    },
    {
      errorMessageMode: mode,
    },
  );
  return data;
}
/**
 * @description: ProductTree
 */
export const getProductTreeList = (params?: ProductotaListItem) =>
  defHttp.get<ProductotaPageListGetResultModel>({ url: Api.getProductList, params });
