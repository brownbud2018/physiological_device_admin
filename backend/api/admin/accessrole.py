#!/usr/bin/env python3
# _*_ coding: utf-8 _*_
# @Time : 2022/11/28 19:18
# @Author : wdm
# @desc : accessrole表接口

from typing import Any, List
from fastapi import APIRouter, Depends, Request
from sqlalchemy import and_, or_
from sqlalchemy.orm import Session

from api.deps import get_db
from schemas import AccessroleUpdate, AccessroleCreate, AccessroleOut, Relation, ResultModel, AccessroleDelete
from crud import accessrole
from utils import resp_200, resp_400, IdNotExist

from models import Accessrole

router = APIRouter()

@router.get("/querybyadminid", response_model=ResultModel[AccessroleOut], summary='查询角色+权限类')
def query_allclassdetail(adminId:int = 0, pageIndex: int = 1, pageSize: int = 10) -> Any:
    where = " where 1=1 "
    if adminId == 0:
        raise IdNotExist(f"没有传递参数.")
    if adminId != 0 :
        where = where + " and role_id in (select role_id from admin where id = " + str(adminId) + ")"
    if pageIndex<1:
        raise IdNotExist(f"页数小于1.")
    if pageSize<1:
        raise IdNotExist(f"每页记录数小于1.")
    limit = " limit " + str((pageIndex - 1) * pageSize) + "," + str(pageSize)
    sql = "select * from admin " + where + limit
    sqlcount = "select count(id) as countid from admin " + where

    data = accessrole.get_data_by_sql(sql)

    if not data:
        raise IdNotExist(f"系统中不存在 相关 的查询结果.")
    for result in data:
        role_id = result["id"]
        where = " where 1=1 and a.role_id = " + str(role_id)
        sql = "select b.* from accessrole a left join access b on a.access_id=b.id " + where
        datachild = accessrole.get_data_by_sql(sql)
        result["child"] = datachild
    count = accessrole.get_count_by_sql(sqlcount)
    backdata = {'count': count, 'dataList': data}
    return {'code': 200, 'data': backdata, 'msg': "查询到了 角色+权限类列表 的查询结果."}

@router.get("/querybyroleid", response_model=ResultModel[AccessroleOut], summary='根据角色ID查询权限类')
def query_auth_by_roleid(roleId:int = 0, pageIndex: int = 1, pageSize: int = 10) -> Any:
    if roleId == 0:
        raise IdNotExist(f"没有传递参数.")
    where = " where 1=1 "
    if roleId != 0 :
        where = where + " and a.role_id = " + str(roleId)
    if pageIndex<1:
        raise IdNotExist(f"页数小于1.")
    if pageSize<1:
        raise IdNotExist(f"每页记录数小于1.")
    limit = " limit " + str((pageIndex - 1) * pageSize) + "," + str(pageSize)
    sql = "select b.* from accessrole a left join access b on a.access_id=b.id " + where + limit
    sqlcount = "select count(b.id) as countid from accessrole a left join access b on a.access_id=b.id " + where
    get_device = accessrole.get_by_sql(sql, sqlcount)
    if not get_device:
        raise IdNotExist(f"系统中不存在 相关 的查询结果.")
    return resp_200(data=get_device, msg=f"查询到了 根据角色ID查询权限类 的查询结果.")

@router.get("/querybyaccessid", response_model=ResultModel[AccessroleOut], summary='根据权限类ID查询角色')
def query_product_by_appproid(accessId:int = 0, pageIndex: int = 1, pageSize: int = 10) -> Any:
    if accessId == 0:
        raise IdNotExist(f"没有传递参数.")
    where = " where 1=1 "
    if accessId != 0 :
        where = where + " and a.access_id = " + str(accessId)
    if pageIndex<1:
        raise IdNotExist(f"页数小于1.")
    if pageSize<1:
        raise IdNotExist(f"每页记录数小于1.")
    limit = " limit " + str((pageIndex - 1) * pageSize) + "," + str(pageSize)
    sql = "select b.* from accessrole a  left join role b on a.role_id=b.id " + where + limit
    sqlcount = "select count(b.id) as countid from accessrole a  left join role b on a.role_id=b.id " + where
    get_device = accessrole.get_by_sql(sql, sqlcount)
    if not get_device:
        raise IdNotExist(f"系统中不存在 相关 的查询结果.")
    return resp_200(data=get_device, msg=f"查询到了 根据权限类ID查询角色 的查询结果.")

@router.get("/", response_model=ResultModel[AccessroleOut], summary='查询角色+权限类')
def query_allaccessrole(pageIndex: int = 1, pageSize: int = 10) -> Any:
    where = " where 1=1 "
    if pageIndex<1:
        raise IdNotExist(f"页数小于1.")
    if pageSize<1:
        raise IdNotExist(f"每页记录数小于1.")
    limit = " limit " + str((pageIndex - 1) * pageSize) + "," + str(pageSize)
    sql = "select * from role " + where + limit
    sqlcount = "select count(id) as countid from role " + where

    data = accessrole.get_data_by_sql(sql)

    if not data:
        raise IdNotExist(f"系统中不存在 相关 的查询结果.")
    for result in data:
        role_id = result["id"]
        where = " where 1=1 and a.role_id = " + str(role_id)
        sql = "select b.* from accessrole a left join access b on a.access_id=b.id " + where
        datachild = accessrole.get_data_by_sql(sql)
        result["child"] = datachild
    count = accessrole.get_count_by_sql(sqlcount)
    backdata = {'count': count, 'dataList': data}
    return {'code': 200, 'data': backdata, 'msg': "查询到了 角色+权限类列表 的查询结果."}

@router.get("/queryweb", response_model=ResultModel[AccessroleOut], summary='根据 条件 查询角色权限信息')
def query_accessrole(ar_name: str = "", role_id: int = 0, access_id: int = 0, pageIndex: int = 1, pageSize: int = 10) -> Any:
    where = " where 1=1 "
    if str.strip(ar_name) != "" :
        where = where + " and (B.role_name like '%%" + str(ar_name) + "%%'"
        where = where + " or C.access_code like '%%" + str(ar_name) + "%%'"
        where = where + " or C.access_name like '%%" + str(ar_name) + "%%')"
    if role_id != 0:
        where = where + " and A.role_id = " + str(role_id)
    if access_id != 0:
        where = where + " and A.access_id = " + str(access_id)
    if pageIndex<1:
        raise IdNotExist(f"页数小于1.")
    if pageSize<1:
        raise IdNotExist(f"每页记录数小于1.")
    order = " order by A.id"
    limit = " limit " + str((pageIndex - 1) * pageSize) + "," + str(pageSize)
    sql = "select A.*,B.role_name,C.access_name,C.access_code from accessrole A left join role B on A.role_id=B.id left join access C on A.access_id=C.id " + where + order + limit
    sqlcount = "select count(A.id) as countid from accessrole A left join role B on A.role_id=B.id left join access C on A.access_id=C.id " + where
    get_accessroles = accessrole.get_by_sql(sql, sqlcount)
    if not get_accessroles:
        raise IdNotExist(f"系统中不存在 角色权限查询关键字 为 {ar_name} 的角色权限结果.")
    return resp_200(data=get_accessroles, msg=f"查询到了 角色权限查询关键字 为 {ar_name} 的角色权限结果.")

@router.post("/updatejson", response_model=ResultModel[AccessroleOut], summary='添加修改角色权限信息')
def update_accessrole_json(*, db: Session = Depends(get_db), accessrole_in: AccessroleCreate) -> Any:
    if accessrole_in.id != 0:
        sqlcount = "select count(id) as countid from accessrole where role_id = " + str(accessrole_in.role_id) + " and access_id = " + str(accessrole_in.access_id) + " and id <> " + str(accessrole_in.id)
        get_exist_count = accessrole.get_by_sql_is_exist(sqlcount)
        if get_exist_count > 0:#已经存在关联，禁止修改
            return {'code': -1, 'data': get_exist_count, 'msg': '已经存在关联！'}
        get_accessrole = accessrole.get(db, id=accessrole_in.id)
        alter_accessrole = accessrole.update(db, db_obj=get_accessrole, obj_in=accessrole_in)
        return resp_200(data=alter_accessrole, msg=f"更新了 id 为 {accessrole_in.id} 的角色权限信息.")
    else:
        sqlcount = "select count(id) as countid from accessrole where role_id = " + str(accessrole_in.role_id) + " and access_id = " + str(accessrole_in.access_id)
        get_exist_count = accessrole.get_by_sql_is_exist(sqlcount)
        if get_exist_count > 0:#已经存在关联，禁止修改
            return {'code': -1, 'data': get_exist_count, 'msg': '已经存在关联！'}
        authabout_in = dict()
        for key,value in accessrole_in:
            if key != "id":
                # 赋值字典
                authabout_in[key] = value
        add_accessrole = accessrole.create(db, obj_in=authabout_in)
        return resp_200(data=add_accessrole, msg=f"添加了 id 为 {add_accessrole.id} 的角色权限信息.")

@router.delete("/delete", response_model=ResultModel[AccessroleOut], summary='通过 id 删除角色权限信息')
def delete_accessrole(*, db: Session = Depends(get_db), accessrole_in: AccessroleDelete) -> Any:
    del_accessrole = accessrole.remove(db, id=accessrole_in.id)
    return resp_200(data=del_accessrole, msg=f"删除了 id 为 {accessrole_in.id} 的角色权限信息.")


