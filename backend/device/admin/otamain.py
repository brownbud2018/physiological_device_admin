#!/usr/bin/env python3
# _*_ coding: utf-8 _*_
# @Time : 2022/11/28 19:18
# @Author : wdm
# @desc : OTA表接口

from typing import Any, List
from fastapi import APIRouter, Depends, Request, Form
from sqlalchemy import and_, or_
from sqlalchemy.orm import Session

from device.deps import get_db
from schemas import OtamainUpdate, OtamainCreate, OtamainOut, Relation, ResultModel, OtamainDelete, OtamainType, OtamainUpdateType
from crud import otamain
from utils import resp_200, resp_400, IdNotExist

from models import Otamain

router = APIRouter()

@router.post("/query", response_model=ResultModel[OtamainOut], summary='根据 条件 查询OTA信息')
def query_otamain(name: str = "", type: int = 0, updateType: int = 0, otamainId: int = 0, pageIndex: int = 1, pageSize: int = 10) -> Any:
    where = " where 1=1 "
    if str.strip(name) != "" :
        where = where + " and (ota_code like '%%" + str(name) + "%%' or ota_name like '%%" + str(name) + "%%' or ota_remark like '%%" + str(name) + "%%')"
    where = where + " and ota_type = " + str(type)
    where = where + " and ota_update_type = " + str(updateType)
    if otamainId != 0 :
        where = where + " and id = " + str(otamainId)
    if pageIndex<1:
        raise IdNotExist(f"页数小于1.")
    if pageSize<1:
        raise IdNotExist(f"每页记录数小于1.")
    limit = " limit " + str((pageIndex - 1) * pageSize) + "," + str(pageSize)
    sql = "select * from otamain " + where + limit
    sqlcount = "select count(id) as countid from otamain " + where
    get_otamain = otamain.get_by_sql(sql, sqlcount)
    if not get_otamain:
        raise IdNotExist(f"系统中不存在 OTA查询关键字 为 {name} 的OTA结果.")
    return resp_200(data=get_otamain, msg=f"查询到了 综合查询 的OTA结果.")

@router.post("/querybyotamainid", response_model=ResultModel[OtamainOut], summary='根据 ID条件 查询OTA类信息')
def query_otamain_id(otamainId: int = 0, pageIndex: int = 1, pageSize: int = 10, db: Session = Depends(get_db)) -> Any:
    if otamainId != 0 :
        if pageIndex<1:
            raise IdNotExist(f"页数小于1.")
        if pageSize<1:
            raise IdNotExist(f"每页记录数小于1.")
        filter_query = (Otamain.id == otamainId)
        get_otamain = otamain.get_by_page_filter(db, filter_query=filter_query, pageIndex=pageIndex, pageSize=pageSize )
        if not get_otamain:
            raise IdNotExist(f"系统中不存在 ID 为 {otamainId} 的OTA类结果.")
        return resp_200(data=get_otamain, msg=f"查询到了 ID 为 {otamainId} 的OTA类结果.")
    else:
        return resp_400()

@router.get("/querybyprodid", response_model=ResultModel[OtamainOut], summary='根据设备类ID查询相关OTA类')
def query_otamain_id(prodId: int = 0, pageIndex: int = 1, pageSize: int = 10) -> Any:
    where = " where 1=1 "
    if prodId != 0 :
        where = where + " and id in (select distinct device_ota as id from device where product_id = " + str(prodId) + ")"
    if pageIndex<1:
        raise IdNotExist(f"页数小于1.")
    if pageSize<1:
        raise IdNotExist(f"每页记录数小于1.")
    limit = " limit " + str((pageIndex - 1) * pageSize) + "," + str(pageSize)
    sql = "select * from otamain " + where + limit
    sqlcount = "select count(id) as countid from otamain " + where
    get_otamain = otamain.get_by_sql(sql, sqlcount)
    if not get_otamain:
        raise IdNotExist(f"系统中不存在 OTA查询关键字deviceID 为 {prodId} 的OTA结果.")
    return resp_200(data=get_otamain, msg=f"查询到了deviceID查询 的OTA结果.")

@router.get("/querymainchildbyprodid", response_model=ResultModel[OtamainOut], summary='根据设备类ID查询相关OTA类+OTA版本')
def query_otamain_id(prodId: int = 0, pageIndex: int = 1, pageSize: int = 10) -> Any:
    where = " where 1=1 "
    if prodId != 0 :
        where = where + " and id in (select distinct device_ota as id from device where product_id = " + str(prodId) + ")"
    if pageIndex<1:
        raise IdNotExist(f"页数小于1.")
    if pageSize<1:
        raise IdNotExist(f"每页记录数小于1.")
    limit = " limit " + str((pageIndex - 1) * pageSize) + "," + str(pageSize)
    sql = "select * from otamain " + where + limit
    sqlcount = "select count(id) as countid from otamain " + where
    data = otamain.get_data_by_sql(sql)
    if not data:
        raise IdNotExist(f"系统中不存在 相关 的查询结果.")
    for result in data:
        otaid = result["id"]
        where = " where 1=1 and ota_main_id = " + str(otaid)
        sql = "select * from otaversion " + where
        datachild = otamain.get_data_by_sql(sql)
        result["child"] = datachild
    count = otamain.get_count_by_sql(sqlcount)
    backdata = {'count': count, 'dataList': data}
    return {'code': 200, 'data': backdata, 'msg': "查询到了 根据设备类ID查询相关OTA类+OTA版本 的查询结果."}

@router.post("/querybydeviceid", response_model=ResultModel[OtamainOut], summary='根据 deviceID 查询OTA信息')
def query_otamain_id(deviceId: int = 0, pageIndex: int = 1, pageSize: int = 10) -> Any:
    where = " where 1=1 "
    if deviceId != 0 :
        where = where + " and id in (select device_ota as id from device where id = " + str(deviceId) + ")"
    if pageIndex<1:
        raise IdNotExist(f"页数小于1.")
    if pageSize<1:
        raise IdNotExist(f"每页记录数小于1.")
    limit = " limit " + str((pageIndex - 1) * pageSize) + "," + str(pageSize)
    sql = "select * from otamain " + where + limit
    sqlcount = "select count(id) as countid from otamain " + where
    get_otamain = otamain.get_by_sql(sql, sqlcount)
    if not get_otamain:
        raise IdNotExist(f"系统中不存在 OTA查询关键字deviceID 为 {deviceId} 的OTA结果.")
    return resp_200(data=get_otamain, msg=f"查询到了deviceID查询 的OTA结果.")

@router.get("/querymainchildbydeviceid", response_model=ResultModel[OtamainOut], summary='根据Device ID查询相关OTA类+OTA版本')
def query_otamain_id(deviceId: int = 0, pageIndex: int = 1, pageSize: int = 10) -> Any:
    where = " where 1=1 "
    if deviceId != 0 :
        where = where + " and id in (select distinct device_ota as id from device where id = " + str(deviceId) + ")"
    if pageIndex<1:
        raise IdNotExist(f"页数小于1.")
    if pageSize<1:
        raise IdNotExist(f"每页记录数小于1.")
    limit = " limit " + str((pageIndex - 1) * pageSize) + "," + str(pageSize)
    sql = "select * from otamain " + where + limit
    sqlcount = "select count(id) as countid from otamain " + where
    data = otamain.get_data_by_sql(sql)
    if not data:
        raise IdNotExist(f"系统中不存在 相关 的查询结果.")
    for result in data:
        otaid = result["id"]
        where = " where 1=1 and ota_main_id = " + str(otaid)
        sql = "select * from otaversion " + where
        datachild = otamain.get_data_by_sql(sql)
        result["child"] = datachild
    count = otamain.get_count_by_sql(sqlcount)
    backdata = {'count': count, 'dataList': data}
    return {'code': 200, 'data': backdata, 'msg': "查询到了 根据Device ID查询相关OTA类+OTA版本 的查询结果."}

@router.post("/querybyname", response_model=ResultModel[OtamainOut], summary='根据 条件 查询OTA类信息')
def query_otamain_name(name: str = "", pageIndex: int = 1, pageSize: int = 10, db: Session = Depends(get_db)) -> Any:
    if str.strip(name) != "" :
        if pageIndex<1:
            raise IdNotExist(f"页数小于1.")
        if pageSize<1:
            raise IdNotExist(f"每页记录数小于1.")
        filter_query = or_ (
             Otamain.ota_code.like('%' + name + '%') ,
             Otamain.ota_name.like('%' + name + '%') ,
             Otamain.ota_remark.like('%' + name + '%') ,
            )
        get_otamain = otamain.get_by_page_filter(db, filter_query=filter_query, pageIndex=pageIndex, pageSize=pageSize )
        if not get_otamain:
            raise IdNotExist(f"系统中不存在 条件 为 {name} 的OTA类结果.")
        return resp_200(data=get_otamain, msg=f"查询到了 条件 为 {name} 的OTA类结果.")
    else :
        raise IdNotExist(f"没有传递 条件 值.")

@router.get("/", response_model=ResultModel[OtamainOut], summary='查询所有OTA类(根据页码和每页个数)')
def read_otamains(db: Session = Depends(get_db), pageIndex: int = 1, pageSize: int = 10) -> Any:
    if pageIndex<1:
        raise IdNotExist(f"页数小于1.")
    if pageSize<1:
        raise IdNotExist(f"每页记录数小于1.")
    get_otamains = otamain.get_multi(db, pageIndex=pageIndex, pageSize=pageSize)
    return resp_200(data=get_otamains, msg=f"查询了第 {pageIndex} 页中的 {pageSize} 个OTA类信息.")

@router.get("/queryweb", response_model=ResultModel[OtamainOut], summary='根据 条件 查询OTA信息')
def query_otamain(ota_name: str = "", pageIndex: int = 1, pageSize: int = 10) -> Any:
    where = " where 1=1 "
    if str.strip(ota_name) != "" :
        where = where + " and (ota_code like '%%" + str(ota_name) + "%%' or ota_name like '%%" + str(ota_name) + "%%' or ota_remark like '%%" + str(ota_name) + "%%')"
    if pageIndex<1:
        return {'code': -1, 'data': pageIndex, 'msg': f'页数:{pageIndex}小于1'}
    if pageSize<1:
        return {'code': -1, 'data': pageSize, 'msg': f'每页记录数:{pageSize}小于1'}
    limit = " limit " + str((pageIndex - 1) * pageSize) + "," + str(pageSize)
    sql = "select A.* from otamain A " + where + limit
    sqlcount = "select count(id) as countid from otamain " + where
    get_otamains = otamain.get_by_sql(sql, sqlcount)
    if not get_otamains:
        return {'code': -1, 'data': pageSize, 'msg': f"系统中不存在 OTA查询关键字 为 {ota_name} 的OTA结果."}
    return resp_200(data=get_otamains, msg=f"查询到了 OTA查询关键字 为 {ota_name} 的OTA结果.")

@router.get("/qtree", response_model=ResultModel[OtamainOut], summary='根据 条件 查询OTA信息')
def query_otamain_tree(ota_name: str = "") -> Any:
    where = " where 1=1 "
    if str.strip(ota_name) != "" :
        where = where + " and (ota_code like '%%" + str(ota_name) + "%%' or ota_name like '%%" + str(ota_name) + "%%' or ota_remark like '%%" + str(ota_name) + "%%')"
    sql = "select *,id as device_ota,id as ota_main_id from otamain " + where
    get_otamains = otamain.get_by_sql_no_count(sql)
    if not get_otamains:
        return {'code': -1, 'data': get_otamains, 'msg': f"系统中不存在 OTA类查询关键字 为 {ota_name} 的OTA类结果."}
    return resp_200(data=get_otamains, msg=f"查询到了OTA类结果.")

@router.post("/updatejson", response_model=ResultModel[OtamainOut], summary='添加OTA信息')
def update_otamain_json(*, db: Session = Depends(get_db), otamain_in: OtamainCreate) -> Any:
    if otamain_in.id != 0:
        get_otamain = otamain.get(db, id=otamain_in.id)
        alter_otamain = otamain.update(db, db_obj=get_otamain, obj_in=otamain_in)
        return resp_200(data=alter_otamain, msg=f"更新了 id 为 {id} 的OTA信息.")
    else:
        ota_in = dict()
        for key,value in otamain_in:
            if key != "id":
                # 赋值字典
                ota_in[key] = value
        add_otamain = otamain.create(db, obj_in=ota_in)
        return resp_200(data=add_otamain, msg=f"添加了 id 为 {add_otamain.id} 的OTA信息.")

@router.post("/updateform", response_model=ResultModel[OtamainOut], summary='添加OTA信息')
def update_otamain_form(*, id: int = Form(...), ota_code: str = Form(...), ota_name: str = Form(...), ota_type: int = Form(...), ota_image: str = Form(...), ota_remark: str = Form(...)) -> Any: #, otamain_in: ProductCreate
    print('id'+ str(id))
    print(id)
    print('ota_code' + str(ota_code))
    print('ota_name' + str(ota_name))
    print('ota_type' + str(ota_type))
    print('ota_image' + str(ota_image))
    print('ota_remark' + str(ota_remark))
    if id != 0:
        raise IdNotExist(f"修改.")
    else:
        raise IdNotExist(f"ID:{id}新增.")

@router.delete("/delete", response_model=ResultModel[OtamainOut], summary='通过 id 删除OTA信息')
def delete_otamain(*, db: Session = Depends(get_db), ota_id: OtamainDelete) -> Any:
    del_otamain = otamain.remove(db, id=ota_id.id)
    return resp_200(data=del_otamain, msg=f"删除了 id 为 {ota_id.id} 的OTA信息.")

@router.get("/querybyid", response_model=ResultModel[OtamainOut], summary='根据 条件 查询OTA信息')
def query_otamain_id(ota_id: int = 0) -> Any:
    where = " where 1=1 "
    if ota_id != 0 :
        where = where + " and A.id=" + str(ota_id)
        sql = "select A.* from otamain A " + where
        get_otamains = otamain.get_by_sql_no_count(sql)
        if not get_otamains:
            return {'code': -1, 'data': get_otamains, 'msg': f"系统中不存在 OTA查询关键字 为 {ota_id} 的OTA结果."}
        return resp_200(data=get_otamains, msg=f"查询到了 OTA查询关键字 为 {ota_id} 的OTA结果.")
    else:
        return resp_400()

@router.post("/settype", response_model=ResultModel[OtamainOut], summary='添加OTA信息')
def update_apppr_type(*, db: Session = Depends(get_db), otamain_in: OtamainType) -> Any:
    if otamain_in.id == 0:
        return {'code': -1, 'data': otamain_in.id, 'msg': f"缺少id."}
    if otamain_in.ota_type == 0 or otamain_in.ota_type == 1:
        get_otamain = otamain.get(db, id=otamain_in.id)
        alter_otamain = otamain.update(db, db_obj=get_otamain, obj_in=otamain_in)
        return resp_200(data=alter_otamain, msg=f"更新了 id 为 {otamain_in.id} 的OTA属性信息.")
    else:
        return {'code': -1, 'data': otamain_in.ota_type, 'msg': f"缺少参数."}

@router.post("/setupdatetype", response_model=ResultModel[OtamainOut], summary='添加OTA更新属性信息')
def update_apppr_update_type(*, db: Session = Depends(get_db), otamain_in: OtamainUpdateType) -> Any:
    if otamain_in.id == 0:
        return {'code': -1, 'data': otamain_in.id, 'msg': f"缺少id."}
    if otamain_in.ota_update_type == 0 or otamain_in.ota_update_type == 1:
        get_otamain = otamain.get(db, id=otamain_in.id)
        alter_otamain = otamain.update(db, db_obj=get_otamain, obj_in=otamain_in)
        return resp_200(data=alter_otamain, msg=f"更新了 id 为 {otamain_in.id} 的OTA更新属性信息.")
    else:
        return {'code': -1, 'data': otamain_in.ota_update_type, 'msg': f"缺少参数."}


