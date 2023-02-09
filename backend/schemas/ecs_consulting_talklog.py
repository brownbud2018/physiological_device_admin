#!/usr/bin/env python3
# _*_ coding: utf-8 _*_
# @Time : 2021/9/22 9:59
# @Author : wdm
# @desc : consulting 关系表模型
from typing import Optional
from pydantic import BaseModel, Field

from schemas import GMT


class Ecs_Consulting_TalklogIn(BaseModel):
    """ 共享模型字段 """
    id: int = Field(...)

class Ecs_Consulting_TalklogCreate(BaseModel):
    """ 添加数据时的字段验证 """
    id: int = Field(...)
    consulting_id: int = Field(...)
    reply_type: int = Field(...)
    reply_uid: str = Field(example='回复设备ID、用户ID、医生ID')
    content_type: str = Field(example='类型（TEXT文字，IMAGE图片，AUDIO音频，VIDEO视频）')
    content: str = Field(example='内容')

class Ecs_Consulting_TalklogUpdate(Ecs_Consulting_TalklogIn):
    """ 更新数据的字段验证 """
    pass


class Ecs_Consulting_TalklogOut(Ecs_Consulting_TalklogCreate):
    """ 查询数据的字段验证 """

    class Config:
        orm_mode = True  # 是否使用orm模型(个人理解: 放行,不验证)

class Ecs_Consulting_TalklogDelete(BaseModel):
    """ 添加数据时的字段验证 """
    id: int = Field(...)
