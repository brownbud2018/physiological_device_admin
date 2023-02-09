#!/usr/bin/env python3
# _*_ coding: utf-8 _*_
# @Time : 2021/9/19 22:24
# @Author : wdm
# @desc : Consulting关联表
from sqlalchemy import Column, Integer, TIMESTAMP, func, Numeric, String

from models import Base


class Ecs_Consulting(Base):
    """ Consulting """
    id = Column(Integer, primary_key=True, autoincrement=True, index=True, comment='自增编号')

    device_id = Column(String(100), nullable=False, index=True, comment='device_id：关联device表')

    type = Column(Integer, default=0, comment='咨询类型（10健康辅导，20付费咨询）')

    leaguer_id = Column(String(100), nullable=False, index=True, comment='成员ID：关联dm_user表')

    content = Column(String(200), nullable=False, index=True, comment='内容')

    image = Column(String(200), nullable=False, index=True, comment='图片地址')

    doctor_type = Column(Integer, default=0, comment='医生类型（1后台，2第三方分配，3自选）')

    doctor_id = Column(Integer, default=0, comment='医生ID（后台，第三方不同区别）')

    add_time = Column(Integer, default=0, comment='提交时间')

    status = Column(Integer, default=0, comment='状态（0待医生接入，1待医生回复，2医生已回复，5完结）')

    price = Column(Numeric, default=0.00, comment='付款金额')

    is_payed = Column(Integer, default=0, comment='是否已付款')

    payed_time = Column(Integer, default=0, comment='付款时间')

    payed_type = Column(String(50), nullable=False, index=True, comment='付款方式')

    payed_sn = Column(String(255), nullable=False, index=True, comment='付款流水号')

    end_time = Column(Integer, default=0, comment='咨询截止时间')

    max_reply_count = Column(Integer, default=0, comment='回复次数上限')

    last_reply_time = Column(Integer, default=0, comment='最后一次回复时间')

    last_reply_content = Column(String(255), nullable=False, index=True, comment='最后一次回复内容')

    last_reply_status = Column(Integer, default=0, comment='最后一次回复已读')

    cyss_problem_id = Column(String(100), nullable=False, index=True, comment='春雨医生问题编号')

    close_type = Column(Integer, default=0, comment='关闭类型：0.未关闭，1.医生关闭，2.用户关闭，3.超过24小时关闭，4.20次回复后自动关闭')

    close_id = Column(Integer, default=0, comment='关闭ID：0.未关闭，int值对应：A.管理员id，B.用户id，C.24小时关闭=99，D.20次回复=999')
