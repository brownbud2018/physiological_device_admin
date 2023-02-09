#!/usr/bin/env python3
# _*_ coding: utf-8 _*_
# @Time : 2022/11/28 19:18
# @Author : wdm
# @desc : d_question表接口
from typing import Any, List
from fastapi import APIRouter, Depends, Request, File, UploadFile
from sqlalchemy.orm import Session

from schemas import D_questionUpdate, D_questionCreate, D_questionOut, Relation, ResultModel, D_questionDelete
from crud import d_question, ecs_consulting
from utils import resp_200, resp_400, IdNotExist, logger

from device.deps import get_db, get_current_user1
from api.deps import getUserWhere, get_current_user
from models import Admin
import time,calendar

router = APIRouter()


@router.get("/", response_model=ResultModel[D_questionOut], summary='D_question列表')
def query_d_question(pageIndex: int = 1, pageSize: int = 10) -> Any:
    where = " where 1=1 "
    if pageIndex<1:
        raise IdNotExist(f"页数小于1.")
    if pageSize<1:
        raise IdNotExist(f"每页记录数小于1.")
    limit = " limit " + str((pageIndex - 1) * pageSize) + "," + str(pageSize)
    sql = "select a.* from d_question a " + where + limit
    sqlcount = "select count(a.id) as countid from d_question a " + where
    get_device = d_question.get_by_sql(sql, sqlcount)
    if not get_device:
        raise IdNotExist(f"系统中不存在 相关 的查询结果.")
    return resp_200(data=get_device, msg=f"查询到了 D_question列表 的查询结果.")

@router.get("/queryweb", response_model=ResultModel[D_questionOut], summary='根据 条件 查询问卷信息')
def query_d_question(
        content: str = "", questionid: int = 0, userid: int = 0, pageIndex: int = 1, pageSize: int = 10,
        db: Session = Depends(get_db), current_user: Admin = Depends(get_current_user)
    ) -> Any:
    where = " where 1=1"
    strWhereUser = getUserWhere(db,current_user)
    where += strWhereUser
    if str.strip(content) != "" :
        where = where + " and (A.questionname like '%%" + str(content) + "%%'"
        where = where + " or DU.name like '%%" + str(content) + "%%')"
    if questionid != 0:
        where = where + " and A.id = " + str(questionid)
    if userid != 0:
        where = where + " and A.userid = " + str(userid)
    if pageIndex<1:
        raise IdNotExist(f"页数小于1.")
    if pageSize<1:
        raise IdNotExist(f"每页记录数小于1.")
    order = " order by A.id desc"
    limit = " limit " + str((pageIndex - 1) * pageSize) + "," + str(pageSize)
    sql = "select A.*,DU.name as dmusername from d_question_user A left join dm_user DU on A.userid=DU.id " + where + order + limit
    sqlcount = "select count(A.id) as countid from d_question_user A left join dm_user DU on A.userid=DU.id " + where + order
    #print(sql)
    get_d_questions = d_question.get_by_sql(sql, sqlcount)
    if not get_d_questions:
        raise IdNotExist(f"系统中不存在 问卷查询关键字 为 {content} 的问卷结果.")
    return resp_200(data=get_d_questions, msg=f"查询到了 问卷查询关键字 为 {content} 的问卷结果.")

@router.get("/querylist", response_model=ResultModel[D_questionOut], summary='根据 条件 查询问卷详情信息')
def query_d_question_list(question_id: int = 0, db: Session = Depends(get_db), current_user: Admin = Depends(get_current_user)) -> Any:
    where = " where 1=1 "
    if question_id == 0:
        raise IdNotExist(f"错误的参数.")
    where1 = where + " and A.id = " + str(question_id)
    strWhereUser = getUserWhere(db,current_user)
    where1 += strWhereUser
    where2 = where + " and A.quid = " + str(question_id)
    order = " order by A.id"
    order2 = " order by A.seq"
    sql = "select A.*,DU.`name` as username from d_question_user A left join dm_user DU on A.userid=DU.id " + where1 + order
    data = d_question.get_data_by_sql(sql)
    if not data:
        raise IdNotExist(f"系统中不存在 查询关键字 为 {question_id} 的问卷信息.")

    for result in data:
        sql = "select * from d_question_user_select A" + where2
        sql += order2
        #print(sql)
        data_info = d_question.get_data_by_sql(sql)
        result['child'] = data_info
    #backdata = {'main': data, 'child': data_info}
    return resp_200(data=data, msg=f"查询到了 问卷关键字 为 {question_id} 的问卷详情结果.")

@router.post("/updatejson", response_model=ResultModel[D_questionOut], summary='添加修改问卷信息')
def update_d_question_json(*, db: Session = Depends(get_db), d_question_in: D_questionCreate) -> Any:
    if d_question_in.id != 0:
        get_d_question = d_question.get(db, id=d_question_in.id)
        alter_d_question = d_question.update(db, db_obj=get_d_question, obj_in=d_question_in)
        return resp_200(data=alter_d_question, msg=f"更新了 id 为 {d_question_in.id} 的问卷信息.")
    else:
        current_GMT = time.gmtime()
        time_stamp = calendar.timegm(current_GMT)
        log_in = dict()
        for key,value in d_question_in:
            if key != "id":
                # 赋值字典
                log_in[key] = value
        log_in['add_time'] = (time_stamp - 28800)
        add_d_question = d_question.create(db, obj_in=log_in)
        #修改主表doctor_id
        get_ecs_consulting = ecs_consulting.get(db, id=d_question_in.consulting_id)
        #print('旧ID', get_ecs_consulting.doctor_id)
        main_update = dict()
        main_update['id'] = get_ecs_consulting.id
        main_update['doctor_id'] = d_question_in.reply_uid
        main_update['status'] = 2
        main_update['last_reply_time'] = (time_stamp - 28800)
        main_update['last_reply_content'] = d_question_in.content
        main_update['last_reply_status'] = 1
        #print('修改结果ID', main_update['doctor_id'])
        alter_ecs_consulting = ecs_consulting.update(db, db_obj=get_ecs_consulting, obj_in=main_update)
        return resp_200(data=add_d_question, msg=f"添加了 id 为 {add_d_question.id} 的问卷信息.")

@router.delete("/delete", response_model=ResultModel[D_questionOut], summary='通过 id 删除问卷信息')
def delete_d_question(*, db: Session = Depends(get_db), d_question_in: D_questionDelete) -> Any:
    del_d_question = d_question.remove(db, id=d_question_in.id)
    return resp_200(data=del_d_question, msg=f"删除了 id 为 {d_question_in.id} 的问卷信息.")