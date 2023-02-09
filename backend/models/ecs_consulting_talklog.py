#!/usr/bin/env python3
# _*_ coding: utf-8 _*_
# @Time : 2021/9/19 22:24
# @Author : wdm
# @desc : Ecs_Consulting_Talklog关联表
from sqlalchemy import Column, Integer, TIMESTAMP, func, Numeric, String

from models import Base


class Ecs_Consulting_Talklog(Base):
    """ Ecs_Consulting_Talklog """
    id = Column(Integer, primary_key=True, autoincrement=True, index=True, comment='自增编号')

    consulting_id = Column(Integer, default=0, comment='咨询主ID')

    reply_type = Column(Integer, default=0, comment='1用户，2医生')

    reply_uid = Column(String(100), nullable=False, index=True, comment='回复设备ID、用户ID、医生ID')

    add_time = Column(Integer, default=0, comment='提交时间')

    content_type = Column(String(20), nullable=False, index=True, comment='类型（TEXT文字，IMAGE图片，AUDIO音频，VIDEO视频）')

    content = Column(String(255), nullable=False, index=True, comment='内容')

    status = Column(Integer, default=0, comment='是否已读')
