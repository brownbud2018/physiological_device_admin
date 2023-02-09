#!/usr/bin/env python3
# _*_ coding: utf-8 _*_
# @Time : 2021/9/19 22:24
# @Author : wdm
# @desc : Devicelog关联表
from sqlalchemy import Column, Integer, TIMESTAMP, func, text, String

from core import settings
from models import Base


class Devicelog(Base):
    """ Devicelog """
    id = Column(Integer, primary_key=True, autoincrement=True, index=True, comment='自增编号')

    log_code = Column(String(20), nullable=False, index=True, comment='log编号')

    device_id = Column(Integer, default=0, comment='device_id：关联Device表')

    log_image = Column(String(60), server_default=text(f"'{settings.STATIC_DIR}/author.jpg'"), comment='log文件地址')

    gmt_create = Column(TIMESTAMP(True), server_default=func.now(), comment='创建时间')

    gmt_modify = Column(TIMESTAMP(True), server_default=func.now(), onupdate=func.now(), comment='更新时间')
