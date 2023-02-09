#!/usr/bin/env python3
# _*_ coding: utf-8 _*_
# @Time : 2021/9/22 9:59
# @Author : wdm
# @desc : Product APP 关系表模型
from typing import Optional
from pydantic import BaseModel, Field

from schemas import GMT


class DevicelogIn(BaseModel):
    """ 共享模型字段 """
    id: int = Field(...)
    log_code: str = Field(...)
    device_id: int = Field(...)

class DevicelogCreate(DevicelogIn):
    """ 添加数据时的字段验证 """
    id: int = Field(...)


class DevicelogUpdate(DevicelogIn):
    """ 更新数据的字段验证 """
    pass


class DevicelogOut(DevicelogCreate, GMT):
    """ 查询数据的字段验证 """

    class Config:
        orm_mode = True  # 是否使用orm模型(个人理解: 放行,不验证)

class DevicelogDelete(BaseModel):
    """ 添加数据时的字段验证 """
    id: int = Field(...)
