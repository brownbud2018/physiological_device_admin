#!/usr/bin/env python3
# _*_ coding: utf-8 _*_
# @Time : 2022/11/28 19:18
# @Author : wdm
# @desc : ecs_consulting表接口
import datetime
from typing import Any, List
from fastapi import APIRouter, Depends, Request, File, UploadFile
from sqlalchemy.orm import Session

from schemas import Ecs_ConsultingUpdate, Ecs_ConsultingCreate, Ecs_ConsultingOut, Relation, ResultModel, Ecs_ConsultingDelete
from crud import ecs_consulting
from utils import resp_200, resp_400, IdNotExist, logger

from models import Device, Ecs_Consulting, Admin

from device.deps import get_db, get_current_user1
from api.deps import getUserDeviceWhere, get_current_user

router = APIRouter()


@router.get("/", response_model=ResultModel[Ecs_ConsultingOut], summary='Device_log列表')
def query_ecs_consulting(
        pageIndex: int = 1, pageSize: int = 10,
        db: Session = Depends(get_db), current_user: Admin = Depends(get_current_user)
    ) -> Any:
    where = " where 1=1 "
    strWhereUser = getUserDeviceWhere(db,current_user)
    where += strWhereUser
    if pageIndex<1:
        raise IdNotExist(f"页数小于1.")
    if pageSize<1:
        raise IdNotExist(f"每页记录数小于1.")
    limit = " limit " + str((pageIndex - 1) * pageSize) + "," + str(pageSize)
    sql = "select a.*,b.device_code,b.name from ecs_consulting a left join device b on a.device_id=b.id " + where + limit
    sqlcount = "select count(a.id) as countid from ecs_consulting a left join device b on a.device_id=b.id " + where
    get_device = ecs_consulting.get_by_sql(sql, sqlcount)
    if not get_device:
        raise IdNotExist(f"系统中不存在 相关 的查询结果.")
    return resp_200(data=get_device, msg=f"查询到了 咨询列表列表 的查询结果.")

@router.get("/queryweb", response_model=ResultModel[Ecs_ConsultingOut], summary='根据 条件 查询咨询列表信息')
def query_ecs_consulting(
        content: str = "", leaguer_id: int = 0, device_id: int = 0, pageIndex: int = 1, pageSize: int = 10,
        db: Session = Depends(get_db), current_user: Admin = Depends(get_current_user)
     ) -> Any:
    where = " where ifnull(C.name,'null_name-not_select')<>'null_name-not_select' and A.type = 10 and is_payed = 1"
    strWhereUser = getUserDeviceWhere(db,current_user)
    where += strWhereUser
    if str.strip(content) != "" :
        where = where + " and (A.content like '%%" + str(content) + "%%'"
        where = where + " or A.last_reply_content like '%%" + str(content) + "%%'"
        where = where + " or A.device_id like '%%" + str(content) + "%%'"
        where = where + " or C.`name` like '%%" + str(content) + "%%'"
        where = where + " or D.`name` like '%%" + str(content) + "%%')"
    if leaguer_id != 0:
        where = where + " and A.leaguer_id = " + str(leaguer_id)
    if device_id != 0:
        where = where + " and A.device_id = " + str(device_id)
    if pageIndex<1:
        raise IdNotExist(f"页数小于1.")
    if pageSize<1:
        raise IdNotExist(f"每页记录数小于1.")
    order = " order by A.id desc"
    limit = " limit " + str((pageIndex - 1) * pageSize) + "," + str(pageSize)
    sql = "select A.*,DV.`name` as device_name,C.`name` as username,DV.device_code,C.headicon,D.name as professor_name "\
          " from ecs_consulting A left join device DV on A.device_id=DV.device_code left join dm_user C on A.leaguer_id=C.id left join ecs_professors D on A.doctor_id=D.professor_id " + where + order + limit
    sqlcount = "select count(A.id) as countid from ecs_consulting A left join device DV on A.device_id=DV.id left join dm_user C on A.leaguer_id=C.id left join ecs_professors D on A.doctor_id=D.professor_id " + where + order
    #print(sql)
    get_ecs_consultings = ecs_consulting.get_by_sql(sql, sqlcount)
    if not get_ecs_consultings:
        raise IdNotExist(f"系统中不存在 咨询列表查询关键字 为 {content} 的咨询列表结果.")
    return resp_200(data=get_ecs_consultings, msg=f"查询到了 咨询列表查询关键字 为 {content} 的咨询列表结果.")

@router.post("/updatejson", response_model=ResultModel[Ecs_ConsultingOut], summary='添加修改咨询列表信息')
def update_ecs_consulting_json(*, db: Session = Depends(get_db), ecs_consulting_in: Ecs_ConsultingCreate) -> Any:
    if ecs_consulting_in.id != 0:
        get_ecs_consulting = ecs_consulting.get(db, id=ecs_consulting_in.id)
        alter_ecs_consulting = ecs_consulting.update(db, db_obj=get_ecs_consulting, obj_in=ecs_consulting_in)
        return resp_200(data=alter_ecs_consulting, msg=f"更新了 id 为 {ecs_consulting_in.id} 的咨询列表信息.")
    else:
        log_in = dict()
        for key,value in ecs_consulting_in:
            if key != "id":
                # 赋值字典
                log_in[key] = value
        add_ecs_consulting = ecs_consulting.create(db, obj_in=log_in)
        return resp_200(data=add_ecs_consulting, msg=f"添加了 id 为 {add_ecs_consulting.id} 的咨询列表信息.")

@router.delete("/delete", response_model=ResultModel[Ecs_ConsultingOut], summary='通过 id 删除咨询列表信息')
def delete_ecs_consulting(*, db: Session = Depends(get_db), ecs_consulting_in: Ecs_ConsultingDelete) -> Any:
    del_ecs_consulting = ecs_consulting.remove(db, id=ecs_consulting_in.id)
    return resp_200(data=del_ecs_consulting, msg=f"删除了 id 为 {ecs_consulting_in.id} 的咨询列表信息.")