#!/usr/bin/env python3
# _*_ coding: utf-8 _*_
# @Time : 2022/11/28 19:18
# @Author : wdm
# @desc : Appclass表接口

from typing import Any, List
from fastapi import APIRouter, Depends, Request, Form
from sqlalchemy import and_, or_
from sqlalchemy.orm import Session

from device.deps import get_db
from schemas import AppclassUpdate, AppclassCreate, AppclassOut, Relation, ResultModel, AppclassDelete, AppclassDesc
from crud import appclass
from utils import resp_200, resp_400, IdNotExist

from models import Appclass

router = APIRouter()

@router.post("/query", response_model=ResultModel[AppclassOut], summary='根据 条件 查询APP分类信息')
def query_appclass(name: str = "", desc: str = "", pageIndex: int = 1, pageSize: int = 10) -> Any:
    where = " where 1=1 "
    if str.strip(name) != "" :
        where = where + " and (class_code like '%%" + str(name) + "%%' or class_name like '%%" + str(name) + "%%' or class_remark like '%%" + str(name) + "%%'"
        if str.strip(desc) != "" :
            where = where + " or class_desc like '%%" + str(desc) + "%%'"
        where = where + ")"
    else:
        raise IdNotExist(f"查询关键字必须.")
    if pageIndex<1:
        raise IdNotExist(f"页数小于1.")
    if pageSize<1:
        raise IdNotExist(f"每页记录数小于1.")
    limit = " limit " + str((pageIndex - 1) * pageSize) + "," + str(pageSize)
    sql = "select * from appclass " + where + limit
    sqlcount = "select count(id) as countid from appclass " + where
    get_appclasss = appclass.get_by_sql(sql, sqlcount)
    if not get_appclasss:
        raise IdNotExist(f"系统中不存在 APP分类查询关键字 为 {name} 的APP分类结果.")
    return resp_200(data=get_appclasss, msg=f"查询到了 APP分类查询关键字 为 {name} 的APP分类结果.")

@router.post("/querybyappclassid", response_model=ResultModel[AppclassOut], summary='根据 条件 查询APP类信息')
def query_appclass_id(appclassId: int = 0, pageIndex: int = 1, pageSize: int = 10, db: Session = Depends(get_db)) -> Any:
    if appclassId != 0 :
        filter_query = (Appclass.id == appclassId)
        get_appclass = appclass.get_by_page_filter(db, filter_query=filter_query, pageIndex=pageIndex, pageSize=pageSize )
        if not get_appclass:
            raise IdNotExist(f"系统中不存在 ID 为 {appclassId} 的APP类结果.")
        return resp_200(data=get_appclass, msg=f"查询到了 ID 为 {appclassId} 的APP类结果.")
    else:
        return resp_400()

@router.post("/querybyname", response_model=ResultModel[AppclassOut], summary='根据 条件 查询APP类信息')
def query_appclass_name(name: str = "", pageIndex: int = 1, pageSize: int = 10, db: Session = Depends(get_db)) -> Any:
    if str.strip(name) != "" :
        filter_query = or_ (
             Appclass.class_code.like('%' + name + '%') ,
             Appclass.class_name.like('%' + name + '%') ,
             Appclass.class_remark.like('%' + name + '%') ,
            )
        get_appclass = appclass.get_by_page_filter(db, filter_query=filter_query, pageIndex=pageIndex, pageSize=pageSize )
        if not get_appclass:
            raise IdNotExist(f"系统中不存在 条件 为 {name} 的APP类结果.")
        return resp_200(data=get_appclass, msg=f"查询到了 条件 为 {name} 的APP类结果.")
    else :
        raise IdNotExist(f"没有传递 条件 值.")

@router.get("/", response_model=ResultModel[AppclassOut], summary='查询所有APP类(根据页码和每页个数)')
def read_appclasss(db: Session = Depends(get_db), pageIndex: int = 1, pageSize: int = 10) -> Any:
    get_appclasss = appclass.get_multi(db, pageIndex=pageIndex, pageSize=pageSize)
    return resp_200(data=get_appclasss, msg=f"查询了第 {pageIndex} 页中的 {pageSize} 个APP类信息.")

@router.get("/queryweb", response_model=ResultModel[AppclassOut], summary='根据 条件 查询APP分类信息')
def query_appclass(class_name: str = "", pageIndex: int = 1, pageSize: int = 10) -> Any:
    where = " where 1=1 "
    if str.strip(class_name) != "" :
        where = where + " and (class_code like '%%" + str(class_name) + "%%' or class_name like '%%"\
                + str(class_name) + "%%' or class_remark like '%%" + str(class_name) + "%%' or class_desc like '%%" + str(class_name) + "%%'"\
                + ")"
    if pageIndex<1:
        raise IdNotExist(f"页数小于1.")
    if pageSize<1:
        raise IdNotExist(f"每页记录数小于1.")
    limit = " limit " + str((pageIndex - 1) * pageSize) + "," + str(pageSize)
    sql = "select * from appclass " + where + limit
    sqlcount = "select count(id) as countid from appclass " + where
    get_appclasss = appclass.get_by_sql(sql, sqlcount)
    if not get_appclasss:
        raise IdNotExist(f"系统中不存在 APP分类查询关键字 为 {class_name} 的APP分类结果.")
    return resp_200(data=get_appclasss, msg=f"查询到了 APP分类查询关键字 为 {class_name} 的APP分类结果.")

@router.get("/qtree", response_model=ResultModel[AppclassOut], summary='根据 条件 查询APP分类信息')
def query_appclass_tree(class_name: str = "") -> Any:
    where = " where 1=1 "
    if str.strip(class_name) != "" :
        where = where + " and (class_code like '%%" + str(class_name) + "%%' or class_name like '%%"\
                + str(class_name) + "%%' or class_remark like '%%" + str(class_name) + "%%' or class_desc like '%%" + str(class_name) + "%%'"\
                + ")"
    sql = "select *,id as app_class_id from appclass " + where
    get_appclasss = appclass.get_by_sql_no_count(sql)
    if not get_appclasss:
        raise IdNotExist(f"系统中不存在 APP分类查询关键字 为 {class_name} 的APP分类结果.")
    return resp_200(data=get_appclasss, msg=f"查询到了APP分类结果.")

@router.get("/qtreeapp", response_model=ResultModel[AppclassOut], summary='根据 条件 查询APP分类信息')
def query_appclass_tree(class_name: str = "") -> Any:
    where = " where 1=1 "
    if str.strip(class_name) != "" :
        where = where + " and (class_code like '%%" + str(class_name) + "%%' or class_name like '%%"\
                + str(class_name) + "%%' or class_remark like '%%" + str(class_name) + "%%' or class_desc like '%%" + str(class_name) + "%%'"\
                + ")"
    sql = "select * from appclass " + where
    get_appclasss = appclass.get_by_sql_fetchall(sql)#List[dict]
    databack = []
    for result in get_appclasss:
        dicttemp = {}
        for k, v in result.items():
            if k == "id" :
                sql = "select * from app where appclass_id = " + str(v)
                get_products = appclass.get_by_sql_fetchall(sql)
                dicttemp[k] = v
                dicttemp["children"] = get_products
            else:
                dicttemp[k] = v
        databack.append(dicttemp)
    if not get_appclasss:
        raise IdNotExist(f"系统中不存在 APP分类查询关键字 为 {class_name} 的APP分类结果.")
    return resp_200(data=databack, msg=f"查询到了APP分类结果.")

@router.post("/updatejson", response_model=ResultModel[AppclassOut], summary='添加APP分类信息')
def update_appclass_json(*, db: Session = Depends(get_db), appclass_in: AppclassCreate) -> Any:
    #print(appclass_in)
    if appclass_in.id != 0:
        get_appclass = appclass.get(db, id=appclass_in.id)
        alter_appclass = appclass.update(db, db_obj=get_appclass, obj_in=appclass_in)
        return resp_200(data=alter_appclass, msg=f"更新了 id 为 {id} 的APP分类信息.")
    else:
        class_in = dict()
        for key,value in appclass_in:
            if key != "id":
                # 赋值字典
                class_in[key] = value
        add_appclass = appclass.create(db, obj_in=class_in)
        return resp_200(data=add_appclass, msg=f"添加了 id 为 {add_appclass.id} 的APP分类信息.")

@router.post("/updateform", response_model=ResultModel[AppclassOut], summary='添加APP分类信息')
def update_appclass_form(*, id: int = Form(...), class_code: str = Form(...), class_name: str = Form(...), class_type: int = Form(...), class_image: str = Form(...), class_remark: str = Form(...)) -> Any: #, appclass_in: AppclassCreate
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

@router.post("/settype", response_model=ResultModel[AppclassOut], summary='添加APP分类信息')
def update_appclass_type(*, db: Session = Depends(get_db), appclass_in: AppclassDesc) -> Any:
    if appclass_in.id == 0:
        raise IdNotExist(f"缺少id.")
    if appclass_in.class_type == 0 or appclass_in.class_type == 1:
        get_appclass = appclass.get(db, id=appclass_in.id)
        alter_appclass = appclass.update(db, db_obj=get_appclass, obj_in=appclass_in)
        return resp_200(data=alter_appclass, msg=f"更新了 id 为 {appclass_in.id} 的APP分类型信息.")
    else:
        raise IdNotExist(f"缺少参数.")

@router.delete("/delete", response_model=ResultModel[AppclassOut], summary='通过 id 删除APP分类信息')
def delete_appclass(*, db: Session = Depends(get_db), class_id: AppclassDelete) -> Any:
    del_appclass = appclass.remove(db, id=class_id.id)
    return resp_200(data=del_appclass, msg=f"删除了 id 为 {class_id.id} 的APP分类信息.")

