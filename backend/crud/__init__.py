#!/usr/bin/env python3
# _*_ coding: utf-8 _*_
# @Time : 2021/10/14 16:59
# @Author : wdm
# @desc : 数据库的增删改查操作(dao层)
from .base import ModelType, CRUDBase
from .access import access
from .accessrole import accessrole
from .admin import admin
from .adminauth import adminauthclass
from .appclass import appclass
from .apppro import apppro
from .appversion import appversion
from .authclass import authclass
from .authclassanddetail import authclassanddetail
from .authdetail import authdetail
from .cities import cities
from .d_question import d_question
from .d_rhmedicalrecord import d_rhmedicalrecord
from .device import device
from .devicelog import devicelog
from .dm_user import dm_user
from .dm_physique import dm_physique
from .ecs_consulting import ecs_consulting
from .ecs_consulting_talklog import ecs_consulting_talklog
from .ecs_professors import ecs_professors
from .excelupload import excelupload
from .otamain import otamain
from .otaversion import otaversion
from .product import product
from .productapp import productapp
from .provinces import provinces
from .project import project
from .role import role
from .statistics import statistics
