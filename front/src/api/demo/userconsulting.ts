import {
  UserconsultingPageParams,
  UserconsultingPageListGetResultModel,
  UserconsultingListItem,
} from './model/userconsultingModel';
import { defHttp } from '/@/utils/http/axios';
import { ErrorMessageMode } from '/#/axios';
import {
  UserconsultingtalklogListItem,
  UserconsultingtalklogPageListGetResultModel,
  UserconsultingtalklogParams
} from "/@/api/demo/model/userconsultingtalklogModel";

enum Api {
  userconsultingDetail = '/device/ecs_consulting_talklog/querylist',
  userconsultingUser = '/device/ecs_consulting_talklog/querybyuser',
  updateUserconsulting = '/device/ecs_consulting/updatejson',
  setUserconsultingType = '/device/ecs_consulting/settype',
  setUserconsultingUpdateType = '/device/ecs_consulting/setupdatetype',
  GetAllUserconsultingList = '/device/ecs_consulting/queryweb',
  UserconsultingDelete = '/device/ecs_consulting/delete',
  userconsultingtalklogList = '/device/userconsultingtalklog/querybyotaid',
  updateUserconsultingtalklog = '/device/ecs_consulting_talklog/updatejson',
}
//咨询相关用户
export const getUserconsultingUser = (consulting_id: number) =>
  defHttp.get({ url: Api.userconsultingUser, params: { consulting_id } });
//咨询详情
export const getUserconsultingDetail = (consulting_id: number) =>
  defHttp.get({ url: Api.userconsultingDetail, params: { consulting_id } });

//咨询查询主列表
export function getUserconsultingtalklogList(
  params: UserconsultingtalklogParams | undefined,
  mode: ErrorMessageMode = 'modal',
) {
  const data = defHttp.get<UserconsultingtalklogPageListGetResultModel>(
    {
      url: Api.userconsultingtalklogList,
      params,
    },
    {
      errorMessageMode: mode,
    },
  );
  return data;
}
//APP列表
export function getUserconsultingList(
  params: UserconsultingPageParams | undefined,
  mode: ErrorMessageMode = 'modal',
) {
  const data = defHttp.get<UserconsultingPageListGetResultModel>(
    {
      url: Api.GetAllUserconsultingList,
      params,
    },
    {
      errorMessageMode: mode,
    },
  );
  return data;
}

export const setUserconsultingType = (id: number, ota_type: number) =>
  defHttp.post({ url: Api.setUserconsultingType, params: { id, ota_type } });

export const setUserconsultingUpdateType = (id: number, ota_update_type: number) =>
  defHttp.post({ url: Api.setUserconsultingUpdateType, params: { id, ota_update_type } });

export const delUserconsulting = (id: number) =>
  defHttp.delete({ url: Api.UserconsultingDelete, params: { id } });

/**
 * @description: 新增/修改咨询主表
 */
export function updateUserconsulting(params: {}, mode: ErrorMessageMode = 'modal') {
  return defHttp.post<UserconsultingListItem>(
    {
      url: Api.updateUserconsulting,
      params,
    },
    {
      errorMessageMode: mode,
    },
  );
}
/**
 * @description: 新增/修改咨询子表
 */
export function updateUserconsultinglog(params: {}, mode: ErrorMessageMode = 'modal') {
  return defHttp.post<UserconsultingtalklogListItem>(
    {
      url: Api.updateUserconsultingtalklog,
      params,
    },
    {
      errorMessageMode: mode,
    },
  );
}
