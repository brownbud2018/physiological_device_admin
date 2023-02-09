#!/usr/bin/env python3
# _*_ coding: utf-8 _*_
# @Time : 2021/9/22 10:01
# @Author : wdm
# @desc : dm_user表的模型
from typing import Union
from pydantic import BaseModel, Field

from core import settings
from schemas import GMT


class Dm_userIn(BaseModel):
    """ 共享模型字段 """
    id: int = Field(...)
    name: str = Field(min_length=1, max_length=100, example='用户名')


class Dm_userCreate(BaseModel):
    """ 添加数据时的字段验证 """
    id: int = Field(...)
    name: str = ""
    headicon: str = ""
    age: str = ""
    sex: str = ""
    deviceid: str = ""
    idcard: str = ""
    height: str = ""
    weight: str = ""
    cityid: int = 0
    cityname: str = ""
    phone: str = ""
    bloodtypeid: int = 0
    bloodtypename: str = ""
    allergyid: int = 0
    allergyname: str = ""
    medicalid: int = 0
    medicalname: str = ""
    geneticid: int = 0
    geneticname: str = ""
    usergeneticname: str = ""
    descr: str = ""


class Dm_userUpdate(Dm_userIn):
    """ 更新数据的字段验证 """
    pass


class Dm_userOut(Dm_userIn):
    """ 查询数据的字段验证 """

    class Config:
        orm_mode = True  # 是否使用orm模型(个人理解: 放行,不验证)

class Dm_userDelete(BaseModel):
    """ 添加数据时的字段验证 """
    id: int = Field(...)

class Dm_userType(BaseModel):
    id: int
    sex: int

class Dm_userCodeCheck(BaseModel):
    id: int
    deviceid: str

class Dm_userCodeCheckNoid(BaseModel):
    deviceid: str

class Dm_userPwd(BaseModel):
    id: int