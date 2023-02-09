#!/usr/bin/env python3
# _*_ coding: utf-8 _*_
# @Time : 2021/10/28 19:01
# @Author : wdm
# @desc : 操作ecs_consulting_talklog用户咨询表
from crud import CRUDBase
from models import Ecs_Consulting_Talklog
from schemas import Ecs_Consulting_TalklogCreate, Ecs_Consulting_TalklogUpdate


class CRUDConsultingTalklog(CRUDBase[Ecs_Consulting_Talklog, Ecs_Consulting_TalklogCreate, Ecs_Consulting_TalklogUpdate]):
    pass


ecs_consulting_talklog = CRUDConsultingTalklog(Ecs_Consulting_Talklog)
