import { BasicPageParams, BasicFetchResult } from '/@/api/model/baseModel';

export type UserParams = {
  user_name?: string;
  deviceid?: string;
};

export type UserPageParams = BasicPageParams & UserParams;

export type UserIDParams = {
  idstr?: string;
};

export interface UserIDListItem {
  excelid: number;
}

export type UserIDSendParams = UserIDParams;
export type UserIDPageListGetResultModel = BasicFetchResult<UserIDListItem>;

export interface UserListItem {
  id: number;
  name: string;
  headicon: string;
  age: string;
  sex: string;
  deviceid: string;
  idcard: string;
  height: string;
  weight: string;
  cityid: number;
  cityname: string;
  phone: string;
  bloodtypeid: number;
  bloodtypename: string;
  allergyid: number;
  allergyname: string;
  medicalid: number;
  medicalname: string;
  geneticid: number;
  geneticname: string;
  usergeneticname: string;
  descr: string;
  updatetime: string;
  updatetimedate: string;
  createtime: string;
  createtimedate: string;
}

/**
 * @description: Request list return value
 */

export type UserPageListGetResultModel = BasicFetchResult<UserListItem>;
