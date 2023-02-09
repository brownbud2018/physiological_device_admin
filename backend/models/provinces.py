#!/usr/bin/env python3
# _*_ coding: utf-8 _*_
# @Time : 2021/9/19 22:24
# @Author : wdm
# @desc : 省份列表
from sqlalchemy import Column, Integer, String, TIMESTAMP, func, text, Numeric, Boolean

from models import Base


class Provinces(Base):
    """ 省份列表 """
    id = Column(Integer, primary_key=True, autoincrement=True, index=True, comment='自增编号')

    provinceid = Column(String(20), server_default=text("'000000'"), index=True, comment='省份编号')

    province = Column(String(50), nullable=False, comment='省份名称')
