#!/usr/bin/env python3
# _*_ coding: utf-8 _*_
# @Time : 2022/5/22 9:59
# @Author : wdm
# @desc : OTA表模型
from typing import Optional
from pydantic import BaseModel, Field

from schemas import GMT


class OtamainIn(BaseModel):
    """ 共享模型字段 """
    id: int = Field(...)
    ota_code: str = Field(min_length=1, max_length=20, example='OTA编号')
    ota_name: str = Field(min_length=1, max_length=30, example='OTA名称')
    ota_image: str = Field(...)
    ota_package: str = Field(...)
    ota_type: int = Field(...)
    ota_update_type: int = Field(...)
    ota_company: str = Field(...)
    ota_info: str = Field(...)
    ota_score: float = Field(...)
    ota_download_amount: int = Field(...)
    ota_desc: str = Field(...)
    ota_remark: str = Field(...)

class OtamainCreate(OtamainIn):
    """ 添加数据时的字段验证 """
    id: int = Field(...)


class OtamainUpdate(OtamainIn):
    """ 更新数据的字段验证 """
    pass


class OtamainOut(OtamainCreate, GMT):
    """ 查询数据的字段验证 """

    class Config:
        orm_mode = True  # 是否使用orm模型(个人理解: 放行,不验证)

class OtamainDelete(BaseModel):
    """ 添加数据时的字段验证 """
    id: int = Field(...)

class OtamainType(BaseModel):
    id: int
    ota_type: int

class OtamainUpdateType(BaseModel):
    id: int
    ota_update_type: int
