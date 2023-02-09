#!/usr/bin/env python3
# _*_ coding: utf-8 _*_
# @Time : 2021/10/28 19:01
# @Author : wdm
# @desc : 操作院系表
from crud import CRUDBase
from models import Appversion
from schemas import AppversionCreate, AppversionUpdate


class CRUDAppversion(CRUDBase[Appversion, AppversionCreate, AppversionUpdate]):
    pass


appversion = CRUDAppversion(Appversion)
