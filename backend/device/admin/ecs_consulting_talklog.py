#!/usr/bin/env python3
# _*_ coding: utf-8 _*_
# @Time : 2022/11/28 19:18
# @Author : wdm
# @desc : ecs_consulting_talklog表接口
import datetime
from typing import Any, List
from fastapi import APIRouter, Depends, Request, File, UploadFile
from sqlalchemy.orm import Session

from schemas import Ecs_Consulting_TalklogUpdate, Ecs_Consulting_TalklogCreate, Ecs_Consulting_TalklogOut, Relation, ResultModel, Ecs_Consulting_TalklogDelete
from crud import ecs_consulting_talklog, ecs_consulting
from utils import resp_200, resp_400, IdNotExist, logger

from models import Device, Ecs_Consulting_Talklog

from device.deps import get_db, get_current_user1
import time,calendar
router = APIRouter()


@router.get("/", response_model=ResultModel[Ecs_Consulting_TalklogOut], summary='Device_log列表')
def query_ecs_consulting_talklog(pageIndex: int = 1, pageSize: int = 10) -> Any:
    where = " where 1=1 "
    if pageIndex<1:
        raise IdNotExist(f"页数小于1.")
    if pageSize<1:
        raise IdNotExist(f"每页记录数小于1.")
    limit = " limit " + str((pageIndex - 1) * pageSize) + "," + str(pageSize)
    sql = "select a.*,b.device_code,b.name from ecs_consulting_talklog a left join device b on a.device_id=b.id " + where + limit
    sqlcount = "select count(a.id) as countid from ecs_consulting_talklog a left join device b on a.device_id=b.id " + where
    get_device = ecs_consulting_talklog.get_by_sql(sql, sqlcount)
    if not get_device:
        raise IdNotExist(f"系统中不存在 相关 的查询结果.")
    return resp_200(data=get_device, msg=f"查询到了 Device_log列表 的查询结果.")

@router.get("/queryweb", response_model=ResultModel[Ecs_Consulting_TalklogOut], summary='根据 条件 查询日志信息')
def query_ecs_consulting_talklog(content: str = "", leaguer_id: int = 0, device_id: int = 0, pageIndex: int = 1, pageSize: int = 10) -> Any:
    where = " where ifnull(C.name,'null_name-not_select')<>'null_name-not_select'"
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
    sql = "select A.*,B.name as device_name,C.`name` as username,B.device_code,C.headicon,D.name as professor_name "\
          " from ecs_consulting_talklog A left join device B on A.device_id=B.id left join dm_user C on A.leaguer_id=C.id left join ecs_professors D on A.doctor_id=D.professor_id " + where + order + limit
    sqlcount = "select count(A.id) as countid from ecs_consulting_talklog A left join device B on A.device_id=B.id left join dm_user C on A.leaguer_id=C.id left join ecs_professors D on A.doctor_id=D.professor_id " + where + order
    #print(sql)
    get_ecs_consulting_talklogs = ecs_consulting_talklog.get_by_sql(sql, sqlcount)
    if not get_ecs_consulting_talklogs:
        raise IdNotExist(f"系统中不存在 日志查询关键字 为 {content} 的日志结果.")
    return resp_200(data=get_ecs_consulting_talklogs, msg=f"查询到了 日志查询关键字 为 {content} 的日志结果.")

@router.get("/querylist", response_model=ResultModel[Ecs_Consulting_TalklogOut], summary='根据 条件 查询咨询详情信息')
def query_ecs_consulting_talklog_list(consulting_id: int = 0) -> Any:
    where = " where 1=1 "
    if consulting_id == 0:
        raise IdNotExist(f"错误的参数.")
    where1 = where + " and A.id = " + str(consulting_id)
    where2 = where + " and E.consulting_id = " + str(consulting_id)
    order = " order by detailid"
    sql = "select 0 as detailid,A.device_id,A.type,1 as reply_type,A.leaguer_id as userid,A.content,A.doctor_type,A.doctor_id,A.add_time,"\
          "B.name as device_name,C.`name` as username,B.device_code,C.headicon,D.name as professor_name,A.close_type,A.close_id "\
          " from ecs_consulting A left join device B on A.device_id=B.device_code left join dm_user C on A.leaguer_id=C.id"\
          " left join ecs_professors D on A.doctor_id=D.professor_id " + where1
    sql += " union all "
    sql += "select E.id as detailid,A.device_id,A.type,E.reply_type,A.leaguer_id as userid,E.content,A.doctor_type,A.doctor_id,E.add_time,"\
           "B.name as device_name,C.`name` as username,B.device_code,C.headicon,D.name as professor_name,A.close_type,A.close_id "\
           " from ecs_consulting A left join device B on A.device_id=B.device_code left join dm_user C on A.leaguer_id=C.id"\
           " left join ecs_consulting_talklog E on A.id=E.consulting_id"\
           " left join ecs_professors D on E.reply_uid=D.professor_id" + where2
    sql += order
    #print(sql)
    get_ecs_consulting_talklogs = ecs_consulting_talklog.getlist(sql)
    if not get_ecs_consulting_talklogs:
        raise IdNotExist(f"系统中不存在 查询关键字 为 {consulting_id} 的咨询详情信息.")
    return resp_200(data=get_ecs_consulting_talklogs, msg=f"查询到了 咨询关键字 为 {consulting_id} 的咨询详情结果.")

@router.get("/querybyuser", response_model=ResultModel[Ecs_Consulting_TalklogOut], summary='根据 条件 查询咨询用户信息')
def query_querybyuser(consulting_id: int = 0) -> Any:
    where = " where 1=1 "
    if consulting_id == 0:
        raise IdNotExist(f"错误的参数.")
    where1 = where + " and A.id = " + str(consulting_id)
    sql = "select A.leaguer_id as user_id,B.*,C.name as devicename,D.province,E.city from ecs_consulting A left join dm_user B on A.leaguer_id = B.id"\
          " left join device C on B.deviceid=C.device_code left join provinces D on C.provinceid=D.provinceid left join cities E on C.cityid=E.cityid"+ where1
    get_ecs_consulting_talklogs = ecs_consulting_talklog.getlist(sql)
    if not get_ecs_consulting_talklogs:
        raise IdNotExist(f"系统中不存在 咨询ID 为 {consulting_id} 的咨询用户信息.")
    return resp_200(data=get_ecs_consulting_talklogs, msg=f"查询到了 咨询ID 为 {consulting_id} 的咨询用户信息.")

@router.post("/updatejson", response_model=ResultModel[Ecs_Consulting_TalklogOut], summary='添加修改咨询信息')
def update_ecs_consulting_talklog_json(*, db: Session = Depends(get_db), ecs_consulting_talklog_in: Ecs_Consulting_TalklogCreate) -> Any:
    if ecs_consulting_talklog_in.id != 0:
        #get_ecs_consulting_talklog = ecs_consulting_talklog.get(db, id=ecs_consulting_talklog_in.id)
        #alter_ecs_consulting_talklog = ecs_consulting_talklog.update(db, db_obj=get_ecs_consulting_talklog, obj_in=ecs_consulting_talklog_in)
        return resp_200(data=None, msg=f"暂未开放咨询信息.")
    else:
        current_GMT = time.gmtime()
        time_stamp = calendar.timegm(current_GMT)
        log_in = dict()
        for key,value in ecs_consulting_talklog_in:
            if key != "id":
                # 赋值字典
                log_in[key] = value
        log_in['add_time'] = (time_stamp - 28800)
        add_ecs_consulting_talklog = ecs_consulting_talklog.create(db, obj_in=log_in)
        #修改主表doctor_id
        get_ecs_consulting = ecs_consulting.get(db, id=ecs_consulting_talklog_in.consulting_id)
        #print('旧ID', get_ecs_consulting.doctor_id)
        main_update = dict()
        main_update['id'] = get_ecs_consulting.id
        main_update['doctor_id'] = ecs_consulting_talklog_in.reply_uid
        main_update['status'] = 2
        main_update['last_reply_time'] = (time_stamp - 28800)
        main_update['last_reply_content'] = ecs_consulting_talklog_in.content
        main_update['last_reply_status'] = 1
        #print('修改结果ID', main_update['doctor_id'])
        alter_ecs_consulting = ecs_consulting.update(db, db_obj=get_ecs_consulting, obj_in=main_update)
        return resp_200(data=add_ecs_consulting_talklog, msg=f"添加了 id 为 {add_ecs_consulting_talklog.id} 的咨询信息.")

@router.delete("/delete", response_model=ResultModel[Ecs_Consulting_TalklogOut], summary='通过 id 删除日志信息')
def delete_ecs_consulting_talklog(*, db: Session = Depends(get_db), ecs_consulting_talklog_in: Ecs_Consulting_TalklogDelete) -> Any:
    del_ecs_consulting_talklog = ecs_consulting_talklog.remove(db, id=ecs_consulting_talklog_in.id)
    return resp_200(data=del_ecs_consulting_talklog, msg=f"删除了 id 为 {ecs_consulting_talklog_in.id} 的日志信息.")