#!/usr/bin/env python3
# _*_ coding: utf-8 _*_
# @Time : 2021/9/22 9:59
# @Author : wdm
# @desc : APP版本表模型
from typing import Optional
from pydantic import BaseModel, Field

from schemas import GMT


class AppversionIn(BaseModel):
    """ 共享模型字段 """
    app_v_code: str = Field(min_length=1, max_length=20, example='APP编号')
    app_v_name: str = Field(min_length=1, max_length=30, example='APP名称')
    app_v_image: Optional[str] = Field(min_length=1, max_length=60, example='APP图标')
    app_v_file: Optional[str] = Field(min_length=1, max_length=60, example='APP文件')
    app_pro_id: int = Field(default=0)
    app_v_default: int = Field(default=0)
    app_v_remark: str = Field(...)

class AppversionCreate(AppversionIn):
    """ 添加数据时的字段验证 """
    id: int = Field(...)


class AppversionUpdate(AppversionIn):
    """ 更新数据的字段验证 """
    pass


class AppversionOut(AppversionCreate, GMT):
    """ 查询数据的字段验证 """

    class Config:
        orm_mode = True  # 是否使用orm模型(个人理解: 放行,不验证)

class AppversionDelete(BaseModel):
    """ 添加数据时的字段验证 """
    id: int = Field(...)

class AppversionType(BaseModel):
    id: int
    app_v_default: int
