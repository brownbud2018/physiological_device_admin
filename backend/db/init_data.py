#!/usr/bin/env python3
# _*_ coding: utf-8 _*_
# @Time : 2021/9/25 20:50
# @Author : wdm
# @desc : 两种初始化表数据的方式(添加的数据均没有验证类型)
from db import DBSession
from db.data import *
from models import *
from utils import logger
from utils.permission_assign import generate_permission_data


def db_conn(func):
    """ 连接数据库的装饰器 """

    def run():
        db = DBSession()  # 创建连接会话
        try:
            func(db)  # 运行sql语句
            db.commit()  # 提交事务
        except Exception as e:
            db.rollback()  # 如果出现错误，回滚事务
            logger.warning(f"运行时{str(func(db))}时出现错误，错误代码: \n{e}")  # 打印报错信息
        finally:
            db.close()  # 关闭数据库连接

    return run


@db_conn
def sqlalchemy_orm_initial(db):
    """ 初始化表数据方式一 : 速度欠佳 性能正常 """

    data = [
        *[Permission(**permission) for permission in generate_permission_data()],
        *[Admin(**admin) for admin in adminData],
        *[Device(**device) for device in deviceData],
        *[Project(**project) for project in projectData],
        *[Product(**product) for product in productData],
        *[Otamain(**otamain) for otamain in otamainData],
        *[Otaversion(**otaversion) for otaversion in otaversionData],
        *[Authclass(**authclass) for authclass in authclassData],
        *[Authdetail(**authdetail) for authdetail in authdetailData],
        *[Authclassanddetail(**authclassanddetail) for authclassanddetail in authclassanddetailData],
        *[Devicelog(**devicelog) for devicelog in devicelogData],
        *[Statistics(**statistics) for statistics in statisticsData],
        *[Excelupload(**excelupload) for excelupload in exceluploadData],
    ]
    # db.add_all(data)
    db.bulk_save_objects(data)
    logger.info("成功初始化所有表数据！！！")


@db_conn
def sqlalchemy_core_initial(db):
    """ 初始化表数据方式二 : 速度与性能并行 """

    # 插入数据
    db.execute(Permission.__table__.insert(), [permission for permission in generate_permission_data()]),
    db.execute(Admin.__table__.insert(), [admin for admin in adminData]),
    db.execute(Device.__table__.insert(), [device for device in deviceData]),
    db.execute(Project.__table__.insert(), [project for project in projectData]),
    db.execute(Product.__table__.insert(), [product for product in productData]),
    db.execute(Otamain.__table__.insert(), [otamain for otamain in otamainData]),
    db.execute(Otaversion.__table__.insert(), [otaversion for otaversion in otaversionData]),
    db.execute(Authclass.__table__.insert(), [authclass for authclass in authclassData]),
    db.execute(Authdetail.__table__.insert(), [authdetail for authdetail in authdetailData]),
    db.execute(Authclassanddetail.__table__.insert(), [authclassanddetail for authclassanddetail in authclassanddetailData]),
    db.execute(Devicelog.__table__.insert(), [devicelog for devicelog in devicelogData]),
    db.execute(Statistics.__table__.insert(), [statistics for statistics in statisticsData]),
    db.execute(Excelupload.__table__.insert(), [excelupload for excelupload in exceluploadData]),

    logger.info("成功初始化所有表数据！！！")
