#!/usr/bin/env python3
# _*_ coding: utf-8 _*_
# @Time : 2021/12/28 19:16
# @Author : wdm
# @desc : 登录
from typing import List, Union
import json
from datetime import timedelta,datetime
from dateutil import relativedelta

from sqlalchemy.orm import Session
from sqlalchemy import and_
from fastapi.encoders import jsonable_encoder
from fastapi import Body, APIRouter, Depends, Request, Security
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel

from core import settings, create_access_token
from db import RedisPlus
from models import Admin, Adminauthclass
from schemas import ResultModel, Token, AdminOut
from api.deps import get_redis, get_db, get_current_user, get_current_active_user, format_menu
from utils import resp_200, SetRedis, ErrorUser, by_ip_get_address
from utils.permission_assign import by_scopes_get_crud
from crud import access, device, adminauthclass, dm_user


router = APIRouter()

class Fromdata(BaseModel):
    username: str
    password: str
    scopes: str

# 这里的登录借助的是OAuth2,与redis存储的token已经没有关系 (前端请求要发送 表单请求)
# OAuth2中token过期时间与 设置的时间 以及 服务的开启关闭 有关, 时间到期或者服务关闭token过期
@router.post("/login", response_model=Token, summary="docs接口文档登录 && 登录接口")
async def login_access_token(
        request: Request,
        db: Session = Depends(get_db),
        form_data: OAuth2PasswordRequestForm = Depends()
):
    """
    兼容OAuth2的令牌登录，为接口文档的请求获取访问令牌
    - username: admin
    - password: 123
    """
    #print(form_data.scopes)
    crud_obj = by_scopes_get_crud(form_data.scopes)  # 权限分配
    user = crud_obj.authenticate(db, username=form_data.username, password=form_data.password)
    if not user:
        raise ErrorUser()

    address = by_ip_get_address(request.client.host)  # 根据ip获取地址
    updated_user = crud_obj.update(db, db_obj=user, obj_in={'address': address})

    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    token = create_access_token({"sub": str(updated_user.id), "scopes": form_data.scopes}, access_token_expires)

    #if not request.headers.get('referer').endswith('docs'):  # True: 前端接口 | False: 文档登录
    try:
        await request.app.state.redis.incr('visit_num')  # 用户访问量 自增1
        await request.app.state.redis.set(token, json.dumps(jsonable_encoder(updated_user)), access_token_expires)
    except Exception as e:
        raise SetRedis(f'Redis存储 token 失败！-- {e}')

    return {"access_token": token, "token_type": "bearer"}  # 这里返回的格式一定这么写,否则get_current_user依赖拿不到token

# 这里的登录借助的是OAuth2,与redis存储的token已经没有关系 (前端请求要发送 表单请求)【json请求】
# OAuth2中token过期时间与 设置的时间 以及 服务的开启关闭 有关, 时间到期或者服务关闭token过期
@router.get("/loginstring", response_model=Token, summary="docs接口文档登录 && 登录接口")
async def login_string_access_token(
        username:str,password:str,scope:str,request: Request,db: Session = Depends(get_db)
):
    """
    兼容OAuth2的令牌登录，为接口文档的请求获取访问令牌
    - username: admin
    - password: 123
    """
    #print(scope)
    scopes = scope.split()
    crud_obj = by_scopes_get_crud(scopes)  # 权限分配
    user = crud_obj.authenticate(db, username=username, password=password)
    if not user:
        raise ErrorUser()

    address = by_ip_get_address(request.client.host)  # 根据ip获取地址
    updated_user = crud_obj.update(db, db_obj=user, obj_in={'address': address})

    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    token = create_access_token({"sub": str(updated_user.id), "scopes": scopes}, access_token_expires)

    #if not request.headers.get('referer').endswith('docs'):  # True: 前端接口 | False: 文档登录
    try:
        await request.app.state.redis.incr('visit_num')  # 用户访问量 自增1
        await request.app.state.redis.set(token, json.dumps(jsonable_encoder(updated_user)), access_token_expires)
    except Exception as e:
        raise SetRedis(f'Redis存储 token 失败！-- {e}')

    return {"access_token": token, "token_type": "bearer"}  # 这里返回的格式一定这么写,否则get_current_user依赖拿不到token

# 这里的登录借助的是OAuth2,与redis存储的token已经没有关系 (前端请求要发送 表单请求)【json请求】
# OAuth2中token过期时间与 设置的时间 以及 服务的开启关闭 有关, 时间到期或者服务关闭token过期
@router.post("/loginjson", response_model=Token, summary="docs接口文档登录 && 登录接口")
async def login_access_token(
        request: Request,
        db: Session = Depends(get_db),
        form_data: Fromdata = Body(
            default={
                "username": "admin",
                "password": "123",
                "scopes": "admin"
            },
        )
        #form_data: OAuth2PasswordRequestForm = Depends()
):
    """
    兼容OAuth2的令牌登录，为接口文档的请求获取访问令牌
    - username: admin
    - password: 123
    """
    crud_obj = by_scopes_get_crud(form_data.scopes)  # 权限分配
    user = crud_obj.authenticate(db, username=form_data.username, password=form_data.password)
    if not user:
        raise ErrorUser()

    address = by_ip_get_address(request.client.host)  # 根据ip获取地址
    updated_user = crud_obj.update(db, db_obj=user, obj_in={'address': address})

    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    token = create_access_token({"sub": str(updated_user.id), "scopes": form_data.scopes}, access_token_expires)

    #if not request.headers.get('referer').endswith('docs'):  # True: 前端接口 | False: 文档登录
    try:
        await request.app.state.redis.incr('visit_num')  # 用户访问量 自增1
        await request.app.state.redis.set(token, json.dumps(jsonable_encoder(updated_user)), access_token_expires)
    except Exception as e:
        raise SetRedis(f'Redis存储 token 失败！-- {e}')

    return {"access_token": token, "token_type": "bearer"}  # 这里返回的格式一定这么写,否则get_current_user依赖拿不到token


@router.get("/login/current_admin", response_model=ResultModel[AdminOut], summary="获取当前管理员")
def get_current_admin(current_user: Admin = Security(get_current_user, scopes=["admin"])):
    datauser = jsonable_encoder(current_user)
    data = {}
    data['id'] = datauser['id']
    data['name'] = datauser['name']
    data['image'] = datauser['image']
    data['is_active'] = datauser['is_active']
    data['address'] = datauser['address']
    data['user_type'] = datauser['user_type']
    data['professor_id'] = datauser['professor_id']
    data['role_id'] = datauser['role_id']
    back_item = []
    #获取菜单树
    sql = "select A1.*,A1.id as access_id,A2.access_name as parent_name from access A1 left join access A2 on A1.parent_id=A2.id where A1.id in (select A.id from accessrole A0 left join access A on A0.access_id=A.id where 1=1 and A.is_check=1 and A0.role_id = " + str(datauser['role_id']) + " order by A.id) or A1.id in (select A.parent_id as id from accessrole A0 left join access A on A0.access_id=A.id where 1=1 and A.is_check=1 and A0.role_id = " + str(datauser['role_id']) + " order by A.id)"
    #sql = "select A.*,A.id as access_id,B.access_name as parent_name from accessrole A0 left join access A on A0.access_id=A.id left join access B on A.parent_id=B.id where 1=1 and A.is_check=1 and A0.role_id = " + str(datauser['role_id']) + " order by A.id"
    get_accesss = access.get_by_sql_fetchall(sql)
    if not get_accesss:
        #还没有权限
        back_item=[]
    else:
        back_item = format_menu(get_accesss)
    data['roles'] = back_item#[{'roleName':"Super Admin",'value':"PageNotFound"},{'roleName':"Admin",'value':"Dashboard"},{'roleName':"Admin",'value':"About"}]
    #print(data)
    return {'code': 200, 'data': data, 'msg': '获取当前管理员信息！'}
    #return resp_200(data, msg='获取当前管理员信息！')


@router.get("/login/current_admin_data", response_model=ResultModel[AdminOut], summary="获取当前管理员统计信息")
def get_current_admin_data(
        db: Session = Depends(get_db),
        current_user: Admin = Security(get_current_user, scopes=["admin"])
    ):
    datauser = jsonable_encoder(current_user)
    data = {}
    data['id'] = datauser['id']
    data['name'] = datauser['name']
    where = " where 1=1 "
    if str.strip(str(datauser['id'])) != "" :
        auth_class_id_ary = []
        auth_class_id_str = ""
        filter_query = and_(
             Adminauthclass.admin_id == datauser['id'] ,
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
            where += " and device_auth_class_id in (" + auth_class_id_str + ")"
    sqlcount = "select count(id) as countid from device " + where
    device_count = device.get_by_sql_is_exist(sqlcount)
    data['device_count'] = device_count
    sqlcount = "select count(id) as countid from device " + where + " and is_active = 1"
    device_active_count = device.get_by_sql_is_exist(sqlcount)
    data['device_active_count'] = device_active_count
    sqlcount = "select count(id) as countid from dm_user where deviceid in (select device_code as deviceid from device " + where + " and is_active = 1)"
    dm_user_count = dm_user.get_by_sql_is_exist(sqlcount)
    data['dm_user_count'] = dm_user_count
    sqlcount = "select count(id) as countid from dm_pbloodoxygen where dmuserid in (select id as dmuserid from dm_user where deviceid in (select device_code as deviceid from device " + where + " and is_active = 1))"
    bloodoxygen_count = dm_user.get_by_sql_is_exist(sqlcount)
    data['bloodoxygen_count'] = bloodoxygen_count
    sqlcount = "select count(id) as countid from dm_pbloodoxygen where (spo <= 94 or pulse <50 or pulse > 120) and dmuserid in (select id as dmuserid from dm_user where deviceid in (select device_code as deviceid from device " + where + " and is_active = 1))"
    bloodoxygen_out_count = dm_user.get_by_sql_is_exist(sqlcount)
    data['bloodoxygen_out_count'] = bloodoxygen_out_count
    sqlcount = "select count(id) as countid from dm_pbloodpressure where dmuserid in (select id as dmuserid from dm_user where deviceid in (select device_code as deviceid from device " + where + " and is_active = 1))"
    bloodpressure_count = dm_user.get_by_sql_is_exist(sqlcount)
    data['bloodpressure_count'] = bloodpressure_count
    sqlcount = "select count(id) as countid from dm_pbloodpressure where (sbp < 90 or sbp > 140 or dbp <60 or dbp > 90) and dmuserid in (select id as dmuserid from dm_user where deviceid in (select device_code as deviceid from device " + where + " and is_active = 1))"
    bloodpressure_out_count = dm_user.get_by_sql_is_exist(sqlcount)
    data['bloodpressure_out_count'] = bloodpressure_out_count
    sqlcount = "select count(id) as countid from dm_pbloodsugar where dmuserid in (select id as dmuserid from dm_user where deviceid in (select device_code as deviceid from device " + where + " and is_active = 1))"
    bloodsugar_count = dm_user.get_by_sql_is_exist(sqlcount)
    data['bloodsugar_count'] = bloodsugar_count
    sqlcount = "select count(id) as countid from dm_pbloodsugar where type = 0 and (pmbg <= 24 or pmbg > 61) and dmuserid in (select id as dmuserid from dm_user where deviceid in (select device_code as deviceid from device " + where + " and is_active = 1))"
    bloodsugarpmbg_out_count = dm_user.get_by_sql_is_exist(sqlcount)
    data['bloodsugarpmbg_out_count'] = bloodsugarpmbg_out_count
    sqlcount = "select count(id) as countid from dm_pbloodsugar where type = 1 and (pbg <= 24 or pbg > 77) and dmuserid in (select id as dmuserid from dm_user where deviceid in (select device_code as deviceid from device " + where + " and is_active = 1))"
    bloodsugarpbg_out_count = dm_user.get_by_sql_is_exist(sqlcount)
    data['bloodsugarpbg_out_count'] = bloodsugarpbg_out_count
    sqlcount = "select count(id) as countid from dm_pheartrate where dmuserid in (select id as dmuserid from dm_user where deviceid in (select device_code as deviceid from device " + where + " and is_active = 1))"
    heartrate_count = dm_user.get_by_sql_is_exist(sqlcount)
    data['heartrate_count'] = heartrate_count
    sqlcount = "select count(id) as countid from dm_pheartrate where (heartrate < 50 or heartrate > 120) and dmuserid in (select id as dmuserid from dm_user where deviceid in (select device_code as deviceid from device " + where + " and is_active = 1))"
    heartrate_out_count = dm_user.get_by_sql_is_exist(sqlcount)
    data['heartrate_out_count'] = heartrate_out_count
    sqlcount = "select count(id) as countid from dm_ptemperature where dmuserid in (select id as dmuserid from dm_user where deviceid in (select device_code as deviceid from device " + where + " and is_active = 1))"
    temperature_count = dm_user.get_by_sql_is_exist(sqlcount)
    data['temperature_count'] = temperature_count
    sqlcount = "select count(id) as countid from dm_ptemperature where (temperature < 36.0 or temperature > 37.5) and dmuserid in (select id as dmuserid from dm_user where deviceid in (select device_code as deviceid from device " + where + " and is_active = 1))"
    temperature_out_count = dm_user.get_by_sql_is_exist(sqlcount)
    data['temperature_out_count'] = temperature_out_count
    return {'code': 200, 'data': data, 'msg': '获取当前管理员统计数据！'}

@router.get("/login/current_admin_devie_data", response_model=ResultModel[AdminOut], summary="获取当前管理员设备信息")
def get_current_admin_device_data(
        db: Session = Depends(get_db),
        current_user: Admin = Security(get_current_user, scopes=["admin"])
    ):
    datauser = jsonable_encoder(current_user)
    data = {}
    data['id'] = datauser['id']
    data['name'] = datauser['name']
    where = " where 1=1 "
    if str.strip(str(datauser['id'])) != "" :
        auth_class_id_ary = []
        auth_class_id_str = ""
        filter_query = and_(
             Adminauthclass.admin_id == datauser['id'] ,
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
            where += " and device_auth_class_id in (" + auth_class_id_str + ")"
    n = datetime.now()
    n6 = n - relativedelta.relativedelta(months=6)
    enddate = n.strftime("%Y-%m-%d") + " 23:59:59"
    begindate = n6.strftime("%Y-%m-%d") + " 00:00:00"
    selectcount = "select left(createtime,10) as ctime,count(id) as countid"
    dmwhere = "createtime between '" + begindate + "' and '" + enddate + "' and dmuserid in (select id as dmuserid from dm_user where deviceid in (select device_code as deviceid from device " + where + " and is_active = 1))"
    groupstr = " group by left(createtime,10)" + "\n"
    sqlcount = "select ALLSUM.ctime,ALLSUM.countid as ALLCount,ifnull(OUTSUM.countid,0) as ExceedanceCount," + "\n"
    sqlcount += "   ifnull(A0.countid,0) as OxygenCount0,ifnull(B0.countid,0) as PressureCount0,ifnull(C0.countid,0) as SugarCount0," + "\n"
    sqlcount += "   ifnull(D0.countid,0) as HeartrateCount0,ifnull(E0.countid,0) as TemperatureCount0," + "\n"
    sqlcount += "   ifnull(A.countid,0) as OxygenExceedanceCount,ifnull(B.countid,0) as PressureExceedanceCount,ifnull(C.countid,0) as SugarExceedanceCount," + "\n"
    sqlcount += "   ifnull(C1.countid,0) as SugarExceedanceCount1,ifnull(D.countid,0) as HeartrateExceedanceCount,ifnull(E.countid,0) as TemperatureExceedanceCount from " + "\n"
    sqlcount += "(" + "\n"
    sqlcount += "   select ctime,sum(countid) as countid from (" + "\n"
    sqlcount += "	" + selectcount + " from dm_pbloodoxygen where " + dmwhere + groupstr
    sqlcount += "	union all"
    sqlcount += "	" + selectcount + " from dm_pbloodpressure where " + dmwhere + groupstr
    sqlcount += "	union all"
    sqlcount += "	" + selectcount + " from dm_pbloodsugar where " + dmwhere + groupstr
    sqlcount += "	union all"
    sqlcount += "	" + selectcount + " from dm_pheartrate where " + dmwhere + groupstr
    sqlcount += "	union all"
    sqlcount += "	" + selectcount + " from dm_ptemperature where " + dmwhere + groupstr
    sqlcount += "	) A group by ctime order by ctime" + "\n"
    sqlcount += "   ) ALLSUM left join (" + "\n"
    sqlcount += "   select ctime,sum(countid) as countid from (" + "\n"
    sqlcount += "	" + selectcount + " from dm_pbloodoxygen where (spo <= 94 or pulse <50 or pulse > 120) and " + dmwhere + groupstr
    sqlcount += "	union all"
    sqlcount += "	" + selectcount + " from dm_pbloodpressure where (sbp < 90 or sbp > 140 or dbp <60 or dbp > 90) and " + dmwhere + groupstr
    sqlcount += "	union all"
    sqlcount += "	" + selectcount + " from dm_pbloodsugar where type = 0 and (pmbg <= 24 or pmbg > 61) and " + dmwhere + groupstr
    sqlcount += "	union all"
    sqlcount += "	" + selectcount + " from dm_pbloodsugar where type = 1 and (pbg <= 24 or pbg > 77) and " + dmwhere + groupstr
    sqlcount += "	union all"
    sqlcount += "	" + selectcount + " from dm_pheartrate where (heartrate < 50 or heartrate > 120) and " + dmwhere + groupstr
    sqlcount += "	union all"
    sqlcount += "	" + selectcount + " from dm_ptemperature where (temperature < 36.0 or temperature > 37.5) and " + dmwhere + groupstr
    sqlcount += "       ) A group by ctime order by ctime" + "\n"
    sqlcount += "   ) OUTSUM ON ALLSUM.ctime=OUTSUM.ctime left join (" + "\n"
    sqlcount += "	" + selectcount + " from dm_pbloodoxygen where " + dmwhere + groupstr
    sqlcount += "   ) A0 ON ALLSUM.ctime=A0.ctime left join ("
    sqlcount += "	" + selectcount + " from dm_pbloodpressure where " + dmwhere + groupstr
    sqlcount += "   ) B0 ON ALLSUM.ctime=B0.ctime left join ("
    sqlcount += "       " + selectcount + " from dm_pbloodsugar where " + dmwhere + groupstr
    sqlcount += "   ) C0 ON ALLSUM.ctime=C0.ctime left join ("
    sqlcount += "       " + selectcount + " from dm_pheartrate where " + dmwhere + groupstr
    sqlcount += "   ) D0 ON ALLSUM.ctime=D0.ctime left join ("
    sqlcount += "       " + selectcount + " from dm_ptemperature where " + dmwhere + groupstr
    sqlcount += "   ) E0 ON ALLSUM.ctime=E0.ctime left join ("
    sqlcount += "       " + selectcount + " from dm_pbloodoxygen where (spo <= 94 or pulse <50 or pulse > 120) and " + dmwhere + groupstr
    sqlcount += "   ) A ON ALLSUM.ctime=A.ctime left join ("
    sqlcount += "       " + selectcount + " from dm_pbloodpressure where (sbp < 90 or sbp > 140 or dbp <60 or dbp > 90) and " + dmwhere + groupstr
    sqlcount += "   ) B ON ALLSUM.ctime=B.ctime left join ("
    sqlcount += "       " + selectcount + " from dm_pbloodsugar where type = 0 and (pmbg <= 24 or pmbg > 61)  and " + dmwhere + groupstr
    sqlcount += "   ) C ON ALLSUM.ctime=C.ctime left join ("
    sqlcount += "       " + selectcount + " from dm_pbloodsugar where type = 1 and (pbg <= 24 or pbg > 77) and " + dmwhere + groupstr
    sqlcount += "   ) C1 ON ALLSUM.ctime=C1.ctime left join ("
    sqlcount += "       " + selectcount + " from dm_pheartrate where (heartrate < 50 or heartrate > 120) and " + dmwhere + groupstr
    sqlcount += "   ) D ON ALLSUM.ctime=D.ctime left join ("
    sqlcount += "       " + selectcount + " from dm_ptemperature where (temperature < 36.0 or temperature > 37.5) and " + dmwhere + groupstr
    sqlcount += "   ) E ON ALLSUM.ctime=E.ctime order by left(ALLSUM.ctime,10) asc"
    #print(sqlcount)
    all_count_data = dm_user.get_by_sql_fetchall(sqlcount)
    data['all_count_data'] = all_count_data
    return {'code': 200, 'data': data, 'msg': '获取当前管理员设备数据！'}

@router.get("/login/current_admin_devie_data1", response_model=ResultModel[AdminOut], summary="获取当前管理员设备信息")
def get_current_admin_device_data1(
        db: Session = Depends(get_db),
        current_user: Admin = Security(get_current_user, scopes=["admin"])
    ):
    datauser = jsonable_encoder(current_user)
    data = {}
    data['id'] = datauser['id']
    data['name'] = datauser['name']
    where = " where 1=1 "
    if str.strip(str(datauser['id'])) != "" :
        auth_class_id_ary = []
        auth_class_id_str = ""
        filter_query = and_(
             Adminauthclass.admin_id == datauser['id'] ,
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
            where += " and device_auth_class_id in (" + auth_class_id_str + ")"
    n = datetime.now()
    n6 = n - relativedelta.relativedelta(months=6)
    enddate = n.strftime("%Y-%m-%d") + " 23:59:59"
    begindate = n6.strftime("%Y-%m-%d") + " 00:00:00"
    selectcount = "select dmuserid,count(id) as countid"
    selectcount1 = "select B.deviceid as device_code,count(A.id) as countid"
    dmwhere = "createtime between '" + begindate + "' and '" + enddate + "' and dmuserid in (select id as dmuserid from dm_user where deviceid in (select device_code as deviceid from device " + where + " and is_active = 1))"
    dmwhere1 = "A.createtime between '" + begindate + "' and '" + enddate + "' and A.dmuserid in (select id as dmuserid from dm_user where deviceid in (select device_code as deviceid from device " + where + " and is_active = 1))"
    groupstr = " group by dmuserid" + "\n"
    groupstr1 = " group by B.deviceid" + "\n"
    jointable = " left join dm_user B on A.dmuserid=B.id"
    sqlcount = "select ALLSUM.device_code,ALLSUM.countid as ALLCount,ifnull(OUTSUM.countid,0) as ExceedanceCount," + "\n"
    sqlcount += "   ifnull(A0.countid,0) as OxygenCount0,ifnull(B0.countid,0) as PressureCount0,ifnull(C0.countid,0) as SugarCount0," + "\n"
    sqlcount += "   ifnull(D0.countid,0) as HeartrateCount0,ifnull(E0.countid,0) as TemperatureCount0," + "\n"
    sqlcount += "   ifnull(A.countid,0) as OxygenExceedanceCount,ifnull(B.countid,0) as PressureExceedanceCount,ifnull(C.countid,0) as SugarExceedanceCount," + "\n"
    sqlcount += "   ifnull(C1.countid,0) as SugarExceedanceCount1,ifnull(D.countid,0) as HeartrateExceedanceCount,ifnull(E.countid,0) as TemperatureExceedanceCount from " + "\n"
    sqlcount += "(" + "\n"
    sqlcount += "   select A0.device_code,ifnull(sum(A.countid),0)  as countid from device A0 left join dm_user B on A0.device_code = B.deviceid left join (" + "\n"
    sqlcount += "	" + selectcount + " from dm_pbloodoxygen where " + dmwhere + groupstr
    sqlcount += "	union all"
    sqlcount += "	" + selectcount + " from dm_pbloodpressure where " + dmwhere + groupstr
    sqlcount += "	union all"
    sqlcount += "	" + selectcount + " from dm_pbloodsugar where " + dmwhere + groupstr
    sqlcount += "	union all"
    sqlcount += "	" + selectcount + " from dm_pheartrate where " + dmwhere + groupstr
    sqlcount += "	union all"
    sqlcount += "	" + selectcount + " from dm_ptemperature where " + dmwhere + groupstr
    sqlcount += "	) A on A.dmuserid = B.id group by A0.device_code order by A0.device_code" + "\n"
    sqlcount += "   ) ALLSUM left join (" + "\n"
    sqlcount += "   select A0.device_code,ifnull(sum(A.countid),0)  as countid from device A0 left join dm_user B on A0.device_code = B.deviceid left join (" + "\n"
    sqlcount += "	" + selectcount + " from dm_pbloodoxygen where (spo <= 94 or pulse <50 or pulse > 120) and " + dmwhere + groupstr
    sqlcount += "	union all"
    sqlcount += "	" + selectcount + " from dm_pbloodpressure where (sbp < 90 or sbp > 140 or dbp <60 or dbp > 90) and " + dmwhere + groupstr
    sqlcount += "	union all"
    sqlcount += "	" + selectcount + " from dm_pbloodsugar where type = 0 and (pmbg <= 24 or pmbg > 61) and " + dmwhere + groupstr
    sqlcount += "	union all"
    sqlcount += "	" + selectcount + " from dm_pbloodsugar where type = 1 and (pbg <= 24 or pbg > 77) and " + dmwhere + groupstr
    sqlcount += "	union all"
    sqlcount += "	" + selectcount + " from dm_pheartrate where (heartrate < 50 or heartrate > 120) and " + dmwhere + groupstr
    sqlcount += "	union all"
    sqlcount += "	" + selectcount + " from dm_ptemperature where (temperature < 36.0 or temperature > 37.5) and " + dmwhere + groupstr
    sqlcount += "       ) A on A.dmuserid = B.id group by A0.device_code order by A0.device_code" + "\n"
    sqlcount += "   ) OUTSUM ON ALLSUM.device_code=OUTSUM.device_code left join (" + "\n"
    sqlcount += "	" + selectcount1 + " from dm_pbloodoxygen A " + jointable + " where " + dmwhere1 + groupstr1
    sqlcount += "   ) A0 ON ALLSUM.device_code=A0.device_code left join ("
    sqlcount += "	" + selectcount1 + " from dm_pbloodpressure A " + jointable + " where " + dmwhere1 + groupstr1
    sqlcount += "   ) B0 ON ALLSUM.device_code=B0.device_code left join ("
    sqlcount += "       " + selectcount1 + " from dm_pbloodsugar A " + jointable + " where " + dmwhere1 + groupstr1
    sqlcount += "   ) C0 ON ALLSUM.device_code=C0.device_code left join ("
    sqlcount += "       " + selectcount1 + " from dm_pheartrate A " + jointable + " where " + dmwhere1 + groupstr1
    sqlcount += "   ) D0 ON ALLSUM.device_code=D0.device_code left join ("
    sqlcount += "       " + selectcount1 + " from dm_ptemperature A " + jointable + " where " + dmwhere1 + groupstr1
    sqlcount += "   ) E0 ON ALLSUM.device_code=E0.device_code left join ("
    sqlcount += "       " + selectcount1 + " from dm_pbloodoxygen A " + jointable + " where (spo <= 94 or pulse <50 or pulse > 120) and " + dmwhere1 + groupstr1
    sqlcount += "   ) A ON ALLSUM.device_code=A.device_code left join ("
    sqlcount += "       " + selectcount1 + " from dm_pbloodpressure A " + jointable + " where (sbp < 90 or sbp > 140 or dbp <60 or dbp > 90) and " + dmwhere1 + groupstr1
    sqlcount += "   ) B ON ALLSUM.device_code=B.device_code left join ("
    sqlcount += "       " + selectcount1 + " from dm_pbloodsugar A " + jointable + " where type = 0 and (pmbg <= 24 or pmbg > 61)  and " + dmwhere1 + groupstr1
    sqlcount += "   ) C ON ALLSUM.device_code=C.device_code left join ("
    sqlcount += "       " + selectcount1 + " from dm_pbloodsugar A " + jointable + " where type = 1 and (pbg <= 24 or pbg > 77) and " + dmwhere1 + groupstr1
    sqlcount += "   ) C1 ON ALLSUM.device_code=C1.device_code left join ("
    sqlcount += "       " + selectcount1 + " from dm_pheartrate A " + jointable + " where (heartrate < 50 or heartrate > 120) and " + dmwhere1 + groupstr1
    sqlcount += "   ) D ON ALLSUM.device_code=D.device_code left join ("
    sqlcount += "       " + selectcount1 + " from dm_ptemperature A " + jointable + " where (temperature < 36.0 or temperature > 37.5) and " + dmwhere1 + groupstr1
    sqlcount += "   ) E ON ALLSUM.device_code=E.device_code where ALLSUM.countid > 0 order by ALLSUM.countid asc"
    #print(sqlcount)
    all_count_data = dm_user.get_by_sql_fetchall(sqlcount)
    data['all_count_data'] = all_count_data
    return {'code': 200, 'data': data, 'msg': '获取当前管理员设备数据！'}

@router.get("/login/current_admin_devie_data2", response_model=ResultModel[AdminOut], summary="获取当前管理员设备信息")
def get_current_admin_device_data2(
        db: Session = Depends(get_db),
        current_user: Admin = Security(get_current_user, scopes=["admin"])
    ):
    datauser = jsonable_encoder(current_user)
    data = {}
    data['id'] = datauser['id']
    data['name'] = datauser['name']
    where = " where 1=1 "
    if str.strip(str(datauser['id'])) != "" :
        auth_class_id_ary = []
        auth_class_id_str = ""
        filter_query = and_(
             Adminauthclass.admin_id == datauser['id'] ,
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
            where += " and device_auth_class_id in (" + auth_class_id_str + ")"
    n = datetime.now()
    n6 = n - relativedelta.relativedelta(months=6)
    enddate = n.strftime("%Y-%m-%d") + " 23:59:59"
    begindate = n6.strftime("%Y-%m-%d") + " 00:00:00"
    selectcount = "select dmuserid,count(id) as countid"
    dmwhere = "createtime between '" + begindate + "' and '" + enddate + "' and dmuserid in (select id as dmuserid from dm_user where deviceid in (select device_code as deviceid from device " + where + " and is_active = 1))"
    groupstr = " group by dmuserid" + "\n"
    sqlcount = "select ALLSUM.dmuserid,DU.`name` as username,ALLSUM.countid as ALLCount,ifnull(OUTSUM.countid,0) as ExceedanceCount," + "\n"
    sqlcount += "   ifnull(A0.countid,0) as OxygenCount0,ifnull(B0.countid,0) as PressureCount0,ifnull(C0.countid,0) as SugarCount0," + "\n"
    sqlcount += "   ifnull(D0.countid,0) as HeartrateCount0,ifnull(E0.countid,0) as TemperatureCount0," + "\n"
    sqlcount += "   ifnull(A.countid,0) as OxygenExceedanceCount,ifnull(B.countid,0) as PressureExceedanceCount,ifnull(C.countid,0) as SugarExceedanceCount," + "\n"
    sqlcount += "   ifnull(C1.countid,0) as SugarExceedanceCount1,ifnull(D.countid,0) as HeartrateExceedanceCount,ifnull(E.countid,0) as TemperatureExceedanceCount from " + "\n"
    sqlcount += "(" + "\n"
    sqlcount += "   select A.dmuserid as dmuserid,ifnull(sum(A.countid),0)  as countid from (" + "\n"
    sqlcount += "	" + selectcount + " from dm_pbloodoxygen where " + dmwhere + groupstr
    sqlcount += "	union all"
    sqlcount += "	" + selectcount + " from dm_pbloodpressure where " + dmwhere + groupstr
    sqlcount += "	union all"
    sqlcount += "	" + selectcount + " from dm_pbloodsugar where " + dmwhere + groupstr
    sqlcount += "	union all"
    sqlcount += "	" + selectcount + " from dm_pheartrate where " + dmwhere + groupstr
    sqlcount += "	union all"
    sqlcount += "	" + selectcount + " from dm_ptemperature where " + dmwhere + groupstr
    sqlcount += "	) A group by A.dmuserid order by A.dmuserid" + "\n"
    sqlcount += "   ) ALLSUM left join (" + "\n"
    sqlcount += "   select A.dmuserid as dmuserid,ifnull(sum(A.countid),0)  as countid from (" + "\n"
    sqlcount += "	" + selectcount + " from dm_pbloodoxygen where (spo <= 94 or pulse <50 or pulse > 120) and " + dmwhere + groupstr
    sqlcount += "	union all"
    sqlcount += "	" + selectcount + " from dm_pbloodpressure where (sbp < 90 or sbp > 140 or dbp <60 or dbp > 90) and " + dmwhere + groupstr
    sqlcount += "	union all"
    sqlcount += "	" + selectcount + " from dm_pbloodsugar where type = 0 and (pmbg <= 24 or pmbg > 61) and " + dmwhere + groupstr
    sqlcount += "	union all"
    sqlcount += "	" + selectcount + " from dm_pbloodsugar where type = 1 and (pbg <= 24 or pbg > 77) and " + dmwhere + groupstr
    sqlcount += "	union all"
    sqlcount += "	" + selectcount + " from dm_pheartrate where (heartrate < 50 or heartrate > 120) and " + dmwhere + groupstr
    sqlcount += "	union all"
    sqlcount += "	" + selectcount + " from dm_ptemperature where (temperature < 36.0 or temperature > 37.5) and " + dmwhere + groupstr
    sqlcount += "       ) A group by A.dmuserid order by A.dmuserid" + "\n"
    sqlcount += "   ) OUTSUM ON ALLSUM.dmuserid=OUTSUM.dmuserid left join (" + "\n"
    selectcount1 = "select A.dmuserid,count(A.id) as countid"
    dmwhere1 = "A.createtime between '" + begindate + "' and '" + enddate + "' and A.dmuserid in (select id as dmuserid from dm_user where deviceid in (select device_code as deviceid from device " + where + " and is_active = 1))"
    groupstr1 = " group by A.dmuserid" + "\n"
    sqlcount += "	" + selectcount1 + " from dm_pbloodoxygen A where " + dmwhere1 + groupstr1
    sqlcount += "   ) A0 ON ALLSUM.dmuserid=A0.dmuserid left join ("
    sqlcount += "	" + selectcount1 + " from dm_pbloodpressure A where " + dmwhere1 + groupstr1
    sqlcount += "   ) B0 ON ALLSUM.dmuserid=B0.dmuserid left join ("
    sqlcount += "       " + selectcount1 + " from dm_pbloodsugar A where " + dmwhere1 + groupstr1
    sqlcount += "   ) C0 ON ALLSUM.dmuserid=C0.dmuserid left join ("
    sqlcount += "       " + selectcount1 + " from dm_pheartrate A where " + dmwhere1 + groupstr1
    sqlcount += "   ) D0 ON ALLSUM.dmuserid=D0.dmuserid left join ("
    sqlcount += "       " + selectcount1 + " from dm_ptemperature A where " + dmwhere1 + groupstr1
    sqlcount += "   ) E0 ON ALLSUM.dmuserid=E0.dmuserid left join ("
    sqlcount += "       " + selectcount1 + " from dm_pbloodoxygen A where (spo <= 94 or pulse <50 or pulse > 120) and " + dmwhere1 + groupstr1
    sqlcount += "   ) A ON ALLSUM.dmuserid=A.dmuserid left join ("
    sqlcount += "       " + selectcount1 + " from dm_pbloodpressure A where (sbp < 90 or sbp > 140 or dbp <60 or dbp > 90) and " + dmwhere1 + groupstr1
    sqlcount += "   ) B ON ALLSUM.dmuserid=B.dmuserid left join ("
    sqlcount += "       " + selectcount1 + " from dm_pbloodsugar A where type = 0 and (pmbg <= 24 or pmbg > 61)  and " + dmwhere1 + groupstr1
    sqlcount += "   ) C ON ALLSUM.dmuserid=C.dmuserid left join ("
    sqlcount += "       " + selectcount1 + " from dm_pbloodsugar A where type = 1 and (pbg <= 24 or pbg > 77) and " + dmwhere1 + groupstr1
    sqlcount += "   ) C1 ON ALLSUM.dmuserid=C1.dmuserid left join ("
    sqlcount += "       " + selectcount1 + " from dm_pheartrate A where (heartrate < 50 or heartrate > 120) and " + dmwhere1 + groupstr1
    sqlcount += "   ) D ON ALLSUM.dmuserid=D.dmuserid left join ("
    sqlcount += "       " + selectcount1 + " from dm_ptemperature A where (temperature < 36.0 or temperature > 37.5) and " + dmwhere1 + groupstr1
    sqlcount += "   ) E ON ALLSUM.dmuserid=E.dmuserid left join dm_user DU ON ALLSUM.dmuserid=DU.id"
    sqlcount += " where ALLSUM.countid > 0 order by ALLSUM.countid asc"
    #print(sqlcount)
    all_count_data = dm_user.get_by_sql_fetchall(sqlcount)
    data['all_count_data'] = all_count_data
    return {'code': 200, 'data': data, 'msg': '获取当前管理员设备数据！'}

@router.get("/login/current_admin_cn", response_model=ResultModel[AdminOut], summary="获取当前管理员全国设备分布信息")
def get_current_admin_cn(
        db: Session = Depends(get_db),
        current_user: Admin = Security(get_current_user, scopes=["admin"])
    ):
    datauser = jsonable_encoder(current_user)
    data = {}
    data['id'] = datauser['id']
    data['name'] = datauser['name']
    where = " where 1=1 "
    if str.strip(str(datauser['id'])) != "" :
        auth_class_id_ary = []
        auth_class_id_str = ""
        filter_query = and_(
             Adminauthclass.admin_id == datauser['id'] ,
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
            where += " and device_auth_class_id in (" + auth_class_id_str + ")"
    dmwhere = where + " and is_active = 1"
    groupstr = " group by A.provinceid,B.province" + "\n"
    sqlcount = "select A.provinceid,B.province,count(A.id) as countid" + "\n"
    sqlcount += "   from device A left join provinces B on A.provinceid=B.provinceid " + dmwhere + groupstr
    #print(sqlcount)
    all_count_data = device.get_by_sql_fetchall(sqlcount)
    data['all_count_data'] = all_count_data
    return {'code': 200, 'data': data, 'msg': '获取当前管理员全国设备分布数据！'}

@router.post("/logout", response_model=ResultModel, summary="退出登录(已隐藏)", include_in_schema=False)
async def logout_token(request: Request, redis: RedisPlus = Depends(get_redis)):
    if 'authorization' in request.headers.keys():
        token = request.headers.get('authorization')[7:]  # 去除token前面的 Bearer
        await redis.delete(token)
    return resp_200(data='', msg='退出登录')

