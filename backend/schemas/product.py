#!/usr/bin/env python3
# _*_ coding: utf-8 _*_
# @Time : 2021/9/22 9:59
# @Author : wdm
# @desc : 院系表模型
from typing import Optional
from pydantic import BaseModel, Field

from schemas import GMT


class ProductIn(BaseModel):
    """ 共享模型字段 """
    id: int = Field(...)
    prod_code: str = Field(min_length=1, max_length=20, example='设备类编号')
    prod_name: str = Field(min_length=1, max_length=30, example='设备类名称')
    prod_image: str = Field(...)
    project_id: str = Field(...)
    prod_remark: str = Field(...)

class ProductCreate(ProductIn):
    """ 添加数据时的字段验证 """
    id: int = Field(...)


class ProductUpdate(ProductIn):
    """ 更新数据的字段验证 """
    pass


class ProductOut(ProductCreate, GMT):
    """ 查询数据的字段验证 """
    id: int
    prod_code: str
    prod_name: str
    prod_image: str
    project_id: int
    prod_remark: str

    class Config:
        orm_mode = True  # 是否使用orm模型(个人理解: 放行,不验证)

class ProductDelete(BaseModel):
    """ 添加数据时的字段验证 """
    id: int = Field(...)
