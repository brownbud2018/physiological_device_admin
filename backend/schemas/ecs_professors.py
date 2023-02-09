#!/usr/bin/env python3
# _*_ coding: utf-8 _*_
# @Time : 2021/9/22 9:59
# @Author : wdm
# @desc : 医生表模型
from typing import Optional, Literal, List
from pydantic import BaseModel, Field


class Ecs_professorsIn(BaseModel):
    """ 共享模型字段 """
    id: Optional[int] = None

class Ecs_professorsCreate(BaseModel):
    """ 添加数据时的字段验证 """
    #pass
    id: int = Field(...)
    avatar: Optional[str]
    cat_id: Optional[int] = None
    email: Optional[str] = None
    expert: Optional[str] = None
    phone: Optional[str] = None
    professor_name: Optional[str] = None
    resume: Optional[str] = None
    sex: Optional[int] = None
    title: Optional[str] = None


class Ecs_professorsUpdate(Ecs_professorsIn):
    """ 更新数据的字段验证 """
    pass


class Ecs_professorsOut(BaseModel):
    """ 查询数据的字段验证 """
    id: int

    class Config:
        orm_mode = True  # 是否使用orm模型(个人理解: 放行,不验证)

class Ecs_professorsDelete(BaseModel):
    """ 添加数据时的字段验证 """
    id: int = Field(...)

class Ecs_professorsType(BaseModel):
    id: int

class Ecs_professorsMenu(Ecs_professorsIn):
    """ 添加数据时的字段验证 """
    id: int = Field(...)