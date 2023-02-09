#!/usr/bin/env python3
# _*_ coding: utf-8 _*_
# @Time : 2022/11/28 19:18
# @Author : wdm
# @desc : dm_physique表接口
import datetime
from typing import Any, List
from fastapi import APIRouter, Depends, Request, File, UploadFile
from sqlalchemy.orm import Session

from schemas import Dm_physiqueUpdate, Dm_physiqueCreate, Dm_physiqueOut, Relation, ResultModel, Dm_physiqueDelete
from crud import dm_physique
from utils import resp_200, resp_400, IdNotExist, logger

from models import Device, Dm_physique

from device.deps import get_db, get_current_user1

router = APIRouter()


@router.get("/", response_model=ResultModel[Dm_physiqueOut], summary='体质辨识列表')
def query_dm_physique(pageIndex: int = 1, pageSize: int = 10) -> Any:
    where = " where 1=1 "
    if pageIndex<1:
        raise IdNotExist(f"页数小于1.")
    if pageSize<1:
        raise IdNotExist(f"每页记录数小于1.")
    limit = " limit " + str((pageIndex - 1) * pageSize) + "," + str(pageSize)
    sql = "select a.*,b.`name` as username,c.device_code,c.`name` as device_name from dm_physique a left join dm_user b on a.dmuserid=b.id left join device c on b.deviceid=c.device_code " + where + limit
    sqlcount = "select count(a.id) as countid from dm_physique a left join dm_user b on a.dmuserid=b.id left join device c on b.deviceid=c.device_code " + where
    get_device = dm_physique.get_by_sql(sql, sqlcount)
    if not get_device:
        raise IdNotExist(f"系统中不存在 相关 的查询结果.")
    return resp_200(data=get_device, msg=f"查询到了 体质辨识列表 的查询结果.")

@router.get("/queryweb", response_model=ResultModel[Dm_physiqueOut], summary='根据 条件 查询体质辨识信息')
def query_dm_physique(content: str = "", dmuserid: int = 0, device_id: int = 0, pageIndex: int = 1, pageSize: int = 10) -> Any:
    where = " where ifnull(B.name,'null_name-not_select')<>'null_name-not_select'"
    if str.strip(content) != "" :
        where = where + " and (A.dmusername like '%%" + str(content) + "%%'"
        where = where + " or B.`name` like '%%" + str(content) + "%%'"
        where = where + " or C.`name` like '%%" + str(content) + "%%')"
    if dmuserid != 0:
        where = where + " and A.dmuserid = " + str(dmuserid)
    if device_id != 0:
        where = where + " and C.device_code = '" + str(device_id) + "'"
    if pageIndex<1:
        raise IdNotExist(f"页数小于1.")
    if pageSize<1:
        raise IdNotExist(f"每页记录数小于1.")
    order = " order by A.id desc"
    limit = " limit " + str((pageIndex - 1) * pageSize) + "," + str(pageSize)
    sql = "select A.*,B.`name` as username,c.device_code,C.`name` as device_name "\
          " from dm_physique A left join dm_user B on A.dmuserid=B.id left join device C on B.deviceid=C.device_code " + where + order + limit
    sqlcount = "select count(A.id) as countid from dm_physique A left join dm_user B on A.dmuserid=B.id left join device C on B.deviceid=C.device_code " + where + order
    #print(sql)
    get_dm_physiques = dm_physique.get_by_sql(sql, sqlcount)
    if not get_dm_physiques:
        raise IdNotExist(f"系统中不存在 体质辨识查询关键字 为 {content} 的体质辨识结果.")
    return resp_200(data=get_dm_physiques, msg=f"查询到了 体质辨识查询关键字 为 {content} 的体质辨识结果.")

@router.post("/updatejson", response_model=ResultModel[Dm_physiqueOut], summary='添加修改体质辨识信息')
def update_dm_physique_json(*, db: Session = Depends(get_db), dm_physique_in: Dm_physiqueCreate) -> Any:
    if dm_physique_in.id != 0:
        get_dm_physique = dm_physique.get(db, id=dm_physique_in.id)
        alter_dm_physique = dm_physique.update(db, db_obj=get_dm_physique, obj_in=dm_physique_in)
        return resp_200(data=alter_dm_physique, msg=f"更新了 id 为 {dm_physique_in.id} 的体质辨识信息.")
    else:
        log_in = dict()
        for key,value in dm_physique_in:
            if key != "id":
                # 赋值字典
                log_in[key] = value
        add_dm_physique = dm_physique.create(db, obj_in=log_in)
        return resp_200(data=add_dm_physique, msg=f"添加了 id 为 {add_dm_physique.id} 的体质辨识信息.")

@router.delete("/delete", response_model=ResultModel[Dm_physiqueOut], summary='通过 id 删除体质辨识信息')
def delete_dm_physique(*, db: Session = Depends(get_db), dm_physique_in: Dm_physiqueDelete) -> Any:
    del_dm_physique = dm_physique.remove(db, id=dm_physique_in.id)
    return resp_200(data=del_dm_physique, msg=f"删除了 id 为 {dm_physique_in.id} 的体质辨识信息.")