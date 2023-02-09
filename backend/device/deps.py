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
from crud import device
from db import MySuperContextManager, RedisPlus
from models import Device
from schemas import TokenData
from utils import PermissionNotEnough, UserNotExist
from utils.permission_assign import by_scopes_get_crud, handle_oauth2_scopes

get_token = OAuth2PasswordBearer(tokenUrl=f"{settings.API_PREFIX}/login", scopes=handle_oauth2_scopes())

async def get_db() -> Generator:
    """ 数据库连接对象 """
    with MySuperContextManager() as db:
        yield db


def get_redis(request: Request) -> RedisPlus:
    """ redis连接对象 """
    return request.app.state.redis


def get_current_user1(security_scopes: SecurityScopes, db: Session = Depends(get_db), token: str = Depends(get_token)):
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


def get_current_active_user(current_user: Device = Security(get_current_user1, scopes=["device"])):
    """ 得到当前登录用户 """
    if not device.is_active_def(current_user):
        raise HTTPException(status_code=400, detail="用户未登录！！！")
    return current_user
