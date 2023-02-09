#!/usr/bin/env python3
# _*_ coding: utf-8 _*_
# @Time : 2021/9/22 10:01
# @Author : wdm
# @desc : 管理员表的模型
from typing import Union
from pydantic import BaseModel, Field

from core import settings
from schemas import GMT


class DeviceIn(BaseModel):
    """ 共享模型字段 """
    id: int = Field(...)
    device_code: str = Field(min_length=1, max_length=20, example='设备类编号')
    name: str = Field(min_length=1, max_length=30, example='设备类名称')
    image: str = Field(...)
    is_active: int = Field(...)
    product_id: int = Field(...)
    device_ota: int = Field(...)
    device_level: int = Field(default=0)
    device_auth_class_id: int = Field(default=0)
    version: str = Field(...)
    provinceid: str = Field(...)
    cityid: str = Field(...)
    address: str = Field(...)


class DeviceCreate(DeviceIn):
    """ 添加数据时的字段验证 """
    password: str = Field(default='123456', max_length=60, example='device管理员密码')  # 未输入密码,默认为'123456'


class DeviceUpdate(DeviceIn):
    """ 更新数据的字段验证 """
    password: Union[str]  # 未输入密码,默认为''(为原密码)


class DeviceOut(DeviceIn, GMT):
    """ 查询数据的字段验证 """
    id: int
    device_code: str
    name: str
    image: str
    product_id: int
    device_ota: int
    version: str

    class Config:
        orm_mode = True  # 是否使用orm模型(个人理解: 放行,不验证)

class DeviceDelete(BaseModel):
    """ 添加数据时的字段验证 """
    id: int = Field(...)

class DeviceType(BaseModel):
    id: int
    is_active: int

class DeviceCodeCheck(BaseModel):
    id: int
    device_code: str

class DeviceCodeCheckNoid(BaseModel):
    device_code: str

class DevicePwd(BaseModel):
    id: int
    hashed_password: str = Field(default='123456', max_length=60, example='device管理员密码')  # 未输入密码,默认为'123456'