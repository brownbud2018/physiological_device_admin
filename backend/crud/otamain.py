#!/usr/bin/env python3
# _*_ coding: utf-8 _*_
# @Time : 2021/10/28 19:01
# @Author : wdm
# @desc : 操作院系表
from crud import CRUDBase
from models import Otamain
from schemas import OtamainCreate, OtamainUpdate


class CRUDOtamain(CRUDBase[Otamain, OtamainCreate, OtamainUpdate]):
    pass


otamain = CRUDOtamain(Otamain)
