#!/usr/bin/env python3
# _*_ coding: utf-8 _*_
# @Time : 2021/9/22 9:59
# @Author : wdm
# @desc : Admin Auth 关系表模型
from typing import Optional
from pydantic import BaseModel, Field

from schemas import GMT


class AdminauthclassIn(BaseModel):
    """ 共享模型字段 """
    id: int = Field(...)
    admin_id: int = Field(...)
    auth_class_id: int = Field(...)

class AdminauthclassCreate(AdminauthclassIn):
    """ 添加数据时的字段验证 """
    id: int = Field(...)


class AdminauthclassUpdate(AdminauthclassIn):
    """ 更新数据的字段验证 """
    pass


class AdminauthclassOut(AdminauthclassCreate, GMT):
    """ 查询数据的字段验证 """

    class Config:
        orm_mode = True  # 是否使用orm模型(个人理解: 放行,不验证)

class AdminauthclassDelete(BaseModel):
    """ 添加数据时的字段验证 """
    id: int = Field(...)