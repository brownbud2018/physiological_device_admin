#!/usr/bin/env python3
# _*_ coding: utf-8 _*_
# @Time : 2021/9/19 22:24
# @Author : wdm
# @desc : 项目表
from sqlalchemy import Column, Integer, String, TIMESTAMP, func, text

from core import settings
from models import Base


class Product(Base):
    """ 设备类型表 """
    id = Column(Integer, primary_key=True, autoincrement=True, index=True, comment='自增编号')

    prod_code = Column(String(20), server_default=text("'V7-EN'"), index=True, comment='设备类代码')

    prod_name = Column(String(30), nullable=False, comment='设备类名称')

    prod_image = Column(String(60), server_default=text(f"'{settings.STATIC_DIR}/author.jpg'"), comment='设备类图标')

    project_id = Column(Integer, default=0, comment='设备类所属项目ID')

    prod_remark = Column(String(60), server_default=text(f"'这是设备类备注'"), comment='设备类备注')

    gmt_create = Column(TIMESTAMP(True), server_default=func.now(), comment='创建时间')

    gmt_modify = Column(TIMESTAMP(True), server_default=func.now(), onupdate=func.now(), comment='更新时间')
