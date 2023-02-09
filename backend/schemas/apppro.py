#!/usr/bin/env python3
# _*_ coding: utf-8 _*_
# @Time : 2021/9/22 9:59
# @Author : wdm
# @desc : 院系表模型
from typing import Optional
from pydantic import BaseModel, Field

from schemas import GMT


class AppproIn(BaseModel):
    """ 共享模型字段 """
    id: int = Field(...)
    app_code: str = Field(min_length=1, max_length=20, example='APP编号')
    app_name: str = Field(min_length=1, max_length=30, example='APP名称')
    app_image: str = Field(...)
    app_class_id: int = Field(...)
    app_package: str = Field(...)
    app_type: int = Field(...)
    app_update_type: int = Field(...)
    app_company: str = Field(...)
    app_info: str = Field(...)
    app_score: float = Field(...)
    app_download_amount: int = Field(...)
    app_desc: str = Field(...)
    app_remark: str = Field(...)

class AppproCreate(AppproIn):
    """ 添加数据时的字段验证 """
    id: int = Field(...)


class AppproUpdate(AppproIn):
    """ 更新数据的字段验证 """
    pass

class AppproOut(AppproCreate, GMT):
    """ 查询数据的字段验证 """

    class Config:
        orm_mode = True  # 是否使用orm模型(个人理解: 放行,不验证)

class AppproDelete(BaseModel):
    """ 添加数据时的字段验证 """
    id: int = Field(...)

class AppproType(BaseModel):
    id: int
    app_type: int

class AppproUpdateType(BaseModel):
    id: int
    app_update_type: int
