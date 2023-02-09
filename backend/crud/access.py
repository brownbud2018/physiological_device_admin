#!/usr/bin/env python3
# _*_ coding: utf-8 _*_
# @Time : 2021/10/28 19:01
# @Author : wdm
# @desc : 操作院系表
from crud import CRUDBase
from models import Access
from schemas import AccessCreate, AccessUpdate


class CRUDAccess(CRUDBase[Access, AccessCreate, AccessUpdate]):
    pass


access = CRUDAccess(Access)
