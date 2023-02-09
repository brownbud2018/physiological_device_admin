#!/usr/bin/env python3
# _*_ coding: utf-8 _*_
# @Time : 2021/10/28 19:01
# @Author : wdm
# @desc : 操作城市表
from crud import CRUDBase
from models import Cities
from schemas import CitiesCreate, CitiesUpdate


class CRUDCities(CRUDBase[Cities, CitiesCreate, CitiesUpdate]):
    pass


cities = CRUDCities(Cities)
