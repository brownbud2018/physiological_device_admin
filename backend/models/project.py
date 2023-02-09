#!/usr/bin/env python3
# _*_ coding: utf-8 _*_
# @Time : 2021/9/19 22:24
# @Author : wdm
# @desc : 项目表
from sqlalchemy import Column, Integer, String, TIMESTAMP, func, text

from core import settings
from models import Base


class Project(Base):
    """ 项目表 """
    id = Column(Integer, primary_key=True, autoincrement=True, index=True, comment='编号')

    pro_code = Column(String(20), server_default=text("'V7'"), index=True, comment='项目代码')

    pro_name = Column(String(30), comment='项目名称')

    pro_image = Column(String(60), server_default=text(f"'{settings.STATIC_DIR}/author.jpg'"), comment='项目图标')

    pro_type = Column(Integer, default=0, comment='项目类型：0.测试项目，1.正式项目')

    pro_remark = Column(String(60), server_default=text(f"'这是项目备注'"), comment='项目备注')

    gmt_create = Column(TIMESTAMP(True), server_default=func.now(), comment='创建时间')

    gmt_modify = Column(TIMESTAMP(True), server_default=func.now(), onupdate=func.now(), comment='更新时间')
