#!/usr/bin/env python3
# _*_ coding: utf-8 _*_
# @Time : 2021/10/15 20:01
# @Author : wdm
# @desc : 接口汇总
from fastapi import APIRouter

from api.admin import dashBoard
from api.admin import access
from api.admin import professors
from api.admin import role
from api.admin import accessrole
from api.admin import admin
from api.admin import adminauth
from api.admin import dm_user
from api.common import upload

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

admin_router = APIRouter()

# include_in_schema=False 隐藏属性
# deprecated=True 弃用属性

# 上传图片
admin_router.include_router(upload.router, tags=["Upload"])

# 首页
admin_router.include_router(dashBoard.router, tags=["Dashboard"])

# access
admin_router.include_router(access.router, prefix="/access", tags=["Access"])
# role
admin_router.include_router(role.router, prefix="/role", tags=["Role"])
# role
admin_router.include_router(professors.router, prefix="/professors", tags=["Professors"])
# role
admin_router.include_router(admin.router, prefix="/admin", tags=["Admin"])
# role
admin_router.include_router(adminauth.router, prefix="/adminauth", tags=["Adminauth"])
# accessrole
admin_router.include_router(accessrole.router, prefix="/accessrole", tags=["Accessrole"])
# dm_user
admin_router.include_router(dm_user.router, prefix="/dm_user", tags=["Dm_user"])

# appclass
admin_router.include_router(appclass.router, prefix="/device/appclass", tags=["APPclass"])
# apppro
admin_router.include_router(apppro.router, prefix="/device/apppro", tags=["APPpro"])
# appversion
admin_router.include_router(appversion.router, prefix="/device/appversion", tags=["Appversion"])
# authclass
admin_router.include_router(authclass.router, prefix="/device/authclass", tags=["Authclass"])
# authclassanddetail
admin_router.include_router(authclassanddetail.router, prefix="/device/authclassanddetail", tags=["Authclassanddetail"])
# authdetail
admin_router.include_router(authdetail.router, prefix="/device/authdetail", tags=["Authdetail"])
#d_question
admin_router.include_router(d_question.router, prefix="/device/d_question", tags=["D_question"])
#d_rhmedicalrecord
admin_router.include_router(d_rhmedicalrecord.router, prefix="/device/d_rhmedicalrecord", tags=["D_rhmedicalrecord"])
# device
admin_router.include_router(device.router, prefix="/device/device", tags=["Device"])
# devicelog
admin_router.include_router(devicelog.router, prefix="/device/devicelog", tags=["Devicelog"])
#ecs_consulting
admin_router.include_router(dm_physique.router, prefix="/device/dm_physique", tags=["Dm_physique"])
#ecs_consulting
admin_router.include_router(ecs_consulting.router, prefix="/device/ecs_consulting", tags=["Ecs_Consulting"])
#ecs_consulting_talklog
admin_router.include_router(ecs_consulting_talklog.router, prefix="/device/ecs_consulting_talklog", tags=["Ecs_Consulting_Talklog"])
# excelupload
admin_router.include_router(excelupload.router, prefix="/device/excelupload", tags=["Excelupload"])
# otamain
admin_router.include_router(otamain.router, prefix="/device/otamain", tags=["OTAmain"])
# otaversion
admin_router.include_router(otaversion.router, prefix="/device/otaversion", tags=["OTAversion"])
# product
admin_router.include_router(product.router, prefix="/device/product", tags=["Product"])
# productapp
admin_router.include_router(productapp.router, prefix="/device/productapp", tags=["Productapp"])
# project
admin_router.include_router(project.router, prefix="/device/project", tags=["Project"])
# statistics
admin_router.include_router(statistics.router, prefix="/device/statistics", tags=["Statistics"])