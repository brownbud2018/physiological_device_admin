#!/usr/bin/env python3
# _*_ coding: utf-8 _*_
# @Time : 2021/9/19 22:24
# @Author : wdm
# @desc : D_rhmedicalrecord关联表
from sqlalchemy import Column, Integer, String

from models import Base


class D_rhmedicalrecord(Base):
    """ D_rhmedicalrecord """
    id = Column(Integer, primary_key=True, autoincrement=True, index=True, comment='自增编号')

    dmuserid = Column(Integer, default=0, comment='设备用户id')

    url = Column(String(500), nullable=False, index=True, comment='病历上传图片地址（逗号分割上传多张图片）')

    recordid = Column(Integer, default=0, comment='检测项目Id')

    recordname = Column(String(50), nullable=False, index=True, comment='检测项目名')

    deviceid = Column(String(50), nullable=False, index=True, comment='设备编号')

    descr = Column(String(500), nullable=False, index=True, comment='病历描述说明')
