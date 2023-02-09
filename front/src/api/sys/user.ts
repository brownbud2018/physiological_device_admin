import { defHttp } from '/@/utils/http/axios';
import { LoginParams, LoginResultModel, GetUserInfoModel } from './model/userModel';
// GetUserDataModel,
import { ErrorMessageMode } from '/#/axios';
import { NewUserInfo } from '/#/store';

enum Api {
  Login = '/login',
  Login1 = '/loginstring',
  Logout = '/logout',
  GetUserInfo = '/login/current_admin',
  GetUserDataInfo = '/login/current_admin_data',
  GetDeviceDataCNInfo = '/login/current_admin_cn',
  GetDeviceDataInfo = '/login/current_admin_devie_data',
  GetDeviceDataInfo1 = '/login/current_admin_devie_data1',
  GetDeviceDataInfo2 = '/login/current_admin_devie_data2',
  GetPermCode = '/getPermCode',
  TestRetry = '/testRetry',
}

/**
 * @description: user login api
 */
export function loginApi(params: LoginParams, mode: ErrorMessageMode = 'modal') {
  return defHttp.get<LoginResultModel>(
    {
      url: Api.Login1,
      params,
    },
    {
      errorMessageMode: mode,
      isReturnNativeResponse: true,
    },
  );
}

/**
 * @description: getUserInfo
 */
export function getUserInfo() {
  return defHttp.get<GetUserInfoModel>({ url: Api.GetUserInfo }, { errorMessageMode: 'none' });
}
/**
 * @description: getUserDataInfo
 */
export function GetUserDataInfo() {
  return defHttp.get<GetUserInfoModel>({ url: Api.GetUserDataInfo }, { errorMessageMode: 'none' });
}
/**
 * @description: GetDeviceDataInfo获取管理员设备数据
 */
export function GetDeviceDataInfo() {
  return defHttp.get<GetUserInfoModel>(
    { url: Api.GetDeviceDataInfo },
    { errorMessageMode: 'none' },
  );
}
/**
 * @description: GetDeviceDataCnInfo获取管理员设备数据
 */
export function GetDeviceDataCnInfo() {
  return defHttp.get<GetUserInfoModel>(
    { url: Api.GetDeviceDataCNInfo },
    { errorMessageMode: 'none' },
  );
}
/**
 * @description: GetDeviceDataInfo1获取管理员设备数据
 */
export function GetDeviceDataInfo1() {
  return defHttp.get<GetUserInfoModel>(
    { url: Api.GetDeviceDataInfo1 },
    { errorMessageMode: 'none' },
  );
}
/**
 * @description: GetDeviceDataInfo2获取管理员设备数据
 */
export function GetDeviceDataInfo2() {
  return defHttp.get<GetUserInfoModel>(
    { url: Api.GetDeviceDataInfo2 },
    { errorMessageMode: 'none' },
  );
}

export function getNewUserInfo() {
  return defHttp.get<NewUserInfo>({ url: Api.GetUserInfo }, { errorMessageMode: 'none' });
}

export function getPermCode() {
  return defHttp.get<string[]>({ url: Api.GetPermCode });
}

export function doLogout() {
  return defHttp.post({ url: Api.Logout });
}

export function testRetry() {
  return defHttp.get(
    { url: Api.TestRetry },
    {
      retryRequest: {
        isOpenRetry: true,
        count: 5,
        waitTime: 1000,
      },
    },
  );
}
