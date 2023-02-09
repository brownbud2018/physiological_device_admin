#!/usr/bin/env python3
# _*_ coding: utf-8 _*_
# @Time : 2021/10/28 19:01
# @Author : wdm
# @desc : 操作Adminauthclass表
from crud import CRUDBase
from models import Adminauthclass
from schemas import AdminauthclassCreate, AdminauthclassUpdate


class CRUDAdminauthclass(CRUDBase[Adminauthclass, AdminauthclassCreate, AdminauthclassUpdate]):
    pass


adminauthclass = CRUDAdminauthclass(Adminauthclass)
