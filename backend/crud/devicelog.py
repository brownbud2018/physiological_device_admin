#!/usr/bin/env python3
# _*_ coding: utf-8 _*_
# @Time : 2021/10/28 19:01
# @Author : wdm
# @desc : 操作devicelog表
from crud import CRUDBase
from models import Devicelog
from schemas import DevicelogCreate, DevicelogUpdate


class CRUDDevicelog(CRUDBase[Devicelog, DevicelogCreate, DevicelogUpdate]):
    pass


devicelog = CRUDDevicelog(Devicelog)
