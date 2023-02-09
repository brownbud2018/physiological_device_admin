#!/usr/bin/env python3
# _*_ coding: utf-8 _*_
# @Time : 2021/9/22 9:59
# @Author : wdm
# @desc : 城市表模型
from typing import Optional
from pydantic import BaseModel, Field

from schemas import GMT


class CitiesIn(BaseModel):
    """ 共享模型字段 """
    id: int = Field(...)
    cityid: str = Field(min_length=1, max_length=20, example='城市编号')
    city: str = Field(min_length=1, max_length=50, example='城市名称')
    provinceid: str = Field(...)

class CitiesCreate(CitiesIn):
    """ 添加数据时的字段验证 """
    id: int = Field(...)


class CitiesUpdate(CitiesIn):
    """ 更新数据的字段验证 """
    pass

class CitiesOut(CitiesCreate, GMT):
    """ 查询数据的字段验证 """

    class Config:
        orm_mode = True  # 是否使用orm模型(个人理解: 放行,不验证)

class CitiesDelete(BaseModel):
    """ 添加数据时的字段验证 """
    id: int = Field(...)
