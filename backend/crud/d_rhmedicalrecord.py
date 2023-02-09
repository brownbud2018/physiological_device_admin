#!/usr/bin/env python3
# _*_ coding: utf-8 _*_
# @Time : 2021/10/28 19:01
# @Author : wdm
# @desc : 操作D_rhmedicalrecord病历记录表
from crud import CRUDBase
from models import D_rhmedicalrecord
from schemas import D_rhmedicalrecordCreate, D_rhmedicalrecordUpdate


class CRUDD_rhmedicalrecord(CRUDBase[D_rhmedicalrecord, D_rhmedicalrecordCreate, D_rhmedicalrecordUpdate]):
    pass


d_rhmedicalrecord = CRUDD_rhmedicalrecord(D_rhmedicalrecord)
