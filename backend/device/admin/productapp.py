#!/usr/bin/env python3
# _*_ coding: utf-8 _*_
# @Time : 2022/11/28 19:18
# @Author : wdm
# @desc : productapp表接口

from typing import Any, List
from fastapi import APIRouter, Depends, Request, Form
from sqlalchemy import and_, or_
from sqlalchemy.orm import Session

from device.deps import get_db
from schemas import ProductappUpdate, ProductappCreate, ProductappOut, Relation, ResultModel, ProductappDelete
from crud import productapp
from utils import resp_200, resp_400, IdNotExist

from models import Productapp

router = APIRouter()


@router.get("/", response_model=ResultModel[ProductappOut], summary='根据设备类ID查询APPPro')
def query_app_by_prodid(prod_id:int = 0, pageIndex: int = 1, pageSize: int = 10) -> Any:
    if prod_id == 0:
        raise IdNotExist(f"没有传递参数.")
    where = " where 1=1 "
    if prod_id != 0 :
        where = where + " and a.prod_id = " + str(prod_id)
    if pageIndex<1:
        raise IdNotExist(f"页数小于1.")
    if pageSize<1:
        raise IdNotExist(f"每页记录数小于1.")
    limit = " limit " + str((pageIndex - 1) * pageSize) + "," + str(pageSize)
    sql = "select b.* from productapp a  left join apppro b on a.app_pro_id=b.id " + where + limit
    sqlcount = "select count(b.id) as countid from productapp a  left join apppro b on a.app_pro_id=b.id " + where
    get_device = productapp.get_by_sql(sql, sqlcount)
    if not get_device:
        raise IdNotExist(f"系统中不存在 相关 的查询结果.")
    return resp_200(data=get_device, msg=f"查询到了 根据设备类ID查询APPPro 的查询结果.")

@router.get("/querybyappproid", response_model=ResultModel[ProductappOut], summary='根据设备类ID查询APPPro')
def query_product_by_appproid(app_pro_id:int = 0, pageIndex: int = 1, pageSize: int = 10) -> Any:
    if app_pro_id == 0:
        raise IdNotExist(f"没有传递参数.")
    where = " where 1=1 "
    if app_pro_id != 0 :
        where = where + " and a.app_pro_id = " + str(app_pro_id)
    if pageIndex<1:
        raise IdNotExist(f"页数小于1.")
    if pageSize<1:
        raise IdNotExist(f"每页记录数小于1.")
    limit = " limit " + str((pageIndex - 1) * pageSize) + "," + str(pageSize)
    sql = "select b.* from productapp a  left join product b on a.prod_id=b.id " + where + limit
    sqlcount = "select count(b.id) as countid from productapp a  left join product b on a.prod_id=b.id " + where
    get_device = productapp.get_by_sql(sql, sqlcount)
    if not get_device:
        raise IdNotExist(f"系统中不存在 相关 的查询结果.")
    return resp_200(data=get_device, msg=f"查询到了 根据设备类ID查询APPPro 的查询结果.")

@router.get("/queryallappbyprodid", response_model=ResultModel[ProductappOut], summary='根据设备类ID查询APP分类+APP+版本')
def query_allapp_by_prodid(prod_id:int = 0, pageIndex: int = 1, pageSize: int = 10) -> Any:
    if prod_id == 0:
        raise IdNotExist(f"没有传递参数.")
    where = " where 1=1 "
    if prod_id != 0 :
        where = where + " and a.prod_id = " + str(prod_id)
    if pageIndex<1:
        raise IdNotExist(f"页数小于1.")
    if pageSize<1:
        raise IdNotExist(f"每页记录数小于1.")
    limit = " limit " + str((pageIndex - 1) * pageSize) + "," + str(pageSize)
    sql = "select b.*,c.class_code,c.class_name,c.class_image,c.class_desc,c.class_remark " \
          "from productapp a  left join apppro b on a.app_pro_id=b.id " \
          "left join appclass c on b.app_class_id=c.id " + where + limit
    sqlcount = "select count(b.id) as countid from productapp a  left join apppro b on a.app_pro_id=b.id left join appclass c on b.app_class_id=c.id " + where

    data = productapp.get_data_by_sql(sql)
    #print(data)
    #返回数据data：List[dict]
    # 示例：[{第一条记录},{第二条记录},{第三条记录}]
    # [
    # {'id': 1, 'app_code': 'wechat', 'app_name': '微信', 'app_image': 'static/author.jpg', 'app_package': 'com.tencent.mm', 'app_type': 1, 'app_update_type': 0, 'app_class_id': 1, 'app_info': '微信简介', 'app_score': Decimal('3.4'), 'app_download_amount': 13800000000, 'app_company': '腾讯', 'app_desc': '微信APP描述', 'app_remark': '这就是个测试APP微信', 'gmt_create': datetime.datetime(2022, 4, 15, 10, 9, 59), 'gmt_modify': datetime.datetime(2022, 4, 15, 10, 9, 59), 'class_code': 'chat', 'class_name': '聊天通信', 'class_image': 'static/author.jpg', 'class_desc': '聊天通信描述', 'class_remark': 'APP的聊天通信类'},
    # {'id': 2, 'app_code': 'jingdong', 'app_name': '京东', 'app_image': 'static/author.jpg', 'app_package': 'com.jingdong.app.mall', 'app_type': 1, 'app_update_type': 0, 'app_class_id': 2, 'app_info': '京东简介', 'app_score': Decimal('2.3'), 'app_download_amount': 15400000000, 'app_company': '京东', 'app_desc': '京东APP描述', 'app_remark': '这就是个测试APP京东', 'gmt_create': datetime.datetime(2022, 4, 15, 10, 9, 59), 'gmt_modify': datetime.datetime(2022, 4, 15, 10, 9, 59), 'class_code': 'onlinebusiness', 'class_name': '电商', 'class_image': 'static/author.jpg', 'class_desc': '电商描述', 'class_remark': 'APP的电商类'},
    # {'id': 3, 'app_code': 'taobao', 'app_name': '淘宝', 'app_image': 'static/author.jpg', 'app_package': 'com.taobao.taobao', 'app_type': 1, 'app_update_type': 0, 'app_class_id': 2, 'app_info': '淘宝简介', 'app_score': Decimal('2.7'), 'app_download_amount': 15000000000, 'app_company': '阿里巴巴', 'app_desc': '淘宝APP描述', 'app_remark': '这就是个测试APP淘宝', 'gmt_create': datetime.datetime(2022, 4, 15, 10, 9, 59), 'gmt_modify': datetime.datetime(2022, 4, 15, 10, 9, 59), 'class_code': 'onlinebusiness', 'class_name': '电商', 'class_image': 'static/author.jpg', 'class_desc': '电商描述', 'class_remark': 'APP的电商类'}
    # ]
    if not data:
        raise IdNotExist(f"系统中不存在 相关 的查询结果.")
    for result in data:
        appid = result["id"]
        where = " where 1=1 and app_pro_id = " + str(appid)
        sql = "select * from appversion " + where
        datachild = productapp.get_data_by_sql(sql)
        result["child"] = datachild
    count = productapp.get_count_by_sql(sqlcount)
    backdata = {'count': count, 'dataList': data}
    return {'code': 200, 'data': backdata, 'msg': "查询到了 根据设备类ID查询相关APP分类+APP+APPVersion 的查询结果."}



@router.get("/queryweb", response_model=ResultModel[ProductappOut], summary='根据 条件 查询product关联app信息')
def query_productapp(productapp_name: str = "", prod_id: int = 0, app_pro_id: int = 0, pageIndex: int = 1, pageSize: int = 10) -> Any:
    where = " where 1=1 "
    if str.strip(productapp_name) != "" :
        where = where + " and (B.prod_name like '%%" + str(productapp_name) + "%%'"
        where = where + " or B.prod_code like '%%" + str(productapp_name) + "%%'"
        where = where + " or C.app_code like '%%" + str(productapp_name) + "%%'"
        where = where + " or C.app_name like '%%" + str(productapp_name) + "%%')"
    if app_pro_id != 0:
        where = where + " and A.app_pro_id = " + str(app_pro_id)
    if prod_id != 0:
        where = where + " and A.prod_id = " + str(prod_id)
    if pageIndex<1:
        raise IdNotExist(f"页数小于1.")
    if pageSize<1:
        raise IdNotExist(f"每页记录数小于1.")
    order = " order by A.id"
    limit = " limit " + str((pageIndex - 1) * pageSize) + "," + str(pageSize)
    sql = "select A.*,B.prod_name,C.app_name,B.prod_code,C.app_code from productapp A left join product B on A.prod_id=B.id left join apppro C on A.app_pro_id=C.id " + where + order + limit
    sqlcount = "select count(A.id) as countid from productapp A left join product B on A.prod_id=B.id left join apppro C on A.app_pro_id=C.id " + where
    get_productapps = productapp.get_by_sql(sql, sqlcount)
    if not get_productapps:
        raise IdNotExist(f"系统中不存在 设备类型关联app查询关键字 为 {productapp_name} 的设备类型关联app结果.")
    return resp_200(data=get_productapps, msg=f"查询到了 设备类型关联app查询关键字 为 {productapp_name} 的设备类型关联app结果.")

@router.post("/updatejson", response_model=ResultModel[ProductappOut], summary='添加修改设备类型关联app信息')
def update_productapp_json(*, db: Session = Depends(get_db), productapp_in: ProductappCreate) -> Any:
    if productapp_in.id != 0:
        sqlcount = "select count(id) as countid from productapp where app_pro_id = " + str(productapp_in.app_pro_id) + " and prod_id = " + str(productapp_in.prod_id) + " and id <> " + str(productapp_in.id)
        get_exist_count = productapp.get_by_sql_is_exist(sqlcount)
        if get_exist_count > 0:#已经存在关联，禁止修改
            return {'code': -1, 'data': get_exist_count, 'msg': '已经存在关联！'}
        get_productapp = productapp.get(db, id=productapp_in.id)
        alter_productapp = productapp.update(db, db_obj=get_productapp, obj_in=productapp_in)
        return resp_200(data=alter_productapp, msg=f"更新了 id 为 {productapp_in.id} 的设备类型关联app信息.")
    else:
        sqlcount = "select count(id) as countid from productapp where app_pro_id = " + str(productapp_in.app_pro_id) + " and prod_id = " + str(productapp_in.prod_id)
        get_exist_count = productapp.get_by_sql_is_exist(sqlcount)
        if get_exist_count > 0:#已经存在关联，禁止修改
            return {'code': -1, 'data': get_exist_count, 'msg': '已经存在关联！'}
        pro_app_in = dict()
        for key,value in productapp_in:
            if key != "id":
                # 赋值字典
                pro_app_in[key] = value
        add_productapp = productapp.create(db, obj_in=pro_app_in)
        return resp_200(data=add_productapp, msg=f"添加了 id 为 {add_productapp.id} 的设备类型关联app信息.")

@router.delete("/delete", response_model=ResultModel[ProductappOut], summary='通过 id 删除设备类型关联app信息')
def delete_apppro(*, db: Session = Depends(get_db), productapp_in: ProductappDelete) -> Any:
    del_apppro = productapp.remove(db, id=productapp_in.id)
    return resp_200(data=del_apppro, msg=f"删除了 id 为 {productapp_in.id} 的设备类型关联app信息.")