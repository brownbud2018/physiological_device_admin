#!/usr/bin/env python3
# _*_ coding: utf-8 _*_
# @Time : 2021/9/19 22:24
# @Author : wdm
# @desc : 角色表
from sqlalchemy import Column, Integer, String, TIMESTAMP, func, text

from models import Base


class Role(Base):
    """ 项目表 """
    id = Column(Integer, primary_key=True, autoincrement=True, index=True, comment='编号')

    role_name = Column(String(30), comment='角色名称')

    role_status = Column(Integer, default=0, comment='角色启用：0.未启用，1.已启用')

    role_desc = Column(String(60), server_default=text(f"'这是角色描述'"), comment='角色描述')

    gmt_create = Column(TIMESTAMP(True), server_default=func.now(), comment='创建时间')

    gmt_modify = Column(TIMESTAMP(True), server_default=func.now(), onupdate=func.now(), comment='更新时间')
