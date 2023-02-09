#!/usr/bin/env python3
# _*_ coding: utf-8 _*_
# @Time : 2021/9/19 22:24
# @Author : wdm
# @desc : Auth分类列表
from sqlalchemy import Column, Integer, String, TIMESTAMP, func, text, Numeric, Boolean

from core import settings
from models import Base


class Access(Base):
    """ Auth分类列表 """
    id = Column(Integer, primary_key=True, autoincrement=True, index=True, comment='自增编号')

    access_code = Column(String(50), server_default=text("'newAccess'"), index=True, comment='Access编号')

    access_name = Column(String(30), nullable=False, comment='Access名称/标题')

    access_path = Column(String(60), server_default=text("/path"), comment='目录')

    access_redirect = Column(String(60), server_default=text("/path/path_redirect"), comment='详细路径')

    access_component = Column(String(60), server_default=text("LAYOUT"), comment='路由')

    sort_order = Column(Integer, default=0, comment='排序')

    menu_icon = Column(String(60), server_default=text(""), comment='菜单图标')

    parent_id = Column(Integer, default=0, comment='父ID')

    access_image = Column(String(60), server_default=text(f"'{settings.STATIC_DIR}/author.jpg'"), comment='Access图标')

    is_check = Column(Boolean(), default=True, comment='是否验证权限 True为验证 False不验证')

    is_menu = Column(Boolean(), default=False, comment='是否为菜单 True菜单 False不是菜单')

    access_desc = Column(String(60), server_default=text(f"'这是Access描述'"), comment='Access描述')

    access_remark = Column(String(60), server_default=text(f"'这是Access备注'"), comment='Access备注')

    gmt_create = Column(TIMESTAMP(True), server_default=func.now(), comment='创建时间')

    gmt_modify = Column(TIMESTAMP(True), server_default=func.now(), onupdate=func.now(), comment='更新时间')
