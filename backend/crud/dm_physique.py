#!/usr/bin/env python3
# _*_ coding: utf-8 _*_
# @Time : 2021/10/28 19:01
# @Author : wdm
# @desc : 操作consulting用户咨询表
from crud import CRUDBase
from models import Dm_physique
from schemas import Dm_physiqueCreate, Dm_physiqueUpdate


class CRUDConsulting(CRUDBase[Dm_physique, Dm_physiqueCreate, Dm_physiqueUpdate]):
    pass


dm_physique = CRUDConsulting(Dm_physique)
