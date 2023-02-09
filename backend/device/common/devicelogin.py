#!/usr/bin/env python3
# _*_ coding: utf-8 _*_
# @Time : 2021/12/28 19:16
# @Author : wdm
# @desc : 登录
import json
from datetime import timedelta

from sqlalchemy.orm import Session
from fastapi.encoders import jsonable_encoder
from fastapi import Body, APIRouter, Depends, Request, Security
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel

from core import settings, create_access_token
from db import RedisPlus
from models import Device
from schemas import ResultModel, Token, DeviceOut
from api.deps import get_redis, get_db, get_current_user, get_current_active_user
from utils import resp_200, SetRedis, ErrorUser, by_ip_get_address
from utils.permission_assign import by_scopes_get_crud

router = APIRouter()

class Fromdata(BaseModel):
    username: str
    password: str
    scope: str

# 这里的登录借助的是OAuth2,与redis存储的token已经没有关系 (前端请求要发送 表单请求)【json请求】
# OAuth2中token过期时间与 设置的时间 以及 服务的开启关闭 有关, 时间到期或者服务关闭token过期
@router.get("/deviceloginstring", response_model=Token, summary="docs接口文档登录 && 登录接口")
async def login_string_access_token(
        username:str,password:str,scope:str,request: Request,db: Session = Depends(get_db)
):
    """
    兼容OAuth2的令牌登录，为接口文档的请求获取访问令牌
    - username: admin
    - password: 123
    """
    scopes = scope.split()

    crud_obj = by_scopes_get_crud(scopes)  # 权限分配
    user = crud_obj.authenticatedevice(db, username=username, password=password)
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
@router.post("/deviceloginjson", response_model=Token, summary="docs接口文档登录 && 登录接口")
async def login_access_token(
        request: Request,
        db: Session = Depends(get_db),
        form_data: Fromdata = Body(
            default={
                "username": "device01",
                "password": "123",
                "scope": "device"
            },
        )
        #form_data: OAuth2PasswordRequestForm = Depends()
):
    """
    兼容OAuth2的令牌登录，为接口文档的请求获取访问令牌
    - username: admin
    - password: 123
    """
    scopes = form_data.scope.split()
    crud_obj = by_scopes_get_crud(scopes)  # 权限分配
    user = crud_obj.authenticatedevice(db, username=form_data.username, password=form_data.password)
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

# 这里的登录借助的是OAuth2,与redis存储的token已经没有关系 (前端请求要发送 表单请求)
# OAuth2中token过期时间与 设置的时间 以及 服务的开启关闭 有关, 时间到期或者服务关闭token过期
@router.post("/devicelogin", response_model=Token, summary="docs接口文档登录 && 登录接口")
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
    crud_obj = by_scopes_get_crud(form_data.scopes)  # 权限分配
    user = crud_obj.authenticatedevice(db, username=form_data.username, password=form_data.password)
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


@router.get("/devicelogin/current_device", response_model=ResultModel[DeviceOut], summary="获取当前管理员")
def get_current_device(current_user: Device = Security(get_current_user, scopes=["device"])):
    return resp_200(data=jsonable_encoder(current_user), msg='获取当前管理员信息！')

@router.post("/devicelogout", response_model=ResultModel, summary="退出登录(已隐藏)", include_in_schema=False)
async def logout_token(request: Request, redis: RedisPlus = Depends(get_redis)):
    if 'authorization' in request.headers.keys():
        token = request.headers.get('authorization')[7:]  # 去除token前面的 Bearer
        await redis.delete(token)
    return resp_200(data='', msg='退出登录')
