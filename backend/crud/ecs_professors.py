#!/usr/bin/env python3
# _*_ coding: utf-8 _*_
# @Time : 2021/10/28 19:01
# @Author : wdm
# @desc : ecs_professors表【医生表】
from crud import CRUDBase
from models import Ecs_professors
from schemas import Ecs_professorsCreate, Ecs_professorsUpdate


class CRUDEcs_professors(CRUDBase[Ecs_professors, Ecs_professorsCreate, Ecs_professorsUpdate]):
    pass


ecs_professors = CRUDEcs_professors(Ecs_professors)
