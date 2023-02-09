#!/usr/bin/env python3
# _*_ coding: utf-8 _*_
# @Time : 2021/9/19 22:24
# @Author : wdm
# @desc : D_question关联表
from sqlalchemy import Column, Integer, String

from models import Base


class D_question(Base):
    """ D_question """
    id = Column(Integer, primary_key=True, autoincrement=True, index=True, comment='自增编号')

    title = Column(String(30), nullable=False, index=True, comment='问卷标题')

    seq = Column(Integer, default=0, comment='序列')

    isopen = Column(String(5), nullable=False, index=True, comment='0:关闭 1：开启')
