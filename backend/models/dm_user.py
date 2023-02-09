#!/usr/bin/env python3
# _*_ coding: utf-8 _*_
# @Time : 2021/9/19 22:24
# @Author : wdm
# @desc : 用户表
from sqlalchemy import Column, Integer, String, TIMESTAMP, func, Boolean, text, null

from core import settings
from models import Base


class Dm_user(Base):
    """ dm_user用户表 """
    id = Column(Integer, primary_key=True, autoincrement=True, index=True, comment='自增编号')

    name = Column(String(100), default=null, comment='用户名称')

    headicon = Column(String(200), default=null, comment='用户头像')

    age = Column(String(10), default=null, comment='用户年龄')

    sex = Column(String(10), default=null, comment='用户性别')

    deviceid = Column(String(50), default=null, comment='用户所属device编号')

    idcard = Column(String(20), default=null, comment='用户身份证号码')

    updatetime = Column(TIMESTAMP(True), server_default=func.now(), comment='修改时间')

    updatetimedate = Column(String(50), default=null, onupdate=func.now(), comment='修改日期')

    height = Column(String(10), default=null, comment='用户身高')

    weight = Column(String(10), default=null, comment='用户体重')

    cityid = Column(Integer, default=null, comment='用户城市ID')

    cityname = Column(String(100), default=null, comment='用户城市名称')

    phone = Column(String(20), default=null, comment='用户手机')

    bloodtypeid = Column(Integer, default=null, comment='用户血型ID')

    bloodtypename = Column(String(20), default=null, comment='用户血型名称')

    allergyid = Column(Integer, default=null, comment='用户过敏ID')

    allergyname = Column(String(50), default=null, comment='用户过敏名称')

    medicalid = Column(Integer, default=null, comment='用户基础疾病ID')

    medicalname = Column(String(20), default=null, comment='用户基础疾病名称')

    geneticid = Column(Integer, default=null, comment='用户遗传病ID')

    geneticname = Column(String(50), default=null, comment='用户遗传病名称')

    usergeneticname = Column(String(100), default=null, comment='用户遗传病')

    descr = Column(String(500), default='', comment='用户说明')

    createtime = Column(TIMESTAMP(True), server_default=func.now(), comment='创建时间')

    createtimedate = Column(String(50), default=func.now(), comment='创建日期')
