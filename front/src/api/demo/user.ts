import {
  UserPageParams,
  UserPageListGetResultModel,
  UserListItem,
  UserIDSendParams,
  UserIDPageListGetResultModel,
} from './model/userModel';
import { defHttp } from '/@/utils/http/axios';
import { ErrorMessageMode } from '/#/axios';
import { LogPageListGetResultModel, LogPageParams } from '/@/api/demo/model/productModel';
import {
  BloodsugarPageListGetResultModel,
  BloodsugarPageParams,
} from '/@/api/demo/model/bloodsugarModel';
import {
  BloodpressurePageListGetResultModel,
  BloodpressurePageParams,
} from '/@/api/demo/model/bloodpressureModel';
import {
  HeartrateListItem,
  HeartratePageListGetResultModel,
  HeartratePageParams,
} from '/@/api/demo/model/heartrateModel';
import {
  BloodoxygenListItem,
  BloodoxygenPageListGetResultModel,
  BloodoxygenPageParams,
} from '/@/api/demo/model/bloodoxygenModel';
import {
  TemperaturePageListGetResultModel,
  TemperaturePageParams,
} from '/@/api/demo/model/temperatureModel';
import { MedicalRecordPageListGetResultModel } from '/@/api/demo/model/medicalRecordModel';
import { QuestionListGetResultModel, QuestionPageParams } from "/@/api/demo/model/questionModel";
import { PhysiqueListGetResultModel, PhysiquePageParams } from "/@/api/demo/model/physiqueModel";

enum Api {
  getBloodtypeList = '/dm_user/qtreebloodtype',
  getAllergyList = '/dm_user/qtreeallergy',
  getMedicalList = '/dm_user/qtreemedical',
  getGeneticList = '/dm_user/qtreegenetic',
  projectDetail = '/dm_user/product/querybyid',
  logList = '/dm_user/userlog/querybyprodid',
  userBloodsugarList = '/dm_user/querybloodsugarbyuserid',
  userBloodsugarList2 = '/dm_user/querybloodsugarbyuserid2',
  userBloodpressureList = '/dm_user/querybloodpressurebyuserid',
  userBloodpressureList2 = '/dm_user/querybloodpressurebyuserid2',
  userHeartrateList = '/dm_user/queryheartratebyuserid',
  userHeartrateList2 = '/dm_user/queryheartratebyuserid2',
  userHeartrateList3 = '/dm_user/queryheartratebyuserid3',
  userBloodoxygenList = '/dm_user/querybloodoxygenbyuserid',
  userBloodoxygenList2 = '/dm_user/querybloodoxygenbyuserid2',
  userBloodoxygenList3 = '/dm_user/querybloodoxygenbyuserid3',
  userTemperatureList = '/dm_user/querytemperaturebyuserid',
  userTemperatureList2 = '/dm_user/querytemperaturebyuserid2',
  userMedicalRecordList = '/dm_user/querymedicalrecordbyuserid',
  userMedicalRecordList2 = '/dm_user/querymedicalrecordbyuserid3',
  userQuestionList = '/device/d_question/queryweb',
  userQuestionList2 = '/device/d_question/querylist',
  userPhysiqueList = '/dm_user/queryphysiquebyuserid',
  userPhysiqueList2 = '/dm_user/queryphysiquebyuserid2',
  updateUser = '/dm_user/updatejson',
  setUserType = '/dm_user/settype',
  setUserPwd = '/dm_user/changepwd',
  deleteUser = '/dm_user/delete',
  GetAllUserList = '/dm_user/queryweb',
  userDetail = '/dm_user/querybyid',
  IsUserExist = '/dm_user/userexist',
  IsNewUserExist = '/dm_user/usernewexist',
  UserOutExcel = '/dm_user/outexcel',
}

export const isUserExist1 = (user_code: string) =>
  defHttp.post({ url: Api.IsNewUserExist, params: { user_code } }, { errorMessageMode: 'none' });

export const isUserExist = (id: number, user_code: string) =>
  defHttp.post({ url: Api.IsUserExist, params: { id, user_code } }, { errorMessageMode: 'none' });
//user??????
export function getUserList(params: UserPageParams | undefined, mode: ErrorMessageMode = 'modal') {
  const data = defHttp.get<UserPageListGetResultModel>(
    {
      url: Api.GetAllUserList,
      params,
    },
    {
      errorMessageMode: mode,
    },
  );
  return data;
}

//??????????????????
export function getUserBloodsugarList1(
  params: BloodsugarPageParams | undefined,
  mode: ErrorMessageMode = 'modal',
) {
  const data = defHttp.get<BloodsugarPageListGetResultModel>(
    {
      url: Api.userBloodsugarList,
      params,
    },
    {
      errorMessageMode: mode,
    },
  );
  return data;
}
//??????????????????
export const getUserBloodsugarList2 = (dmuserid: number) =>
  defHttp.get<BloodsugarPageListGetResultModel>({
    url: Api.userBloodsugarList2,
    params: { dmuserid },
  });
//??????????????????1
export function getUserBloodpressureList1(
  params: BloodpressurePageParams | undefined,
  mode: ErrorMessageMode = 'modal',
) {
  const data = defHttp.get<BloodpressurePageListGetResultModel>(
    {
      url: Api.userBloodpressureList,
      params,
    },
    {
      errorMessageMode: mode,
    },
  );
  return data;
}
//??????????????????2
export const getUserBloodpressureList2 = (dmuserid: number) =>
  defHttp.get<BloodpressurePageListGetResultModel>({
    url: Api.userBloodpressureList2,
    params: { dmuserid },
  });
//??????????????????1
export function getUserHeartrateList1(
  params: HeartratePageParams | undefined,
  mode: ErrorMessageMode = 'modal',
) {
  const data = defHttp.get<HeartratePageListGetResultModel>(
    {
      url: Api.userHeartrateList,
      params,
    },
    {
      errorMessageMode: mode,
    },
  );
  return data;
}
//??????????????????2
export const getUserHeartrateList2 = (dmuserid: number) =>
  defHttp.get<HeartratePageListGetResultModel>({
    url: Api.userHeartrateList2,
    params: { dmuserid },
  });
//??????????????????3
export const getUserHeartrateList3 = (heartrateid: String) =>
  defHttp.get<HeartrateListItem>({
    url: Api.userHeartrateList3,
    params: { heartrateid },
  });
//??????????????????1
export function getUserBloodoxygenList1(
  params: BloodoxygenPageParams | undefined,
  mode: ErrorMessageMode = 'modal',
) {
  const data = defHttp.get<BloodoxygenPageListGetResultModel>(
    {
      url: Api.userBloodoxygenList,
      params,
    },
    {
      errorMessageMode: mode,
    },
  );
  return data;
}
//??????????????????2
export const getUserBloodoxygenList2 = (dmuserid: number) =>
  defHttp.get<BloodoxygenPageListGetResultModel>({
    url: Api.userBloodoxygenList2,
    params: { dmuserid },
  });
//??????????????????3
export const getUserBloodoxygenList3 = (bloodoxygenid: String) =>
  defHttp.get<BloodoxygenListItem>({
    url: Api.userBloodoxygenList3,
    params: { bloodoxygenid },
  });
//??????????????????
export function getUserTemperatureList1(
  params: TemperaturePageParams | undefined,
  mode: ErrorMessageMode = 'modal',
) {
  const data = defHttp.get<TemperaturePageListGetResultModel>(
    {
      url: Api.userTemperatureList,
      params,
    },
    {
      errorMessageMode: mode,
    },
  );
  return data;
}
//??????????????????
export const getUserTemperatureList2 = (dmuserid: number) =>
  defHttp.get<TemperaturePageListGetResultModel>({
    url: Api.userTemperatureList2,
    params: { dmuserid },
  });
//??????????????????
export function getUserMedicalRecordList1(
  params: TemperaturePageParams | undefined,
  mode: ErrorMessageMode = 'modal',
) {
  const data = defHttp.get<MedicalRecordPageListGetResultModel>(
    {
      url: Api.userMedicalRecordList,
      params,
    },
    {
      errorMessageMode: mode,
    },
  );
  return data;
}
//??????????????????
export const getUserMedicalRecordList2 = (medicalrecordid: string) =>
  defHttp.get<MedicalRecordPageListGetResultModel>({
    url: Api.userMedicalRecordList2,
    params: { medicalrecordid },
  });
//??????????????????
export function getQuestionList1(
  params: QuestionPageParams | undefined,
  mode: ErrorMessageMode = 'modal',
) {
  const data = defHttp.get<QuestionListGetResultModel>(
    {
      url: Api.userQuestionList,
      params,
    },
    {
      errorMessageMode: mode,
    },
  );
  return data;
}
//??????????????????
export const getUserQuestionList2 = (question_id: string) =>
  defHttp.get<QuestionListGetResultModel>({
    url: Api.userQuestionList2,
    params: { question_id },
  });
//????????????????????????
export function getUserPhysiqueList1(
  params: PhysiquePageParams | undefined,
  mode: ErrorMessageMode = 'modal',
) {
  const data = defHttp.get<PhysiqueListGetResultModel>(
    {
      url: Api.userPhysiqueList,
      params,
    },
    {
      errorMessageMode: mode,
    },
  );
  return data;
}
//????????????????????????
export const getUserPhysiqueList2 = (physiqueid: number) =>
  defHttp.get<PhysiqueListGetResultModel>({
    url: Api.userPhysiqueList2,
    params: { physiqueid },
  });
//user??????
export const getUserDetail = (user_id: number) =>
  defHttp.get({ url: Api.userDetail, params: { user_id } });
/**
 * @description: Bloodtype???Tree??????
 */
export const getBloodtypeTreeList = (params?: UserListItem) =>
  defHttp.get<UserPageListGetResultModel>({ url: Api.getBloodtypeList, params });
/**
 * @description: Allergy???Tree???????????????
 */
export const getAllergyTreeList = (params?: UserListItem) =>
  defHttp.get<UserPageListGetResultModel>({ url: Api.getAllergyList, params });
/**
 * @description: Medical???Tree????????????
 */
export const getMedicalTreeList = (params?: UserListItem) =>
  defHttp.get<UserPageListGetResultModel>({ url: Api.getMedicalList, params });
/**
 * @description: Genetic???Tree?????????
 */
export const getGeneticTreeList = (params?: UserListItem) =>
  defHttp.get<UserPageListGetResultModel>({ url: Api.getGeneticList, params });

//??????????????????????????????
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

export const setUserType = (id: number, is_active: number) =>
  defHttp.post({ url: Api.setUserType, params: { id, is_active } });

export const setUserPwd = (id: number, hashed_password: string) =>
  defHttp.post({ url: Api.setUserPwd, params: { id, hashed_password } });

export const delUserType = (id: number) => defHttp.delete({ url: Api.deleteUser, params: { id } });

/**
 * @description: ??????/??????User??????
 */
export function updateUser(params: {}, mode: ErrorMessageMode = 'modal') {
  //console.log(params);
  return defHttp.post<UserListItem>(
    {
      url: Api.updateUser,
      params,
    },
    {
      errorMessageMode: mode,
      isReturnNativeResponse: true,
    },
  );
}
/**
 * @description: ??????Excel
 */
export function outExcelUser(
  params: UserIDSendParams | undefined,
  mode: ErrorMessageMode = 'modal',
) {
  const data = defHttp.get<UserIDPageListGetResultModel>(
    {
      url: Api.UserOutExcel,
      params,
    },
    {
      errorMessageMode: mode,
    },
  );
  return data;
}
