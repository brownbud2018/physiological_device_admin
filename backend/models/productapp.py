#!/usr/bin/env python3
# _*_ coding: utf-8 _*_
# @Time : 2021/9/19 22:24
# @Author : wdm
# @desc : APP Product关联表
from sqlalchemy import Column, Integer, TIMESTAMP, func

from models import Base


class Productapp(Base):
    """ APP版本 """
    id = Column(Integer, primary_key=True, autoincrement=True, index=True, comment='自增编号')

    prod_id = Column(Integer, default=0, comment='prod_id：关联Product表')

    app_pro_id = Column(Integer, default=0, comment='APPProID：关联APPPro表')

    gmt_create = Column(TIMESTAMP(True), server_default=func.now(), comment='创建时间')

    gmt_modify = Column(TIMESTAMP(True), server_default=func.now(), onupdate=func.now(), comment='更新时间')
