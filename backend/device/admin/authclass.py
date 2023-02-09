#!/usr/bin/env python3
# _*_ coding: utf-8 _*_
# @Time : 2022/11/28 19:18
# @Author : wdm
# @desc : 授权类表接口

from typing import Any, List
from fastapi import APIRouter, Depends, Request, Form
from sqlalchemy import and_, or_
from sqlalchemy.orm import Session

from device.deps import get_db
from schemas import AuthclassUpdate, AuthclassCreate, AuthclassOut, Relation, ResultModel, AuthclassDelete
from crud import authclass
from utils import resp_200, resp_400, IdNotExist

from models import Authclass

router = APIRouter()

@router.post("/query", response_model=ResultModel[AuthclassOut], summary='根据 条件 查询授权类信息')
def query_authclass(name: str = "", type: int = 0, pageIndex: int = 1, pageSize: int = 10) -> Any:
    where = " where 1=1 "
    if str.strip(name) != "" :
        where = where + " and (class_code like '%%" + str(name) + "%%' or class_name like '%%" + str(name) + "%%' or class_remark like '%%" + str(name) + "%%')"
    else:
        raise IdNotExist(f"查询关键字必须.")
    where = where + " and pro_type = " + str(type)
    if pageIndex<1:
        raise IdNotExist(f"页数小于1.")
    if pageSize<1:
        raise IdNotExist(f"每页记录数小于1.")
    limit = " limit " + str((pageIndex - 1) * pageSize) + "," + str(pageSize)
    sql = "select * from authclass " + where + limit
    sqlcount = "select count(id) as countid from authclass " + where
    get_authclasss = authclass.get_by_sql(sql, sqlcount)
    if not get_authclasss:
        raise IdNotExist(f"系统中不存在 授权类查询关键字 为 {name} 的授权类结果.")
    return resp_200(data=get_authclasss, msg=f"查询到了 授权类查询关键字 为 {name} 的授权类结果.")

@router.post("/querybyauthclassid", response_model=ResultModel[AuthclassOut], summary='根据 条件 查询授权类信息')
def query_authclass_id(authclassId: int = 0, pageIndex: int = 1, pageSize: int = 10, db: Session = Depends(get_db)) -> Any:
    if authclassId != 0 :
        filter_query = (Authclass.id == authclassId)
        get_authclass = authclass.get_by_page_filter(db, filter_query=filter_query, pageIndex=pageIndex, pageSize=pageSize )
        if not get_authclass:
            raise IdNotExist(f"系统中不存在 ID 为 {authclassId} 的授权类结果.")
        return resp_200(data=get_authclass, msg=f"查询到了 ID 为 {authclassId} 的授权类结果.")
    else:
        return resp_400()

@router.post("/querybyname", response_model=ResultModel[AuthclassOut], summary='根据 条件 查询授权类信息')
def query_authclass_name(name: str = "", pageIndex: int = 1, pageSize: int = 10, db: Session = Depends(get_db)) -> Any:
    if str.strip(name) != "" :
        filter_query = or_ (
             Authclass.class_code.like('%' + name + '%') ,
             Authclass.class_name.like('%' + name + '%') ,
             Authclass.class_remark.like('%' + name + '%') ,
            )
        get_authclass = authclass.get_by_page_filter(db, filter_query=filter_query, pageIndex=pageIndex, pageSize=pageSize )
        if not get_authclass:
            raise IdNotExist(f"系统中不存在 条件 为 {name} 的授权类结果.")
        return resp_200(data=get_authclass, msg=f"查询到了 条件 为 {name} 的授权类结果.")
    else :
        raise IdNotExist(f"没有传递 条件 值.")

@router.get("/", response_model=ResultModel[AuthclassOut], summary='查询所有授权类(根据页码和每页个数)')
def read_authclasss(db: Session = Depends(get_db), pageIndex: int = 1, pageSize: int = 10) -> Any:
    get_authclasss = authclass.get_multi(db, pageIndex=pageIndex, pageSize=pageSize)
    return resp_200(data=get_authclasss, msg=f"查询了第 {pageIndex} 页中的 {pageSize} 个授权类信息.")

@router.get("/queryweb", response_model=ResultModel[AuthclassOut], summary='根据 条件 查询授权信息')
def query_authclass(class_name: str = "", pageIndex: int = 1, pageSize: int = 10) -> Any:
    where = " where 1=1 "
    if str.strip(class_name) != "" :
        where = where + " and (class_code like '%%" + str(class_name) + "%%' or class_name like '%%" + str(class_name) + "%%' or class_remark like '%%" + str(class_name) + "%%')"
    if pageIndex<1:
        return {'code': -1, 'data': pageIndex, 'msg': f'页数:{pageIndex}小于1'}
    if pageSize<1:
        return {'code': -1, 'data': pageSize, 'msg': f'每页记录数:{pageSize}小于1'}
    limit = " limit " + str((pageIndex - 1) * pageSize) + "," + str(pageSize)
    sql = "select A.* from authclass A " + where + limit
    sqlcount = "select count(id) as countid from authclass " + where
    get_authclasss = authclass.get_by_sql(sql, sqlcount)
    if not get_authclasss:
        return {'code': -1, 'data': pageSize, 'msg': f"系统中不存在 授权查询关键字 为 {class_name} 的授权结果."}
    return resp_200(data=get_authclasss, msg=f"查询到了 授权查询关键字 为 {class_name} 的授权结果.")

@router.get("/qtree", response_model=ResultModel[AuthclassOut], summary='根据 条件 查询授权信息')
def query_authclass_tree(class_name: str = "") -> Any:
    where = " where 1=1 "
    if str.strip(class_name) != "" :
        where = where + " and (class_code like '%%" + str(class_name) + "%%' or class_name like '%%" + str(class_name) + "%%' or class_remark like '%%" + str(class_name) + "%%')"
    sql = "select *,id as class_id,id as device_auth_class_id,id as auth_class_id from authclass " + where
    get_authclasss = authclass.get_by_sql_no_count(sql)
    if not get_authclasss:
        return {'code': -1, 'data': get_authclasss, 'msg': f"系统中不存在 授权类查询关键字 为 {class_name} 的授权类结果."}
    return resp_200(data=get_authclasss, msg=f"查询到了 授权查询关键字 为 {class_name} 的授权结果.")

@router.post("/updatejson", response_model=ResultModel[AuthclassOut], summary='添加授权信息')
def update_authclass_json(*, db: Session = Depends(get_db), authclass_in: AuthclassCreate) -> Any:
    if authclass_in.id != 0:
        get_authclass = authclass.get(db, id=authclass_in.id)
        alter_authclass = authclass.update(db, db_obj=get_authclass, obj_in=authclass_in)
        return resp_200(data=alter_authclass, msg=f"更新了 id 为 {id} 的授权信息.")
    else:
        class_in = dict()
        for key,value in authclass_in:
            if key != "id":
                # 赋值字典
                class_in[key] = value
        add_authclass = authclass.create(db, obj_in=class_in)
        return resp_200(data=add_authclass, msg=f"添加了 id 为 {add_authclass.id} 的授权信息.")

@router.post("/updateform", response_model=ResultModel[AuthclassOut], summary='添加授权信息')
def update_authclass_form(*, id: int = Form(...), class_code: str = Form(...), class_name: str = Form(...), class_type: int = Form(...), class_image: str = Form(...), class_remark: str = Form(...)) -> Any: #, authclass_in: ProductCreate
    print('id'+ str(id))
    print(id)
    print('class_code' + str(class_code))
    print('class_name' + str(class_name))
    print('class_type' + str(class_type))
    print('class_image' + str(class_image))
    print('class_remark' + str(class_remark))
    if id != 0:
        raise IdNotExist(f"修改.")
    else:
        raise IdNotExist(f"ID:{id}新增.")

@router.delete("/delete", response_model=ResultModel[AuthclassOut], summary='通过 id 删除授权信息')
def delete_authclass(*, db: Session = Depends(get_db), class_id: AuthclassDelete) -> Any:
    del_authclass = authclass.remove(db, id=class_id.id)
    return resp_200(data=del_authclass, msg=f"删除了 id 为 {class_id.id} 的授权信息.")

@router.get("/querybyid", response_model=ResultModel[AuthclassOut], summary='根据 条件 查询授权信息')
def query_authclass_id(class_id: int = 0) -> Any:
    where = " where 1=1 "
    if class_id != 0 :
        where = where + " and A.id=" + str(class_id)
        sql = "select A.* from authclass A " + where
        get_authclasss = authclass.get_by_sql_no_count(sql)
        if not get_authclasss:
            return {'code': -1, 'data': get_authclasss, 'msg': f"系统中不存在 授权查询关键字 为 {class_id} 的授权结果."}
        return resp_200(data=get_authclasss, msg=f"查询到了 授权查询关键字 为 {class_id} 的授权结果.")
    else:
        return resp_400()

