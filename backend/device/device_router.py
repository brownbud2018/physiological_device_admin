#!/usr/bin/env python3
# _*_ coding: utf-8 _*_
# @Time : 2021/10/15 20:01
# @Author : wdm
# @desc : 接口汇总
from fastapi import APIRouter

from device.admin import appclass
from device.admin import apppro
from device.admin import appversion
from device.admin import authclass
from device.admin import authclassanddetail
from device.admin import authdetail
from device.admin import d_question
from device.admin import d_rhmedicalrecord
from device.admin import device
from device.admin import devicelog
from device.admin import dm_physique
from device.admin import ecs_consulting
from device.admin import ecs_consulting_talklog
from device.admin import excelupload
from device.admin import otamain
from device.admin import otaversion
from device.admin import product
from device.admin import productapp
from device.admin import project
from device.admin import statistics

from device.common import upload

device_router = APIRouter()

# 上传文件
device_router.include_router(upload.router, tags=["Uploadlog"])

# 首页
# appclass
device_router.include_router(appclass.router, prefix="/appclass", tags=["APPclass"])
# apppro
device_router.include_router(apppro.router, prefix="/apppro", tags=["APPpro"])
# appversion
device_router.include_router(appversion.router, prefix="/appversion", tags=["Appversion"])
# authclass
device_router.include_router(authclass.router, prefix="/authclass", tags=["Authclass"])
# authclassanddetail
device_router.include_router(authclassanddetail.router, prefix="/authclassanddetail", tags=["Authclassanddetail"])
# authdetail
device_router.include_router(authdetail.router, prefix="/authdetail", tags=["Authdetail"])
# d_question
device_router.include_router(d_question.router, prefix="/d_question", tags=["D_question"])
# d_rhmedicalrecord
device_router.include_router(d_rhmedicalrecord.router, prefix="/d_rhmedicalrecord", tags=["D_rhmedicalrecord"])
# device
device_router.include_router(device.router, prefix="/device", tags=["Device"])
# devicelog
device_router.include_router(devicelog.router, prefix="/devicelog", tags=["Devicelog"])
# dm_physique
device_router.include_router(dm_physique.router, prefix="/dm_physique", tags=["Dm_physique"])
# ecs_consulting
device_router.include_router(ecs_consulting.router, prefix="/ecs_consulting", tags=["Ecs_Consulting"])
# ecs_consulting_talklog
device_router.include_router(ecs_consulting_talklog.router, prefix="/ecs_consulting_talklog", tags=["Ecs_Consulting_Talklog"])
# excelupload
device_router.include_router(excelupload.router, prefix="/excelupload", tags=["Excelupload"])
# otamain
device_router.include_router(otamain.router, prefix="/otamain", tags=["OTAmain"])
# otaversion
device_router.include_router(otaversion.router, prefix="/otaversion", tags=["OTAversion"])
# product
device_router.include_router(product.router, prefix="/product", tags=["Product"])
# productapp
device_router.include_router(productapp.router, prefix="/productapp", tags=["Productapp"])
# project
device_router.include_router(project.router, prefix="/project", tags=["Project"])
# statistics
device_router.include_router(statistics.router, prefix="/statistics", tags=["Statistics"])

