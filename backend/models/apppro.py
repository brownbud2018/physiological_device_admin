#!/usr/bin/env python3
# _*_ coding: utf-8 _*_
# @Time : 2021/9/19 22:24
# @Author : wdm
# @desc : APP表
from sqlalchemy import Column, Integer, String, TIMESTAMP, func, text, Numeric, BIGINT

from core import settings
from models import Base


class Apppro(Base):
    """ APP列表 """
    id = Column(Integer, primary_key=True, autoincrement=True, index=True, comment='自增编号')

    app_code = Column(String(20), server_default=text("'wechat'"), index=True, comment='APP编号')

    app_name = Column(String(30), nullable=False, comment='APP名称/标题')

    app_image = Column(String(60), server_default=text(f"'{settings.STATIC_DIR}/author.jpg'"), comment='APP图标')

    app_package = Column(String(60), server_default=text(f"'com.tencent.mm'"), comment='APP包名')

    app_type = Column(Integer, default=0, comment='APP属性：0.应用市场，1.内置应用')

    app_update_type = Column(Integer, default=0, comment='APP更新属性：0.非强制更新，1.强制更新【静默更新】')

    app_class_id = Column(Integer, default=0, comment='APP分类：关联APP分类表ID')

    app_info = Column(String(60), server_default=text(f"'这是APP简介'"), comment='APP简介')

    app_score = Column(Numeric(11,1), default=0.0, comment='APP评分：0~5分')

    app_download_amount = Column(BIGINT, default=0, comment='APP下载次数')

    app_company = Column(String(60), server_default=text(f"'深圳吉祥星'"), comment='APP开发公司')

    app_desc = Column(String(60), server_default=text(f"'这是APP描述'"), comment='APP描述')

    app_remark = Column(String(60), server_default=text(f"'这是APP备注'"), comment='APP备注')

    gmt_create = Column(TIMESTAMP(True), server_default=func.now(), comment='创建时间')

    gmt_modify = Column(TIMESTAMP(True), server_default=func.now(), onupdate=func.now(), comment='更新时间')
