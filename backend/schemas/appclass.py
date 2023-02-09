#!/usr/bin/env python3
# _*_ coding: utf-8 _*_
# @Time : 2021/9/22 9:59
# @Author : wdm
# @desc : APP分类表模型
from typing import Optional
from pydantic import BaseModel, Field

from schemas import GMT


class AppclassIn(BaseModel):
    """ 共享模型字段 """
    id: int = Field(...)
    class_code: str = Field(min_length=1, max_length=20, example='项目代码')
    class_name: str = Field(min_length=1, max_length=30, example='项目名称')
    class_image: str = Field(...)
    class_desc: str = Field(...)
    class_remark: str = Field(...)

class AppclassCreate(AppclassIn):
    """ 添加数据时的字段验证 """
    id: int = Field(...)


class AppclassUpdate(AppclassIn):
    """ 更新数据的字段验证 """
    pass


class AppclassOut(BaseModel):
    """ 查询数据的字段验证 """
    id: int
    class_code: str
    class_name: str
    class_image: str
    class_desc: str
    class_remark: str

    class Config:
        orm_mode = True  # 是否使用orm模型(个人理解: 放行,不验证)

class AppclassDelete(BaseModel):
    """ 添加数据时的字段验证 """
    id: int = Field(...)

class AppclassDesc(BaseModel):
    id: int
    class_desc: int
