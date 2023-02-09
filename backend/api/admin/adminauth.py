#!/usr/bin/env python3
# _*_ coding: utf-8 _*_
# @Time : 2022/11/28 19:18
# @Author : wdm
# @desc : adminauthclass表接口

from typing import Any, List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from schemas import AdminauthclassCreate, AdminauthclassUpdate, AdminauthclassOut, AdminauthclassDelete, ResultModel
from crud import adminauthclass
from utils import resp_200, resp_400, IdNotExist, logger
from api.deps import get_db, get_current_user

router = APIRouter()

@router.get("/queryweb", response_model=ResultModel[AdminauthclassOut], summary='根据 条件 查询管理员关联授权信息')
def query_adminauthclass(class_name: str = "", class_id: int = 0, admin_id: int = 0, pageIndex: int = 1, pageSize: int = 10) -> Any:
    where = " where 1=1 "
    if str.strip(class_name) != "" :
        where = where + " and (B.class_name like '%%" + str(class_name) + "%%'"
        where = where + " or B.class_code like '%%" + str(class_name) + "%%'"
        where = where + " or B.class_desc like '%%" + str(class_name) + "%%'"
        where = where + " or C.name like '%%" + str(class_name) + "%%'"
        where = where + " or C.nickname like '%%" + str(class_name) + "%%')"
    if class_id != 0:
        where = where + " and A.auth_class_id = " + str(class_id)
    if admin_id != 0:
        where = where + " and A.admin_id = " + str(admin_id)
    if pageIndex<1:
        raise IdNotExist(f"页数小于1.")
    if pageSize<1:
        raise IdNotExist(f"每页记录数小于1.")
    order = " order by A.id"
    limit = " limit " + str((pageIndex - 1) * pageSize) + "," + str(pageSize)
    sql = "select A.*,B.class_name,B.class_code,C.name,C.nickname,C.user_type from adminauthclass A left join authclass B on A.auth_class_id=B.id left join admin C on A.admin_id=C.id " + where + order + limit
    sqlcount = "select count(A.id) as countid from adminauthclass A left join authclass B on A.auth_class_id=B.id left join admin C on A.admin_id=C.id " + where
    get_adminauthclasss = adminauthclass.get_by_sql(sql, sqlcount)
    if not get_adminauthclasss:
        raise IdNotExist(f"系统中不存在 管理员关联授权查询关键字 为 {class_name} 的管理员关联授权结果.")
    return resp_200(data=get_adminauthclasss, msg=f"查询到了 管理员关联授权查询关键字 为 {class_name} 的管理员关联授权结果.")

@router.post("/updatejson", response_model=ResultModel[AdminauthclassOut], summary='添加修改管理员关联授权信息')
def update_adminauthclass_json(*, db: Session = Depends(get_db), adminauthclass_in: AdminauthclassCreate) -> Any:
    if adminauthclass_in.id != 0:
        sqlcount = "select count(id) as countid from adminauthclass where auth_class_id = " + str(adminauthclass_in.auth_class_id) + " and admin_id = " + str(adminauthclass_in.admin_id) + " and id <> " + str(adminauthclass_in.id)
        get_exist_count = adminauthclass.get_by_sql_is_exist(sqlcount)
        if get_exist_count > 0:#已经存在关联，禁止修改
            return {'code': -1, 'data': get_exist_count, 'msg': '已经存在关联！'}
        get_adminauthclass = adminauthclass.get(db, id=adminauthclass_in.id)
        alter_adminauthclass = adminauthclass.update(db, db_obj=get_adminauthclass, obj_in=adminauthclass_in)
        return resp_200(data=alter_adminauthclass, msg=f"更新了 id 为 {adminauthclass_in.id} 的管理员关联授权信息.")
    else:
        sqlcount = "select count(id) as countid from adminauthclass where auth_class_id = " + str(adminauthclass_in.auth_class_id) + " and admin_id = " + str(adminauthclass_in.admin_id)
        get_exist_count = adminauthclass.get_by_sql_is_exist(sqlcount)
        if get_exist_count > 0:#已经存在关联，禁止修改
            return {'code': -1, 'data': get_exist_count, 'msg': '已经存在关联！'}
        authabout_in = dict()
        for key,value in adminauthclass_in:
            if key != "id":
                # 赋值字典
                authabout_in[key] = value
        add_adminauthclass = adminauthclass.create(db, obj_in=authabout_in)
        return resp_200(data=add_adminauthclass, msg=f"添加了 id 为 {add_adminauthclass.id} 的管理员关联授权信息.")

@router.delete("/delete", response_model=ResultModel[AdminauthclassOut], summary='通过 id 删除管理员关联授权信息')
def delete_adminauthclass(*, db: Session = Depends(get_db), adminauthclass_in: AdminauthclassDelete) -> Any:
    del_adminauthclass = adminauthclass.remove(db, id=adminauthclass_in.id)
    return resp_200(data=del_adminauthclass, msg=f"删除了 id 为 {adminauthclass_in.id} 的管理员关联授权信息.")


