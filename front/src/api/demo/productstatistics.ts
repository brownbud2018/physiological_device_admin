import {
  ProductstatisticsParams,
  ProductstatisticsPageListGetResultModel,
  ProductstatisticsUpdateItem,
} from './model/productstatisticsModel';
import { defHttp } from '/@/utils/http/axios';
import { ErrorMessageMode } from '/#/axios';
import { ProductListGetResultModel, ProductListItem } from '/@/api/demo/model/productModel';
import { DevicePageListGetResultModel, DeviceListItem } from '/@/api/demo/model/deviceModel';

enum Api {
  productList = '/device/product/qtree',
  deviceList = '/device/device/qtree',
  GetAllProductstatisticsList = '/device/statistics/queryweb',
  ProductstatisticsDelete = '/device/statistics/delete',
  updateProductstatistics = '/device/statistics/updatejson',
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
export function getProductstatisticsList(
  params: ProductstatisticsParams | undefined,
  mode: ErrorMessageMode = 'modal',
) {
  const data = defHttp.get<ProductstatisticsPageListGetResultModel>(
    {
      url: Api.GetAllProductstatisticsList,
      params,
    },
    {
      errorMessageMode: mode,
    },
  );
  return data;
}

export const delProductstatistics = (id: number) =>
  defHttp.delete({ url: Api.ProductstatisticsDelete, params: { id } });

/**
 * @description: 新增/修改关联
 */
export function updateProductstatistics(params: {}, mode: ErrorMessageMode = 'modal') {
  return defHttp.post<ProductstatisticsUpdateItem>(
    {
      url: Api.updateProductstatistics,
      params,
    },
    {
      errorMessageMode: mode,
      //isReturnNativeResponse: true,
    },
  );
}
