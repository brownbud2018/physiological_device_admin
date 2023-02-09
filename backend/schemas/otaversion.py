#!/usr/bin/env python3
# _*_ coding: utf-8 _*_
# @Time : 2021/9/22 9:59
# @Author : wdm
# @desc : OTA版本表模型
from typing import Optional
from pydantic import BaseModel, Field

from schemas import GMT


class OtaversionIn(BaseModel):
    """ 共享模型字段 """
    ota_v_code: str = Field(min_length=1, max_length=20, example='OTA编号')
    ota_v_name: str = Field(min_length=1, max_length=30, example='OTA名称')
    ota_v_image: Optional[str] = Field(min_length=1, max_length=60, example='OTA图标')
    ota_v_file: Optional[str] = Field(min_length=1, max_length=60, example='OTA文件')
    ota_main_id: int = Field(default=0)
    ota_v_default: int = Field(default=0)
    ota_v_md5: str = Field(...)
    ota_v_remark: str = Field(...)

class OtaversionCreate(OtaversionIn):
    """ 添加数据时的字段验证 """
    id: int = Field(...)


class OtaversionUpdate(OtaversionIn):
    """ 更新数据的字段验证 """
    pass


class OtaversionOut(OtaversionCreate, GMT):
    """ 查询数据的字段验证 """

    class Config:
        orm_mode = True  # 是否使用orm模型(个人理解: 放行,不验证)

class OtaversionDelete(BaseModel):
    """ 添加数据时的字段验证 """
    id: int = Field(...)

class OtaversionType(BaseModel):
    id: int
    ota_v_default: int
