#!/usr/bin/env python3
# _*_ coding: utf-8 _*_
# @Time : 2022/11/28 19:18
# @Author : wdm
# @desc : d_rhmedicalrecord表接口
from typing import Any, List
from fastapi import APIRouter, Depends, Request, File, UploadFile
from sqlalchemy.orm import Session

from schemas import D_rhmedicalrecordUpdate, D_rhmedicalrecordCreate, D_rhmedicalrecordOut, Relation, ResultModel, D_rhmedicalrecordDelete
from crud import d_rhmedicalrecord, ecs_consulting
from utils import resp_200, resp_400, IdNotExist, logger

from device.deps import get_db, get_current_user1
import time,calendar
router = APIRouter()


@router.get("/", response_model=ResultModel[D_rhmedicalrecordOut], summary='D_rhmedicalrecord列表')
def query_d_rhmedicalrecord(pageIndex: int = 1, pageSize: int = 10) -> Any:
    where = " where 1=1 "
    if pageIndex<1:
        raise IdNotExist(f"页数小于1.")
    if pageSize<1:
        raise IdNotExist(f"每页记录数小于1.")
    limit = " limit " + str((pageIndex - 1) * pageSize) + "," + str(pageSize)
    sql = "select a.*,b.device_code,b.name from d_rhmedicalrecord a left join device b on a.deviceid=b.id " + where + limit
    sqlcount = "select count(a.id) as countid from d_rhmedicalrecord a left join device b on a.deviceid=b.id " + where
    get_device = d_rhmedicalrecord.get_by_sql(sql, sqlcount)
    if not get_device:
        raise IdNotExist(f"系统中不存在 相关 的查询结果.")
    return resp_200(data=get_device, msg=f"查询到了 D_rhmedicalrecord列表 的查询结果.")

@router.get("/queryweb", response_model=ResultModel[D_rhmedicalrecordOut], summary='根据 条件 查询病历信息')
def query_d_rhmedicalrecord(content: str = "", dmuserid: int = 0, deviceid: str = 0, pageIndex: int = 1, pageSize: int = 10) -> Any:
    where = " where ifnull(C.name,'null_name-not_select')<>'null_name-not_select'"
    if str.strip(content) != "" :
        where = where + " and (A.recordname like '%%" + str(content) + "%%'"
        where = where + " or A.descr like '%%" + str(content) + "%%'"
        where = where + " or C.`name` like '%%" + str(content) + "%%')"
    if dmuserid != 0:
        where = where + " and A.dmuserid = " + str(dmuserid)
    if deviceid != 0:
        where = where + " and A.deviceid = '" + str(deviceid) + "'"
    if pageIndex<1:
        raise IdNotExist(f"页数小于1.")
    if pageSize<1:
        raise IdNotExist(f"每页记录数小于1.")
    order = " order by A.id desc"
    limit = " limit " + str((pageIndex - 1) * pageSize) + "," + str(pageSize)
    sql = "select A.*,B.device_code,B.`name` as device_name,C.`name` as username,C.headicon "\
          " from d_rhmedicalrecord A left join device B on A.deviceid=B.device_code left join dm_user C on A.dmuserid=C.id " + where + order + limit
    sqlcount = "select count(A.id) as countid from d_rhmedicalrecord A left join device B on A.deviceid=B.device_code left join dm_user C on A.dmuserid=C.id " + where + order
    #print(sql)
    get_d_rhmedicalrecords = d_rhmedicalrecord.get_by_sql(sql, sqlcount)
    if not get_d_rhmedicalrecords:
        raise IdNotExist(f"系统中不存在 病历查询关键字 为 {content} 的病历结果.")
    return resp_200(data=get_d_rhmedicalrecords, msg=f"查询到了 病历查询关键字 为 {content} 的病历结果.")

@router.get("/querylist", response_model=ResultModel[D_rhmedicalrecordOut], summary='根据 条件 查询病历详情信息')
def query_d_rhmedicalrecord_list(consulting_id: int = 0) -> Any:
    where = " where 1=1 "
    if consulting_id == 0:
        raise IdNotExist(f"错误的参数.")
    where1 = where + " and A.id = " + str(consulting_id)
    where2 = where + " and E.consulting_id = " + str(consulting_id)
    order = " order by detailid"
    sql = "select 0 as detailid,A.deviceid,A.type,1 as reply_type,A.leaguer_id as userid,A.content,A.doctor_type,A.doctor_id,A.add_time,"\
          "B.name as device_name,C.`name` as username,B.device_code,C.headicon,D.name as professor_name,A.close_type,A.close_id "\
          " from ecs_consulting A left join device B on A.deviceid=B.device_code left join dm_user C on A.leaguer_id=C.id"\
          " left join ecs_professors D on A.doctor_id=D.professor_id " + where1
    sql += " union all "
    sql += "select E.id as detailid,A.deviceid,A.type,E.reply_type,A.leaguer_id as userid,E.content,A.doctor_type,A.doctor_id,E.add_time,"\
           "B.name as device_name,C.`name` as username,B.device_code,C.headicon,D.name as professor_name,A.close_type,A.close_id "\
           " from ecs_consulting A left join device B on A.deviceid=B.device_code left join dm_user C on A.leaguer_id=C.id"\
           " left join d_rhmedicalrecord E on A.id=E.consulting_id"\
           " left join ecs_professors D on E.reply_uid=D.professor_id" + where2
    sql += order
    #print(sql)
    get_d_rhmedicalrecords = d_rhmedicalrecord.getlist(sql)
    if not get_d_rhmedicalrecords:
        raise IdNotExist(f"系统中不存在 查询关键字 为 {consulting_id} 的病历详情信息.")
    return resp_200(data=get_d_rhmedicalrecords, msg=f"查询到了 病历关键字 为 {consulting_id} 的病历详情结果.")

@router.post("/updatejson", response_model=ResultModel[D_rhmedicalrecordOut], summary='添加修改病历信息')
def update_d_rhmedicalrecord_json(*, db: Session = Depends(get_db), d_rhmedicalrecord_in: D_rhmedicalrecordCreate) -> Any:
    if d_rhmedicalrecord_in.id != 0:
        get_d_rhmedicalrecord = d_rhmedicalrecord.get(db, id=d_rhmedicalrecord_in.id)
        alter_d_rhmedicalrecord = d_rhmedicalrecord.update(db, db_obj=get_d_rhmedicalrecord, obj_in=d_rhmedicalrecord_in)
        return resp_200(data=alter_d_rhmedicalrecord, msg=f"更新了 id 为 {d_rhmedicalrecord_in.id} 的病历信息.")
    else:
        current_GMT = time.gmtime()
        time_stamp = calendar.timegm(current_GMT)
        log_in = dict()
        for key,value in d_rhmedicalrecord_in:
            if key != "id":
                # 赋值字典
                log_in[key] = value
        log_in['add_time'] = (time_stamp - 28800)
        add_d_rhmedicalrecord = d_rhmedicalrecord.create(db, obj_in=log_in)
        #修改主表doctor_id
        get_ecs_consulting = ecs_consulting.get(db, id=d_rhmedicalrecord_in.consulting_id)
        #print('旧ID', get_ecs_consulting.doctor_id)
        main_update = dict()
        main_update['id'] = get_ecs_consulting.id
        main_update['doctor_id'] = d_rhmedicalrecord_in.reply_uid
        main_update['status'] = 2
        main_update['last_reply_time'] = (time_stamp - 28800)
        main_update['last_reply_content'] = d_rhmedicalrecord_in.content
        main_update['last_reply_status'] = 1
        #print('修改结果ID', main_update['doctor_id'])
        alter_ecs_consulting = ecs_consulting.update(db, db_obj=get_ecs_consulting, obj_in=main_update)
        return resp_200(data=add_d_rhmedicalrecord, msg=f"添加了 id 为 {add_d_rhmedicalrecord.id} 的病历信息.")

@router.delete("/delete", response_model=ResultModel[D_rhmedicalrecordOut], summary='通过 id 删除病历信息')
def delete_d_rhmedicalrecord(*, db: Session = Depends(get_db), d_rhmedicalrecord_in: D_rhmedicalrecordDelete) -> Any:
    del_d_rhmedicalrecord = d_rhmedicalrecord.remove(db, id=d_rhmedicalrecord_in.id)
    return resp_200(data=del_d_rhmedicalrecord, msg=f"删除了 id 为 {d_rhmedicalrecord_in.id} 的病历信息.")