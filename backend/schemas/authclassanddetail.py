#!/usr/bin/env python3
# _*_ coding: utf-8 _*_
# @Time : 2021/9/22 9:59
# @Author : wdm
# @desc : Product APP 关系表模型
from typing import Optional
from pydantic import BaseModel, Field

from schemas import GMT


class AuthclassanddetailIn(BaseModel):
    """ 共享模型字段 """
    id: int = Field(...)
    class_id: int = Field(...)
    detail_id: int = Field(...)

class AuthclassanddetailCreate(AuthclassanddetailIn):
    """ 添加数据时的字段验证 """
    id: int = Field(...)


class AuthclassanddetailUpdate(AuthclassanddetailIn):
    """ 更新数据的字段验证 """
    pass


class AuthclassanddetailOut(AuthclassanddetailCreate, GMT):
    """ 查询数据的字段验证 """

    class Config:
        orm_mode = True  # 是否使用orm模型(个人理解: 放行,不验证)

class AuthclassanddetailDelete(BaseModel):
    """ 添加数据时的字段验证 """
    id: int = Field(...)