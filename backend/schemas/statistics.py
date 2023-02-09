#!/usr/bin/env python3
# _*_ coding: utf-8 _*_
# @Time : 2021/9/22 9:59
# @Author : wdm
# @desc : 院系表模型
from typing import Optional
from pydantic import BaseModel, Field

from schemas import GMT


class StatisticsIn(BaseModel):
    """ 共享模型字段 """
    id: int = Field(...)
    stat_code: str = Field(...)
    stat_name: str = Field(...)
    prod_id: int = Field(...)
    stat_num: int = Field(...)
    stat_remark: str = Field(...)

class StatisticsCreate(StatisticsIn):
    """ 添加数据时的字段验证 """
    id: int = Field(...)


class StatisticsUpdate(StatisticsIn):
    """ 更新数据的字段验证 """
    pass


class StatisticsOut(StatisticsCreate, GMT):
    """ 查询数据的字段验证 """

    class Config:
        orm_mode = True  # 是否使用orm模型(个人理解: 放行,不验证)

class StatisticsDelete(BaseModel):
    """ 添加数据时的字段验证 """
    id: int = Field(...)
