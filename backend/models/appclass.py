#!/usr/bin/env python3
# _*_ coding: utf-8 _*_
# @Time : 2021/9/19 22:24
# @Author : wdm
# @desc : APP分类表
from sqlalchemy import Column, Integer, String, TIMESTAMP, func, text, Numeric, BIGINT

from core import settings
from models import Base


class Appclass(Base):
    """ APP分类列表 """
    id = Column(Integer, primary_key=True, autoincrement=True, index=True, comment='自增编号')

    class_code = Column(String(20), server_default=text("'wechat'"), index=True, comment='APP编号')

    class_name = Column(String(30), nullable=False, comment='APP名称/标题')

    class_image = Column(String(60), server_default=text(f"'{settings.STATIC_DIR}/author.jpg'"), comment='APP图标')

    class_desc = Column(String(60), server_default=text(f"'这是APP描述'"), comment='APP描述')

    class_remark = Column(String(60), server_default=text(f"'这是APP备注'"), comment='APP备注')

    gmt_create = Column(TIMESTAMP(True), server_default=func.now(), comment='创建时间')

    gmt_modify = Column(TIMESTAMP(True), server_default=func.now(), onupdate=func.now(), comment='更新时间')
