#!/usr/bin/env python3
# _*_ coding: utf-8 _*_
# @Time : 2021/9/22 9:59
# @Author : wdm
# @desc : 角色表模型
from typing import Optional, Literal, List
from pydantic import BaseModel, Field


class RoleIn(BaseModel):
    """ 共享模型字段 """
    id: int = Field(...)
    role_name: str = Field(min_length=1, max_length=30, example='角色名称')
    role_status: Literal[0, 1] = Field(default=0, example='角色启用：0.未启用，1.已启用')
    role_desc: str = Field(...)

class RoleCreate(RoleIn):
    """ 添加数据时的字段验证 """
    #pass
    id: int = Field(...)


class RoleUpdate(RoleIn):
    """ 更新数据的字段验证 """
    pass


class RoleOut(BaseModel):
    """ 查询数据的字段验证 """
    id: int
    role_name: str
    role_status: int
    role_desc: str

    class Config:
        orm_mode = True  # 是否使用orm模型(个人理解: 放行,不验证)

class RoleDelete(BaseModel):
    """ 添加数据时的字段验证 """
    id: int = Field(...)

class RoleType(BaseModel):
    id: int
    role_status: int

class RoleMenu(RoleIn):
    """ 添加数据时的字段验证 """
    id: int = Field(...)
    menu: List = []