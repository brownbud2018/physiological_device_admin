import {
  ProductauthPageParams,
  ProductauthPageListGetResultModel,
  ProductauthListItem,
} from './model/productauthModel';
import { defHttp } from '/@/utils/http/axios';
import { ErrorMessageMode } from '/#/axios';

enum Api {
  getProductList = '/device/product/qtree',
  GetAllProductauthList = '/device/authclassanddetail/queryproduct',
}
//OTA列表
export function getProductauthList(
  params: ProductauthPageParams | undefined,
  mode: ErrorMessageMode = 'modal',
) {
  const data = defHttp.get<ProductauthPageListGetResultModel>(
    {
      url: Api.GetAllProductauthList,
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
export const getProductTreeList = (params?: ProductauthListItem) =>
  defHttp.get<ProductauthPageListGetResultModel>({ url: Api.getProductList, params });
