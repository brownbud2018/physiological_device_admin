#!/usr/bin/env python3
# _*_ coding: utf-8 _*_
# @Time : 2021/9/19 22:24
# @Author : wdm
# @desc : 医生表
from sqlalchemy import Column, Integer, String, TIMESTAMP, func, text

from models import Base


class Ecs_professors(Base):
    """ 项目表 """
    professor_id = Column(Integer, primary_key=True, autoincrement=True, index=True, comment='编号')

    name = Column(String(60), comment='医生名字')

    email = Column(String(60), server_default=text(f"'email'"), comment='email')

    sex = Column(Integer, default=0, comment='性别：1.男，2.女')

    title = Column(String(255), comment='职称')

    expert = Column(String(255), comment='擅长领域')

    education = Column(String(255), comment='教育背景')

    phone = Column(String(255), comment='电话')

    avatar = Column(String(255), comment='头像')

    address = Column(String(255), comment='地址')

    remark = Column(String(255), comment='备注')

    resume = Column(String(1000), comment='专家简介')

    reg_time = Column(Integer, default=0, comment='注册时间戳')

    cat_id = Column(Integer, default=0, comment='专家分类')

    clinic_name = Column(String(100), comment='所属科室')

    hospital = Column(String(100), comment='所属医院')

    hospital_grade = Column(String(100), comment='所属医院分级')

    source = Column(String(20), comment='来源')

    source_id = Column(String(100), comment='第三方ID')

    recommend_rate = Column(Integer, default=50, comment='推荐指数')

    solution_score = Column(Integer, default=50, comment='专业度指数')

    good_rate = Column(Integer, default=80, comment='好评率')

    reply_num = Column(Integer, default=0, comment='咨询数')
