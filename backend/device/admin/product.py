#!/usr/bin/env python3
# _*_ coding: utf-8 _*_
# @Time : 2022/11/28 19:18
# @Author : wdm
# @desc : 院系表接口
import json
from typing import Any, List
from fastapi import APIRouter, Depends, Request, Form
from sqlalchemy import and_, or_
from sqlalchemy.orm import Session

from device.deps import get_db
from schemas import ProductUpdate, ProductCreate, ProductOut, ProductDelete, ResultModel, ResultPlusModel
from crud import product
from utils import resp_200, resp_400, IdNotExist

from models import Product

router = APIRouter()

@router.post("/query", response_model=ResultModel[ProductOut], summary='根据 条件 查询设备类信息')
def query_product(request: Request, name: str = "", db: Session = Depends(get_db)) -> Any:
    if str.strip(name) != "" :
        filter_query = or_(
             Product.prod_code.like('%' + name + '%') ,
             Product.prod_name.like('%' + name + '%') ,
             Product.prod_remark.like('%' + name + '%') ,
            )
        get_product = product.get_by_any(db, filter_query=filter_query)
        if not get_product:
            raise IdNotExist(f"系统中不存在 条件 为 {name} 的设备类结果.")
        return resp_200(data=get_product, msg=f"查询到了 条件 为 {name} 的设备类结果.")
    else:
        return resp_400()

@router.post("/querybyprojectid", response_model=ResultModel[ProductOut], summary='根据 条件 查询设备类信息')
def query_project_id(projectId: int = 0, pageIndex: int = 1, pageSize: int = 10, db: Session = Depends(get_db)) -> Any:
    if projectId != 0 :
        if pageIndex<1:
            raise IdNotExist(f"页数小于1.")
        if pageSize<1:
            raise IdNotExist(f"每页记录数小于1.")
        filter_query = (Product.project_id == projectId)
        get_product = product.get_by_page_filter(db, filter_query=filter_query, pageIndex=pageIndex, pageSize=pageSize )
        if not get_product:
            raise IdNotExist(f"系统中不存在 ID 为 {projectId} 的设备类结果.")
        return resp_200(data=get_product, msg=f"查询到了 ID 为 {projectId} 的设备类结果.")
    else:
        return resp_400()

@router.post("/querybyname", response_model=ResultModel[ProductOut], summary='根据 条件 查询设备类信息')
def query_product_name(name: str = "", pageIndex: int = 1, pageSize: int = 10, db: Session = Depends(get_db)) -> Any:
    if str.strip(name) != "" :
        if pageIndex<1:
            raise IdNotExist(f"页数小于1.")
        if pageSize<1:
            raise IdNotExist(f"每页记录数小于1.")
        filter_query = or_ (
             Product.prod_code.like('%' + name + '%') ,
             Product.prod_name.like('%' + name + '%') ,
             Product.prod_remark.like('%' + name + '%') ,
            )
        get_product = product.get_by_page_filter(db, filter_query=filter_query, pageIndex=pageIndex, pageSize=pageSize )
        if not get_product:
            raise IdNotExist(f"系统中不存在 条件 为 {name} 的设备类结果.")
        return resp_200(data=get_product, msg=f"查询到了 条件 为 {name} 的设备类结果.")
    else :
        raise IdNotExist(f"没有传递 条件 值.")

@router.get("/", response_model=ResultModel[ProductOut], summary='查询所有设备类(根据页码和每页个数)')
def read_products(db: Session = Depends(get_db), pageIndex: int = 1, pageSize: int = 10) -> Any:
    if pageIndex<1:
        raise IdNotExist(f"页数小于1.")
    if pageSize<1:
        raise IdNotExist(f"每页记录数小于1.")
    get_products = product.get_multi(db, pageIndex=pageIndex, pageSize=pageSize)
    return resp_200(data=get_products, msg=f"查询了第 {pageIndex} 页中的 {pageSize} 个设备类信息.")

@router.get("/queryweb", response_model=ResultModel[ProductOut], summary='根据 条件 查询设备信息')
def query_product(prod_name: str = "", pageIndex: int = 1, projectId: int = 0, pageSize: int = 10) -> Any:
    where = " where 1=1 "
    if str.strip(prod_name) != "" :
        where = where + " and (prod_code like '%%" + str(prod_name) + "%%' or prod_name like '%%" + str(prod_name) + "%%' or prod_remark like '%%" + str(prod_name) + "%%')"
    if projectId != 0:
        where = where + " and project_id = " + str(projectId)
    if pageIndex<1:
        raise IdNotExist(f"页数小于1.")
    if pageSize<1:
        raise IdNotExist(f"每页记录数小于1.")
    limit = " limit " + str((pageIndex - 1) * pageSize) + "," + str(pageSize)
    sql = "select A.*,B.pro_name from product A left join project B on A.project_id=B.id" + where + limit
    sqlcount = "select count(id) as countid from product " + where
    get_products = product.get_by_sql(sql, sqlcount)
    if not get_products:
        raise IdNotExist(f"系统中不存在 设备类查询关键字 为 {prod_name} 的设备类结果.")
    return resp_200(data=get_products, msg=f"查询到了 设备类查询关键字 为 {prod_name} 的设备类结果.")

@router.get("/qtree", response_model=ResultModel[ProductOut], summary='根据 条件 查询项目信息')
def query_product_tree(prod_name: str = "") -> Any:
    where = " where 1=1 "
    if str.strip(prod_name) != "" :
        where = where + " and (prod_code like '%%" + str(prod_name) + "%%' or prod_name like '%%" + str(prod_name) + "%%' or prod_remark like '%%" + str(prod_name) + "%%')"
    sql = "select *,id as product_id,id as prod_id from product " + where
    get_products = product.get_by_sql_no_count(sql)
    if not get_products:
        raise IdNotExist(f"系统中不存在 项目类查询关键字 为 {prod_name} 的项目类结果.")
    #return {'code': 200, 'data': get_products, 'message': f"查询到了 项目类查询关键字 为 {pro_name} 的项目类结果.", 'type': 'success'}
    return resp_200(data=get_products, msg=f"查询到了项目类结果.")

@router.post("/updatejson", response_model=ResultModel[ProductOut], summary='添加设备信息')
def update_product_json(*, db: Session = Depends(get_db), product_in: ProductCreate) -> Any:
    print(product_in)
    if product_in.id != 0:
        get_product = product.get(db, id=product_in.id)
        alter_product = product.update(db, db_obj=get_product, obj_in=product_in)
        return resp_200(data=alter_product, msg=f"更新了 id 为 {id} 的设备信息.")
    else:
        prod_in = dict()
        for key,value in product_in:
            if key != "id":
                # 赋值字典
                prod_in[key] = value
        add_product = product.create(db, obj_in=prod_in)
        return resp_200(data=add_product, msg=f"添加了 id 为 {add_product.id} 的设备信息.")

@router.post("/updateform", response_model=ResultModel[ProductOut], summary='添加设备信息')
def update_product_form(*, id: int = Form(...), prod_code: str = Form(...), prod_name: str = Form(...), prod_type: int = Form(...), prod_image: str = Form(...), prod_remark: str = Form(...)) -> Any: #, product_in: ProductCreate
    print('id'+ str(id))
    print(id)
    print('prod_code' + str(prod_code))
    print('prod_name' + str(prod_name))
    print('prod_type' + str(prod_type))
    print('prod_image' + str(prod_image))
    print('prod_remark' + str(prod_remark))
    if id != 0:
        raise IdNotExist(f"修改.")
    else:
        raise IdNotExist(f"ID:{id}新增.")

@router.delete("/delete", response_model=ResultModel[ProductOut], summary='通过 id 删除设备信息')
def delete_product(*, db: Session = Depends(get_db), prod_id: ProductDelete) -> Any:
    del_product = product.remove(db, id=prod_id.id)
    return resp_200(data=del_product, msg=f"删除了 id 为 {prod_id.id} 的设备信息.")

@router.get("/querybyid", response_model=ResultModel[ProductOut], summary='根据 条件 查询设备类信息')
def query_product_id(prod_id: int = 0) -> Any:
    where = " where 1=1 "
    if prod_id != 0 :
        where = where + " and A.id=" + str(prod_id)
        sql = "select A.*,B.pro_name from product A left join project B on A.project_id=B.id" + where
        get_products = product.get_by_sql_no_count(sql)
        if not get_products:
            raise IdNotExist(f"系统中不存在 设备类查询关键字 为 {prod_id} 的设备类结果.")
        return resp_200(data=get_products, msg=f"查询到了 设备类查询关键字 为 {prod_id} 的设备类结果.")
    else:
        return resp_400()

@router.get("/queryproductota", response_model=ResultModel[ProductOut], summary='根据 条件 查询设备关联OTA信息')
def query_productota(prod_name: str = "", ota_name: str = "", prod_id: int = 0,  pageIndex: int = 1, pageSize: int = 10) -> Any:
    where = " where 1=1 and not isnull(C.ota_name)"
    if str.strip(prod_name) != "" :
        where = where + " and (prod_code like '%%" + str(prod_name) + "%%' or prod_name like '%%" + str(prod_name) + "%%' or prod_remark like '%%" + str(prod_name) + "%%')"
    if str.strip(ota_name) != "" :
        where = where + " and (ota_code like '%%" + str(ota_name) + "%%' or ota_name like '%%" + str(ota_name) + "%%' or ota_remark like '%%" + str(ota_name) + "%%')"
    if prod_id != 0 :
        where = where + " and A.id=" + str(prod_id)
    if pageIndex<1:
        raise IdNotExist(f"页数小于1.")
    if pageSize<1:
        raise IdNotExist(f"每页记录数小于1.")
    limit = " limit " + str((pageIndex - 1) * pageSize) + "," + str(pageSize)
    sql = "select distinct C.id,A.prod_name,A.prod_code,C.ota_name,C.ota_code,C.ota_image,C.ota_package,C.ota_type,C.ota_update_type,C.gmt_create from product A left join device B on A.id=B.product_id left join otamain C on B.device_ota=C.id" + where + limit
    sqlcount = "select count(A.id) as countid from (select distinct C.id,A.prod_name,A.prod_code,C.ota_name,C.ota_code,C.ota_image,C.ota_package,C.ota_type,C.ota_update_type,C.gmt_create from product A left join device B on A.id=B.product_id left join otamain C on B.device_ota=C.id" + where + ") A"
    get_products = product.get_by_sql(sql, sqlcount)
    if not get_products:
        raise IdNotExist(f"系统中不存在 设备类查询关键字 为 {prod_name} 的设备关联OTA结果.")
    return resp_200(data=get_products, msg=f"查询到了 设备类查询关键字 为 {prod_name} 的设备关联OTA结果.")
