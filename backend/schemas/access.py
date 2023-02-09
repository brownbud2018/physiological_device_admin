#!/usr/bin/env python3
# _*_ coding: utf-8 _*_
# @Time : 2021/9/22 9:59
# @Author : wdm
# @desc : 权限表模型
from typing import Optional
from pydantic import BaseModel, Field

from schemas import GMT


class AccessIn(BaseModel):
    """ 共享模型字段 """
    id: int = Field(...)
    access_code: str = Field(min_length=1, max_length=50, example='权限编号')
    access_name: str = Field(min_length=1, max_length=30, example='权限名称')
    access_path: str = Field(...)
    access_redirect: str = Field(...)
    menu_icon: str = Field(...)
    parent_id: int = Field(...)
    is_check: int = Field(...)
    is_menu: int = Field(...)
    access_desc: str = Field(...)
    access_remark: str = Field(...)
    sort_order: int = Field(...)

class AccessCreate(AccessIn):
    """ 添加数据时的字段验证 """
    id: int = Field(...)


class AccessUpdate(AccessIn):
    """ 更新数据的字段验证 """
    pass

class AccessOut(AccessCreate, GMT):
    """ 查询数据的字段验证 """

    class Config:
        orm_mode = True  # 是否使用orm模型(个人理解: 放行,不验证)

class AccessDelete(BaseModel):
    """ 添加数据时的字段验证 """
    id: int = Field(...)

class AccessType(BaseModel):
    id: int
    is_check: int

class AccessUpdateType(BaseModel):
    id: int
    access_update_type: int

class AccessType1(BaseModel):
    id: int
    is_menu: int

class AccessUpdateType1(BaseModel):
    id: int
    access_update_type: int

class AccessCodeCheck(BaseModel):
    id: int
    access_code: str

class AccessCodeCheckNoid(BaseModel):
    access_code: str