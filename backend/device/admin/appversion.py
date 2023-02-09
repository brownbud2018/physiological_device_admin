#!/usr/bin/env python3
# _*_ coding: utf-8 _*_
# @Time : 2022/11/28 19:18
# @Author : wdm
# @desc : APP版本表接口

from typing import Any, List
from fastapi import APIRouter, Depends, Request, Form
from sqlalchemy import and_, or_
from sqlalchemy.orm import Session

from device.deps import get_db
from schemas import AppversionUpdate, AppversionCreate, AppversionOut, Relation, ResultModel, AppversionType, AppversionDelete
from crud import appversion
from utils import resp_200, resp_400, IdNotExist

from models import Appversion

router = APIRouter()

@router.post("/query", response_model=ResultModel[AppversionOut], summary='根据 条件 查询APP信息')
def query_appversion(name: str = "", type: int = 0, appversionId: int = 0, appproId: int = 0, pageIndex: int = 1, pageSize: int = 10) -> Any:
    where = " where 1=1 "
    if str.strip(name) != "" :
        where = where + " and (app_v_code like '%%" + str(name) + "%%' or app_v_name like '%%" + str(name) + "%%' or app_v_remark like '%%" + str(name) + "%%')"
    where = where + " and app_v_default = " + str(type)
    if appproId != 0 :
        where = where + " and app_pro_id = " + str(appproId)
    if appversionId != 0 :
        where = where + " and id = " + str(appversionId)
    if pageIndex<1:
        raise IdNotExist(f"页数小于1.")
    if pageSize<1:
        raise IdNotExist(f"每页记录数小于1.")
    limit = " limit " + str((pageIndex - 1) * pageSize) + "," + str(pageSize)
    sql = "select * from appversion " + where + limit
    sqlcount = "select count(id) as countid from appversion " + where
    get_appversions = appversion.get_by_sql(sql, sqlcount)
    if not get_appversions:
        raise IdNotExist(f"查询APP版本结果为空.")
    return resp_200(data=get_appversions, msg=f"查询到了 综合查询 的APP版本结果.")

@router.post("/querybyappversionid", response_model=ResultModel[AppversionOut], summary='根据 条件 查询APP版本信息')
def query_appversion_id(appversionId: int = 0, pageIndex: int = 1, pageSize: int = 10, db: Session = Depends(get_db)) -> Any:
    if appversionId != 0 :
        filter_query = (Appversion.id == appversionId)
        get_appversion = appversion.get_by_page_filter(db, filter_query=filter_query, pageIndex=pageIndex, pageSize=pageSize )
        if not get_appversion:
            raise IdNotExist(f"系统中不存在 ID 为 {appversionId} 的APP版本结果.")
        return resp_200(data=get_appversion, msg=f"查询到了 ID 为 {appversionId} 的APP版本结果.")
    else:
        return resp_400()

@router.post("/querybyappproid", response_model=ResultModel[AppversionOut], summary='根据 APP分类ID 查询APP版本信息')
def query_apppro_id(appproId: int = 0, pageIndex: int = 1, pageSize: int = 10, db: Session = Depends(get_db)) -> Any:
    if appproId != 0 :
        filter_query = (Appversion.app_pro_id == appproId)
        get_appversion = appversion.get_by_page_filter(db, filter_query=filter_query, pageIndex=pageIndex, pageSize=pageSize )
        if not get_appversion:
            raise IdNotExist(f"系统中不存在 APPProID 为 {appproId} 的APP版本结果.")
        return resp_200(data=get_appversion, msg=f"查询到了 APPProID 为 {appproId} 的APP版本结果.")
    else:
        return resp_400()

@router.get("/querybyappid", response_model=ResultModel[AppversionOut], summary='根据 条件 查询APP版本信息')
def query_app_id(app_pro_id: int = 0, pageIndex: int = 1, pageSize: int = 10, db: Session = Depends(get_db)) -> Any:
    where = " where 1=1 "
    if app_pro_id != 0 :
        where = where + " and A.app_pro_id=" + str(app_pro_id)
        sql = "select A.*,B.app_name from appversion A left join apppro B on A.app_pro_id=B.id" + where
        get_appversion = appversion.get_by_sql_no_count(sql)
        if not get_appversion:
            return {'code': -1, 'data': app_pro_id, 'msg': f"系统中不存在 APPID 为 {app_pro_id} 的版本号结果."}
        return resp_200(data=get_appversion, msg=f"查询到了 APPID 为 {app_pro_id} 的APP版本结果.")
    else:
        return resp_400()

@router.post("/querybyname", response_model=ResultModel[AppversionOut], summary='根据 条件 查询APP版本信息')
def query_appversion_name(name: str = "", pageIndex: int = 1, pageSize: int = 10, db: Session = Depends(get_db)) -> Any:
    if str.strip(name) != "" :
        filter_query = or_ (
             Appversion.app_v_code.like('%' + name + '%') ,
             Appversion.app_v_name.like('%' + name + '%') ,
             Appversion.app_v_remark.like('%' + name + '%') ,
            )
        get_appversion = appversion.get_by_page_filter(db, filter_query=filter_query, pageIndex=pageIndex, pageSize=pageSize )
        if not get_appversion:
            raise IdNotExist(f"系统中不存在 条件 为 {name} 的APP版本结果.")
        return resp_200(data=get_appversion, msg=f"查询到了 条件 为 {name} 的APP版本结果.")
    else :
        raise IdNotExist(f"没有传递 条件 值.")

@router.get("/", response_model=ResultModel[AppversionOut], summary='查询所有APP版本(根据页码和每页个数)')
def read_appversions(db: Session = Depends(get_db), pageIndex: int = 1, pageSize: int = 10) -> Any:
    get_appversions = appversion.get_multi(db, pageIndex=pageIndex, pageSize=pageSize)
    return resp_200(data=get_appversions, msg=f"查询了第 {pageIndex} 页中的 {pageSize} 个APP版本信息.")

@router.get("/queryweb", response_model=ResultModel[AppversionOut], summary='根据 条件 查询appversion信息')
def query_appversion(appversion_name: str = "", app_pro_id: int = 0, pageIndex: int = 1, pageSize: int = 10) -> Any:
    where = " where 1=1 "
    if str.strip(appversion_name) != "" :
        where = where + " and (app_v_name like '%%" + str(appversion_name) + "%%'"
        where = where + " or app_v_code like '%%" + str(appversion_name) + "%%'"
        where = where + " or app_v_remark like '%%" + str(appversion_name) + "%%'"
        where = where + " or B.app_name like '%%" + str(appversion_name) + "%%')"
    if app_pro_id != 0:
        where = where + " and app_pro_id = " + str(app_pro_id)
    if pageIndex<1:
        raise IdNotExist(f"页数小于1.")
    if pageSize<1:
        raise IdNotExist(f"每页记录数小于1.")
    order = " order by A.id"
    limit = " limit " + str((pageIndex - 1) * pageSize) + "," + str(pageSize)
    sql = "select A.*,B.app_name from appversion A left join apppro B on A.app_pro_id=B.id " + where + order + limit
    sqlcount = "select count(A.id) as countid from appversion A left join apppro B on A.app_pro_id=B.id " + where
    get_appversions = appversion.get_by_sql(sql, sqlcount)
    if not get_appversions:
        raise IdNotExist(f"系统中不存在 appversion查询关键字 为 {appversion_name} 的appversion结果.")
    return resp_200(data=get_appversions, msg=f"查询到了 appversion查询关键字 为 {appversion_name} 的appversion结果.")

@router.post("/updatejson", response_model=ResultModel[AppversionOut], summary='添加版本信息')
def update_appversion_json(*, db: Session = Depends(get_db), appversion_in: AppversionCreate) -> Any:
    if appversion_in.id != 0:
        sqlcount = "select count(id) as countid from appversion where app_pro_id = " + str(appversion_in.app_pro_id) + " and id <> " + str(appversion_in.id)
        get_exist_count = appversion.get_by_sql_is_exist(sqlcount)
        if get_exist_count == 0:#没有其它存在的版本，就只有这一个版本，那么就改成默认版本
            appversion_in.app_v_default = 1
        else:
            if appversion_in.app_v_default == 1:#默认版本，相同APP下的其它版本设置为非默认
                sqlupdate = "update appversion set app_v_default = 0 where app_pro_id = " + str(appversion_in.app_pro_id) + " and id <> " + str(appversion_in.id)
                get_update = appversion.update_by_sql(sqlupdate)
        get_appversion = appversion.get(db, id=appversion_in.id)
        alter_appversion = appversion.update(db, db_obj=get_appversion, obj_in=appversion_in)
        return resp_200(data=alter_appversion, msg=f"更新了 id 为 {id} 的版本信息.")
    else:
        sqlcount = "select count(id) as countid from appversion where app_pro_id = " + str(appversion_in.app_pro_id)
        get_exist_count = appversion.get_by_sql_is_exist(sqlcount)
        if get_exist_count == 0:#没有其它存在的版本，就只有这一个版本，那么就改成默认版本
            appversion_in.app_v_default = 1
        else:
            if appversion_in.app_v_default == 1:#默认版本，相同APP下的其它版本设置为非默认
                sqlupdate = "update appversion set app_v_default = 0 where app_pro_id = " + str(appversion_in.app_pro_id) + " and id <> " + str(appversion_in.id)
                get_update = appversion.update_by_sql(sqlupdate)
        version_in = dict()
        for key,value in appversion_in:
            if key != "id":
                # 赋值字典
                version_in[key] = value
        add_appversion = appversion.create(db, obj_in=version_in)
        return resp_200(data=add_appversion, msg=f"添加了 id 为 {add_appversion.id} 的版本信息.")

@router.post("/updateform", response_model=ResultModel[AppversionOut], summary='添加版本信息')
def update_appversion_form(*, id: int = Form(...), app_v_code: str = Form(...), app_v_name: str = Form(...), app_v_image: str = Form(...), app_v_file: str = Form(...), app_pro_id: str = Form(...), app_v_default: int = Form(...), app_v_remark: str = Form(...)) -> Any:
    print('id'+ str(id))
    print(id)
    if id != 0:
        raise IdNotExist(f"修改.")
    else:
        raise IdNotExist(f"ID:{id}新增.")

@router.post("/settype", response_model=ResultModel[AppversionOut], summary='添加appversion信息')
def update_appversion_type(*, db: Session = Depends(get_db), appversion_in: AppversionType) -> Any:
    if appversion_in.id == 0:
        raise IdNotExist(f"缺少id.")
    if appversion_in.app_v_default == 0 or appversion_in.app_v_default == 1:
        get_appversion = appversion.get(db, id=appversion_in.id)
        if appversion_in.app_v_default == 1:#默认版本，相同APP下的其它版本设置为非默认
            sqlupdate = "update appversion set app_v_default = 0 where app_pro_id = " + str(get_appversion.app_pro_id) + " and id <> " + str(get_appversion.id)
            get_update = appversion.update_by_sql(sqlupdate)
            alter_appversion = appversion.update(db, db_obj=get_appversion, obj_in=appversion_in)
            return resp_200(data=alter_appversion, msg=f"更新了 id 为 {appversion_in.id} 的appversion默认版本信息.")
        else:
            sqlcount = "select count(id) as countid from appversion where app_pro_id = " + str(get_appversion.app_pro_id) + " and id <> " + str(get_appversion.id)
            get_exist_count = appversion.get_by_sql_is_exist(sqlcount)
            if get_exist_count == 0:#没有其它存在的版本，就只有这一个版本
                return {'code': -1, 'data': get_appversion, 'msg': '只有唯一一个版本，不能设置为非默认版本！'}
            else:
                sqlupdate = "update appversion set app_v_default = 1 where id in (select a.id from (select max(id) as id from appversion where app_pro_id = " + str(get_appversion.app_pro_id) + " and id <> " + str(get_appversion.id) + ") a)"
                get_update = appversion.update_by_sql(sqlupdate)
                get_appversion = appversion.get(db, id=appversion_in.id)
                alter_appversion = appversion.update(db, db_obj=get_appversion, obj_in=appversion_in)
                return resp_200(data=alter_appversion, msg=f"更新了 id 为 {appversion_in.id} 的appversion默认版本信息.")
    else:
        raise IdNotExist(f"缺少参数.")

@router.delete("/delete", response_model=ResultModel[AppversionOut], summary='通过 id 删除APP版本信息')
def delete_appversion(*, db: Session = Depends(get_db), appversion_id: AppversionDelete) -> Any:
    get_appversion = appversion.get(db, id=appversion_id.id)
    if get_appversion.app_v_default == 1:#如果删除的APP版本是APP的【默认版本】，修改当前相同APP下的其它版本的【ID值最大的记录】设置为默认
        sqlupdate = "update appversion set app_v_default = 1 where id in (select a.id from (select max(id) as id from appversion where app_pro_id = " + str(get_appversion.app_pro_id) + " and id <> " + str(get_appversion.id) + ") a)"
        get_update = appversion.update_by_sql(sqlupdate)
    del_appversion = appversion.remove(db, id=appversion_id.id)
    return resp_200(data=del_appversion, msg=f"删除了 id 为 {appversion_id.id} 的APP版本信息.")

@router.get("/querybyid", response_model=ResultModel[AppversionOut], summary='根据 条件 查询appversion信息')
def query_appversion_id(appversion_id: int = 0) -> Any:
    where = " where 1=1 "
    if appversion_id != 0 :
        where = where + " and A.id=" + str(appversion_id)
        sql = "select A.*,B.app_name from appversion A left join apppro B on A.app_pro_id=B.id " + where
        get_appversions = appversion.get_by_sql_no_count(sql)
        if not get_appversions:
            raise IdNotExist(f"系统中不存在 appversion查询关键字 为 {appversion_id} 的appversion结果.")
        return resp_200(data=get_appversions, msg=f"查询到了 appversion查询关键字 为 {appversion_id} 的appversion结果.")
    else:
        return resp_400()
