#!/usr/bin/env python3
# _*_ coding: utf-8 _*_
# @Time : 2021/9/19 22:24
# @Author : wdm
# @desc : 管理员表
from sqlalchemy import Column, Integer, String, TIMESTAMP, func, Boolean, text, ForeignKey

from core import settings
from models import Base


class Admin(Base):
    """ 管理员表 """
    id = Column(Integer, primary_key=True, autoincrement=True, index=True, comment='编号')

    name = Column(String(20), nullable=False, index=True, comment='用户名')

    nickname = Column(String(60), server_default=text("'新管理员'"), comment='昵称')

    role_id = Column(Integer, default=0, comment='关联角色ID')

    address = Column(String(60), server_default=text("'广东省深圳市'"), comment='地址')

    image = Column(String(60), server_default=text(f"'{settings.STATIC_DIR}/author.jpg'"), comment='头像')

    hashed_password = Column(String(60), nullable=False, comment='密码')

    is_active = Column(Boolean(), default=True, comment='是否登录')

    user_type = Column(Boolean(), default=False, comment='是否超级管理员')

    professor_id = Column(Integer, default=0, comment='关联医生ID')

    gmt_create = Column(TIMESTAMP(True), server_default=func.now(), comment='创建时间')

    gmt_modify = Column(TIMESTAMP(True), server_default=func.now(), onupdate=func.now(), comment='更新时间')
