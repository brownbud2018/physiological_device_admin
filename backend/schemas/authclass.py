#!/usr/bin/env python3
# _*_ coding: utf-8 _*_
# @Time : 2021/9/22 9:59
# @Author : wdm
# @desc : 院系表模型
from typing import Optional
from pydantic import BaseModel, Field

from schemas import GMT


class AuthclassIn(BaseModel):
    """ 共享模型字段 """
    id: int = Field(...)
    class_code: str = Field(min_length=1, max_length=20, example='授权编号')
    class_name: str = Field(min_length=1, max_length=30, example='授权名称')
    class_image: str = Field(...)
    class_desc: str = Field(...)
    class_remark: str = Field(...)

class AuthclassCreate(AuthclassIn):
    """ 添加数据时的字段验证 """
    id: int = Field(...)


class AuthclassUpdate(AuthclassIn):
    """ 更新数据的字段验证 """
    pass


class AuthclassOut(AuthclassCreate, GMT):
    """ 查询数据的字段验证 """

    class Config:
        orm_mode = True  # 是否使用orm模型(个人理解: 放行,不验证)

class AuthclassDelete(BaseModel):
    """ 添加数据时的字段验证 """
    id: int = Field(...)
