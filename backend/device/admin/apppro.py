#!/usr/bin/env python3
# _*_ coding: utf-8 _*_
# @Time : 2022/11/28 19:18
# @Author : wdm
# @desc : 院系表接口

from typing import Any, List
from fastapi import APIRouter, Depends, Request, Form
from sqlalchemy import and_, or_
from sqlalchemy.orm import Session

from device.deps import get_db
from schemas import AppproUpdate, AppproCreate, AppproOut, Relation, ResultModel, AppproDelete, AppproType, AppproUpdateType
from crud import apppro
from utils import resp_200, resp_400, IdNotExist

from models import Apppro

router = APIRouter()

@router.post("/query", response_model=ResultModel[AppproOut], summary='根据 条件 查询APP信息')
def query_apppro(name: str = "", type: int = 0, appproId: int = 0, appclassId: int = 0, pageIndex: int = 1, pageSize: int = 10) -> Any:
    where = " where 1=1 "
    if str.strip(name) != "" :
        where = where + " and (app_code like '%%" + str(name) + "%%' or app_name like '%%" + str(name) + "%%' or app_remark like '%%" + str(name) + "%%')"
    where = where + " and app_type = " + str(type)
    if appclassId != 0 :
        where = where + " and app_class_id = " + str(appclassId)
    if appproId != 0 :
        where = where + " and id = " + str(appproId)
    if pageIndex<1:
        raise IdNotExist(f"页数小于1.")
    if pageSize<1:
        raise IdNotExist(f"每页记录数小于1.")
    limit = " limit " + str((pageIndex - 1) * pageSize) + "," + str(pageSize)
    sql = "select * from apppro " + where + limit
    sqlcount = "select count(id) as countid from apppro " + where
    get_apppro = apppro.get_by_sql(sql, sqlcount)
    if not get_apppro:
        raise IdNotExist(f"系统中不存在 APP查询关键字 为 {name} 的APP结果.")
    return resp_200(data=get_apppro, msg=f"查询到了 综合查询 的APP结果.")

@router.post("/querybyappproid", response_model=ResultModel[AppproOut], summary='根据 条件 查询APP类信息')
def query_apppro_id(appproId: int = 0, pageIndex: int = 1, pageSize: int = 10, db: Session = Depends(get_db)) -> Any:
    if appproId != 0 :
        filter_query = (Apppro.id == appproId)
        get_apppro = apppro.get_by_page_filter(db, filter_query=filter_query, pageIndex=pageIndex, pageSize=pageSize )
        if not get_apppro:
            raise IdNotExist(f"系统中不存在 ID 为 {appproId} 的APP类结果.")
        return resp_200(data=get_apppro, msg=f"查询到了 ID 为 {appproId} 的APP类结果.")
    else:
        return resp_400()

@router.post("/querybyappclassid", response_model=ResultModel[AppproOut], summary='根据 APPID 查询APP信息')
def query_apppro_id(appclassId: int = 0, pageIndex: int = 1, pageSize: int = 10, db: Session = Depends(get_db)) -> Any:
    if appclassId != 0 :
        filter_query = (Apppro.app_class_id == appclassId)
        get_apppro = apppro.get_by_page_filter(db, filter_query=filter_query, pageIndex=pageIndex, pageSize=pageSize )
        if not get_apppro:
            raise IdNotExist(f"系统中不存在 APPID 为 {appclassId} 的APP结果.")
        return resp_200(data=get_apppro, msg=f"查询到了 APPID 为 {appclassId} 的APP结果.")
    else:
        return resp_400()

@router.post("/querybyname", response_model=ResultModel[AppproOut], summary='根据 条件 查询APP类信息')
def query_apppro_name(name: str = "", pageIndex: int = 1, pageSize: int = 10, db: Session = Depends(get_db)) -> Any:
    if str.strip(name) != "" :
        filter_query = or_ (
             Apppro.app_code.like('%' + name + '%') ,
             Apppro.app_name.like('%' + name + '%') ,
             Apppro.app_remark.like('%' + name + '%') ,
            )
        get_apppro = apppro.get_by_page_filter(db, filter_query=filter_query, pageIndex=pageIndex, pageSize=pageSize )
        if not get_apppro:
            raise IdNotExist(f"系统中不存在 条件 为 {name} 的APP类结果.")
        return resp_200(data=get_apppro, msg=f"查询到了 条件 为 {name} 的APP类结果.")
    else :
        raise IdNotExist(f"没有传递 条件 值.")

@router.get("/", response_model=ResultModel[AppproOut], summary='查询所有APP类(根据页码和每页个数)')
def read_apppros(db: Session = Depends(get_db), pageIndex: int = 1, pageSize: int = 10) -> Any:
    get_apppros = apppro.get_multi(db, pageIndex=pageIndex, pageSize=pageSize)
    return resp_200(data=get_apppros, msg=f"查询了第 {pageIndex} 页中的 {pageSize} 个APP类信息.")

@router.get("/queryweb", response_model=ResultModel[AppproOut], summary='根据 条件 查询APP信息')
def query_apppro(app_name: str = "", app_class_id: int = 0, pageIndex: int = 1, pageSize: int = 10) -> Any:
    where = " where 1=1 "
    if str.strip(app_name) != "" :
        where = where + " and (app_code like '%%" + str(app_name) + "%%' or app_name like '%%" + str(app_name) + "%%' or app_remark like '%%" + str(app_name) + "%%')"
    if app_class_id != 0:
        where = where + " and app_class_id = " + str(app_class_id)
    if pageIndex<1:
        raise IdNotExist(f"页数小于1.")
    if pageSize<1:
        raise IdNotExist(f"每页记录数小于1.")
    limit = " limit " + str((pageIndex - 1) * pageSize) + "," + str(pageSize)
    sql = "select A.*,B.class_name from apppro A left join appclass B on A.app_class_id=B.id" + where + limit
    sqlcount = "select count(id) as countid from apppro " + where
    get_apppros = apppro.get_by_sql(sql, sqlcount)
    if not get_apppros:
        raise IdNotExist(f"系统中不存在 APP查询关键字 为 {app_name} 的APP结果.")
    return resp_200(data=get_apppros, msg=f"查询到了 APP查询关键字 为 {app_name} 的APP结果.")

@router.get("/qtree", response_model=ResultModel[AppproOut], summary='根据 条件 查询APP分类信息')
def query_apppro_tree(app_name: str = "") -> Any:
    where = " where 1=1 "
    if str.strip(app_name) != "" :
        where = where + " and (app_code like '%%" + str(app_name) + "%%' or app_name like '%%" + str(app_name) + "%%' or app_remark like '%%" + str(app_name) + "%%')"
    sql = "select *,id as app_id,id as app_pro_id from apppro " + where
    get_apppros = apppro.get_by_sql_no_count(sql)
    if not get_apppros:
        raise IdNotExist(f"系统中不存在 项目类查询关键字 为 {app_name} 的APP分类结果.")
    #return {'code': 200, 'data': get_apppros, 'message': f"查询到了 项目类查询关键字 为 {pro_name} 的项目类结果.", 'type': 'success'}
    return resp_200(data=get_apppros, msg=f"查询到了APP分类结果.")

@router.post("/updatejson", response_model=ResultModel[AppproOut], summary='添加APP信息')
def update_apppro_json(*, db: Session = Depends(get_db), apppro_in: AppproCreate) -> Any:
    print(apppro_in)
    if apppro_in.id != 0:
        get_apppro = apppro.get(db, id=apppro_in.id)
        alter_apppro = apppro.update(db, db_obj=get_apppro, obj_in=apppro_in)
        return resp_200(data=alter_apppro, msg=f"更新了 id 为 {id} 的APP信息.")
    else:
        app_in = dict()
        for key,value in apppro_in:
            if key != "id":
                # 赋值字典
                app_in[key] = value
        add_apppro = apppro.create(db, obj_in=app_in)
        return resp_200(data=add_apppro, msg=f"添加了 id 为 {add_apppro.id} 的APP信息.")

@router.post("/updateform", response_model=ResultModel[AppproOut], summary='添加APP信息')
def update_apppro_form(*, id: int = Form(...), app_code: str = Form(...), app_name: str = Form(...), app_type: int = Form(...), app_image: str = Form(...), app_remark: str = Form(...)) -> Any: #, apppro_in: ProductCreate
    print('id'+ str(id))
    print(id)
    print('app_code' + str(app_code))
    print('app_name' + str(app_name))
    print('app_type' + str(app_type))
    print('app_image' + str(app_image))
    print('app_remark' + str(app_remark))
    if id != 0:
        raise IdNotExist(f"修改.")
    else:
        raise IdNotExist(f"ID:{id}新增.")

@router.delete("/delete", response_model=ResultModel[AppproOut], summary='通过 id 删除APP信息')
def delete_apppro(*, db: Session = Depends(get_db), app_id: AppproDelete) -> Any:
    del_apppro = apppro.remove(db, id=app_id.id)
    return resp_200(data=del_apppro, msg=f"删除了 id 为 {app_id.id} 的APP信息.")

@router.get("/querybyid", response_model=ResultModel[AppproOut], summary='根据 条件 查询APP信息')
def query_apppro_id(app_id: int = 0) -> Any:
    where = " where 1=1 "
    if app_id != 0 :
        where = where + " and A.id=" + str(app_id)
        sql = "select A.*,B.class_name from apppro A left join appclass B on A.app_class_id=B.id" + where
        get_apppros = apppro.get_by_sql_no_count(sql)
        if not get_apppros:
            raise IdNotExist(f"系统中不存在 APP查询关键字 为 {app_id} 的APP结果.")
        return resp_200(data=get_apppros, msg=f"查询到了 APP查询关键字 为 {app_id} 的APP结果.")
    else:
        return resp_400()

@router.post("/settype", response_model=ResultModel[AppproOut], summary='添加APP信息')
def update_apppr_type(*, db: Session = Depends(get_db), apppro_in: AppproType) -> Any:
    if apppro_in.id == 0:
        raise IdNotExist(f"缺少id.")
    if apppro_in.app_type == 0 or apppro_in.app_type == 1:
        get_apppro = apppro.get(db, id=apppro_in.id)
        alter_apppro = apppro.update(db, db_obj=get_apppro, obj_in=apppro_in)
        return resp_200(data=alter_apppro, msg=f"更新了 id 为 {apppro_in.id} 的APP属性信息.")
    else:
        raise IdNotExist(f"缺少参数.")

@router.post("/setupdatetype", response_model=ResultModel[AppproOut], summary='添加APP更新属性信息')
def update_apppr_update_type(*, db: Session = Depends(get_db), apppro_in: AppproUpdateType) -> Any:
    if apppro_in.id == 0:
        raise IdNotExist(f"缺少id.")
    if apppro_in.app_update_type == 0 or apppro_in.app_update_type == 1:
        get_apppro = apppro.get(db, id=apppro_in.id)
        alter_apppro = apppro.update(db, db_obj=get_apppro, obj_in=apppro_in)
        return resp_200(data=alter_apppro, msg=f"更新了 id 为 {apppro_in.id} 的APP更新属性信息.")
    else:
        raise IdNotExist(f"缺少参数.")

