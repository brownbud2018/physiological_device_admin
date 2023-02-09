#!/usr/bin/env python3
# _*_ coding: utf-8 _*_
# @Time : 2022/11/28 19:18
# @Author : wdm
# @desc : 权限详情表接口

from typing import Any, List
from fastapi import APIRouter, Depends, Request, Form
from sqlalchemy import and_, or_
from sqlalchemy.orm import Session

from device.deps import get_db
from schemas import AuthdetailUpdate, AuthdetailCreate, AuthdetailOut, Relation, ResultModel, ResultPlusModel, AuthdetailType, AuthdetailDelete
from crud import authdetail
from utils import resp_200, resp_400, IdNotExist

from models import Authdetail

router = APIRouter()

@router.post("/query", response_model=ResultModel[AuthdetailOut], summary='根据 条件 查询权限详情信息')
def query_authdetail(name: str = "", type: int = 0, pageIndex: int = 1, pageSize: int = 10) -> Any:
    where = " where 1=1 "
    if str.strip(name) != "" :
        where = where + " and (detail_code like '%%" + str(name) + "%%' or detail_name like '%%" + str(name) + "%%' or detail_remark like '%%" + str(name) + "%%')"
    else:
        raise IdNotExist(f"查询关键字必须.")
    where = where + " and detail_type = " + str(type)
    if pageIndex<1:
        raise IdNotExist(f"页数小于1.")
    if pageSize<1:
        raise IdNotExist(f"每页记录数小于1.")
    limit = " limit " + str((pageIndex - 1) * pageSize) + "," + str(pageSize)
    sql = "select * from authdetail " + where + limit
    sqlcount = "select count(id) as countid from authdetail " + where
    get_authdetails = authdetail.get_by_sql(sql, sqlcount)
    if not get_authdetails:
        raise IdNotExist(f"系统中不存在 权限详情查询关键字 为 {name} 的权限详情结果.")
    return resp_200(data=get_authdetails, msg=f"查询到了 权限详情查询关键字 为 {name} 的权限详情结果.")

@router.post("/querybyauthdetailid", response_model=ResultModel[AuthdetailOut], summary='根据 条件 查询权限详情信息')
def query_authdetail_id(authdetailId: int = 0, pageIndex: int = 1, pageSize: int = 10, db: Session = Depends(get_db)) -> Any:
    if authdetailId != 0 :
        filter_query = (Authdetail.id == authdetailId)
        get_authdetail = authdetail.get_by_page_filter(db, filter_query=filter_query, pageIndex=pageIndex, pageSize=pageSize )
        if not get_authdetail:
            raise IdNotExist(f"系统中不存在 ID 为 {authdetailId} 的权限详情结果.")
        return resp_200(data=get_authdetail, msg=f"查询到了 ID 为 {authdetailId} 的权限详情结果.")
    else:
        return resp_400()

@router.post("/querybyname", response_model=ResultModel[AuthdetailOut], summary='根据 条件 查询权限详情信息')
def query_authdetail_name(name: str = "", pageIndex: int = 1, pageSize: int = 10, db: Session = Depends(get_db)) -> Any:
    if str.strip(name) != "" :
        filter_query = or_ (
             Authdetail.detail_code.like('%' + name + '%') ,
             Authdetail.detail_name.like('%' + name + '%') ,
             Authdetail.detail_remark.like('%' + name + '%') ,
            )
        get_authdetail = authdetail.get_by_page_filter(db, filter_query=filter_query, pageIndex=pageIndex, pageSize=pageSize )
        if not get_authdetail:
            raise IdNotExist(f"系统中不存在 条件 为 {name} 的权限详情结果.")
        return resp_200(data=get_authdetail, msg=f"查询到了 条件 为 {name} 的权限详情结果.")
    else :
        raise IdNotExist(f"没有传递 条件 值.")

@router.get("/", response_model=ResultModel[AuthdetailOut], summary='查询所有权限详情(根据页码和每页个数)')
def read_authdetails(db: Session = Depends(get_db), pageIndex: int = 1, pageSize: int = 10) -> Any:
    get_authdetails = authdetail.get_multi(db, pageIndex=pageIndex, pageSize=pageSize)
    return resp_200(data=get_authdetails, msg=f"查询了第 {pageIndex} 页中的 {pageSize} 个权限详情信息.")

@router.get("/queryweb", response_model=ResultModel[AuthdetailOut], summary='根据 条件 查询权限信息')
def query_authdetail(detail_name: str = "", class_id: int = 0, pageIndex: int = 1, pageSize: int = 10) -> Any:
    where = " where 1=1 "
    where1 = " where 1=1 "
    if str.strip(detail_name) != "" :
        where = where + " and (detail_name like '%%" + str(detail_name) + "%%'"
        where = where + " or detail_code like '%%" + str(detail_name) + "%%'"
        where = where + " or detail_remark like '%%" + str(detail_name) + "%%')"
    if class_id != 0:
        where1 = where1 + " and B.class_id = " + str(class_id)
    if pageIndex<1:
        return {'code': -1, 'data': pageIndex, 'msg': f"页数小于1."}
    if pageSize<1:
        return {'code': -1, 'data': pageSize, 'msg': f"每页记录数小于1."}
    order = " order by A.id"
    group = " group by B.detail_id"
    limit = " limit " + str((pageIndex - 1) * pageSize) + "," + str(pageSize)
    if class_id != 0:
        sql = "select A.*,B.class_name from (select B.detail_id,GROUP_CONCAT(C.class_name) as class_name from authclassanddetail B left join authclass C on B.class_id=C.id " + where1 + group + ") B left join authdetail A on A.id=B.detail_id" + where + order + limit
        sqlcount = "select count(A.id) as countid from (select B.detail_id,GROUP_CONCAT(C.class_name) as class_name from authclassanddetail B left join authclass C on B.class_id=C.id " + where1 + group + ") B left join authdetail A on A.id=B.detail_id" + where + order
    else:
        sql = "select A.*,B.class_name from authdetail A left join (select B.detail_id,GROUP_CONCAT(C.class_name) as class_name from authclassanddetail B left join authclass C on B.class_id=C.id " + where1 + group + ") B on A.id=B.detail_id" + where + order + limit
        sqlcount = "select count(A.id) as countid from authdetail A left join (select B.detail_id,GROUP_CONCAT(C.class_name) as class_name from authclassanddetail B left join authclass C on B.class_id=C.id " + where1 + group + ") B on A.id=B.detail_id" + where + order
    get_authdetails = authdetail.get_by_sql(sql, sqlcount)
    if not get_authdetails:
        return {'code': -1, 'data': pageSize, 'msg': f"系统中不存在 权限查询关键字 为 {detail_name} 的权限信息结果."}
    return resp_200(data=get_authdetails, msg=f"查询到了 权限查询关键字 为 {detail_name} 的权限信息结果.")

@router.get("/querybyclassid", response_model=ResultModel[AuthdetailOut], summary='根据 条件 查询权限信息')
def query_class_id(class_id: int = 0, pageIndex: int = 1, pageSize: int = 10, db: Session = Depends(get_db)) -> Any:
    where = " where 1=1 "
    if class_id != 0 :
        where = where + " and A.ota_main_id=" + str(class_id)
        sql = "select A.*,B.ota_name from authdetail A left join otamain B on A.ota_main_id=B.id" + where
        get_authdetail = authdetail.get_by_sql_no_count(sql)
        if not get_authdetail:
            return {'code': -1, 'data': get_authdetail, 'msg': f'系统中不存在 ID 为 {class_id} 的权限结果.'}
        return resp_200(data=get_authdetail, msg=f"查询到了 ID 为 {class_id} 的权限结果.")
    else:
        return resp_400()

@router.get("/qtree", response_model=ResultModel[AuthdetailOut], summary='根据 条件 查询授权信息')
def query_authdetail_tree(detail_name: str = "") -> Any:
    where = " where 1=1 "
    if str.strip(detail_name) != "" :
        where = where + " and (detail_code like '%%" + str(detail_name) + "%%' or detai_name like '%%" + str(detail_name) + "%%' or detai_remark like '%%" + str(detail_name) + "%%')"
    sql = "select *,id as detail_id from authdetail " + where
    get_authdetails = authdetail.get_by_sql_no_count(sql)
    if not get_authdetails:
        return {'code': -1, 'data': get_authdetails, 'msg': f"系统中不存在 授权类查询关键字 为 {detail_name} 的授权类结果."}
    return resp_200(data=get_authdetails, msg=f"查询到了 授权查询关键字 为 {detail_name} 的授权结果.")

@router.post("/updatejson", response_model=ResultModel[AuthdetailOut], summary='添加权限信息')
def update_authdetail_json(*, db: Session = Depends(get_db), authdetail_in: AuthdetailCreate) -> Any:
    if authdetail_in.id != 0:
        get_authdetail = authdetail.get(db, id=authdetail_in.id)
        alter_authdetail = authdetail.update(db, db_obj=get_authdetail, obj_in=authdetail_in)
        return resp_200(data=alter_authdetail, msg=f"更新了 id 为 {id} 的权限信息.")
    else:
        version_in = dict()
        for key,value in authdetail_in:
            if key != "id":
                # 赋值字典
                version_in[key] = value
        add_authdetail = authdetail.create(db, obj_in=version_in)
        return resp_200(data=add_authdetail, msg=f"添加了 id 为 {add_authdetail.id} 的权限信息.")

@router.post("/updateform", response_model=ResultModel[AuthdetailOut], summary='添加权限信息')
def update_authdetail_form(*, id: int = Form(...), ota_v_code: str = Form(...), ota_v_name: str = Form(...), ota_v_image: str = Form(...), ota_v_file: str = Form(...), ota_main_id: str = Form(...), detail_type: int = Form(...), ota_v_remark: str = Form(...)) -> Any:
    print('id'+ str(id))
    print(id)
    if id != 0:
        raise IdNotExist(f"修改.")
    else:
        raise IdNotExist(f"ID:{id}新增.")

@router.post("/settype", response_model=ResultModel[AuthdetailOut], summary='添加权限信息')
def update_authdetail_type(*, db: Session = Depends(get_db), authdetail_in: AuthdetailType) -> Any:
    if authdetail_in.id == 0:
        return {'code': -1, 'data': "", 'msg': '缺少id！'}
    if authdetail_in.detail_type == 0 or authdetail_in.detail_type == 1:
        get_authdetail = authdetail.get(db, id=authdetail_in.id)
        alter_authdetail = authdetail.update(db, db_obj=get_authdetail, obj_in=authdetail_in)
        return resp_200(data=alter_authdetail, msg=f"更新了 id 为 {authdetail_in.id} 的权限信息默认权限信息.")
    else:
        return {'code': -1, 'data': "", 'msg': '错误参数！'}

@router.delete("/delete", response_model=ResultModel[AuthdetailOut], summary='通过 id 删除权限信息')
def delete_authdetail(*, db: Session = Depends(get_db), authdetail_id: AuthdetailDelete) -> Any:
    del_authdetail = authdetail.remove(db, id=authdetail_id.id)
    return resp_200(data=del_authdetail, msg=f"删除了 id 为 {authdetail_id.id} 的权限信息.")

@router.get("/querybyid", response_model=ResultModel[AuthdetailOut], summary='根据 条件 查询权限信息')
def query_authdetail_id(authdetail_id: int = 0) -> Any:
    where = " where 1=1 "
    if authdetail_id != 0 :
        where = where + " and A.id=" + str(authdetail_id)
        sql = "select A.*,C.class_name from authdetail A left join authclassanddetail B on A.id=B.detail_id left join authclass C on B.class_id=C.id " + where
        get_authdetails = authdetail.get_by_sql_no_count(sql)
        if not get_authdetails:
            return {'code': -1, 'data': get_authdetails, 'msg': f"系统中不存在 权限查询关键字 为 {authdetail_id} 的权限结果."}
        return resp_200(data=get_authdetails, msg=f"查询到了 权限查询关键字 为 {authdetail_id} 的权限结果.")
    else:
        return resp_400()

