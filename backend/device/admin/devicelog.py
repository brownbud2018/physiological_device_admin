#!/usr/bin/env python3
# _*_ coding: utf-8 _*_
# @Time : 2022/11/28 19:18
# @Author : wdm
# @desc : devicelog表接口
import datetime
from typing import Any, List
from fastapi import APIRouter, Depends, Request, File, UploadFile
from sqlalchemy import and_, or_
from sqlalchemy.orm import Session

from schemas import DevicelogUpdate, DevicelogCreate, DevicelogOut, Relation, ResultModel, DevicelogDelete
from crud import devicelog
from utils import resp_200, resp_400, IdNotExist, logger

from models import Device, Devicelog

import shutil
from core import settings
from utils.create_dir import create_dir
from pathlib import Path
from tempfile import NamedTemporaryFile
from device.deps import get_db, get_current_user1

router = APIRouter()


@router.get("/", response_model=ResultModel[DevicelogOut], summary='Device_log列表')
def query_devicelog(pageIndex: int = 1, pageSize: int = 10) -> Any:
    where = " where 1=1 "
    if pageIndex<1:
        raise IdNotExist(f"页数小于1.")
    if pageSize<1:
        raise IdNotExist(f"每页记录数小于1.")
    limit = " limit " + str((pageIndex - 1) * pageSize) + "," + str(pageSize)
    sql = "select a.*,b.device_code,b.name from devicelog a left join device b on a.device_id=b.id " + where + limit
    sqlcount = "select count(a.id) as countid from devicelog a left join device b on a.device_id=b.id " + where
    get_device = devicelog.get_by_sql(sql, sqlcount)
    if not get_device:
        raise IdNotExist(f"系统中不存在 相关 的查询结果.")
    return resp_200(data=get_device, msg=f"查询到了 Device_log列表 的查询结果.")

@router.get("/querybydeviceid", response_model=ResultModel[DevicelogOut], summary='根据deviceID查询log日志')
def query_log_by_deviceid(deviceId:int = 0, pageIndex: int = 1, pageSize: int = 10) -> Any:
    #raise IdNotExist(f"系统中不存在 相关 的查询结果.")
    where = " where 1=1 "
    if deviceId == 0:
        raise IdNotExist(f"没有传递参数.")
    if deviceId != 0 :
        where = where + " and a.device_id = " + str(deviceId)
    if pageIndex<1:
        raise IdNotExist(f"页数小于1.")
    if pageSize<1:
        raise IdNotExist(f"每页记录数小于1.")
    limit = " limit " + str((pageIndex - 1) * pageSize) + "," + str(pageSize)
    sql = "select a.*,b.device_code,b.name from devicelog a left join device b on a.device_id=b.id " + where + limit
    sqlcount = "select count(a.id) as countid from devicelog a left join device b on a.device_id=b.id " + where
    get_device = devicelog.get_by_sql(sql, sqlcount)
    if not get_device:
        raise IdNotExist(f"系统中不存在 相关 的查询结果.")
    return resp_200(data=get_device, msg=f"查询到了 根据deviceID查询log日志 的查询结果.")

@router.get("/querybyprodid", response_model=ResultModel[DevicelogOut], summary='根据deviceID查询log日志')
def query_log_by_prodid(prod_id:int = 0, search_name: str = "", pageIndex: int = 1, pageSize: int = 10) -> Any:
    #raise IdNotExist(f"系统中不存在 相关 的查询结果.")
    where = " where 1=1 "
    if str.strip(search_name) != "" :
        where = where + " and (c.prod_code like '%%" + str(search_name) + "%%' or c.prod_name like '%%" + str(search_name) + "%%' or b.device_code like '%%" + str(search_name) + "%%' or b.name like '%%" + str(search_name) + "%%' or a.log_code like '%%" + str(search_name) + "%%')"
    if prod_id == 0:
        raise IdNotExist(f"没有传递参数.")
    if prod_id != 0 :
        where = where + " and a.device_id in (select id as device_id from device where product_id = " + str(prod_id) + ")"
    if pageIndex<1:
        raise IdNotExist(f"页数小于1.")
    if pageSize<1:
        raise IdNotExist(f"每页记录数小于1.")
    order = " order by a.id desc"
    limit = " limit " + str((pageIndex - 1) * pageSize) + "," + str(pageSize)
    sql = "select a.*,b.device_code,b.name as device_name,c.prod_code,c.prod_name from devicelog a left join device b on a.device_id=b.id left join product c on b.product_id=c.id " + where + order + limit
    sqlcount = "select count(a.id) as countid from devicelog a left join device b on a.device_id=b.id left join product c on b.product_id=c.id " + where
    get_device = devicelog.get_by_sql(sql, sqlcount)
    if not get_device:
        raise IdNotExist(f"系统中不存在 相关 的查询结果.")
    return resp_200(data=get_device, msg=f"查询到了 根据deviceID查询log日志 的查询结果.")

@router.post("/upload/file", summary="上传log")
async def upload_log(
        file: UploadFile = File(...),
        current_user: Device = Depends(get_current_user1),
        db: Session = Depends(get_db)
):
    static_path = create_dir(settings.STATIC_DIR + "/log")
    logger.info(f"用户 {current_user.name} 正在上传文件 {file.filename}.")
    try:
        suffix = Path(file.filename).suffix
        with NamedTemporaryFile(delete=False, suffix=suffix, dir=static_path) as tmp:
            shutil.copyfileobj(file.file, tmp)
            tmp_file_name = Path(tmp.name).name
    finally:
        file.file.close()
    user = "ID:" + str(current_user.id) + ",编号：" + str(current_user.device_code) + ",名称：" + str(current_user.name)
    cur_time = datetime.datetime.now()
    date_str = cur_time.strftime('%y%m%d')
    time_str = cur_time.strftime('%H%M%S')
    data = {
        'log_code': 'Log' + date_str + time_str,
        'device_id': current_user.id,
        'log_image': f"{settings.STATIC_DIR}/log/{tmp_file_name}",
    }
    add_log = devicelog.create(db, obj_in=data)
    backdata = {'user': user, 'file_temp': f"{settings.STATIC_DIR}/log/{tmp_file_name}", 'create_data': add_log}
    return resp_200(data=backdata, msg='上传成功！')

@router.get("/queryweb", response_model=ResultModel[DevicelogOut], summary='根据 条件 查询日志信息')
def query_devicelog(log_name: str = "", prod_id: int = 0, device_id: int = 0, pageIndex: int = 1, pageSize: int = 10) -> Any:
    where = " where 1=1 "
    if str.strip(log_name) != "" :
        where = where + " and (A.log_code like '%%" + str(log_name) + "%%'"
        where = where + " or B.name like '%%" + str(log_name) + "%%'"
        where = where + " or B.device_code like '%%" + str(log_name) + "%%'"
        where = where + " or C.prod_code like '%%" + str(log_name) + "%%'"
        where = where + " or C.prod_name like '%%" + str(log_name) + "%%')"
    if prod_id != 0:
        where = where + " and C.id = " + str(prod_id)
    if device_id != 0:
        where = where + " and B.id = " + str(device_id)
    if pageIndex<1:
        raise IdNotExist(f"页数小于1.")
    if pageSize<1:
        raise IdNotExist(f"每页记录数小于1.")
    order = " order by A.id"
    limit = " limit " + str((pageIndex - 1) * pageSize) + "," + str(pageSize)
    sql = "select A.*,B.name as device_name,C.prod_name,B.device_code,C.prod_code from devicelog A left join device B on A.device_id=B.id left join product C on B.product_id=C.id " + where + order + limit
    sqlcount = "select count(A.id) as countid from devicelog A left join device B on A.device_id=B.id left join product C on B.product_id=C.id " + where + order
    get_devicelogs = devicelog.get_by_sql(sql, sqlcount)
    if not get_devicelogs:
        raise IdNotExist(f"系统中不存在 日志查询关键字 为 {log_name} 的日志结果.")
    return resp_200(data=get_devicelogs, msg=f"查询到了 日志查询关键字 为 {log_name} 的日志结果.")

@router.post("/updatejson", response_model=ResultModel[DevicelogOut], summary='添加修改日志信息')
def update_devicelog_json(*, db: Session = Depends(get_db), devicelog_in: DevicelogCreate) -> Any:
    if devicelog_in.id != 0:
        get_devicelog = devicelog.get(db, id=devicelog_in.id)
        alter_devicelog = devicelog.update(db, db_obj=get_devicelog, obj_in=devicelog_in)
        return resp_200(data=alter_devicelog, msg=f"更新了 id 为 {devicelog_in.id} 的日志信息.")
    else:
        log_in = dict()
        for key,value in devicelog_in:
            if key != "id":
                # 赋值字典
                log_in[key] = value
        add_devicelog = devicelog.create(db, obj_in=log_in)
        return resp_200(data=add_devicelog, msg=f"添加了 id 为 {add_devicelog.id} 的日志信息.")

@router.delete("/delete", response_model=ResultModel[DevicelogOut], summary='通过 id 删除日志信息')
def delete_devicelog(*, db: Session = Depends(get_db), devicelog_in: DevicelogDelete) -> Any:
    del_devicelog = devicelog.remove(db, id=devicelog_in.id)
    return resp_200(data=del_devicelog, msg=f"删除了 id 为 {devicelog_in.id} 的日志信息.")