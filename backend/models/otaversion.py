#!/usr/bin/env python3
# _*_ coding: utf-8 _*_
# @Time : 2021/9/19 22:24
# @Author : wdm
# @desc : OTA表
from sqlalchemy import Column, Integer, String, TIMESTAMP, func, text, Numeric, BIGINT

from core import settings
from models import Base


class Otaversion(Base):
    """ OTA列表 """
    id = Column(Integer, primary_key=True, autoincrement=True, index=True, comment='自增编号')

    ota_v_code = Column(String(20), server_default=text("'wechat8.0.21'"), index=True, comment='OTA版本编号')

    ota_v_name = Column(String(30), nullable=False, comment='OTA版本名称/版本标题')

    ota_v_image = Column(String(60), server_default=text(f"'{settings.STATIC_DIR}/author.jpg'"), comment='OTA版本图标')

    ota_v_file = Column(String(120), server_default=text(f"'{settings.STATIC_DIR}/apk/2022/wechat8.0.21.apk'"), comment='OTA版本文件地址')

    ota_v_md5 = Column(String(60), default='', comment='OTA md5校验')

    ota_v_updateInfo = Column(String(120), default='', comment='OTA 更新包信息展示')

    ota_main_id = Column(Integer, default=0, comment='OTAMainID：关联OTAMain表')

    ota_v_default = Column(Integer, default=0, comment='是否默认版本：0.非默认【历史版本】，1.默认【当前最新版本】。一个OTA的所有版本中，仅允许一个版本是默认版本')

    ota_v_remark = Column(String(60), server_default=text(f"'这是OTA版本备注'"), comment='OTA版本备注')

    gmt_create = Column(TIMESTAMP(True), server_default=func.now(), comment='创建时间')

    gmt_modify = Column(TIMESTAMP(True), server_default=func.now(), onupdate=func.now(), comment='更新时间')
