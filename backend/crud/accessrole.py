#!/usr/bin/env python3
# _*_ coding: utf-8 _*_
# @Time : 2021/10/28 19:01
# @Author : wdm
# @desc : 操作Accessrole表
from crud import CRUDBase
from models import Accessrole
from schemas import AccessroleCreate, AccessroleUpdate


class CRUDAccessrole(CRUDBase[Accessrole, AccessroleCreate, AccessroleUpdate]):
    pass


accessrole = CRUDAccessrole(Accessrole)
