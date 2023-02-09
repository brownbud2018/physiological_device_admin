#!/usr/bin/env python3
# _*_ coding: utf-8 _*_
# @Time : 2021/9/19 22:24
# @Author : wdm
# @desc : OTA表
from sqlalchemy import Column, Integer, String, TIMESTAMP, func, text, Numeric, BIGINT

from core import settings
from models import Base


class Otamain(Base):
    """ OTA列表 """
    id = Column(Integer, primary_key=True, autoincrement=True, index=True, comment='自增编号')

    ota_code = Column(String(20), server_default=text("'OTA_EN'"), index=True, comment='OTA编号')

    ota_name = Column(String(30), nullable=False, comment='OTA名称/标题')

    ota_image = Column(String(60), server_default=text(f"'{settings.STATIC_DIR}/author.jpg'"), comment='OTA图标')

    ota_package = Column(String(60), server_default=text(f"'com.luckystar.v7enota'"), comment='OTA包名')

    ota_type = Column(Integer, default=0, comment='OTA属性：0.非内置，1.内置应用')

    ota_update_type = Column(Integer, default=0, comment='OTA更新属性：0.非强制，1.强制更新【静默更新】')

    ota_info = Column(String(60), server_default=text(f"'这是OTA简介'"), comment='OTA简介')

    ota_score = Column(Numeric(11,1), default=0.0, comment='OTA评分：0~5分')

    ota_download_amount = Column(BIGINT, default=0, comment='OTA下载次数')

    ota_company = Column(String(60), server_default=text(f"'深圳吉祥星'"), comment='OTA开发公司')

    ota_desc = Column(String(60), server_default=text(f"'这是OTA描述'"), comment='OTA描述')

    ota_remark = Column(String(60), server_default=text(f"'这是OTA备注'"), comment='OTA备注')

    gmt_create = Column(TIMESTAMP(True), server_default=func.now(), comment='创建时间')

    gmt_modify = Column(TIMESTAMP(True), server_default=func.now(), onupdate=func.now(), comment='更新时间')
