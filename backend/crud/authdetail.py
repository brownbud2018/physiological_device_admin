#!/usr/bin/env python3
# _*_ coding: utf-8 _*_
# @Time : 2021/10/28 19:01
# @Author : wdm
# @desc : 操作授权类表
from crud import CRUDBase
from models import Authdetail
from schemas import AuthdetailCreate, AuthdetailUpdate


class CRUDAuthdetail(CRUDBase[Authdetail, AuthdetailCreate, AuthdetailUpdate]):
    pass


authdetail = CRUDAuthdetail(Authdetail)
