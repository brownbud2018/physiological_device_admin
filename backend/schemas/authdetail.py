#!/usr/bin/env python3
# _*_ coding: utf-8 _*_
# @Time : 2021/9/22 9:59
# @Author : wdm
# @desc : 院系表模型
from typing import Optional
from pydantic import BaseModel, Field

from schemas import GMT


class AuthdetailIn(BaseModel):
    """ 共享模型字段 """
    detail_code: str = Field(min_length=1, max_length=20, example='权限编号')
    detail_name: str = Field(min_length=1, max_length=30, example='权限名称')
    detail_image: Optional[str] = Field(min_length=1, max_length=60, example='权限图标')
    detail_type: int = Field(default=0)
    detail_desc: str = Field(...)
    detail_remark: str = Field(...)

class AuthdetailCreate(AuthdetailIn):
    """ 添加数据时的字段验证 """
    id: int = Field(...)


class AuthdetailUpdate(AuthdetailIn):
    """ 更新数据的字段验证 """
    pass


class AuthdetailOut(AuthdetailCreate, GMT):
    """ 查询数据的字段验证 """

    class Config:
        orm_mode = True  # 是否使用orm模型(个人理解: 放行,不验证)

class AuthdetailDelete(BaseModel):
    """ 添加数据时的字段验证 """
    id: int = Field(...)

class AuthdetailType(BaseModel):
    id: int
    detail_type: int
