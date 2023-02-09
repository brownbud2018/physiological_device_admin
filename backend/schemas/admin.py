#!/usr/bin/env python3
# _*_ coding: utf-8 _*_
# @Time : 2021/9/22 10:01
# @Author : wdm
# @desc : 管理员表的模型
from typing import Union, Literal
from pydantic import BaseModel, Field

from core import settings
from schemas import GMT


class AdminIn(BaseModel):
    """ 共享模型字段 """
    id: int = Field(...)
    name: str = Field(min_length=1, max_length=20, example='用户名')
    nickname: str = Field(...)
    role_id: int = Field(...)
    image: str = Field(...)
    address: str = Field(...)
    is_active: int = Field(...)
    user_type: int = Field(...)
    professor_id: int = Field(...)


class AdminCreate(AdminIn):
    """ 添加数据时的字段验证 """
    password: str = Field(default='123456', max_length=60, example='管理员密码')  # 未输入密码,默认为'123456'


class AdminUpdate(AdminIn):
    """ 更新数据的字段验证 """
    password: Union[str]  # 未输入密码,默认为''(为原密码)


class AdminOut(AdminIn, GMT):
    """ 查询数据的字段验证 """
    id: int = Field(..., example='自增编号')

    class Config:
        orm_mode = True  # 是否使用orm模型(个人理解: 放行,不验证)
class AdminDelete(BaseModel):
    """ 添加数据时的字段验证 """
    id: int = Field(...)

class AdminType(BaseModel):
    id: int
    is_active: int

class AdminType1(BaseModel):
    id: int
    user_type: int

class AdminCodeCheck(BaseModel):
    id: int
    admin_code: str

class AdminCodeCheckNoid(BaseModel):
    admin_code: str

class AdminPwd(BaseModel):
    id: int
    hashed_password: str = Field(default='123456', max_length=60, example='admin管理员密码')  # 未输入密码,默认为'123456'
