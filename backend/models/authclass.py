#!/usr/bin/env python3
# _*_ coding: utf-8 _*_
# @Time : 2021/9/19 22:24
# @Author : wdm
# @desc : Auth分类列表
from sqlalchemy import Column, Integer, String, TIMESTAMP, func, text, Numeric, BIGINT

from core import settings
from models import Base


class Authclass(Base):
    """ Auth分类列表 """
    id = Column(Integer, primary_key=True, autoincrement=True, index=True, comment='自增编号')

    class_code = Column(String(20), server_default=text("'V7EN001'"), index=True, comment='Auth类编号')

    class_name = Column(String(30), nullable=False, comment='Auth类名称/标题')

    class_image = Column(String(60), server_default=text(f"'{settings.STATIC_DIR}/author.jpg'"), comment='Auth类图标')

    class_desc = Column(String(60), server_default=text(f"'这是Auth类描述'"), comment='Auth类描述')

    class_remark = Column(String(60), server_default=text(f"'这是Auth类备注'"), comment='Auth类备注')

    gmt_create = Column(TIMESTAMP(True), server_default=func.now(), comment='创建时间')

    gmt_modify = Column(TIMESTAMP(True), server_default=func.now(), onupdate=func.now(), comment='更新时间')
