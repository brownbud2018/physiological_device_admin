#!/usr/bin/env python3
# _*_ coding: utf-8 _*_
# @Time : 2021/9/22 9:59
# @Author : wdm
# @desc : consulting 关系表模型
from typing import Optional
from pydantic import BaseModel, Field

from schemas import GMT


class Ecs_ConsultingIn(BaseModel):
    """ 共享模型字段 """
    id: int = Field(...)

class Ecs_ConsultingCreate(Ecs_ConsultingIn):
    """ 添加数据时的字段验证 """
    id: int = Field(...)


class Ecs_ConsultingUpdate(Ecs_ConsultingIn):
    """ 更新数据的字段验证 """
    pass


class Ecs_ConsultingOut(Ecs_ConsultingCreate):
    """ 查询数据的字段验证 """

    class Config:
        orm_mode = True  # 是否使用orm模型(个人理解: 放行,不验证)

class Ecs_ConsultingDelete(BaseModel):
    """ 添加数据时的字段验证 """
    id: int = Field(...)
