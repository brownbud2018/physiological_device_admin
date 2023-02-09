#!/usr/bin/env python3
# _*_ coding: utf-8 _*_
# @Time : 2021/9/19 22:24
# @Author : wdm
# @desc : APP版本表
from sqlalchemy import Column, Integer, String, TIMESTAMP, func, text

from core import settings
from models import Base


class Appversion(Base):
    """ APP版本 """
    id = Column(Integer, primary_key=True, autoincrement=True, index=True, comment='自增编号')

    app_v_code = Column(String(20), server_default=text("'APP版本编号'"), index=True, comment='APP版本编号')

    app_v_name = Column(String(30), nullable=False, comment='APP版本名称/版本标题')

    app_v_image = Column(String(60), server_default=text(f"'{settings.STATIC_DIR}/author.jpg'"), comment='APP版本图标')

    app_v_file = Column(String(60), server_default=text(f"'{settings.STATIC_DIR}/author.jpg'"), comment='APP版本文件地址')

    app_pro_id = Column(Integer, default=0, comment='APPProID：关联APPPro表')

    app_v_default = Column(Integer, default=0, comment='是否默认版本：0.非默认【历史版本】，1.默认【当前最新版本】。一个APP的所有版本中，仅允许一个版本是默认版本')

    app_v_remark = Column(String(60), server_default=text(f"'这是APP版本备注'"), comment='APP版本备注')

    gmt_create = Column(TIMESTAMP(True), server_default=func.now(), comment='创建时间')

    gmt_modify = Column(TIMESTAMP(True), server_default=func.now(), onupdate=func.now(), comment='更新时间')
