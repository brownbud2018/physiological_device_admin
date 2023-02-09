#!/usr/bin/env python3
# _*_ coding: utf-8 _*_
# @Time : 2021/10/28 19:01
# @Author : wdm
# @desc : 用户表
from crud import CRUDBase
from models import Dm_user
from schemas import Dm_userCreate, Dm_userUpdate


class CRUDDm_user(CRUDBase[Dm_user, Dm_userCreate, Dm_userUpdate]):
    pass


dm_user = CRUDDm_user(Dm_user)
