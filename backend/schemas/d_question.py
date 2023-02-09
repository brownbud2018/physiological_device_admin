#!/usr/bin/env python3
# _*_ coding: utf-8 _*_
# @Time : 2021/9/22 9:59
# @Author : wdm
# @desc : d_question 关系表模型
from pydantic import BaseModel, Field

class D_questionIn(BaseModel):
    """ 共享模型字段 """
    id: int = Field(...)

class D_questionCreate(BaseModel):
    """ 添加数据时的字段验证 """
    id: int = Field(...)
    title: str = Field(example='问卷标题')
    seq: int = Field(...)
    isopen: str = Field(example='0:关闭 1：开启')

class D_questionUpdate(D_questionIn):
    """ 更新数据的字段验证 """
    pass


class D_questionOut(D_questionCreate):
    """ 查询数据的字段验证 """

    class Config:
        orm_mode = True  # 是否使用orm模型(个人理解: 放行,不验证)

class D_questionDelete(BaseModel):
    """ 添加数据时的字段验证 """
    id: int = Field(...)
