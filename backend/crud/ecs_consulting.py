#!/usr/bin/env python3
# _*_ coding: utf-8 _*_
# @Time : 2021/10/28 19:01
# @Author : wdm
# @desc : 操作consulting用户咨询表
from crud import CRUDBase
from models import Ecs_Consulting
from schemas import Ecs_ConsultingCreate, Ecs_ConsultingUpdate


class CRUDConsulting(CRUDBase[Ecs_Consulting, Ecs_ConsultingCreate, Ecs_ConsultingUpdate]):
    pass


ecs_consulting = CRUDConsulting(Ecs_Consulting)
