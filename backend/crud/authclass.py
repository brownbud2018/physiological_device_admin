#!/usr/bin/env python3
# _*_ coding: utf-8 _*_
# @Time : 2021/10/28 19:01
# @Author : wdm
# @desc : 操作授权类表
from crud import CRUDBase
from models import Authclass
from schemas import AuthclassCreate, AuthclassUpdate


class CRUDAuthclass(CRUDBase[Authclass, AuthclassCreate, AuthclassUpdate]):
    pass


authclass = CRUDAuthclass(Authclass)
