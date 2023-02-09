#!/usr/bin/env python3
# _*_ coding: utf-8 _*_
# @Time : 2021/10/15 20:10
# @Author : wdm
# @desc : 依赖项
from typing import Generator
from fastapi import Depends, Security, HTTPException
from fastapi.security import OAuth2PasswordBearer, SecurityScopes
from sqlalchemy.orm import Session
from starlette.requests import Request

from core import settings, check_jwt_token
from crud import admin, adminauthclass
from db import MySuperContextManager, RedisPlus
from models import Admin, Adminauthclass
from schemas import TokenData
from utils import PermissionNotEnough, UserNotExist
from utils.permission_assign import by_scopes_get_crud, handle_oauth2_scopes

get_token = OAuth2PasswordBearer(tokenUrl=f"{settings.API_PREFIX}/login", scopes=handle_oauth2_scopes())

from sqlalchemy import and_, or_

async def get_db() -> Generator:
    """ 数据库连接对象 """
    with MySuperContextManager() as db:
        yield db


def get_redis(request: Request) -> RedisPlus:
    """ redis连接对象 """
    return request.app.state.redis


def get_current_user(security_scopes: SecurityScopes, db: Session = Depends(get_db), token: str = Depends(get_token)):
    """ 得到当前用户(docs接口文档) """
    payload = check_jwt_token(token)  # 检验token是否过期
    token_scopes = payload.get("scopes", [])  # 得不到值,返回[]
    token_data = TokenData(scopes=token_scopes, sub=payload.get("sub"))  # token存储的用户权限
    crud_obj = by_scopes_get_crud(token_scopes)  # 验证用户是否存在
    user = crud_obj.get(db, id=payload.get("sub"))
    if not user:
        raise UserNotExist()
    for scope in security_scopes.scopes:  # 勾选的用户权限
        if scope not in token_data.scopes:
            raise PermissionNotEnough()
    return user


def get_current_active_user(current_user: Admin = Security(get_current_user, scopes=["admin"])):
    """ 得到当前登录用户 """
    if not admin.is_active_def(current_user):
        raise HTTPException(status_code=400, detail="用户未登录！！！")
    return current_user

# 暂时未用到
# def get_current_active_superuser(current_user: Admin = Depends(get_current_user)):
#     """ 得到当前超级用户 """
#     if not admin.is_superuser(current_user):
#         raise HTTPException(status_code=401, detail="这个用户没有足够的权限！！！")
#     return current_user

# 菜单树转换
def format_menu(menus):
    nodes = {}
    data_temp = []
    i = 0
    for item in menus:
        i = i + 1
        #print(item)
        '''id              = item["id"]
        print('item' + str(i) + 'id:' + str(id))
        parent_id        = item["parent_id"]
        print('item' + str(i) + 'parent_id:' + str(parent_id))
        access_code     = item["access_code"]
        print('item' + str(i) + 'access_code:' + str(access_code))
        access_name     = item["access_name"]
        print('item' + str(i) + 'access_name:' + str(access_name))
        is_check        = item["is_check"]
        print('item' + str(i) + 'is_check:' + str(is_check))
        is_menu         = item["is_menu"]
        print('item' + str(i) + 'is_menu:' + str(is_menu))
        sort_order      = item["sort_order"]
        print('item' + str(i) + 'sort_order:' + str(sort_order))
        menu_icon       = item["menu_icon"]
        print('item' + str(i) + 'menu_icon:' + str(menu_icon))'''
        id, access_id, parent_id, parent_name, access_code, access_name, is_check, is_menu, sort_order, menu_icon = item["id"], item["access_id"], item["parent_id"], item["parent_name"], item["access_code"], item["access_name"], item["is_check"], item["is_menu"], item["sort_order"], item["menu_icon"]
        access_path, access_redirect, access_component, access_type, access_desc, access_remark, gmt_create = item["access_path"], item["access_redirect"], item["access_component"], item["access_type"], item["access_desc"], item["access_remark"], item["gmt_create"]
        # nodes[]保存需要的字典格式
        nodes[id] = {'id': id, "access_id": access_id, "parent_id": parent_id, "parent_name": parent_name, "access_code": access_code, "access_name": access_name, "is_check": is_check, "is_menu": is_menu, "sort_order": sort_order,
                     "access_path": access_path, "access_redirect": access_redirect, "access_component": access_component, "access_type": access_type, "access_desc": access_desc, "access_remark": access_remark, "gmt_create": gmt_create,
                     "menu_icon": menu_icon, 'children': []}
        # data_temp 保存id,parent_id
        data_temp.append({'id': id, "parent_id": parent_id})
    data = []
    for i in data_temp:
        id = i['id']
        parent_id = i['parent_id']
        node = nodes[id]
        if id == parent_id:
            data.append(node)
        else:
            parent = nodes.get(parent_id)
            if parent:
                parent['children'].append(node)
            else:
                data.append(node)
    return data
# 菜单树转换1
def format_menu1(menus):
    nodes = {}
    data_temp = []
    i = 0
    for item in menus:
        i = i + 1
        #print(item)
        '''id              = item["id"]
        print('item' + str(i) + 'id:' + str(id))
        parent_id        = item["parent_id"]
        print('item' + str(i) + 'parent_id:' + str(parent_id))
        access_code     = item["access_code"]
        print('item' + str(i) + 'access_code:' + str(access_code))
        access_name     = item["access_name"]
        print('item' + str(i) + 'access_name:' + str(access_name))
        is_check        = item["is_check"]
        print('item' + str(i) + 'is_check:' + str(is_check))
        is_menu         = item["is_menu"]
        print('item' + str(i) + 'is_menu:' + str(is_menu))
        sort_order      = item["sort_order"]
        print('item' + str(i) + 'sort_order:' + str(sort_order))
        menu_icon       = item["menu_icon"]
        print('item' + str(i) + 'menu_icon:' + str(menu_icon))'''
        id, access_id, parent_id, parent_name, access_code, access_name, is_check, is_menu, sort_order, menu_icon = item["id"], item["access_id"], item["parent_id"], item["parent_name"], item["access_code"], item["access_name"], item["is_check"], item["is_menu"], item["sort_order"], item["menu_icon"]
        access_path, access_redirect, access_component, access_type, access_desc, access_remark, gmt_create = item["access_path"], item["access_redirect"], item["access_component"], item["access_type"], item["access_desc"], item["access_remark"], item["gmt_create"]
        # nodes[]保存需要的字典格式
        nodes[id] = {"component": access_component, "createTime": gmt_create, "icon": menu_icon, 'id': id, "menuName": access_name, "orderNo": sort_order,
                     "parentMenu": parent_id, "permission": "permission", "status": str(is_check), "type": str(is_menu),
                     'children': []}
        # data_temp 保存id,parent_id
        data_temp.append({'id': id, "parent_id": parent_id})
    data = []
    for i in data_temp:
        id = i['id']
        parent_id = i['parent_id']
        node = nodes[id]
        if id == parent_id:
            data.append(node)
        else:
            parent = nodes.get(parent_id)
            if parent:
                parent['children'].append(node)
            else:
                data.append(node)
    return data

'''/**
 * 获取血压结论
 *
 * @param dbp 基础数据值【收缩压/高压】
 * @param sbp 基础数据值【舒张压/低压】
 * @return 基础数据实体
 */'''
def checkBloodPressureConclusion(sbp: int, dbp: int):
    conclusionBean = {}
    if (sbp < 90):
        if (dbp < 60):
            if ((sbp - dbp) < 21):
                conclusionBean['id'] = 1
                conclusionBean["conclusion"] = "血压偏低了，脉压差过小"
                conclusionBean["hint"] = "收缩压与舒张压之间的压差值称为脉压差。正常值为30～40mmHg，压差大于60mmHg称之为脉压差过大，小于20mmHg称之为压差过小。  引起脉压差减小的常见疾病有心包大量积液、缩窄性心包炎、严重的二尖瓣狭窄、主动脉瓣狭窄，还有由于肥胖、血液粘稠度增高或合并糖尿病、高脂血症等也能引起。  如果连续三天的检测均发现脉压差异常，请您尽快到正规医院确诊查明原因，并由专业医生治疗原发疾病。"
                conclusionBean["colorstring"] = "red"
            elif ((sbp - dbp) < 60) :
                conclusionBean['id'] = 2
                conclusionBean["conclusion"] = "血压偏低了"
                conclusionBean["hint"] = "您此次测量的血压偏低，如果连续三天测试结果均为低值，请尽快到专业医院就医确诊，由专业医生分析诊治。平时适当增加食盐用量，同时多饮水，吃些人参、黄芪、生脉饮等。"
                conclusionBean["colorstring"] = "red"
            else :
                conclusionBean['id'] = 3
                conclusionBean["conclusion"] = "血压偏低了，脉压差过大"
                conclusionBean["hint"] = "收缩压与舒张压之间的压差值称为脉压差。正常值为30～40mmHg，压差大于60mmHg称之为脉压差过大，小于20mmHg称之为压差过小。　脉压差大反映大动脉弹性减弱，僵硬度增加，心脏泵入大动脉的血不能有弹性地调节，因而增加心脏负担，是心脏血管事件危险因素之一，应当积极防治，采取措施控制好血压。  如果连续三天的检测数据均超标，请您尽快到正规医院确诊查明原因，并由专业医生提供诊治。"
                conclusionBean["colorstring"] = "red"
        elif (dbp < 81) :
            if ((sbp - dbp) < 21):
                conclusionBean['id'] = 4
                conclusionBean["conclusion"] = "收缩压偏低，脉压差过小"
                conclusionBean["hint"] = "收缩压与舒张压之间的压差值称为脉压差。正常值为30～40mmHg，压差大于60mmHg称之为脉压差过大，小于20mmHg称之为压差过小。  引起脉压差减小的常见疾病有心包大量积液、缩窄性心包炎、严重的二尖瓣狭窄、主动脉瓣狭窄，还有由于肥胖、血液粘稠度增高或合并糖尿病、高脂血症等也能引起。  如果连续三天的检测均发现脉压差异常，请您尽快到正规医院确诊查明原因，并由专业医生治疗原发疾病。"
                conclusionBean["colorstring"] = "red"
            else :
                conclusionBean['id'] = 5
                conclusionBean["conclusion"] = "收缩压偏低了"
                conclusionBean["hint"] = "请保持定期监测血压的习惯，如果连续三天测试结果均偏低，请及时到正规医院检查确诊。"
                conclusionBean["colorstring"] = "red"
        elif (dbp < 90) :
            conclusionBean['id'] = 6
            conclusionBean["conclusion"] = "收缩压偏低，脉压差过小"
            conclusionBean["hint"] = "收缩压与舒张压之间的压差值称为脉压差。正常值为30～40mmHg，压差大于60mmHg称之为脉压差过大，小于20mmHg称之为压差过小。  引起脉压差减小的常见疾病有心包大量积液、缩窄性心包炎、严重的二尖瓣狭窄、主动脉瓣狭窄，还有由于肥胖、血液粘稠度增高或合并糖尿病、高脂血症等也能引起。  如果连续三天的检测均发现脉压差异常，请您尽快到正规医院确诊查明原因，并由专业医生治疗原发疾病。"
            conclusionBean["colorstring"] = "red"
        else :
            conclusionBean['id'] = 7
            conclusionBean["conclusion"] = "不存在"
            conclusionBean["hint"] = "人类达不到这种血压"
            conclusionBean["colorstring"] = "red"
    elif (sbp < 120) :
        if (dbp < 60):
            if ((sbp - dbp) < 60):
                conclusionBean['id'] = 8
                conclusionBean["conclusion"] = "舒张压偏低了"
                conclusionBean["hint"] = "请保持定期监测血压的习惯，如果连续三天测试结果均偏低，请及时到正规医院检查确诊。"
                conclusionBean["colorstring"] = "red"
            else :
                conclusionBean['id'] = 9
                conclusionBean["conclusion"] = "舒张压偏低了，脉压差过大"
                conclusionBean["hint"] = "收缩压与舒张压之间的压差值称为脉压差。正常值为30～40mmHg，压差大于60mmHg称之为脉压差过大，小于20mmHg称之为压差过小。　脉压差大反映大动脉弹性减弱，僵硬度增加，心脏泵入大动脉的血不能有弹性地调节，因而增加心脏负担，是心脏血管事件危险因素之一，应当积极防治，采取措施控制好血压。  如果连续三天的检测数据均超标，请您尽快到正规医院确诊查明原因，并由专业医生提供诊治。"
                conclusionBean["colorstring"] = "red"
        elif (dbp < 81) :
            if ((sbp - dbp) < 21):
                conclusionBean['id'] = 10
                conclusionBean["conclusion"] = "血压非常理想，脉压差过小"
                conclusionBean["hint"] = "收缩压与舒张压之间的压差值称为脉压差。正常值为30～40mmHg，压差大于60mmHg称之为脉压差过大，小于20mmHg称之为压差过小。  引起脉压差减小的常见疾病有心包大量积液、缩窄性心包炎、严重的二尖瓣狭窄、主动脉瓣狭窄，还有由于肥胖、血液粘稠度增高或合并糖尿病、高脂血症等也能引起。  如果连续三天的检测均发现脉压差异常，请您尽快到正规医院确诊查明原因，并由专业医生治疗原发疾病。"
                conclusionBean["colorstring"] = "green"
            else :
                conclusionBean['id'] = 11
                conclusionBean["conclusion"] = "血压非常理想"
                conclusionBean["hint"] = "请继续保持良好的饮食卫生习惯和适当的体育运动。"
                conclusionBean["colorstring"] = "green"
        elif (dbp < 85) :
            if ((sbp - dbp) < 21):
                conclusionBean['id'] = 12
                conclusionBean["conclusion"] = "血压属于正常血压范围，脉压差过小"
                conclusionBean["hint"] = "收缩压与舒张压之间的压差值称为脉压差。正常值为30～40mmHg，压差大于60mmHg称之为脉压差过大，小于20mmHg称之为压差过小。  引起脉压差减小的常见疾病有心包大量积液、缩窄性心包炎、严重的二尖瓣狭窄、主动脉瓣狭窄，还有由于肥胖、血液粘稠度增高或合并糖尿病、高脂血症等也能引起。  如果连续三天的检测均发现脉压差异常，请您尽快到正规医院确诊查明原因，并由专业医生治疗原发疾病。"
                conclusionBean["colorstring"] = "purple"
            else :
                conclusionBean['id'] = 13
                conclusionBean["conclusion"] = "血压属于正常血压范围"
                conclusionBean["hint"] = "请保持定期监测血压的习惯，继续保持良好的饮食卫生习惯和适当的体育运动。"
                conclusionBean["colorstring"] = "purple"
        elif (dbp < 90) :
            if ((sbp - dbp) < 21):
                conclusionBean['id'] = 14
                conclusionBean["conclusion"] = "血压属于正常高值范围，脉压差过小"
                conclusionBean["hint"] = "收缩压与舒张压之间的压差值称为脉压差。正常值为30～40mmHg，压差大于60mmHg称之为脉压差过大，小于20mmHg称之为压差过小。  引起脉压差减小的常见疾病有心包大量积液、缩窄性心包炎、严重的二尖瓣狭窄、主动脉瓣狭窄，还有由于肥胖、血液粘稠度增高或合并糖尿病、高脂血症等也能引起。  如果连续三天的检测均发现脉压差异常，请您尽快到正规医院确诊查明原因，并由专业医生治疗原发疾病。"
                conclusionBean["colorstring"] = "purple"
            else :
                conclusionBean['id'] = 15
                conclusionBean["conclusion"] = "血压属于正常高值范围"
                conclusionBean["hint"] = "请保持定期监测血压，注意是否工作生活压力过大,饮食不合理,作息不规律,以及长期接触电脑空调等。"
                conclusionBean["colorstring"] = "purple"
        else :
            if ((sbp - dbp) < 21):
                conclusionBean['id'] = 16
                conclusionBean["conclusion"] = "您的血压偏高了，脉压差过小"
                conclusionBean["hint"] = "收缩压与舒张压之间的压差值称为脉压差。正常值为30～40mmHg，压差大于60mmHg称之为脉压差过大，小于20mmHg称之为压差过小。  引起脉压差减小的常见疾病有心包大量积液、缩窄性心包炎、严重的二尖瓣狭窄、主动脉瓣狭窄，还有由于肥胖、血液粘稠度增高或合并糖尿病、高脂血症等也能引起。  如果连续三天的检测均发现脉压差异常，请您尽快到正规医院确诊查明原因，并由专业医生治疗原发疾病。"
                conclusionBean["colorstring"] = "red"
            else :
                conclusionBean['id'] = 17
                conclusionBean["conclusion"] = "您的血压偏高了"
                conclusionBean["hint"] = "请注意减少钠盐食用量,减少膳食脂肪并补充适量优质蛋白,注意补充钙和钾,多吃蔬菜和水果,戒烟戒酒,科学饮水。建议到专业医院进一步确诊治疗。"
                conclusionBean["colorstring"] = "red"
    elif (sbp < 130) :
        if (dbp < 60):
            conclusionBean['id'] = 18
            conclusionBean["conclusion"] = "舒张压偏低了，脉压差过大"
            conclusionBean["hint"] = "收缩压与舒张压之间的压差值称为脉压差。正常值为30～40mmHg，压差大于60mmHg称之为脉压差过大，小于20mmHg称之为压差过小。　脉压差大反映大动脉弹性减弱，僵硬度增加，心脏泵入大动脉的血不能有弹性地调节，因而增加心脏负担，是心脏血管事件危险因素之一，应当积极防治，采取措施控制好血压。  如果连续三天的检测数据均超标，请您尽快到正规医院确诊查明原因，并由专业医生提供诊治。"
            conclusionBean["colorstring"] = "red"
        elif (dbp < 81) :
            if ((sbp - dbp) < 60):
                conclusionBean['id'] = 19
                conclusionBean["conclusion"] = "血压属于正常血压范围"
                conclusionBean["hint"] = "请保持定期监测血压的习惯，继续保持良好的饮食卫生习惯和适当的体育运动。"
                conclusionBean["colorstring"] = "green"
            else :
                conclusionBean['id'] = 20
                conclusionBean["conclusion"] = "血压属于正常血压范围，脉压差过大"
                conclusionBean["hint"] = "收缩压与舒张压之间的压差值称为脉压差。正常值为30～40mmHg，压差大于60mmHg称之为脉压差过大，小于20mmHg称之为压差过小。　脉压差大反映大动脉弹性减弱，僵硬度增加，心脏泵入大动脉的血不能有弹性地调节，因而增加心脏负担，是心脏血管事件危险因素之一，应当积极防治，采取措施控制好血压。  如果连续三天的检测数据均超标，请您尽快到正规医院确诊查明原因，并由专业医生提供诊治。"
                conclusionBean["colorstring"] = "purple"
        elif (dbp < 85) :
            conclusionBean['id'] = 21
            conclusionBean["conclusion"] = "血压属于正常血压范围"
            conclusionBean["hint"] = "请保持定期监测血压的习惯，继续保持良好的饮食卫生习惯和适当的体育运动。"
            conclusionBean["colorstring"] = "purple"
        elif (dbp < 90) :
            conclusionBean['id'] = 22
            conclusionBean["conclusion"] = "血压属于正常高值范围"
            conclusionBean["hint"] = "请保持定期监测血压，注意是否工作生活压力过大,饮食不合理,作息不规律,以及长期接触电脑空调等。"
            conclusionBean["colorstring"] = "purple"
        else :
            if ((sbp - dbp) < 21):
                conclusionBean['id'] = 23
                conclusionBean["conclusion"] = "您的血压偏高了，脉压差过小"
                conclusionBean["hint"] = "收缩压与舒张压之间的压差值称为脉压差。正常值为30～40mmHg，压差大于60mmHg称之为脉压差过大，小于20mmHg称之为压差过小。  引起脉压差减小的常见疾病有心包大量积液、缩窄性心包炎、严重的二尖瓣狭窄、主动脉瓣狭窄，还有由于肥胖、血液粘稠度增高或合并糖尿病、高脂血症等也能引起。  如果连续三天的检测均发现脉压差异常，请您尽快到正规医院确诊查明原因，并由专业医生治疗原发疾病。"
                conclusionBean["colorstring"] = "red"
            else :
                conclusionBean['id'] = 24
                conclusionBean["conclusion"] = "您的血压偏高了"
                conclusionBean["hint"] = "请注意减少钠盐食用量,减少膳食脂肪并补充适量优质蛋白,注意补充钙和钾,多吃蔬菜和水果,戒烟戒酒,科学饮水。建议到专业医院进一步确诊治疗。"
                conclusionBean["colorstring"] = "red"
    elif (sbp < 140) :
        if (dbp < 60):
            conclusionBean['id'] = 25
            conclusionBean["conclusion"] = "舒张压偏低了，脉压差过大"
            conclusionBean["hint"] = "收缩压与舒张压之间的压差值称为脉压差。正常值为30～40mmHg，压差大于60mmHg称之为脉压差过大，小于20mmHg称之为压差过小。　脉压差大反映大动脉弹性减弱，僵硬度增加，心脏泵入大动脉的血不能有弹性地调节，因而增加心脏负担，是心脏血管事件危险因素之一，应当积极防治，采取措施控制好血压。  如果连续三天的检测数据均超标，请您尽快到正规医院确诊查明原因，并由专业医生提供诊治。"
            conclusionBean["colorstring"] = "red"
        elif (dbp < 81) :
            if ((sbp - dbp) < 60):
                conclusionBean['id'] = 26
                conclusionBean["conclusion"] = "血压属于正常高值范围"
                conclusionBean["hint"] = "请保持定期监测血压，注意是否工作生活压力过大,饮食不合理,作息不规律,以及长期接触电脑空调等。"
                conclusionBean["colorstring"] = "purple"
            else :
                conclusionBean['id'] = 27
                conclusionBean["conclusion"] = "血压属于正常高值范围，脉压差过大"
                conclusionBean["hint"] = "收缩压与舒张压之间的压差值称为脉压差。正常值为30～40mmHg，压差大于60mmHg称之为脉压差过大，小于20mmHg称之为压差过小。　脉压差大反映大动脉弹性减弱，僵硬度增加，心脏泵入大动脉的血不能有弹性地调节，因而增加心脏负担，是心脏血管事件危险因素之一，应当积极防治，采取措施控制好血压。  如果连续三天的检测数据均超标，请您尽快到正规医院确诊查明原因，并由专业医生提供诊治。"
                conclusionBean["colorstring"] = "purple"
        elif (dbp < 85) :
            conclusionBean['id'] = 28
            conclusionBean["conclusion"] = "血压属于正常高值范围"
            conclusionBean["hint"] = "请保持定期监测血压，注意是否工作生活压力过大,饮食不合理,作息不规律,以及长期接触电脑空调等。"
            conclusionBean["colorstring"] = "purple"
        elif (dbp < 90) :
            conclusionBean['id'] = 29
            conclusionBean["conclusion"] = "血压属于正常高值范围"
            conclusionBean["hint"] = "请保持定期监测血压，注意是否工作生活压力过大,饮食不合理,作息不规律,以及长期接触电脑空调等。"
            conclusionBean["colorstring"] = "purple"
        else :
            if ((sbp - dbp) < 21):
                conclusionBean['id'] = 30
                conclusionBean["conclusion"] = "您的血压偏高了，脉压差过小"
                conclusionBean["hint"] = "收缩压与舒张压之间的压差值称为脉压差。正常值为30～40mmHg，压差大于60mmHg称之为脉压差过大，小于20mmHg称之为压差过小。  引起脉压差减小的常见疾病有心包大量积液、缩窄性心包炎、严重的二尖瓣狭窄、主动脉瓣狭窄，还有由于肥胖、血液粘稠度增高或合并糖尿病、高脂血症等也能引起。  如果连续三天的检测均发现脉压差异常，请您尽快到正规医院确诊查明原因，并由专业医生治疗原发疾病。"
                conclusionBean["colorstring"] = "red"
            else :
                conclusionBean['id'] = 31
                conclusionBean["conclusion"] = "您的血压偏高了"
                conclusionBean["hint"] = "请注意减少钠盐食用量,减少膳食脂肪并补充适量优质蛋白,注意补充钙和钾,多吃蔬菜和水果,戒烟戒酒,科学饮水。建议到专业医院进一步确诊治疗。"
                conclusionBean["colorstring"] = "red"
    else :
        if (dbp < 60):
            conclusionBean['id'] = 32
            conclusionBean["conclusion"] = "不存在"
            conclusionBean["hint"] = "人类达不到这种血压"
            conclusionBean["colorstring"] = "red"
        elif (dbp < 81) :
            conclusionBean['id'] = 33
            conclusionBean["conclusion"] = "收缩压偏高了，脉压差过大"
            conclusionBean["hint"] = "收缩压与舒张压之间的压差值称为脉压差。正常值为30～40mmHg，压差大于60mmHg称之为脉压差过大，小于20mmHg称之为压差过小。　脉压差大反映大动脉弹性减弱，僵硬度增加，心脏泵入大动脉的血不能有弹性地调节，因而增加心脏负担，是心脏血管事件危险因素之一，应当积极防治，采取措施控制好血压。  如果连续三天的检测数据均超标，请您尽快到正规医院确诊查明原因，并由专业医生提供诊治。"
            conclusionBean["colorstring"] = "red"
        elif (dbp < 85) :
            if ((sbp - dbp) < 60):
                conclusionBean['id'] = 34
                conclusionBean["conclusion"] = "您的血压偏高了"
                conclusionBean["hint"] = "请注意减少钠盐食用量,减少膳食脂肪并补充适量优质蛋白,注意补充钙和钾,多吃蔬菜和水果,戒烟戒酒,科学饮水。建议到专业医院进一步确诊治疗。"
                conclusionBean["colorstring"] = "red"
            else :
                conclusionBean['id'] = 35
                conclusionBean["conclusion"] = "您的血压偏高了，脉压差过大"
                conclusionBean["hint"] = "收缩压与舒张压之间的压差值称为脉压差。正常值为30～40mmHg，压差大于60mmHg称之为脉压差过大，小于20mmHg称之为压差过小。　脉压差大反映大动脉弹性减弱，僵硬度增加，心脏泵入大动脉的血不能有弹性地调节，因而增加心脏负担，是心脏血管事件危险因素之一，应当积极防治，采取措施控制好血压。  如果连续三天的检测数据均超标，请您尽快到正规医院确诊查明原因，并由专业医生提供诊治。"
                conclusionBean["colorstring"] = "red"
        elif (dbp < 90) :
            if ((sbp - dbp) < 60):
                conclusionBean['id'] = 36
                conclusionBean["conclusion"] = "您的血压偏高了"
                conclusionBean["hint"] = "请注意减少钠盐食用量,减少膳食脂肪并补充适量优质蛋白,注意补充钙和钾,多吃蔬菜和水果,戒烟戒酒,科学饮水。建议到专业医院进一步确诊治疗。"
                conclusionBean["colorstring"] = "red"
            else :
                conclusionBean['id'] = 37
                conclusionBean["conclusion"] = "您的血压偏高了，脉压差过大"
                conclusionBean["hint"] = "收缩压与舒张压之间的压差值称为脉压差。正常值为30～40mmHg，压差大于60mmHg称之为脉压差过大，小于20mmHg称之为压差过小。　脉压差大反映大动脉弹性减弱，僵硬度增加，心脏泵入大动脉的血不能有弹性地调节，因而增加心脏负担，是心脏血管事件危险因素之一，应当积极防治，采取措施控制好血压。  如果连续三天的检测数据均超标，请您尽快到正规医院确诊查明原因，并由专业医生提供诊治。"
                conclusionBean["colorstring"] = "red"
        else :
            if ((sbp - dbp) < 60):
                conclusionBean['id'] = 38
                conclusionBean["conclusion"] = "您的血压偏高了"
                conclusionBean["hint"] = "请注意减少钠盐食用量,减少膳食脂肪并补充适量优质蛋白,注意补充钙和钾,多吃蔬菜和水果,戒烟戒酒,科学饮水。建议到专业医院进一步确诊治疗。"
                conclusionBean["colorstring"] = "red"
            else :
                conclusionBean['id'] = 39
                conclusionBean["conclusion"] = "您的血压偏高了，脉压差过大"
                conclusionBean["hint"] = "收缩压与舒张压之间的压差值称为脉压差。正常值为30～40mmHg，压差大于60mmHg称之为脉压差过大，小于20mmHg称之为压差过小。　脉压差大反映大动脉弹性减弱，僵硬度增加，心脏泵入大动脉的血不能有弹性地调节，因而增加心脏负担，是心脏血管事件危险因素之一，应当积极防治，采取措施控制好血压。  如果连续三天的检测数据均超标，请您尽快到正规医院确诊查明原因，并由专业医生提供诊治。"
                conclusionBean["colorstring"] = "red"
    return conclusionBean
'''/**
 * 获取体温结论
 *
 * @param temperature 基础数据值
 * @return 基础数据实体
 */'''
def checkTemperatureConclusion(temperature: float) :
    conclusionBean = {}
    if (temperature < 30) :
        conclusionBean['id'] = 1
        conclusionBean["conclusion"] = "LO"
        conclusionBean["hint"] = "超低温"
        conclusionBean["colorstring"] = "red"
    elif (temperature < 36) :
        conclusionBean['id'] = 2
        conclusionBean["conclusion"] = "您的体温偏低"
        conclusionBean["hint"] = "请检查是否保暖防寒条件不足；过量饮酒引起的全身血管收缩；服用某些中枢神经抑制药物,如镇静剂,安眠药,防抑郁药等； 老年人如果持续出现低体温,经过自我调节仍无好转者,就应去医院作内分泌学检查,以确定有无甲状腺机能减退等疾病。"
        conclusionBean["colorstring"] = "red"
    elif (temperature <= 37.5) :
        conclusionBean['id'] = 3
        conclusionBean["conclusion"] = "您的体温正常"
        conclusionBean["hint"] = "正常人体温并不是固定不变的，可随性别、年龄、昼夜、运动和情绪的变化等因素而有所波动，但这种改变经常是在正常范围内。"
        conclusionBean["colorstring"] = "green"
    elif (temperature <= 38) :
        conclusionBean['id'] = 4
        conclusionBean["conclusion"] = "您的体温低热"
        conclusionBean["hint"] = "排除剧烈运动或者过热环境等因素影响，建议您尽快就医诊断查明病因并及时治疗。"
        conclusionBean["colorstring"] = "red"
    elif (temperature <= 39) :
        conclusionBean['id'] = 5
        conclusionBean["conclusion"] = "您的体温中度热"
        conclusionBean["hint"] = "有肌肉乏力，肌肉酸痛等表现"
        conclusionBean["colorstring"] = "red"
    elif (temperature <= 42.9) :
        conclusionBean['id'] = 6
        conclusionBean["conclusion"] = "您的体温高热"
        conclusionBean["hint"] = "体温在40℃以上时属于超高热了，随时会有生命危险，请紧急就医。"
        conclusionBean["colorstring"] = "red"
        '''/*elif (temperature <= 46.5) :
            conclusionBean['id'] = 9
            conclusionBean["conclusion"] = "即将到达人类极限"
            conclusionBean["hint"] = "人类历史上发烧的最高纪录是46.5℃"
            conclusionBean["colorstring"] = "red"*/'''
    else :
        conclusionBean['id'] = 7
        conclusionBean["conclusion"] = "HI"
        conclusionBean["hint"] = "超高温"
        conclusionBean["colorstring"] = "red"
    return conclusionBean
'''/**
 * 获取心率结论
 *
 * @param heartrate 基础数据值
 * @return 基础数据实体
 */'''
def checkHeartrateConclusion(heartrate: int ) :
    conclusionBean = {}
    if (heartrate <= 49) :
        conclusionBean['id'] = 1
        conclusionBean["conclusion"] = "可能心动过缓"
        conclusionBean["hint"] = ""
        conclusionBean["colorstring"] = "red"
    elif (heartrate <= 59) :
        conclusionBean['id'] = 2
        conclusionBean["conclusion"] = "心率正常"
        conclusionBean["hint"] = ""
        conclusionBean["colorstring"] = "purple"
    elif (heartrate <= 100) :
        conclusionBean['id'] = 3
        conclusionBean["conclusion"] = "心率正常"
        conclusionBean["hint"] = ""
        conclusionBean["colorstring"] = "green"
    elif (heartrate <= 120) :
        conclusionBean['id'] = 4
        conclusionBean["conclusion"] = "心率正常"
        conclusionBean["hint"] = ""
        conclusionBean["colorstring"] = "purple"
    else :
        conclusionBean['id'] = 5
        conclusionBean["conclusion"] = "可能心动过速"
        conclusionBean["hint"] = ""
        conclusionBean["colorstring"] = "red"
    return conclusionBean
'''/**
 * 获取餐前血糖结论
 *
 * @param pmbg 基础数据值
 * @return 基础数据实体
 */'''
def  checkGluPMBGConclusion(pmbg: float) :
    conclusionBean = {}
    if (pmbg <= 2.4) :
        conclusionBean['id'] = 1
        conclusionBean["conclusion"] = "您有低血糖的症状"
        conclusionBean["hint"] = "异常低血糖诊断标准通常为：男＜2.78mmol/L，女＜2.5mmol/L，婴儿和儿童＜2.22mmol/L。请尽快到专业医院确诊。可以食用红枣、阿胶等，或遵医嘱。"
        conclusionBean["colorstring"] = "red"
    elif (pmbg > 2.4 and pmbg <= 3.8) :
        conclusionBean['id'] = 2
        conclusionBean["conclusion"] = "您的血糖值偏低"
        conclusionBean["hint"] = "与高血压病相反，本病宜选择适当的高钠、高胆固醇饮食。氯化钠（即食盐）每日需摄足12-15克。含胆固醇多的脑、肝、蛋、奶油、鱼卵、猪骨等食品，适量常吃，有利于提高血胆固醇浓度，增加动脉紧张度，使血压上升。"
        conclusionBean["colorstring"] = "purple"
    elif (pmbg > 3.8 and pmbg <= 6.1) :
        conclusionBean['id'] = 3
        conclusionBean["conclusion"] = "您的血糖值很正常"
        conclusionBean["hint"] = "请保持良好的饮食卫生习惯和适当的运动锻炼"
        conclusionBean["colorstring"] = "green"
    elif (pmbg > 6.1 and pmbg <= 6.9) :
        conclusionBean['id'] = 4
        conclusionBean["conclusion"] = "您的糖耐量减低（IGT）"
        conclusionBean["hint"] = "请及早重视，咨询相关专业医生的指导建议，防止发展成为糖尿病。"
        conclusionBean["colorstring"] = "purple"
    else :
        conclusionBean['id'] = 5
        conclusionBean["conclusion"] = "您的血糖值偏高"
        conclusionBean["hint"] = "请再重复检测一次，如仍达以上值者，极有可能患有糖尿病，请尽快到专业医院确诊。"
        conclusionBean["colorstring"] = "red"
    return conclusionBean
'''/**
 * 获取餐后血糖结论
 *
 * @param pbg 基础数据值
 * @return 基础数据实体
 */'''
def  checkGluPBGConclusion(pbg: float) :
    conclusionBean = {}
    if (pbg <= 2.4) :
        conclusionBean['id'] = 1
        conclusionBean["conclusion"] = "您有低血糖的症状"
        conclusionBean["hint"] = "异常低血糖诊断标准通常为：男＜2.78mmol/L，女＜2.5mmol/L，婴儿和儿童＜2.22mmol/L。请尽快到专业医院确诊。可以食用红枣、阿胶等，或遵医嘱。"
        conclusionBean["colorstring"] = "red"
    elif (pbg > 2.4 and pbg <= 3.8) :
        conclusionBean['id'] = 2
        conclusionBean["conclusion"] = "您的血糖值偏低"
        conclusionBean["hint"] = "与高血压病相反，本病宜选择适当的高钠、高胆固醇饮食。氯化钠（即食盐）每日需摄足12-15克。含胆固醇多的脑、肝、蛋、奶油、鱼卵、猪骨等食品，适量常吃，有利于提高血胆固醇浓度，增加动脉紧张度，使血压上升。"
        conclusionBean["colorstring"] = "purple"
    elif (pbg > 3.8 and pbg <= 7.7) :
        conclusionBean['id'] = 3
        conclusionBean["conclusion"] = "您的血糖值很正常"
        conclusionBean["hint"] = "请保持良好的饮食卫生习惯和适当的运动锻炼"
        conclusionBean["colorstring"] = "green"
    elif (pbg > 7.7 and pbg <= 11) :
        conclusionBean['id'] = 4
        conclusionBean["conclusion"] = "您的糖耐量减低（IGT）"
        conclusionBean["hint"] = "请及早重视，咨询相关专业医生的指导建议，防止发展成为糖尿病。"
        conclusionBean["colorstring"] = "purple"
    else :
        conclusionBean['id'] = 5
        conclusionBean["conclusion"] = "您的血糖值偏高"
        conclusionBean["hint"] = "请再重复检测一次，如仍达以上值者，极有可能患有糖尿病，请尽快到专业医院确诊。"
        conclusionBean["colorstring"] = "red"
    return conclusionBean
'''/**
 * 获取血氧饱和度结论
 *
 * @param spo 基础数据值
 * @return 基础数据实体
 */'''
def  checkOxygenSpoConclusion(spo: int) :
    conclusionBean = {}
    if (spo < 94) :
        conclusionBean['id'] = 1
        conclusionBean["conclusion"] = "血氧偏低"
        conclusionBean["hint"] = "请适当吸氧，或增加体质锻炼。如果低于75%，建议及时通过医生检查，明确诊断，一般先进行吸氧治疗的，改善氧气饱和度，然后再对因治疗。"
        conclusionBean["colorstring"] = "red"
    elif (spo <= 99) :
        conclusionBean['id'] = 2
        conclusionBean["conclusion"] = "血氧正常"
        conclusionBean["hint"] = "血氧饱和度(SpO2)是血液中被氧结合的氧合血红蛋白(HbO2)的容量占全部可结合的血红蛋白(Hb)容量的百分比，即血液中血氧的浓度，它是呼吸循环的重要生理参数。"
        conclusionBean["colorstring"] = "green"
    else :
        conclusionBean['id'] = 3
        conclusionBean["conclusion"] = "您的血氧超过99"
        conclusionBean["hint"] = "正常人血氧饱和度不可能达到100%"
        conclusionBean["colorstring"] = "red"
    return conclusionBean
'''/**
 * 获取脉率结论
 *
 * @param pulse 基础数据值
 * @return 基础数据实体
 */'''
def  checkOxygenPulseConclusion(pulse: int) :
    conclusionBean = {}
    if (pulse < 50) :
        conclusionBean['id'] = 1
        conclusionBean["conclusion"] = "可能心动过缓"
        conclusionBean["hint"] = "经常从事重体力劳动或者体育锻炼的人，如无头晕无力等不良症状，可视为正常。"
        conclusionBean["colorstring"] = "red"
    elif (pulse <= 120) :
        conclusionBean['id'] = 2
        conclusionBean["conclusion"] = "脉率正常"
        conclusionBean["hint"] = "一般老年人脉率较慢，可低于60次/分钟，新生儿的脉率较快，可达到140次/分钟。正常人脉率规则，不会出现脉搏间隔时间长短不一的现象。正常人脉搏强弱均等，不会出现强弱交替的现象。"
        conclusionBean["colorstring"] = "green"
    else :
        conclusionBean['id'] = 3
        conclusionBean["conclusion"] = "可能心动过速"
        conclusionBean["hint"] = "运动和情绪激动时可使脉率增快。如果正常情况下有心慌气短等不良症状，请及时就医。"
        conclusionBean["colorstring"] = "red"
    return conclusionBean
'''/**
 * 获取体质辨识结论
 *
 * @param temperature 基础数据值
 * @return 基础数据实体
 */'''
def checkPhysiqueConclusion(physique: str) :
    hints_a1 = "no data"
    hintsarr1 = []
    hintsarr2 = []
    hints_a = "<br>\t\t<b>平和体质</b>是正常体质，这类人体形匀称健壮，面色、肤色润泽，头发稠密有光泽，目光有神，唇色红润，不易疲劳，精力充沛，睡眠、食欲好，大小便正常，性格随和开朗，患病少。" \
              "<br>\t\t<b>养生要点：</b>重在维护。" \
              "<br>\t\t<b>对策：</b>平时只要注意饮食有节、劳逸结合、坚持锻炼即可。"

    hints_b = "<br>\t\t<b>气虚体质</b>的人经常感觉疲乏、气短、讲话的声音低弱、容易出汗、舌边有齿痕。患病倾向有容易感冒，生病后抗病能力弱且难以痊愈，还易患内脏下垂比如胃下垂等。" \
              "<br>\t\t<b>养生要点：</b>益气健脾，注意胃下垂等疾病。" \
              "<br>\t\t<b>对策：</b>平时多食用益气健脾的食物，如黄豆、白扁豆、鸡肉、香菇、大枣、桂圆、蜂蜜等。少食具有耗气作用的食物，如空心菜、生萝卜等。起居宜有规律，夏季午间适当休息，保持充足睡眠。注意保暖，避免劳动或激烈运动时出汗受风。不要过于劳作，以免损伤正气。运动宜柔缓，不宜剧烈运动。"

    hints_c = "<br>\t\t<b>阳虚体质</b>的人，肌肉不健壮，时感手脚发凉，胃脘部、背部或腰膝部怕冷，衣服比别人穿得多，夏天不喜吹空调，喜欢安静，吃或喝凉的食物不舒服，容易大便稀溏，小便颜色清而量多。性格多沉闷、内向。患病倾向，易出现寒病，腹泻、阳痿等。" \
              "<br>\t\t<b>养生要点：</b>温阳补益气，防腹泻、阳痿等疾病。" \
              "<br>\t\t<b>对策：</b>食宜温阳。可多食牛肉、羊肉、韭菜、生姜、葱头等温阳之品。少食梨、西瓜、荸荠等生冷寒凉食物，少饮绿茶。起居要保暖，特别是背部及下腹丹田部位，避免长时间待在空调房，防止出汗过多，在阳光充足的情况下适当进行户外活动。运动避风寒，冬天避免在大风、大寒、大雾、大雪及空气污染的环境中锻炼。"

    hints_d = "<br>\t\t<b>阴虚质</b>的人体形多瘦长，经常感到手、脚心发热，脸上冒火，面颊潮红或偏红，耐受不了夏天的暑热，常感到眼睛干涩，口干咽燥，总想喝水，皮肤干燥，性情急躁，外向好动，舌质偏红，苔少。患病倾向为易患咳嗽、干燥综合征、甲亢等。" \
              "<br>\t\t<b>养生要点：</b>滋阴，注意甲亢等疾病。" \
              "<br>\t\t<b>对策：</b>注意食宜滋阴，多吃瘦猪肉、鸭肉、绿豆、冬瓜等甘凉滋润之品，少食羊肉、韭菜、辣椒、葵瓜子等性温燥烈之品。起居忌熬夜，避免在高温酷暑下工作。运动勿太过，锻炼时要控制出汗量，及时补充水分，不宜洗桑拿。"

    hints_e = "<br>\t\t<b>痰湿体质</b>的人，体形肥胖，腹部肥满而松软。容易出汗，经常感觉导肢体酸困沉重、不轻松。经常感觉脸上一层油，嘴里常有黏黏的或甜腻的感觉，嗓子老有痰，舌苔较厚，性格比较温和，舌苔厚腻。患病倾向，易患消渴、中风、胸痹等。" \
              "<br>\t\t<b>养生要点：</b>化痰祛湿，防中风、胸痹等疾病。" \
              "<br>\t\t<b>对策：</b>食宜清淡。饮食应以清淡为主，少食肥肉及甜、黏、油腻的食物，如炸糕、驴打滚。可多食海带、冬瓜等。起居忌潮湿，居住环境宜干燥而不宜潮湿，平时多进行户外活动。衣着应透气散湿，经常晒太阳或进行日光浴。在湿冷的气候条件下，应减少户外活动，避免受寒淋雨，不要过于安逸。运动宜渐进，因形体肥胖，易于困倦，故应根据自己的具体情况循序渐进，长期坚持运动锻炼。"

    hints_f = "<br>\t\t<b>湿热体质</b>的人，面部和鼻尖总是油光发亮，脸上容易生粉刺，皮肤容易瘙痒。常感到口苦、口臭或嘴里有异味，大便粘滞不爽，小便有发热感，尿色发黄，女性常带下色黄，男性阴囊总是潮湿多汗。患病倾向是疮疖、黄疸等病。" \
              "<br>\t\t<b>养生要点：</b>注意清热利湿。" \
              "<br>\t\t<b>对策：</b>食忌辛温滋腻的食物。饮食以清淡为主，可多食赤小豆、绿豆、芹菜、黄瓜、藕等甘寒、甘平的食物。少食羊肉、韭菜、生姜、辣椒、胡椒、花椒等甘温滋腻及火锅、烹炸、烧烤等辛温助热的食物。起居避暑湿，居住环境宜干燥，通风。不要熬夜、过于劳累。盛夏暑湿较重，减少户外活动时间。运动宜增强，适合做大强度、大运动量的锻炼。"

    hints_g = "<br>\t\t<b>血瘀体质</b>的人，面色偏暗，嘴唇颜色偏暗，舌下的静脉瘀紫。皮肤比较粗糙，有时在不知不觉中会出现皮肤淤青。眼睛里的红血丝很多，刷牙是牙龈容易出血。容易烦躁、健忘、性情急躁。" \
              "<br>\t\t<b>养生要点：</b>行气活血，防肿瘤、中风、胸痹等疾病。" \
              "<br>\t\t<b>对策：</b>宜食行气活血的食物，多食山楂、醋、玫瑰花、金橘等具有活血、散结、行气、疏肝解郁作用的食物，少食肥肉等滋腻之品。起居不要过于安逸，以免气机郁滞而致血行不畅，保持足够的睡眠，可早睡早起多锻炼。"

    hints_h = "<br>\t\t<b>气郁体质</b>的人，体形偏瘦，常感闷闷不乐、情绪低沉，容易紧张、焦虑不安，多愁善感，感情脆弱，容易感到害怕或容易受到惊吓，常感到乳房及两胁部胀痛，常有胸闷的感觉，经常无缘无故地叹气，咽喉部经常有堵塞感或异物感，容易失眠。神情抑郁、忧虑脆弱。患病倾向有失眠、抑郁症、神经官能症、乳腺增生等。" \
              "<br>\t\t<b>养生要点：</b>防抑郁症、神经官能症、乳腺增生等疾病。" \
              "<br>\t\t<b>对策：</b>食宜宽胸理气，多食黄花菜、海带、山楂、玫瑰花等具有行气、解郁、消食、醒神食物。起居宜动不宜静，气郁体质的人不要总待在家里，应尽量增加户外活动，居住环境应安静，防止嘈杂的环境影响心情。睡前避免饮茶、咖啡和可可等具有提神醒脑作用的饮料。宜参加群体运动，多参加群众性的体育运动项目，如打球，跳舞，下棋等，以便更多地融入社会。"

    hints_i = "<br>\t\t<b>特禀体质</b>是一类特殊体质特殊的人群。有的即使不感冒也经常鼻塞、打喷嚏、流鼻涕，容易患哮喘。容易对药物、食物、气味、花粉、季节过敏，有的皮肤容易起荨麻疹，皮肤常因过敏出现紫红色瘀点，瘀斑，皮肤常一抓就红，并出现抓痕。" \
              "<br>\t\t<b>养生要点：</b>防哮喘、皮肤疾病。" \
              "<br>\t\t<b>对策：</b>平时只要注意饮食有节、劳逸结合、坚持锻炼即可。"
    hintsarr1.append(hints_a)
    hintsarr1.append(hints_b)
    hintsarr1.append(hints_c)
    hintsarr1.append(hints_d)
    hintsarr1.append(hints_e)
    hintsarr1.append(hints_f)
    hintsarr1.append(hints_g)
    hintsarr1.append(hints_h)
    hintsarr1.append(hints_i)

    hintsarr2.append(hints_b)
    hintsarr2.append(hints_c)
    hintsarr2.append(hints_d)
    hintsarr2.append(hints_e)
    hintsarr2.append(hints_f)
    hintsarr2.append(hints_g)
    hintsarr2.append(hints_h)
    hintsarr2.append(hints_i)

    constution_instruction = "\t\t中医体质分类与判定，以表格形式展现中医体质与判定表供用户选择。针对每一条目为单选，每个选项的分数如下所示:" \
                             "\n\t\t没有(根本不) -> 1分，很少(有一点) -> 2分，有时(有些) -> 3分，经常(相当) -> 4分， 总是(非常) -> 5分" \
                             "\n\t\t( < b > 注：蓝色字选项为反向记分，即从5分到1分</b>)。" \
                             "\n\n\t\t请根据近1年的体验和感觉回答以下问题"
    conclusionBean = {}
    p1ary = physique.split(",")
    c1 = len(p1ary)
    values = []
    Varr = []
    for i in range(0,len(p1ary)):
        c2 = 0
        if i < 5:
            c2 = 8
        elif i == 5:
            c2 = 6
        else:
            c2 = 7
        v1 = getReallyScore(int(p1ary[i]),c2)
        values.append(str(round(v1, 2)))
        Varr.append(round(v1, 2))
        #print(i,p1ary[i],c2,v1)

    strall = ','.join(values)
    str_back_hint = ""
    str_back_conclusion = ""
    j = 0
    #0.平和质，1.气虚质，2.阳虚质，3.阴虚质，4.痰湿质，5.湿热质，6.血瘀质，7.气郁质，8.特禀质

    #print(Varr)
    Varr2 = []
    V1 = Varr[0]
    V2 = Varr[1]
    V3 = Varr[2]
    V4 = Varr[3]
    V5 = Varr[4]
    V6 = Varr[5]
    V7 = Varr[6]
    V8 = Varr[7]
    V9 = Varr[8]
    Varr2.append(V2)
    Varr2.append(V3)
    Varr2.append(V4)
    Varr2.append(V5)
    Varr2.append(V6)
    Varr2.append(V7)
    Varr2.append(V8)
    Varr2.append(V9)

    #arrTop3 = getMaxValue(Varr2, hintsarr2)
    #topV1 = arrTop3[0]['topvalue']
    #获取除了平和质以外的数值的最大值
    maxvalue = 0.00
    for i in range(0, len(Varr2)):
        if (Varr2[i] > maxvalue):
            maxvalue = Varr2[i]
    topV1 = maxvalue
    #判断体质
    '''
        体质类型         条件                  判定结果
        平和质     转化分 >= 60                 是
                  其他 8 种体质转化分均 < 30
                  转化分 >= 60                 基本是
                  其他 8 种体质转化分均 < 40
                  不满足上述条件者               否
        偏颇体质    转化分 >= 40                 是
                  转化分 30 – 39 分             倾向是
                  转化分均 < 30                   否               奇怪，您的体质特征不明显，您还是抽空请医生帮您看一下吧。
    '''
    if V1 >= 60.00 and topV1 < 40:
        if topV1 < 30.00:#是：平和质
            str_back_hint = "您的体质是平和质。很棒哦，请继续保持！"
            str_back_conclusion = hints_a
        else:#是平和质+倾向体质
            str_back_hint = "您的体质基本是平和质。有"
            str_back_conclusion = hints_a
            #0.平和质，1.气虚质，2.阳虚质，3.阴虚质，4.痰湿质，5.湿热质，6.血瘀质，7.气郁质，8.特禀质
            if V2 >= 30.00 and V2 < 40.00:
                str_back_hint += "气虚质、"
                str_back_conclusion += hints_b
            if V3 >= 30.00 and V3 < 40.00:
                str_back_hint += "阳虚质、"
                str_back_conclusion += hints_c
            if V4 >= 30.00 and V4 < 40.00:
                str_back_hint += "阴虚质、"
                str_back_conclusion += hints_d
            if V5 >= 30.00 and V5 < 40.00:
                str_back_hint += "痰湿质、"
                str_back_conclusion += hints_e
            if V6 >= 30.00 and V6 < 40.00:
                str_back_hint += "湿热质、"
                str_back_conclusion += hints_f
            if V7 >= 30.00 and V7 < 40.00:
                str_back_hint += "血瘀质、"
                str_back_conclusion += hints_g
            if V8 >= 30.00 and V8 < 40.00:
                str_back_hint += "气郁质、"
                str_back_conclusion += hints_h
            if V9 >= 30.00 and V9 < 40.00:
                str_back_hint += "特禀质、"
                str_back_conclusion += hints_i
            str_back_hint += "倾向。总的来说，您的身体很棒哦，请继续保持！"
    else:#偏颇体质
        if topV1 < 30.00:
            str_back_hint = "奇怪，您的体质特征不明显，您还是抽空请医生帮您看一下吧。"
            str_back_conclusion = ""
        else:
            str_back_hint1 = "您的体质是"
            str_back_hint2 = ""
            str_back_conclusion = ""
            #0.平和质，1.气虚质，2.阳虚质，3.阴虚质，4.痰湿质，5.湿热质，6.血瘀质，7.气郁质，8.特禀质
            if V2 >= 40.00:
                str_back_hint1 += "气虚质、"
                str_back_conclusion += hints_b
            if V2 >= 30.00 and V2 < 40.00:
                str_back_hint2 += "气虚质、"
                str_back_conclusion += hints_b

            if V3 >= 40.00:
                str_back_hint1 += "阳虚质、"
                str_back_conclusion += hints_c
            if V3 >= 30.00 and V3 < 40.00:
                str_back_hint2 += "阳虚质、"
                str_back_conclusion += hints_c

            if V4 >= 40.00:
                str_back_hint1 += "阳虚质、"
                str_back_conclusion += hints_d
            if V4 >= 30.00 and V4 < 40.00:
                str_back_hint2 += "阴虚质、"
                str_back_conclusion += hints_d

            if V5 >= 40.00:
                str_back_hint1 += "痰湿质、"
                str_back_conclusion += hints_e
            if V5 >= 30.00 and V5 < 40.00:
                str_back_hint2 += "痰湿质、"
                str_back_conclusion += hints_e

            if V6 >= 40.00:
                str_back_hint1 += "湿热质、"
                str_back_conclusion += hints_f
            if V6 >= 30.00 and V6 < 40.00:
                str_back_hint2 += "湿热质、"
                str_back_conclusion += hints_f

            if V7 >= 40.00:
                str_back_hint1 += "血瘀质、"
                str_back_conclusion += hints_g
            if V7 >= 30.00 and V7 < 40.00:
                str_back_hint2 += "血瘀质、"
                str_back_conclusion += hints_g

            if V8 >= 40.00:
                str_back_hint1 += "气郁质、"
                str_back_conclusion += hints_h
            if V8 >= 30.00 and V8 < 40.00:
                str_back_hint2 += "气郁质、"
                str_back_conclusion += hints_h

            if V9 >= 40.00:
                str_back_hint1 += "特禀质、"
                str_back_conclusion += hints_i
            if V9 >= 30.00 and V9 < 40.00:
                str_back_hint2 += "特禀质、"
                str_back_conclusion += hints_i
            str_back_hint = str_back_hint1.rstrip('、') + "。"
            if str_back_hint2 != "":
                str_back_hint += "。有" + str_back_hint2.rstrip('、') + "的混合体质，"
            str_back_hint +=  "比较复杂，您还是抽空时找医生帮您调理一下吧。"

    conclusionBean['id'] = 1
    conclusionBean["conclusion"] = str_back_conclusion
    conclusionBean["hint"] = str_back_hint
    conclusionBean["colorstring"] = strall
    return conclusionBean

def getReallyScore(score: int,count:int) :
    if (score == 0 or score < count):
        return 0
    return (float) (score - count) / (count * 4) * 100

def getUserDeviceWhere(db: Session = Depends(get_db), current_user: Admin = Depends(get_current_user)):
    backWhereStr = ""
    if str.strip(str(current_user.id)) != "" :
        auth_class_id_ary = []
        auth_class_id_str = ""
        filter_query = and_(
             Adminauthclass.admin_id == current_user.id ,
            )
        get_adminauthclass = adminauthclass.get_by_filter(db, filter_query=filter_query)
        if get_adminauthclass:
            for item in get_adminauthclass:
                auth_class_id_ary.append(item.auth_class_id)
        if len(auth_class_id_ary) > 1:
            auth_class_id_str = ",".join('%s' %id for id in auth_class_id_ary)
        else:
            if len(auth_class_id_ary) == 1:
                auth_class_id_str = str(auth_class_id_ary[0])
        if auth_class_id_str != "":
            backWhereStr = " and DV.device_auth_class_id in (" + auth_class_id_str + ")"
    return backWhereStr

def getUserWhere(db: Session = Depends(get_db), current_user: Admin = Depends(get_current_user)):
    backWhereStr = ""
    if str.strip(str(current_user.id)) != "" :
        auth_class_id_ary = []
        auth_class_id_str = ""
        filter_query = and_(
             Adminauthclass.admin_id == current_user.id ,
        )
        get_adminauthclass = adminauthclass.get_by_filter(db, filter_query=filter_query)
        if get_adminauthclass:
            for item in get_adminauthclass:
                auth_class_id_ary.append(item.auth_class_id)
        if len(auth_class_id_ary) > 1:
            auth_class_id_str = ",".join('%s' %id for id in auth_class_id_ary)
        else:
            if len(auth_class_id_ary) == 1:
                auth_class_id_str = str(auth_class_id_ary[0])
        if auth_class_id_str != "":
            backWhereStr = " and DU.deviceid in (select device_code as deviceid from device where device_auth_class_id in (" + auth_class_id_str + "))"
    return backWhereStr