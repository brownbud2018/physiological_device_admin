#!/usr/bin/env python3
# _*_ coding: utf-8 _*_
# @Time : 2021/9/22 9:59
# @Author : wdm
# @desc : 省份表模型
from typing import Optional
from pydantic import BaseModel, Field

from schemas import GMT


class ProvincesIn(BaseModel):
    """ 共享模型字段 """
    id: int = Field(...)
    provinceid: str = Field(min_length=1, max_length=20, example='省份编号')
    province: str = Field(min_length=1, max_length=50, example='省份名称')

class ProvincesCreate(ProvincesIn):
    """ 添加数据时的字段验证 """
    id: int = Field(...)


class ProvincesUpdate(ProvincesIn):
    """ 更新数据的字段验证 """
    pass

class ProvincesOut(ProvincesCreate, GMT):
    """ 查询数据的字段验证 """

    class Config:
        orm_mode = True  # 是否使用orm模型(个人理解: 放行,不验证)

class ProvincesDelete(BaseModel):
    """ 添加数据时的字段验证 """
    id: int = Field(...)
