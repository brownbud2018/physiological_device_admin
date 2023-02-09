#!/usr/bin/env python3
# _*_ coding: utf-8 _*_
# @Time : 2021/9/19 22:24
# @Author : wdm
# @desc : Consulting关联表
from sqlalchemy import Column, Integer, TIMESTAMP, func, Numeric, String

from models import Base


class Dm_physique(Base):
    """ Consulting """
    id = Column(Integer, primary_key=True, autoincrement=True, index=True, comment='自增编号')

    dmuserid = Column(Integer, default=0, comment='用户ID：关联dm_user表')

    dmusername = Column(String(200), nullable=False, index=True, comment='用户名：关联dm_user表')

    hint = Column(String(200),  nullable=False, index=True, comment='温馨提示')

    physique = Column(String(200), nullable=False, index=True, comment='体质辨识数据')

    createtime = Column(TIMESTAMP(True), server_default=func.now(), comment='创建时间')

    createtimedate = Column(String(50), default=func.now(), comment='创建日期')
