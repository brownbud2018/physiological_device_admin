#!/usr/bin/env python3
# _*_ coding: utf-8 _*_
# @Time : 2021/9/19 22:24
# @Author : wdm
# @desc : 项目表
from sqlalchemy import Column, Integer, String, TIMESTAMP, func, text, Boolean

from core import settings
from models import Base


class Excelupload(Base):
    """ Excel上传表 """
    id = Column(Integer, primary_key=True, autoincrement=True, index=True, comment='编号')

    excel_code = Column(String(20), server_default=text("'V7'"), index=True, comment='上传Excel代码')

    excel_name = Column(String(30), comment='上传Excel名称')

    excel_address = Column(String(60), server_default=text(f"'{settings.STATIC_DIR}/author.xlsx'"), comment='上传Excel地址')

    is_import = Column(Integer, default=0, comment='是否导入：0.未导入，1.已导入')

    excel_remark = Column(String(60), server_default=text(f"'这是上传Excel备注'"), comment='上传Excel备注')

    name = Column(String(20), server_default=text("'投影仪V7'"), comment='device名称')

    device_ota = Column(Integer, default=0, comment='device所属ota类ID')

    version = Column(String(20), server_default=text("'V7-1.0.1'"), comment='device版本/其它')

    product_id = Column(Integer, default=0, comment='device所属设备类ID')

    address = Column(String(60), server_default=text("'广东省深圳市'"), comment='device地址/其它备注')

    image = Column(String(60), server_default=text(f"'{settings.STATIC_DIR}/author.jpg'"), comment='device图标')

    is_active = Column(Integer, default=1, comment='是否激活')

    device_level = Column(Integer, default=0, comment='等级权限：0.普通等级，1.授权等级，2.VIP等级，3...')

    device_auth_class_id = Column(Integer, default=0, comment='device对应授权类属性ID：例如1.V7EN项目授权类1【测试样机】，2.V7EN项目授权类2【客户样机】，3.V7CN项目授权类1【第一批试产机器】，4...')

    hashed_password = Column(String(60), nullable=False, comment='密码')

    gmt_create = Column(TIMESTAMP(True), server_default=func.now(), comment='创建时间')

    gmt_modify = Column(TIMESTAMP(True), server_default=func.now(), onupdate=func.now(), comment='更新时间')
