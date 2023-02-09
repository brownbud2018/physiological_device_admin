#!/usr/bin/env python3
# _*_ coding: utf-8 _*_
# @Time : 2021/10/28 19:01
# @Author : wdm
# @desc : 操作productapp表
from crud import CRUDBase
from models import Productapp
from schemas import ProductappCreate, ProductappUpdate


class CRUDProductapp(CRUDBase[Productapp, ProductappCreate, ProductappUpdate]):
    pass


productapp = CRUDProductapp(Productapp)
