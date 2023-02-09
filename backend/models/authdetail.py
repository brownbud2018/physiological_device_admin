#!/usr/bin/env python3
# _*_ coding: utf-8 _*_
# @Time : 2021/9/19 22:24
# @Author : wdm
# @desc : Auth详情列表
from sqlalchemy import Column, Integer, String, TIMESTAMP, func, text, Numeric, BIGINT

from core import settings
from models import Base


class Authdetail(Base):
    """ Auth详情列表 """
    id = Column(Integer, primary_key=True, autoincrement=True, index=True, comment='自增编号')

    detail_code = Column(String(20), server_default=text("'V7ENDetial001'"), index=True, comment='Auth详情编号')

    detail_name = Column(String(30), nullable=False, comment='Auth详情名称/标题')

    detail_image = Column(String(60), server_default=text(f"'{settings.STATIC_DIR}/author.jpg'"), comment='Auth详情图标')

    detail_type = Column(Integer, default=0, comment='Auth详情属性：0.默认，1.特殊')

    detail_desc = Column(String(60), server_default=text(f"'这是Auth详情描述'"), comment='Auth详情描述')

    detail_remark = Column(String(60), server_default=text(f"'这是Auth详情备注'"), comment='Auth详情备注')

    gmt_create = Column(TIMESTAMP(True), server_default=func.now(), comment='创建时间')

    gmt_modify = Column(TIMESTAMP(True), server_default=func.now(), onupdate=func.now(), comment='更新时间')
