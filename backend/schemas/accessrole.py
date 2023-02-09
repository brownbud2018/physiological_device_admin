#!/usr/bin/env python3
# _*_ coding: utf-8 _*_
# @Time : 2021/9/22 9:59
# @Author : wdm
# @desc : Accessrole 关系表模型
from typing import Optional
from pydantic import BaseModel, Field

from schemas import GMT


class AccessroleIn(BaseModel):
    """ 共享模型字段 """
    id: int = Field(...)
    role_id: int = Field(...)
    access_id: int = Field(...)

class AccessroleCreate(AccessroleIn):
    """ 添加数据时的字段验证 """
    id: int = Field(...)


class AccessroleUpdate(AccessroleIn):
    """ 更新数据的字段验证 """
    pass


class AccessroleOut(AccessroleCreate, GMT):
    """ 查询数据的字段验证 """

    class Config:
        orm_mode = True  # 是否使用orm模型(个人理解: 放行,不验证)

class AccessroleDelete(BaseModel):
    """ 添加数据时的字段验证 """
    id: int = Field(...)