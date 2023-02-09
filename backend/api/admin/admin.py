#!/usr/bin/env python3
# _*_ coding: utf-8 _*_
# @Time : 2022/11/28 19:18
# @Author : wdm
# @desc : admin表接口

from typing import Any, List
from fastapi import APIRouter, Depends, Request, File, UploadFile, Form
from sqlalchemy import and_, or_
from sqlalchemy.orm import Session

from schemas import AdminUpdate, AdminCreate, AdminOut, AdminDelete, ResultModel, AdminType, AdminType1, AdminCodeCheck, AdminCodeCheckNoid, AdminPwd
from crud import admin
from utils import resp_200, resp_400, IdNotExist, logger

from models import Admin

import shutil
from core import settings
from utils.create_dir import create_dir
from pathlib import Path
from tempfile import NamedTemporaryFile
from api.deps import get_db, get_current_user
from core import get_password_hash

router = APIRouter()

@router.post("/query", response_model=ResultModel[AdminOut], summary='根据 条件 查询设备号信息')
def query_admin(roleId: int = 0, pageIndex: int = 1, pageSize: int = 10) -> Any:
    where = " where 1=1 "
    if roleId != 0 :
        where = where + " and role_id = " + str(roleId)
    else:
        raise IdNotExist(f"设备类ID必须.")
    if pageIndex<1:
        raise IdNotExist(f"页数小于1.")
    if pageSize<1:
        raise IdNotExist(f"每页记录数小于1.")
    limit = " limit " + str((pageIndex - 1) * pageSize) + "," + str(pageSize)
    sql = "select * from admin " + where + limit
    sqlcount = "select count(id) as countid from admin " + where
    get_admin = admin.get_by_sql(sql, sqlcount)
    if not get_admin:
        raise IdNotExist(f"系统中不存在 设备类ID 为 {roleId} 的设备号结果.")
    return resp_200(data=get_admin, msg=f"查询到了 设备类ID 为 {roleId} 的设备号结果.")

@router.post("/querybyroleid", response_model=ResultModel[AdminOut], summary='根据 条件 查询设备号信息')
def query_admin_id(roleId: int = 0, pageIndex: int = 1, pageSize: int = 10, db: Session = Depends(get_db)) -> Any:
    if roleId != 0 :
        filter_query = (Admin.role_id == roleId)
        get_admin = admin.get_by_page_filter(db, filter_query=filter_query, pageIndex=pageIndex, pageSize=pageSize )
        if not get_admin:
            raise IdNotExist(f"系统中不存在 设备类ID 为 {roleId} 的设备号结果.")
        return resp_200(data=get_admin, msg=f"查询到了 设备类ID 为 {roleId} 的设备号结果.")
    else:
        return resp_400()

@router.post("/querybyname", response_model=ResultModel[AdminOut], summary='根据 条件 查询设备号信息')
def query_admin_name(name: str = "", pageIndex: int = 1, pageSize: int = 10, db: Session = Depends(get_db)) -> Any:
    if str.strip(name) != "" :
        filter_query = or_ (
             Admin.name.like('%' + name + '%') ,
             Admin.name.like('%' + name + '%') ,
             Admin.version.like('%' + name + '%') ,
            )
        get_admin = admin.get_by_page_filter(db, filter_query=filter_query, pageIndex=pageIndex, pageSize=pageSize )
        if not get_admin:
            raise IdNotExist(f"系统中不存在 条件 为 {name} 的设备号结果.")
        return resp_200(data=get_admin, msg=f"查询到了 条件 为 {name} 的设备号结果.")
    else :
        raise IdNotExist(f"没有传递 条件 值.")

@router.get("/", response_model=ResultModel[AdminOut], summary='查询所有设备号(根据页码和每页个数)')
def read_admins(db: Session = Depends(get_db), pageIndex: int = 1, pageSize: int = 10) -> Any:
    get_admins = admin.get_multi(db, pageIndex=pageIndex, pageSize=pageSize)
    return resp_200(data=get_admins, msg=f"查询了第 {pageIndex} 页中的 {pageSize} 个设备号信息.")

@router.post("/upload/file/log", summary="上传log")
async def upload_log(
        file: UploadFile = File(...),
        current_user: Admin = Depends(get_current_user)
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
    user = "ID:" + str(current_user.id) + ",用户名：" + str(current_user.name) + ",名称：" + str(current_user.name)
    backdata = {'user': user, 'file_temp': f"{settings.STATIC_DIR}/log/{tmp_file_name}"}
    #user = crud.admin.update(db, db_obj=current_user,
    #                         obj_in={'image': f"{settings.BASE_URL}/{settings.STATIC_DIR}/{tmp_file_name}"})
    return resp_200(data=backdata, msg='上传成功！')

@router.get("/queryweb", response_model=ResultModel[AdminOut], summary='根据 条件 查询admin信息')
def query_admin(admin_name: str = "", roleId: int = 0, pageIndex: int = 1, pageSize: int = 10) -> Any:
    where = " where 1=1 "
    if str.strip(admin_name) != "" :
        where = where + " and (A.name like '%%" + str(admin_name) + "%%'"
        where = where + " or A.nickname like '%%" + str(admin_name) + "%%'"
        where = where + " or A.address like '%%" + str(admin_name) + "%%')"
    if roleId != 0:
        where = where + " and A.role_id = " + str(roleId)
    if pageIndex<1:
        raise IdNotExist(f"页数小于1.")
    if pageSize<1:
        raise IdNotExist(f"每页记录数小于1.")
    order = " order by A.id"
    limit = " limit " + str((pageIndex - 1) * pageSize) + "," + str(pageSize)
    sql = "select A.*,B.role_name,C.name as professor_name from admin A left join role B on A.role_id=B.id left join ecs_professors C on A.professor_id=C.professor_id " + where + order + limit
    sqlcount = "select count(A.id) as countid from admin A left join role B on A.role_id=B.id " + where
    get_admins = admin.get_by_sql(sql, sqlcount)
    if not get_admins:
        raise IdNotExist(f"系统中不存在 admin查询关键字 为 {admin_name} 的admin结果.")
    return resp_200(data=get_admins, msg=f"查询到了 admin查询关键字 为 {admin_name} 的admin结果.")

@router.get("/qtree", response_model=ResultModel[AdminOut], summary='根据 条件 查询管理员信息')
def query_admin_tree(admin_name: str = "") -> Any:
    where = " where 1=1 "
    if str.strip(admin_name) != "" :
        where = where + " and (name like '%%" + str(admin_name) + "%%' or nickname like '%%" + str(admin_name) + "%%')"
    sql = "select *,id as admin_id from admin " + where
    get_admins = admin.get_by_sql_no_count(sql)
    if not get_admins:
        return {'code': -1, 'data': get_admins, 'msg': f"系统中不存在 管理员查询关键字 为 {admin_name} 的管理员结果."}
    return resp_200(data=get_admins, msg=f"查询到了 授权查询关键字 为 {admin_name} 的管理员结果.")

@router.post("/updatejson", response_model=ResultModel[AdminOut], summary='添加设备信息')
def update_admin_json(*, db: Session = Depends(get_db), admin_in: AdminCreate) -> Any:
    if admin_in.id != 0:
        get_admin = admin.get(db, id=admin_in.id)
        if get_admin.name == admin_in.name:
            #没有修改name
            #name用户名=提交的name用户名
            alter_admin = admin.update(db, db_obj=get_admin, obj_in=admin_in)
            return resp_200(data=alter_admin, msg=f"更新了 id 为 {admin_in.id} 的设备信息.")
        else:
            #修改了name
            # 查找admin表里面有没有name对应的记录
            get_admin1 = admin.get_by_name(db, name=admin_in.name)
            if get_admin1:
                #name用户名已存在
                raise IdNotExist(f"用户名：{admin_in.name}已经在数据库中存在了.")
            alter_admin = admin.update(db, db_obj=get_admin, obj_in=admin_in)
            return resp_200(data=alter_admin, msg=f"更新了 id 为 {admin_in.id} 的管理员信息.")
    else:
        get_admin = admin.get_by_name(db, name=admin_in.name)#查找admin表里面有没有name对应的记录
        if get_admin:
            #name用户名已经存，则返回错误
            raise IdNotExist(f"用户名：{admin_in.name}已经在数据库中存在了.")
        prod_in = dict()
        for key,value in admin_in:
            if key != "id":
                # 赋值字典
                prod_in[key] = value
        add_admin = admin.create(db, obj_in=prod_in)
        return resp_200(data=add_admin, msg=f"添加了 id 为 {add_admin.id} 的管理员信息.")

@router.post("/updateform", response_model=ResultModel[AdminOut], summary='添加管理员信息')
def update_admin_form(*, id: int = Form(...), prod_code: str = Form(...), role_name: str = Form(...), prod_type: int = Form(...), prod_image: str = Form(...), prod_remark: str = Form(...)) -> Any: #, admin_in: ProductCreate
    print('id'+ str(id))
    print(id)
    print('prod_code' + str(prod_code))
    print('role_name' + str(role_name))
    print('prod_type' + str(prod_type))
    print('prod_image' + str(prod_image))
    print('prod_remark' + str(prod_remark))
    if id != 0:
        raise IdNotExist(f"修改.")
    else:
        raise IdNotExist(f"ID:{id}新增.")

@router.post("/settype", response_model=ResultModel[AdminOut], summary='添加管理员信息')
def update_admin_type(*, db: Session = Depends(get_db), admin_in: AdminType) -> Any:
    if admin_in.id == 0:
        raise IdNotExist(f"缺少id.")
    if admin_in.is_active == 0 or admin_in.is_active == 1:
        get_admin = admin.get(db, id=admin_in.id)
        alter_admin = admin.update(db, db_obj=get_admin, obj_in=admin_in)
        return resp_200(data=alter_admin, msg=f"更新了 id 为 {admin_in.id} 的admin激活信息.")
    else:
        raise IdNotExist(f"缺少参数.")

@router.post("/settype1", response_model=ResultModel[AdminOut], summary='添加管理员信息')
def update_admin_type(*, db: Session = Depends(get_db), admin_in: AdminType1) -> Any:
    if admin_in.id == 0:
        raise IdNotExist(f"缺少id.")
    if admin_in.user_type == 0 or admin_in.user_type == 1:
        get_admin = admin.get(db, id=admin_in.id)
        alter_admin = admin.update(db, db_obj=get_admin, obj_in=admin_in)
        return resp_200(data=alter_admin, msg=f"更新了 id 为 {admin_in.id} 的admin激活信息.")
    else:
        raise IdNotExist(f"缺少参数.")

@router.delete("/delete", response_model=ResultModel[AdminOut], summary='通过 id 删除设备信息')
def delete_admin(*, db: Session = Depends(get_db), admin_id: AdminDelete) -> Any:
    del_admin = admin.remove(db, id=admin_id.id)
    return resp_200(data=del_admin, msg=f"删除了 id 为 {admin_id.id} 的设备信息.")

@router.get("/querybyid", response_model=ResultModel[AdminOut], summary='根据 条件 查询admin信息')
def query_admin_id(admin_id: int = 0) -> Any:
    where = " where 1=1 "
    if admin_id != 0 :
        where = where + " and A.id=" + str(admin_id)
        sql = "select A.*,B.role_name from admin A left join role B on A.role_id=B.id " + where
        get_admins = admin.get_by_sql_no_count(sql)
        if not get_admins:
            raise IdNotExist(f"系统中不存在 admin查询关键字 为 {admin_id} 的admin结果.")
        return resp_200(data=get_admins, msg=f"查询到了 admin查询关键字 为 {admin_id} 的admin结果.")
    else:
        return resp_400()

@router.post("/adminexist", response_model=ResultModel[AdminOut], summary='判断是否存在name')
def update_admin_exist(*, admin_in: AdminCodeCheck) -> Any:
    if admin_in.id == 0:#新增
        if admin_in.admin_code == "":
            raise IdNotExist(f"缺少用户名.")
        name = admin_in.admin_code
        sqlcount = "select count(id) as countid from admin where name = '" + name + "'"
        get_admin = admin.get_by_sql_is_exist(sqlcount)
        if get_admin == 0:
            return resp_200(data=get_admin, msg=f"查询了 用户名为 {admin_in.admin_code} 的信息,此用户名在数据库中不存在，可以添加.")
        else:
            return {'code': -1, 'data': get_admin, 'msg': 'admin用户名已经存在，不能重复添加一样的用户名！'}
    else:#编辑
        if admin_in.admin_code == "":
            raise IdNotExist(f"缺少用户名.")
        name = admin_in.admin_code
        sqlcount = "select count(id) as countid from admin where name = '" + name + "' and id <> " + str(admin_in.id)
        get_admin = admin.get_by_sql_is_exist(sqlcount)
        if get_admin == 0:
            return resp_200(data=get_admin, msg=f"查询了 用户名为 {admin_in.admin_code} 的信息,此用户名在数据库中不存在，可以添加.")
        else:
            return {'code': -1, 'data': get_admin, 'msg': 'admin用户名已经存在，不能重复添加一样的用户名！'}

@router.post("/adminnewexist", response_model=ResultModel[AdminOut], summary='判断是否存在name')
def update_admin_new_exist(*, admin_in: AdminCodeCheckNoid) -> Any:
    if admin_in.admin_code == "":
        raise IdNotExist(f"缺少用户名.")
    sqlcount = "select count(id) as countid from admin where name = '" + admin_in.admin_code + "'"
    get_admin = admin.get_by_sql_is_exist(sqlcount)
    if get_admin == 0:
        return resp_200(data=get_admin, msg=f"查询了 用户名为 {admin_in.admin_code} 的信息,此用户名在数据库中不存在，可以添加.")
    else:
        return {'code': -1, 'data': get_admin, 'msg': 'admin用户名已经存在，不能重复添加一样的用户名！'}

@router.post("/changepwd", response_model=ResultModel[AdminOut], summary='修改密码')
def update_admin_changepwd(*, db: Session = Depends(get_db), admin_in: AdminPwd) -> Any:
    if admin_in.id == 0:
        raise IdNotExist(f"缺少id.")
    if admin_in.hashed_password == "":
        raise IdNotExist(f"缺少密码.")
    else:
        hashed_password = get_password_hash(admin_in.hashed_password)
        admin_in.hashed_password = hashed_password
        get_project = admin.get(db, id=admin_in.id)
        alter_project = admin.update(db, db_obj=get_project, obj_in=admin_in)
        return resp_200(data=alter_project, msg=f"更新了 id 为 {admin_in.id} 的密码.")

