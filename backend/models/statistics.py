#!/usr/bin/env python3
# _*_ coding: utf-8 _*_
# @Time : 2021/9/19 22:24
# @Author : wdm
# @desc : 统计表
from sqlalchemy import Column, Integer, String, TIMESTAMP, func, text, BIGINT

from core import settings
from models import Base


class Statistics(Base):
    """ 统计型表 """
    id = Column(Integer, primary_key=True, autoincrement=True, index=True, comment='自增编号')

    stat_code = Column(String(20), server_default=text("'S001'"), index=True, comment='统计代码')

    stat_name = Column(String(30), nullable=False, comment='统计名称')

    prod_id = Column(Integer, default=0, comment='统计所属设备类ID')

    stat_num = Column(BIGINT, default=0, comment='功能或APP使用次数')

    stat_remark = Column(String(60), server_default=text(f"'这是统计备注'"), comment='统计备注')

    gmt_create = Column(TIMESTAMP(True), server_default=func.now(), comment='创建时间')

    gmt_modify = Column(TIMESTAMP(True), server_default=func.now(), onupdate=func.now(), comment='更新时间')
