#!/usr/bin/env python3
# _*_ coding: utf-8 _*_
# @Time : 2021/10/28 19:01
# @Author : wdm
# @desc : 操作省份表
from crud import CRUDBase
from models import Provinces
from schemas import ProvincesCreate, ProvincesUpdate


class CRUDProvinces(CRUDBase[Provinces, ProvincesCreate, ProvincesUpdate]):
    pass


provinces = CRUDProvinces(Provinces)
