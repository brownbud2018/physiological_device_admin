#!/usr/bin/env python3
# _*_ coding: utf-8 _*_
# @Time : 2021/10/28 19:01
# @Author : wdm
# @desc : 操作statistics统计表
from crud import CRUDBase
from models import Statistics
from schemas import StatisticsCreate, StatisticsUpdate


class CRUDStatistics(CRUDBase[Statistics, StatisticsCreate, StatisticsUpdate]):
    pass


statistics = CRUDStatistics(Statistics)
