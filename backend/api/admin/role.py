#!/usr/bin/env python3
# _*_ coding: utf-8 _*_
# @Time : 2022/11/28 19:18
# @Author : wdm
# @desc : 角色控制器接口
import json
from typing import Any, List
from fastapi import APIRouter, Depends, Request, Form
from sqlalchemy import and_, or_
from sqlalchemy.orm import Session

from api.deps import get_db
from schemas import RoleUpdate, RoleCreate, RoleOut, Relation, ResultModel, NewResultModel, RoleType, RoleDelete, RoleMenu
from crud import role, access, accessrole
from models import Role, Access, Accessrole
from utils import resp_200, resp_400, IdNotExist, resp_new_200


router = APIRouter()

@router.get("/query", response_model=ResultModel[RoleOut], summary='根据 条件 查询角色信息')
def query_role(name: str = "", type: int = 0, pageIndex: int = 1, pageSize: int = 10) -> Any:
    where = " where 1=1 "
    if str.strip(name) != "" :
        where = where + " and (role_name like '%%" + str(name) + "%%' or role_desc like '%%" + str(name) + "%%')"
    else:
        raise IdNotExist(f"查询关键字必须.")
    where = where + " and role_status = " + str(type)
    if pageIndex<1:
        raise IdNotExist(f"页数小于1.")
    if pageSize<1:
        raise IdNotExist(f"每页记录数小于1.")
    limit = " limit " + str((pageIndex - 1) * pageSize) + "," + str(pageSize)
    sql = "select * from role " + where + limit
    sqlcount = "select count(id) as countid from role " + where
    get_roles = role.get_by_sql(sql, sqlcount)
    if not get_roles:
        raise IdNotExist(f"系统中不存在 角色类查询关键字 为 {name} 的角色类结果.")
    return resp_200(data=get_roles, msg=f"查询到了 角色类查询关键字 为 {name} 的角色类结果.")

@router.post("/queryandor", response_model=ResultModel[RoleOut], summary='根据 条件 查询角色信息')
def query_role(name: str = "", type: int = 0, pageIndex: int = 1, pageSize: int = 10, db: Session = Depends(get_db)) -> Any:
    if str.strip(name) != "" :
        if pageIndex<1:
            raise IdNotExist(f"页数小于1.")
        if pageSize<1:
            raise IdNotExist(f"每页记录数小于1.")
        filter_query = and_(
                Role.role_status == type ,
            )
        filter_query1 = or_(
                Role.role_name.like('%' + name + '%') ,
                Role.role_desc.like('%' + name + '%') ,
            )
        get_role = role.get_by_page_and_or(db, filter_query=filter_query,filter_query1=filter_query1, pageIndex=pageIndex, pageSize=pageSize )
        if not get_role:
            raise IdNotExist(f"系统中不存在 条件 为 {name} 的角色结果.")
        return resp_200(data=get_role, msg=f"查询到了 条件 为 {name} 的角色结果.")
    else:
        return resp_400()

@router.get("/", response_model=ResultModel[RoleOut], summary='查询所有角色(根据页码和每页个数)')
def read_roles(db: Session = Depends(get_db), pageIndex: int = 1, pageSize: int = 10) -> Any:
    if pageIndex<1:
        raise IdNotExist(f"页数小于1.")
    if pageSize<1:
        raise IdNotExist(f"每页记录数小于1.")
    get_roles = role.get_multi(db, pageIndex=pageIndex, pageSize=pageSize)
    return resp_200(data=get_roles, msg=f"查询了第 {pageIndex} 页中的 {pageSize} 个角色信息.")

@router.get("/queryweb", response_model=ResultModel[RoleOut], summary='根据 条件 查询角色信息')
def query_role(role_name: str = "", role_status: int = 99, pageIndex: int = 1, pageSize: int = 10) -> Any:
    where = " where 1=1 "
    if str.strip(role_name) != "" :
        where = where + " and (role_name like '%%" + str(role_name) + "%%' or role_desc like '%%" + str(role_name) + "%%')"
    if role_status != 99:
        where = where + " and role_status = " + str(role_status)
    if pageIndex<1:
        raise IdNotExist(f"页数小于1.")
    if pageSize<1:
        raise IdNotExist(f"每页记录数小于1.")
    limit = " limit " + str((pageIndex - 1) * pageSize) + "," + str(pageSize)
    sql = "select * from role " + where + limit
    sqlcount = "select count(id) as countid from role " + where
    get_count = role.get_by_sql_count(sqlcount)
    get_roles = role.get_by_sql_fetchall(sql)
    if not get_roles:
        raise IdNotExist(f"系统中不存在 角色类查询关键字 为 {role_name} 的角色类结果.")
    databack = []
    for result in get_roles:
        dicttemp = {}
        for k, v in result.items():
            if k == "id" :
                sql = "select GROUP_CONCAT(access_id) as concat_field from accessrole where role_id = " + str(v) + " and access_id not in (select id as access_id from access where parent_id = 0)"
                get_access = role.get_by_sql_group_concat(sql)
                dicttemp[k] = v
                if get_access == None:
                    dicttemp["menu"] = []
                else:
                    arr1 = get_access.split(",")
                    arr2 = [int(x) for x in arr1]
                    dicttemp["menu"] = arr2
            else:
                dicttemp[k] = v
        databack.append(dicttemp)
    #print(databack)
    databack1 = {'count': get_count, 'dataList': databack}
    #print(databack1)
    return resp_200(data=databack1, msg=f"查询到了 角色类查询关键字 为 {role_name} 的角色类结果.")

@router.get("/qtree", response_model=ResultModel[RoleOut], summary='根据 条件 查询角色信息')
def query_role_tree(role_name: str = "", role_status: int = 99) -> Any:
    where = " where 1=1 "
    if str.strip(role_name) != "" :
        where = where + " and (role_name like '%%" + str(role_name) + "%%' or role_desc like '%%" + str(role_name) + "%%')"
    if role_status != 99:
        where = where + " and role_status = " + str(role_status)
    sql = "select *,id as role_id from role " + where
    get_roles = role.get_by_sql_no_count(sql)
    if not get_roles:
        raise IdNotExist(f"系统中不存在 角色类查询关键字 为 {role_name} 的角色类结果.")
    #return {'code': 200, 'data': get_roles, 'message': f"查询到了 角色类查询关键字 为 {role_name} 的角色类结果.", 'type': 'success'}
    return resp_200(data=get_roles, msg=f"查询到了角色类结果.")

@router.get("/qtreedevice", response_model=ResultModel[RoleOut], summary='根据 条件 查询角色信息')
def query_role_tree(role_name: str = "", role_status: int = 99) -> Any:
    where = " where 1=1 "
    if str.strip(role_name) != "" :
        where = where + " and (role_name like '%%" + str(role_name) + "%%' or role_desc like '%%" + str(role_name) + "%%')"
    if role_status != 99:
        where = where + " and role_status = " + str(role_status)
    sql = "select * from role " + where
    get_roles = role.get_by_sql_fetchall(sql)#List[dict]
    databack = []
    for result in get_roles:
        dicttemp = {}
        for k, v in result.items():
            if k == "id" :
                sql = "select * from product where role_id = " + str(v)
                get_products = role.get_by_sql_fetchall(sql)
                dicttemp[k] = v
                dicttemp["children"] = get_products
            else:
                dicttemp[k] = v
        databack.append(dicttemp)
    if not get_roles:
        raise IdNotExist(f"系统中不存在 角色类查询关键字 为 {role_name} 的角色类结果.")
    return resp_200(data=databack, msg=f"查询到了角色类结果.")

@router.post("/updatejson", response_model=ResultModel[RoleOut], summary='添加角色信息')
def update_role_json(*, db: Session = Depends(get_db), role_in: RoleMenu) -> Any:
    if role_in.id != 0:
        get_role = role.get(db, id=role_in.id)
        role_update = dict()
        menu_list = List
        for key,value in role_in:
            if key != "menu":
                # 赋值字典
                role_update[key] = value
            else:
                menu_list = value
        alter_role = role.update(db, db_obj=get_role, obj_in=role_update)
        alter_menu = []
        if len(menu_list) > 0:
            nums_str = ''
            for i in menu_list:
                nums_str = nums_str + str(i) + ','
            nums_str = nums_str[:-1]
            sql = "delete from accessrole where role_id = " + str(role_in.id) + " and access_id not in (" + nums_str + ")"
            del_accessroles = accessrole.delete_by_sql(sql)
            for x in menu_list:
                filter_query = and_(
                     Accessrole.role_id == role_in.id ,
                     Accessrole.access_id == x ,
                )
                get_accessrole = accessrole.get_by_any(db, filter_query=filter_query)
                if len(get_accessrole) > 0:
                    print('已经存在', get_accessrole)
                    #alter_role = accessrole.update(db, db_obj=get_accessrole, obj_in=accessrole_list)
                else:
                    role_insert = dict()
                    role_insert["role_id"] = role_in.id
                    role_insert["access_id"] = x

                    print('str(x)', str(x))
                    get_access = access.get(db, id=x)
                    parent_id = get_access.parent_id
                    print('parent_id', parent_id)
                    filter_query = and_(
                        Accessrole.role_id == role_in.id ,
                        Accessrole.access_id == parent_id ,
                    )
                    get_accessrole = accessrole.get_by_any(db, filter_query=filter_query)
                    if len(get_accessrole) > 0:
                        pass
                    else:
                        role_parent = dict()
                        role_parent["role_id"] = role_in.id
                        role_parent["access_id"] = parent_id
                        alter_parent = accessrole.create(db, obj_in=role_parent)
                    alter_menu = accessrole.create(db, obj_in=role_insert)
        return resp_200(data=role_in, msg=f"更新了 id 为 {role_in.id} 的角色信息.")
    else:
        role_insert = dict()
        menu_list = List
        for key,value in role_in:
            if key != "menu":
                if key != "id":
                    # 赋值字典
                    role_insert[key] = value
            else:
                menu_list = value
        add_role = role.create(db, obj_in=role_insert)
        if len(menu_list) > 0:
            for x in menu_list:
                role_insert = dict()
                role_insert["role_id"] = add_role.id
                role_insert["access_id"] = x
                alter_menu = accessrole.create(db, obj_in=role_insert)
        return resp_200(data=add_role, msg=f"添加了 id 为 {add_role.id} 的角色信息.")

@router.post("/updateform", response_model=ResultModel[RoleOut], summary='添加角色信息')
def update_role_form(*, id: int = Form(...), role_name: str = Form(...), role_status: int = Form(...), role_desc: str = Form(...)) -> Any: #, role_in: RoleCreate
    print('id'+ str(id))
    print(id)
    print('role_name' + str(role_name))
    print('role_status' + str(role_status))
    print('role_desc' + str(role_desc))
    if id != 0:
        raise IdNotExist(f"修改.")
    else:
        raise IdNotExist(f"ID:{id}新增.")

@router.post("/settype", response_model=ResultModel[RoleOut], summary='添加角色信息')
def update_role_type(*, db: Session = Depends(get_db), role_in: RoleType) -> Any:
    if role_in.id == 0:
        raise IdNotExist(f"缺少id.")
    if role_in.role_status == 0 or role_in.role_status == 1:
        get_role = role.get(db, id=role_in.id)
        alter_role = role.update(db, db_obj=get_role, obj_in=role_in)
        return resp_200(data=alter_role, msg=f"更新了 id 为 {role_in.id} 的角色类型信息.")
    else:
        raise IdNotExist(f"缺少参数.")

@router.delete("/delete", response_model=ResultModel[RoleOut], summary='通过 id 删除角色信息')
def delete_role(*, db: Session = Depends(get_db), role_id: RoleDelete) -> Any:
    del_role = role.remove(db, id=role_id.id)
    #filter_query = {'role_id': role_id.id}
    filters = {
        Accessrole.role_id == role_id.id
    }
    del_accessrole = accessrole.removefield(db, filters)
    return resp_200(data=del_role, msg=f"删除了 id 为 {role_id.id} 的角色信息.")