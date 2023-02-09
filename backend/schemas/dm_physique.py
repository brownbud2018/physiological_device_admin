#!/usr/bin/env python3
# _*_ coding: utf-8 _*_
# @Time : 2021/9/22 9:59
# @Author : wdm
# @desc : Dm_physique 关系表模型
from typing import Optional
from pydantic import BaseModel, Field

from schemas import GMT


class Dm_physiqueIn(BaseModel):
    """ 共享模型字段 """
    id: int = Field(...)

class Dm_physiqueCreate(Dm_physiqueIn):
    """ 添加数据时的字段验证 """
    id: int = Field(...)


class Dm_physiqueUpdate(Dm_physiqueIn):
    """ 更新数据的字段验证 """
    pass


class Dm_physiqueOut(Dm_physiqueCreate):
    """ 查询数据的字段验证 """

    class Config:
        orm_mode = True  # 是否使用orm模型(个人理解: 放行,不验证)

class Dm_physiqueDelete(BaseModel):
    """ 添加数据时的字段验证 """
    id: int = Field(...)
