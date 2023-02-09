#!/usr/bin/env python3
# _*_ coding: utf-8 _*_
# @Time : 2021/9/19 17:14
# @Author : wdm
# @desc : 封装 ORM父类 的函数
from typing import Any

from sqlalchemy.ext.declarative import as_declarative, declared_attr

from sqlalchemy.ext.declarative import declarative_base

myBase = declarative_base()

@as_declarative()
class Base:
    id: Any
    __name__: str
    # 设置表的字符集
    __table_args__ = {"mysql_charset": "utf8"}

    # 将类名小写并转化为表名 __tablename__
    @declared_attr
    def __tablename__(cls) -> str:
        return cls.__name__.lower()
