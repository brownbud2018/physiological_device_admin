#!/usr/bin/env python3
# _*_ coding: utf-8 _*_
# @Time : 2022/11/28 19:18
# @Author : wdm
# @desc : Excelupload接口
import json
from typing import Any, List
from fastapi import APIRouter, Depends, Request, Form
from sqlalchemy import and_, or_
from sqlalchemy.orm import Session

from device.deps import get_db
from schemas import DeviceIn, ExceluploadUpdate, ExceluploadCreate, ExceluploadOut, Relation, ResultModel, ExceluploadImport, ExceluploadType, ExceluploadDelete
from crud import excelupload
from crud import device
from utils import resp_200, resp_400, IdNotExist, resp_new_200

from models import Excelupload

import os
from core import settings
from core import get_password_hash
import xlrd

from xlrd import xldate_as_tuple

import datetime

router = APIRouter()

@router.get("/query", response_model=ResultModel[ExceluploadOut], summary='根据 条件 查询上传Excel信息')
def query_excelupload(name: str = "", type: int = 0, pageIndex: int = 1, pageSize: int = 10) -> Any:
    where = " where 1=1 "
    if str.strip(name) != "" :
        where = where + " and (excel_code like '%%" + str(name) + "%%' or excel_name like '%%" + str(name) + "%%' or excel_remark like '%%" + str(name) + "%%')"
    else:
        raise IdNotExist(f"查询关键字必须.")
    where = where + " and is_import = " + str(type)
    if pageIndex<1:
        raise IdNotExist(f"页数小于1.")
    if pageSize<1:
        raise IdNotExist(f"每页记录数小于1.")
    limit = " limit " + str((pageIndex - 1) * pageSize) + "," + str(pageSize)
    sql = "select * from excelupload " + where + limit
    sqlcount = "select count(id) as countid from excelupload " + where
    get_exceluploads = excelupload.get_by_sql(sql, sqlcount)
    if not get_exceluploads:
        raise IdNotExist(f"系统中不存在 上传Excel类查询关键字 为 {name} 的上传Excel类结果.")
    return resp_200(data=get_exceluploads, msg=f"查询到了 上传Excel类查询关键字 为 {name} 的上传Excel类结果.")

@router.post("/queryandor", response_model=ResultModel[ExceluploadOut], summary='根据 条件 查询上传Excel信息')
def query_excelupload(request: Request, name: str = "", type: int = 0, pageIndex: int = 1, pageSize: int = 10, db: Session = Depends(get_db)) -> Any:
    if str.strip(name) != "" :
        if pageIndex<1:
            raise IdNotExist(f"页数小于1.")
        if pageSize<1:
            raise IdNotExist(f"每页记录数小于1.")
        filter_query = and_(
                Excelupload.is_import == type ,
            )
        filter_query1 = or_(
                Excelupload.excel_code.like('%' + name + '%') ,
                Excelupload.excel_name.like('%' + name + '%') ,
                Excelupload.excel_remark.like('%' + name + '%') ,
            )
        get_excelupload = excelupload.get_by_page_and_or(db, filter_query=filter_query,filter_query1=filter_query1, pageIndex=pageIndex, pageSize=pageSize )
        if not get_excelupload:
            raise IdNotExist(f"系统中不存在 条件 为 {name} 的上传Excel结果.")
        return resp_200(data=get_excelupload, msg=f"查询到了 条件 为 {name} 的上传Excel结果.")
    else:
        return resp_400()

@router.get("/", response_model=ResultModel[ExceluploadOut], summary='查询所有上传Excel(根据页码和每页个数)')
def read_exceluploads(db: Session = Depends(get_db), pageIndex: int = 1, pageSize: int = 10) -> Any:
    if pageIndex<1:
        raise IdNotExist(f"页数小于1.")
    if pageSize<1:
        raise IdNotExist(f"每页记录数小于1.")
    get_exceluploads = excelupload.get_multi(db, pageIndex=pageIndex, pageSize=pageSize)
    return resp_200(data=get_exceluploads, msg=f"查询了第 {pageIndex} 页中的 {pageSize} 个上传Excel信息.")

@router.get("/queryweb", response_model=ResultModel[ExceluploadOut], summary='根据 条件 查询上传Excel信息')
def query_excelupload(search_name: str = "", is_import: int = 99, pageIndex: int = 1, pageSize: int = 10) -> Any:
    where = " where 1=1 "
    if str.strip(search_name) != "" :
        where = where + " and (excel_code like '%%" + str(search_name) + "%%' or excel_name like '%%" + str(search_name) + "%%' or excel_remark like '%%" + str(search_name) + "%%')"
    if is_import != 99:
        where = where + " and is_import = " + str(is_import)
    if pageIndex<1:
        raise IdNotExist(f"页数小于1.")
    if pageSize<1:
        raise IdNotExist(f"每页记录数小于1.")
    limit = " limit " + str((pageIndex - 1) * pageSize) + "," + str(pageSize)
    sql = "select A.*,B.ota_name,C.class_name,D.prod_name from excelupload A left join otamain B on A.device_ota = B.id left join authclass C on A.device_auth_class_id=C.id left join product D on A.product_id=D.id " + where + limit
    sqlcount = "select count(A.id) as countid from excelupload A left join otamain B on A.device_ota = B.id left join authclass C on A.device_auth_class_id=C.id " + where
    get_exceluploads = excelupload.get_by_sql(sql, sqlcount)
    if not get_exceluploads:
        raise IdNotExist(f"系统中不存在 上传Excel类查询关键字 为 {search_name} 的上传Excel类结果.")
    return resp_200(data=get_exceluploads, msg=f"查询到了 上传Excel类查询关键字 为 {search_name} 的上传Excel类结果.")

@router.get("/qtree", response_model=ResultModel[ExceluploadOut], summary='根据 条件 查询上传Excel信息')
def query_excelupload_tree(excel_name: str = "", is_import: int = 99) -> Any:
    where = " where 1=1 "
    if str.strip(excel_name) != "" :
        where = where + " and (excel_code like '%%" + str(excel_name) + "%%' or excel_name like '%%" + str(excel_name) + "%%' or excel_remark like '%%" + str(excel_name) + "%%')"
    if is_import != 99:
        where = where + " and is_import = " + str(is_import)
    sql = "select *,id as excelupload_id from excelupload " + where
    get_exceluploads = excelupload.get_by_sql_no_count(sql)
    if not get_exceluploads:
        raise IdNotExist(f"系统中不存在 上传Excel类查询关键字 为 {excel_name} 的上传Excel类结果.")
    #return {'code': 200, 'data': get_exceluploads, 'message': f"查询到了 上传Excel类查询关键字 为 {excel_name} 的上传Excel类结果.", 'type': 'success'}
    return resp_200(data=get_exceluploads, msg=f"查询到了上传Excel类结果.")

@router.post("/updatejson", response_model=ResultModel[ExceluploadOut], summary='添加上传Excel信息')
def update_excelupload_json(*, db: Session = Depends(get_db), excelupload_in: ExceluploadCreate) -> Any:
    #print(excelupload_in)
    if excelupload_in.id != 0:
        get_excelupload = excelupload.get(db, id=excelupload_in.id)
        alter_excelupload = excelupload.update(db, db_obj=get_excelupload, obj_in=excelupload_in)
        return resp_200(data=alter_excelupload, msg=f"更新了 id 为 {id} 的上传Excel信息.")
    else:
        excel_in = dict()
        for key,value in excelupload_in:
            if key != "id":
                # 赋值字典
                excel_in[key] = value
        add_excelupload = excelupload.create(db, obj_in=excel_in)
        return resp_200(data=add_excelupload, msg=f"添加了 id 为 {add_excelupload.id} 的上传Excel信息.")

@router.post("/updateform", response_model=ResultModel[ExceluploadOut], summary='添加上传Excel信息')
def update_excelupload_form(*, id: int = Form(...), excel_code: str = Form(...), excel_name: str = Form(...), is_import: int = Form(...), pro_image: str = Form(...), excel_remark: str = Form(...)) -> Any: #, excelupload_in: ExceluploadCreate
    print('id'+ str(id))
    print(id)
    print('excel_code' + str(excel_code))
    print('excel_name' + str(excel_name))
    print('is_import' + str(is_import))
    print('pro_image' + str(pro_image))
    print('excel_remark' + str(excel_remark))
    if id != 0:
        raise IdNotExist(f"修改.")
    else:
        raise IdNotExist(f"ID:{id}新增.")

@router.post("/settype", response_model=ResultModel[ExceluploadOut], summary='添加上传Excel信息')
def update_excelupload_type(*, db: Session = Depends(get_db), excelupload_in: ExceluploadType) -> Any:
    if excelupload_in.id == 0:
        raise IdNotExist(f"缺少id.")
    if excelupload_in.is_import == 0 or excelupload_in.is_import == 1:
        get_excelupload = excelupload.get(db, id=excelupload_in.id)
        alter_excelupload = excelupload.update(db, db_obj=get_excelupload, obj_in=excelupload_in)
        return resp_200(data=alter_excelupload, msg=f"更新了 id 为 {excelupload_in.id} 的上传Excel类型信息.")
    else:
        raise IdNotExist(f"缺少参数.")

@router.post("/setimport", response_model=ResultModel[ExceluploadOut], summary='导入上传Excel信息')
def update_excelupload_import(*, db: Session = Depends(get_db), excelupload_in: ExceluploadImport) -> Any:
    if excelupload_in.id == 0:
        raise IdNotExist(f"缺少id.")
    get_excelupload = excelupload.get_by_sql_fetchone("select * from excelupload where id = " + str(excelupload_in.id))
    if not get_excelupload:
        return {'code': -1, 'data': get_excelupload, 'msg': f"系统中不存在 上传查询关键字 为 {excelupload_in.id} 的上传结果."}
    else:
        outdata = dict()
        excel_data = get_excelupload.excel_address
        filename = f"{excel_data}"
        if os.path.isfile(filename):
            data = xlrd.open_workbook(filename)
            table = data.sheets()[0]#Excel第一个工作表
            tables1 = table.col_values(0)#第一列
            for i in range(len(tables1)):
                #print(tables1[i])#第一列的每一行代表对应的：device_code
                get_device = device.get_by_device_code(db, name=tables1[i])#查找device表里面有没有device_code对应的记录
                if not get_device:
                    #不存在，则新增
                    excel_in_device = dict()
                    excel_in_device['device_code']          = tables1[i]
                    excel_in_device['name']                 = get_excelupload.name
                    excel_in_device['device_ota']           = get_excelupload.device_ota
                    excel_in_device['version']              = get_excelupload.version
                    excel_in_device['product_id']           = get_excelupload.product_id
                    excel_in_device['address']              = get_excelupload.address
                    excel_in_device['image']                = get_excelupload.image
                    excel_in_device['is_active']            = get_excelupload.is_active
                    excel_in_device['device_level']         = get_excelupload.device_level
                    excel_in_device['device_auth_class_id'] = get_excelupload.device_auth_class_id
                    excel_in_device['password']             = get_excelupload.hashed_password

                    add_device = device.create(db, obj_in=excel_in_device)
                    outdata['msg' + str(i) + ':'] = str(tables1[i]) + '添加成功，新增ID是：' + str(add_device.id)
                else:
                    #已经存，则修改
                    excel_in_device = dict()
                    excel_in_device['device_code']          = tables1[i]
                    excel_in_device['name']                 = get_excelupload.name
                    excel_in_device['device_ota']           = get_excelupload.device_ota
                    excel_in_device['version']              = get_excelupload.version
                    excel_in_device['product_id']           = get_excelupload.product_id
                    excel_in_device['address']              = get_excelupload.address
                    excel_in_device['image']                = get_excelupload.image
                    excel_in_device['is_active']            = get_excelupload.is_active
                    excel_in_device['device_level']         = get_excelupload.device_level
                    excel_in_device['device_auth_class_id'] = get_excelupload.device_auth_class_id
                    excel_in_device['password']             = get_excelupload.hashed_password

                    add_device = device.update(db, db_obj=get_device, obj_in=excel_in_device)
                    outdata['msg' + str(i) + ':'] = str(tables1[i]) +  '修改成功。'
        get_excelupload = excelupload.get(db, id=excelupload_in.id)
        update_obj = dict()
        update_obj['id'] = excelupload_in.id
        update_obj['is_import'] = 1
        #alter_excelupload = excelupload.update(db, db_obj=get_excelupload, obj_in=excelupload_in)
        alter_excelupload = excelupload.update(db, db_obj=get_excelupload, obj_in=update_obj)
        return resp_200(data=outdata, msg=f"更新了 id 为 {excelupload_in.id} 的上传Excel导入信息.")

@router.delete("/delete", response_model=ResultModel[ExceluploadOut], summary='通过 id 删除上传Excel信息')
def delete_excelupload(*, db: Session = Depends(get_db), excel_id: ExceluploadDelete) -> Any:
    if excel_id.id == 0:
        raise IdNotExist(f"缺少id.")
    get_excelupload = excelupload.get_by_sql_fetchone("select * from excelupload where id = " + str(excel_id.id))
    if not get_excelupload:
        return {'code': -1, 'data': get_excelupload, 'msg': f"系统中不存在 上传ExcelID 为 {excel_id.id} 的上传Excel结果."}
    else:
        outdata = dict()
        excel_data = get_excelupload.excel_address
        filename = f"{excel_data}"
        if os.path.isfile(filename):
            data = xlrd.open_workbook(filename)
            table = data.sheets()[0]#Excel第一个工作表
            tables1 = table.col_values(0)#第一列
            for i in range(len(tables1)):
                #print(tables1[i])#第一列的每一行代表对应的：device_code
                get_device = device.get_by_device_code(db, name=tables1[i])#查找device表里面有没有device_code对应的记录
                if get_device == None:
                    #Device表不存在记录
                    outdata['msg' + str(i) + ':'] = str(tables1[i]) +  '不存在。'
                else:
                    if get_device.id>0:
                        #已经存，则删除
                        del_device = device.remove(db, id=get_device.id)
                        outdata['msg' + str(i) + ':'] = str(tables1[i]) +  '删除成功。'
        del_excelupload = excelupload.remove(db, id=excel_id.id)
        return resp_200(data=del_excelupload, msg=f"删除了 id 为 {excel_id.id} 的上传Excel信息.")

@router.get("/querybyid", response_model=ResultModel[ExceluploadOut], summary='根据 条件 查询上传信息')
def query_excelupload_id(excel_id: int = 0) -> Any:
    where = " where 1=1 "
    if excel_id != 0 :
        where = where + " and A.id=" + str(excel_id)
        sql = "select A.*,B.ota_name,C.class_name,D.prod_name from excelupload A left join otamain B on A.device_ota = B.id left join authclass C on A.device_auth_class_id=C.id left join product D on A.product_id=D.id " + where
        #sql = "select A.* from excelupload A " + where
        get_exceluploads = excelupload.get_by_sql_fetchall(sql)
        backdata = {'data': get_exceluploads}
        if not get_exceluploads:
            return {'code': -1, 'data': get_exceluploads, 'msg': f"系统中不存在 上传查询关键字 为 {excel_id} 的上传结果."}
        else:
            excel_data = get_exceluploads[0]['excel_address']
            filename = f"{excel_data}"
            if os.path.isfile(filename):
                data = xlrd.open_workbook(filename)
                table = data.sheets()[0]
                tables1 = table.col_values(0)
                backdata['table'] = tables1
        return resp_200(data=backdata, msg=f"查询到了 上传查询关键字 为 {excel_id} 的上传结果.")
    else:
        return resp_400()

# 将excel表格内容导入到tables列表中

def import_excel(excel):
    tables = []

    for i in range(excel.nrows):
        tables.append(excel.cell_value(i,0))#第一列
    return tables
