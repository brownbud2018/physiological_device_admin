#!/usr/bin/env python3
# _*_ coding: utf-8 _*_
# @Time : 2022/11/28 19:18
# @Author : wdm
# @desc : authclassanddetail表接口

from typing import Any, List
from fastapi import APIRouter, Depends, Request
from sqlalchemy import and_, or_
from sqlalchemy.orm import Session

from device.deps import get_db
from schemas import AuthclassanddetailUpdate, AuthclassanddetailCreate, AuthclassanddetailOut, Relation, ResultModel, AuthclassanddetailDelete
from crud import authclassanddetail
from utils import resp_200, resp_400, IdNotExist

from models import Authclassanddetail

router = APIRouter()

@router.get("/querybyprodid", response_model=ResultModel[AuthclassanddetailOut], summary='查询授权类+权限类')
def query_allclassdetail(prodId:int = 0, pageIndex: int = 1, pageSize: int = 10) -> Any:
    where = " where 1=1 "
    if prodId == 0:
        raise IdNotExist(f"没有传递参数.")
    if prodId != 0 :
        where = where + " and id in (select distinct device_auth_class_id as class_id from device where product_id = " + str(prodId) + ")"
    if pageIndex<1:
        raise IdNotExist(f"页数小于1.")
    if pageSize<1:
        raise IdNotExist(f"每页记录数小于1.")
    limit = " limit " + str((pageIndex - 1) * pageSize) + "," + str(pageSize)
    sql = "select * from authclass " + where + limit
    sqlcount = "select count(id) as countid from authclass " + where

    data = authclassanddetail.get_data_by_sql(sql)

    if not data:
        raise IdNotExist(f"系统中不存在 相关 的查询结果.")
    for result in data:
        class_id = result["id"]
        where = " where 1=1 and a.class_id = " + str(class_id)
        sql = "select b.* from authclassanddetail a left join authdetail b on a.detail_id=b.id " + where
        datachild = authclassanddetail.get_data_by_sql(sql)
        result["child"] = datachild
    count = authclassanddetail.get_count_by_sql(sqlcount)
    backdata = {'count': count, 'dataList': data}
    return {'code': 200, 'data': backdata, 'msg': "查询到了 授权类+权限类列表 的查询结果."}

@router.get("/querybydeviceid", response_model=ResultModel[AuthclassanddetailOut], summary='查询授权类+权限类')
def query_allclassdetail(deviceId:int = 0, pageIndex: int = 1, pageSize: int = 10) -> Any:
    where = " where 1=1 "
    if deviceId == 0:
        raise IdNotExist(f"没有传递参数.")
    if deviceId != 0 :
        where = where + " and id in (select device_auth_class_id as class_id from device where id = " + str(deviceId) + ")"
    if pageIndex<1:
        raise IdNotExist(f"页数小于1.")
    if pageSize<1:
        raise IdNotExist(f"每页记录数小于1.")
    limit = " limit " + str((pageIndex - 1) * pageSize) + "," + str(pageSize)
    sql = "select * from authclass " + where + limit
    sqlcount = "select count(id) as countid from authclass " + where

    data = authclassanddetail.get_data_by_sql(sql)

    if not data:
        raise IdNotExist(f"系统中不存在 相关 的查询结果.")
    for result in data:
        class_id = result["id"]
        where = " where 1=1 and a.class_id = " + str(class_id)
        sql = "select b.* from authclassanddetail a left join authdetail b on a.detail_id=b.id " + where
        datachild = authclassanddetail.get_data_by_sql(sql)
        result["child"] = datachild
    count = authclassanddetail.get_count_by_sql(sqlcount)
    backdata = {'count': count, 'dataList': data}
    return {'code': 200, 'data': backdata, 'msg': "查询到了 授权类+权限类列表 的查询结果."}

@router.get("/querybyclassid", response_model=ResultModel[AuthclassanddetailOut], summary='根据授权类ID查询权限类')
def query_auth_by_classid(classId:int = 0, pageIndex: int = 1, pageSize: int = 10) -> Any:
    if classId == 0:
        raise IdNotExist(f"没有传递参数.")
    where = " where 1=1 "
    if classId != 0 :
        where = where + " and a.class_id = " + str(classId)
    if pageIndex<1:
        raise IdNotExist(f"页数小于1.")
    if pageSize<1:
        raise IdNotExist(f"每页记录数小于1.")
    limit = " limit " + str((pageIndex - 1) * pageSize) + "," + str(pageSize)
    sql = "select b.* from authclassanddetail a  left join authdetail b on a.detail_id=b.id " + where + limit
    sqlcount = "select count(b.id) as countid from authclassanddetail a  left join authdetail b on a.detail_id=b.id " + where
    get_device = authclassanddetail.get_by_sql(sql, sqlcount)
    if not get_device:
        raise IdNotExist(f"系统中不存在 相关 的查询结果.")
    return resp_200(data=get_device, msg=f"查询到了 根据授权类ID查询权限类 的查询结果.")

@router.get("/querybydetailid", response_model=ResultModel[AuthclassanddetailOut], summary='根据权限类ID查询授权类')
def query_product_by_appproid(detailId:int = 0, pageIndex: int = 1, pageSize: int = 10) -> Any:
    if detailId == 0:
        raise IdNotExist(f"没有传递参数.")
    where = " where 1=1 "
    if detailId != 0 :
        where = where + " and a.detail_id = " + str(detailId)
    if pageIndex<1:
        raise IdNotExist(f"页数小于1.")
    if pageSize<1:
        raise IdNotExist(f"每页记录数小于1.")
    limit = " limit " + str((pageIndex - 1) * pageSize) + "," + str(pageSize)
    sql = "select b.* from authclassanddetail a  left join authclass b on a.class_id=b.id " + where + limit
    sqlcount = "select count(b.id) as countid from authclassanddetail a  left join authclass b on a.class_id=b.id " + where
    get_device = authclassanddetail.get_by_sql(sql, sqlcount)
    if not get_device:
        raise IdNotExist(f"系统中不存在 相关 的查询结果.")
    return resp_200(data=get_device, msg=f"查询到了 根据权限类ID查询授权类 的查询结果.")

@router.get("/", response_model=ResultModel[AuthclassanddetailOut], summary='查询授权类+权限类')
def query_allclassdetail(pageIndex: int = 1, pageSize: int = 10) -> Any:
    where = " where 1=1 "
    if pageIndex<1:
        raise IdNotExist(f"页数小于1.")
    if pageSize<1:
        raise IdNotExist(f"每页记录数小于1.")
    limit = " limit " + str((pageIndex - 1) * pageSize) + "," + str(pageSize)
    sql = "select * from authclass " + where + limit
    sqlcount = "select count(id) as countid from authclass " + where

    data = authclassanddetail.get_data_by_sql(sql)

    if not data:
        raise IdNotExist(f"系统中不存在 相关 的查询结果.")
    for result in data:
        class_id = result["id"]
        where = " where 1=1 and a.class_id = " + str(class_id)
        sql = "select b.* from authclassanddetail a left join authdetail b on a.detail_id=b.id " + where
        datachild = authclassanddetail.get_data_by_sql(sql)
        result["child"] = datachild
    count = authclassanddetail.get_count_by_sql(sqlcount)
    backdata = {'count': count, 'dataList': data}
    return {'code': 200, 'data': backdata, 'msg': "查询到了 授权类+权限类列表 的查询结果."}

@router.get("/queryweb", response_model=ResultModel[AuthclassanddetailOut], summary='根据 条件 查询授权关联权限信息')
def query_authclassanddetail(auth_name: str = "", class_id: int = 0, detail_id: int = 0, pageIndex: int = 1, pageSize: int = 10) -> Any:
    where = " where 1=1 "
    if str.strip(auth_name) != "" :
        where = where + " and (B.class_name like '%%" + str(auth_name) + "%%'"
        where = where + " or B.class_code like '%%" + str(auth_name) + "%%'"
        where = where + " or C.detail_code like '%%" + str(auth_name) + "%%'"
        where = where + " or C.detail_name like '%%" + str(auth_name) + "%%')"
    if class_id != 0:
        where = where + " and A.class_id = " + str(class_id)
    if detail_id != 0:
        where = where + " and A.detail_id = " + str(detail_id)
    if pageIndex<1:
        raise IdNotExist(f"页数小于1.")
    if pageSize<1:
        raise IdNotExist(f"每页记录数小于1.")
    order = " order by A.id"
    limit = " limit " + str((pageIndex - 1) * pageSize) + "," + str(pageSize)
    sql = "select A.*,B.class_name,C.detail_name,B.class_code,C.detail_code from authclassanddetail A left join authclass B on A.class_id=B.id left join authdetail C on A.detail_id=C.id " + where + order + limit
    sqlcount = "select count(A.id) as countid from authclassanddetail A left join authclass B on A.class_id=B.id left join authdetail C on A.detail_id=C.id " + where
    get_authclassanddetails = authclassanddetail.get_by_sql(sql, sqlcount)
    if not get_authclassanddetails:
        raise IdNotExist(f"系统中不存在 授权关联权限查询关键字 为 {auth_name} 的授权关联权限结果.")
    return resp_200(data=get_authclassanddetails, msg=f"查询到了 授权关联权限查询关键字 为 {auth_name} 的授权关联权限结果.")

@router.get("/queryproduct", response_model=ResultModel[AuthclassanddetailOut], summary='根据 条件 查询授权关联权限信息')
def query_product_authclassanddetail(auth_name: str = "", class_id: int = 0, prod_id: int = 0, pageIndex: int = 1, pageSize: int = 10) -> Any:
    where = " where 1=1 "
    where1 = ""
    if str.strip(auth_name) != "" :
        where = where + " and (B.class_name like '%%" + str(auth_name) + "%%'"
        where = where + " or B.class_code like '%%" + str(auth_name) + "%%'"
        where = where + " or A.prod_code like '%%" + str(auth_name) + "%%'"
        where = where + " or A.prod_name like '%%" + str(auth_name) + "%%')"
    if class_id != 0:
        where = where + " and A.class_id = " + str(class_id)
    if prod_id != 0:
        where1 = where1 + " and B.id = " + str(prod_id)
    if pageIndex<1:
        raise IdNotExist(f"页数小于1.")
    if pageSize<1:
        raise IdNotExist(f"每页记录数小于1.")
    order = " order by A.id"
    limit = " limit " + str((pageIndex - 1) * pageSize) + "," + str(pageSize)
    sql = "select A.id as prod_id,A.prod_code,A.prod_name,A.concat_class_id,B.* from "
    sql = sql + " ("
    sql = sql + " select * from ("
    sql = sql + "       select B.id,B.prod_name,B.prod_code,GROUP_CONCAT(C.device_auth_class_id) as concat_class_id "
    sql = sql + "       from product B left join device C on B.id=C.product_id"
    sql = sql + "       where 1=1 " + where1
    sql = sql + "       group by B.id"
    sql = sql + "   ) A1"
    sql = sql + "   where concat_class_id is not null "
    sql = sql + " ) A"
    sql = sql + " left join authclass B on find_in_set(B.id,A.concat_class_id)" + where + order + limit
    sqlcount = "select count(A.id) as countid from "
    sqlcount = sqlcount + " ("
    sqlcount = sqlcount + " select * from ("
    sqlcount = sqlcount + "       select B.id,B.prod_name,B.prod_code,GROUP_CONCAT(C.device_auth_class_id) as concat_class_id "
    sqlcount = sqlcount + "       from product B left join device C on B.id=C.product_id"
    sqlcount = sqlcount + "       where 1=1 " + where1
    sqlcount = sqlcount + "       group by B.id"
    sqlcount = sqlcount + "   ) A1"
    sqlcount = sqlcount + "   where concat_class_id is not null "
    sqlcount = sqlcount + " ) A"
    sqlcount = sqlcount + " left join authclass B on find_in_set(B.id,A.concat_class_id)" + where + order
    #sqlcount = "select count(A.id) as countid from authclassanddetail A left join authclass B on A.class_id=B.id left join authdetail C on A.detail_id=C.id " + where
    get_authclassanddetails = authclassanddetail.get_by_sql(sql, sqlcount)
    if not get_authclassanddetails:
        raise IdNotExist(f"系统中不存在 授权关联权限查询关键字 为 {auth_name} 的授权关联权限结果.")
    return resp_200(data=get_authclassanddetails, msg=f"查询到了 授权关联权限查询关键字 为 {auth_name} 的授权关联权限结果.")

@router.post("/updatejson", response_model=ResultModel[AuthclassanddetailOut], summary='添加修改授权关联权限信息')
def update_authclassanddetail_json(*, db: Session = Depends(get_db), authclassanddetail_in: AuthclassanddetailCreate) -> Any:
    if authclassanddetail_in.id != 0:
        sqlcount = "select count(id) as countid from authclassanddetail where class_id = " + str(authclassanddetail_in.class_id) + " and detail_id = " + str(authclassanddetail_in.detail_id) + " and id <> " + str(authclassanddetail_in.id)
        get_exist_count = authclassanddetail.get_by_sql_is_exist(sqlcount)
        if get_exist_count > 0:#已经存在关联，禁止修改
            return {'code': -1, 'data': get_exist_count, 'msg': '已经存在关联！'}
        get_authclassanddetail = authclassanddetail.get(db, id=authclassanddetail_in.id)
        alter_authclassanddetail = authclassanddetail.update(db, db_obj=get_authclassanddetail, obj_in=authclassanddetail_in)
        return resp_200(data=alter_authclassanddetail, msg=f"更新了 id 为 {authclassanddetail_in.id} 的授权关联权限信息.")
    else:
        sqlcount = "select count(id) as countid from authclassanddetail where class_id = " + str(authclassanddetail_in.class_id) + " and detail_id = " + str(authclassanddetail_in.detail_id)
        get_exist_count = authclassanddetail.get_by_sql_is_exist(sqlcount)
        if get_exist_count > 0:#已经存在关联，禁止修改
            return {'code': -1, 'data': get_exist_count, 'msg': '已经存在关联！'}
        authabout_in = dict()
        for key,value in authclassanddetail_in:
            if key != "id":
                # 赋值字典
                authabout_in[key] = value
        add_authclassanddetail = authclassanddetail.create(db, obj_in=authabout_in)
        return resp_200(data=add_authclassanddetail, msg=f"添加了 id 为 {add_authclassanddetail.id} 的授权关联权限信息.")

@router.delete("/delete", response_model=ResultModel[AuthclassanddetailOut], summary='通过 id 删除授权关联权限信息')
def delete_authclassanddetail(*, db: Session = Depends(get_db), authclassanddetail_in: AuthclassanddetailDelete) -> Any:
    del_authclassanddetail = authclassanddetail.remove(db, id=authclassanddetail_in.id)
    return resp_200(data=del_authclassanddetail, msg=f"删除了 id 为 {authclassanddetail_in.id} 的授权关联权限信息.")

@router.get("/querydetailbyclassid", response_model=ResultModel[AuthclassanddetailOut], summary='根据授权类ID查询权限类')
def query_auth_by_classid(class_id:int = 0, pageIndex: int = 1, pageSize: int = 10) -> Any:
    if class_id == 0:
        raise IdNotExist(f"没有传递参数.")
    where = " where 1=1 "
    if class_id != 0 :
        where = where + " and a.class_id = " + str(class_id)
    if pageIndex<1:
        raise IdNotExist(f"页数小于1.")
    if pageSize<1:
        raise IdNotExist(f"每页记录数小于1.")
    limit = " limit " + str((pageIndex - 1) * pageSize) + "," + str(pageSize)
    sql = "select b.* from authclassanddetail a  left join authdetail b on a.detail_id=b.id " + where + limit
    sqlcount = "select count(b.id) as countid from authclassanddetail a  left join authdetail b on a.detail_id=b.id " + where
    get_device = authclassanddetail.get_by_sql(sql, sqlcount)
    if not get_device:
        raise IdNotExist(f"系统中不存在 相关 的查询结果.")
    return resp_200(data=get_device, msg=f"查询到了 根据授权类ID查询权限类 的查询结果.")

