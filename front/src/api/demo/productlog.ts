import {
  ProductlogParams,
  ProductlogPageListGetResultModel,
  ProductlogUpdateItem,
} from './model/productlogModel';
import { defHttp } from '/@/utils/http/axios';
import { ErrorMessageMode } from '/#/axios';
import { ProductListGetResultModel, ProductListItem } from '/@/api/demo/model/productModel';
import { DevicePageListGetResultModel, DeviceListItem } from '/@/api/demo/model/deviceModel';

enum Api {
  productList = '/device/product/qtree',
  deviceList = '/device/device/qtree',
  GetAllProductlogList = '/device/devicelog/queryweb',
  ProductlogDelete = '/device/devicelog/delete',
  updateProductlog = '/device/devicelog/updatejson',
}

/**
 * @description: 设备类型列表
 */
export const getProductList = (params?: ProductListItem) =>
  defHttp.get<ProductListGetResultModel>({ url: Api.productList, params });
/**
 * @description: Device列表
 */
export const getDeviceList = (params?: DeviceListItem) =>
  defHttp.get<DevicePageListGetResultModel>({ url: Api.deviceList, params });

//设备关联Device列表
export function getProductlogList(
  params: ProductlogParams | undefined,
  mode: ErrorMessageMode = 'modal',
) {
  const data = defHttp.get<ProductlogPageListGetResultModel>(
    {
      url: Api.GetAllProductlogList,
      params,
    },
    {
      errorMessageMode: mode,
    },
  );
  return data;
}

export const delProductlog = (id: number) =>
  defHttp.delete({ url: Api.ProductlogDelete, params: { id } });

/**
 * @description: 新增/修改关联
 */
export function updateProductlog(params: {}, mode: ErrorMessageMode = 'modal') {
  return defHttp.post<ProductlogUpdateItem>(
    {
      url: Api.updateProductlog,
      params,
    },
    {
      errorMessageMode: mode,
      //isReturnNativeResponse: true,
    },
  );
}
