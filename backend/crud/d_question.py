#!/usr/bin/env python3
# _*_ coding: utf-8 _*_
# @Time : 2021/10/28 19:01
# @Author : wdm
# @desc : 操作D_question病历记录表
from crud import CRUDBase
from models import D_question
from schemas import D_questionCreate, D_questionUpdate


class CRUDD_question(CRUDBase[D_question, D_questionCreate, D_questionUpdate]):
    pass


d_question = CRUDD_question(D_question)
