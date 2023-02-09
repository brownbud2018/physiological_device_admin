#!/usr/bin/env python3
# _*_ coding: utf-8 _*_
# @Time : 2021/10/28 19:01
# @Author : wdm
# @desc : 操作Authclassanddetail表
from crud import CRUDBase
from models import Authclassanddetail
from schemas import AuthclassanddetailCreate, AuthclassanddetailUpdate


class CRUDAuthclassanddetail(CRUDBase[Authclassanddetail, AuthclassanddetailCreate, AuthclassanddetailUpdate]):
    pass


authclassanddetail = CRUDAuthclassanddetail(Authclassanddetail)
