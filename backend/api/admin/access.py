#!/usr/bin/env python3
# _*_ coding: utf-8 _*_
# @Time : 2022/11/28 19:18
# @Author : wdm
# @desc : 权限表接口

from typing import Any, List
from fastapi import APIRouter, Depends, Request, Form
from sqlalchemy import and_, or_
from sqlalchemy.orm import Session

from api.deps import get_db, format_menu, format_menu1
from schemas import AccessUpdate, AccessCreate, AccessOut, Relation, ResultModel, AccessDelete, AccessType, AccessUpdateType, AccessType1, AccessUpdateType1, AccessCodeCheck, AccessCodeCheckNoid
from crud import access
from utils import resp_200, resp_400, IdNotExist

from models import Access

router = APIRouter()

@router.post("/query", response_model=ResultModel[AccessOut], summary='根据 条件 查询Access信息')
def query_access(name: str = "", type: int = 0, accessId: int = 0, parentId: int = 0, pageIndex: int = 1, pageSize: int = 10) -> Any:
    where = " where 1=1 "
    if str.strip(name) != "" :
        where = where + " and (access_code like '%%" + str(name) + "%%' or access_name like '%%" + str(name) + "%%' or access_remark like '%%" + str(name) + "%%')"
    where = where + " and is_check = " + str(type)
    if parentId != 0 :
        where = where + " and parent_id = " + str(parentId)
    if accessId != 0 :
        where = where + " and id = " + str(accessId)
    if pageIndex<1:
        raise IdNotExist(f"页数小于1.")
    if pageSize<1:
        raise IdNotExist(f"每页记录数小于1.")
    limit = " limit " + str((pageIndex - 1) * pageSize) + "," + str(pageSize)
    sql = "select * from access " + where + limit
    sqlcount = "select count(id) as countid from access " + where
    get_access = access.get_by_sql(sql, sqlcount)
    if not get_access:
        raise IdNotExist(f"系统中不存在 Access查询关键字 为 {name} 的Access结果.")
    return resp_200(data=get_access, msg=f"查询到了 综合查询 的Access结果.")

@router.post("/querybyaccessid", response_model=ResultModel[AccessOut], summary='根据 条件 查询Access类信息')
def query_access_id(accessId: int = 0, pageIndex: int = 1, pageSize: int = 10, db: Session = Depends(get_db)) -> Any:
    if accessId != 0 :
        filter_query = (Access.id == accessId)
        get_access = access.get_by_page_filter(db, filter_query=filter_query, pageIndex=pageIndex, pageSize=pageSize )
        if not get_access:
            raise IdNotExist(f"系统中不存在 ID 为 {accessId} 的Access类结果.")
        return resp_200(data=get_access, msg=f"查询到了 ID 为 {accessId} 的Access类结果.")
    else:
        return resp_400()

@router.post("/querybyparentid", response_model=ResultModel[AccessOut], summary='根据 AccessID 查询Access信息')
def query_access_id(parentId: int = 0, pageIndex: int = 1, pageSize: int = 10, db: Session = Depends(get_db)) -> Any:
    if parentId != 0 :
        filter_query = (Access.parent_id == parentId)
        get_access = access.get_by_page_filter(db, filter_query=filter_query, pageIndex=pageIndex, pageSize=pageSize )
        if not get_access:
            raise IdNotExist(f"系统中不存在 AccessID 为 {parentId} 的Access结果.")
        return resp_200(data=get_access, msg=f"查询到了 AccessID 为 {parentId} 的Access结果.")
    else:
        return resp_400()

@router.post("/querybyname", response_model=ResultModel[AccessOut], summary='根据 条件 查询Access类信息')
def query_access_name(name: str = "", pageIndex: int = 1, pageSize: int = 10, db: Session = Depends(get_db)) -> Any:
    if str.strip(name) != "" :
        filter_query = or_ (
             Access.access_code.like('%' + name + '%') ,
             Access.access_name.like('%' + name + '%') ,
             Access.access_remark.like('%' + name + '%') ,
            )
        get_access = access.get_by_page_filter(db, filter_query=filter_query, pageIndex=pageIndex, pageSize=pageSize )
        if not get_access:
            raise IdNotExist(f"系统中不存在 条件 为 {name} 的Access类结果.")
        return resp_200(data=get_access, msg=f"查询到了 条件 为 {name} 的Access类结果.")
    else :
        raise IdNotExist(f"没有传递 条件 值.")

@router.get("/", response_model=ResultModel[AccessOut], summary='查询所有Access类(根据页码和每页个数)')
def read_accesss(db: Session = Depends(get_db), pageIndex: int = 1, pageSize: int = 10) -> Any:
    get_accesss = access.get_multi(db, pageIndex=pageIndex, pageSize=pageSize)
    return resp_200(data=get_accesss, msg=f"查询了第 {pageIndex} 页中的 {pageSize} 个Access类信息.")

@router.get("/queryweb", response_model=ResultModel[AccessOut], summary='根据 条件 查询Access信息')
def query_access(access_name: str = "", parent_id: int = 0, roleId: int = 0, is_check: int = 99, pageIndex: int = 1, pageSize: int = 10) -> Any:
    where = " where 1=1 "
    if str.strip(access_name) != "" :
        where = where + " and (access_code like '%%" + str(access_name) + "%%' or access_name like '%%" + str(access_name) + "%%' or access_remark like '%%" + str(access_name) + "%%')"
    if parent_id != 0:
        where = where + " and parent_id = " + str(parent_id)
    if roleId != 0:
        where = where + " and A.id in (select access_id as id from accessrole where role_id = " + str(roleId) + ")"
    if is_check != 99:
        where = where + " and A.is_check = " + str(is_check)
    if pageIndex<1:
        raise IdNotExist(f"页数小于1.")
    if pageSize<1:
        raise IdNotExist(f"每页记录数小于1.")
    limit = " limit " + str((pageIndex - 1) * pageSize) + "," + str(pageSize)
    sql = "select A.*,A.id as access_id,B.access_name as parent_name from access A left join access B on A.parent_id=B.id" + where + " order by A.sort_order" #+ limit
    #print(sql)
    sqlcount = "select count(id) as countid from access A " + where + " order by A.sort_order"
    #get_accesss = access.get_by_sql(sql, sqlcount)
    get_accesss = access.get_by_sql_fetchall(sql)
    if not get_accesss:
        raise IdNotExist(f"系统中不存在 Access查询关键字 为 {access_name} 的Access结果.")
    back_item = format_menu(get_accesss)
    #print(back_item)
    return resp_200(data=back_item, msg=f"查询到了 Access查询关键字 为 {access_name} 的Access结果.")

@router.get("/querywebtree", response_model=ResultModel[AccessOut], summary='根据 条件 查询Access信息')
def query_access_webtree(access_name: str = "", parent_id: int = 0, pageIndex: int = 1, pageSize: int = 10) -> Any:
    where = " where 1=1 "
    if str.strip(access_name) != "" :
        where = where + " and (access_code like '%%" + str(access_name) + "%%' or access_name like '%%" + str(access_name) + "%%' or access_remark like '%%" + str(access_name) + "%%')"
    if parent_id != 0:
        where = where + " and parent_id = " + str(parent_id)
    if pageIndex<1:
        raise IdNotExist(f"页数小于1.")
    if pageSize<1:
        raise IdNotExist(f"每页记录数小于1.")
    limit = " limit " + str((pageIndex - 1) * pageSize) + "," + str(pageSize)
    sql = "select A.*,B.access_name as parent_name from access A left join access B on A.parent_id=B.id" + where + limit
    get_accesss = access.get_by_sql_fetchall(sql)
    if not get_accesss:
        raise IdNotExist(f"系统中不存在 Access查询关键字 为 {access_name} 的Access结果.")
    back_item = format_menu(get_accesss)
    return resp_200(data=back_item, msg=f"查询到了 Access查询关键字 为 {access_name} 的Access结果.")

@router.get("/qtree", response_model=ResultModel[AccessOut], summary='根据 条件 查询Access分类信息')
def query_access_tree(access_id: int = 0) -> Any:
    where = " where 1=1 "
    if access_id != 0 :
        where = where + " and A.id <> " + str(access_id)
    sql = "select A.*,A.id as access_id,B.access_name as parent_name from access A left join access B on A.parent_id=B.id" + where
    get_accesss = access.get_by_sql_fetchall(sql)
    if not get_accesss:
        raise IdNotExist(f"系统中不存在 权限类查询关键字 为 {access_id} 的Access分类结果.")
    back_item = format_menu(get_accesss)
    return resp_200(data=back_item, msg=f"查询到了Access分类结果.")

@router.get("/qtree1", response_model=ResultModel[AccessOut], summary='根据 条件 查询Access分类信息')
def query_access_tree(role_id: int = 0) -> Any:
    where = " where 1=1 "
    if role_id != 0 :
        where = where + " and A.id in (select access_id as id from accessrole where role_id = " + str(role_id) + ")"
    sql = "select A.*,A.id as access_id,B.access_name as parent_name from access A left join access B on A.parent_id=B.id"# + where
    #print(sql)
    get_accesss = access.get_by_sql_fetchall(sql)
    if not get_accesss:
        raise IdNotExist(f"系统中不存在 权限类查询关键字 为 {role_id} 的Access分类结果.")
    back_item = format_menu1(get_accesss)
    return resp_200(data=back_item, msg=f"查询到了Access分类结果.")

@router.post("/updatejson", response_model=ResultModel[AccessOut], summary='添加Access信息')
def update_access_json(*, db: Session = Depends(get_db), access_in: AccessCreate) -> Any:
    #print(access_in)
    if access_in.id != 0:
        get_access = access.get(db, id=access_in.id)
        alter_access = access.update(db, db_obj=get_access, obj_in=access_in)
        return resp_200(data=alter_access, msg=f"更新了 id 为 {id} 的Access信息.")
    else:
        access_add = dict()
        for key,value in access_in:
            if key != "id":
                # 赋值字典
                access_add[key] = value
        add_access = access.create(db, obj_in=access_add)
        return resp_200(data=add_access, msg=f"添加了 id 为 {add_access.id} 的Access信息.")

@router.post("/updateform", response_model=ResultModel[AccessOut], summary='添加Access信息')
def update_access_form(*, id: int = Form(...), access_code: str = Form(...), access_name: str = Form(...), access_type: int = Form(...), access_image: str = Form(...), access_remark: str = Form(...)) -> Any: #, access_in: ProductCreate
    print('id'+ str(id))
    print(id)
    print('access_code' + str(access_code))
    print('access_name' + str(access_name))
    print('access_type' + str(access_type))
    print('access_image' + str(access_image))
    print('access_remark' + str(access_remark))
    if id != 0:
        raise IdNotExist(f"修改.")
    else:
        raise IdNotExist(f"ID:{id}新增.")

@router.delete("/delete", response_model=ResultModel[AccessOut], summary='通过 id 删除Access信息')
def delete_access(*, db: Session = Depends(get_db), access_id: AccessDelete) -> Any:
    del_access = access.remove(db, id=access_id.id)
    return resp_200(data=del_access, msg=f"删除了 id 为 {access_id.id} 的Access信息.")

@router.get("/querybyid", response_model=ResultModel[AccessOut], summary='根据 条件 查询Access信息')
def query_access_id(access_id: int = 0) -> Any:
    where = " where 1=1 "
    if access_id != 0 :
        where = where + " and A.id=" + str(access_id)
        sql = "select A.*,B.access_name as parent_name from access A left join access B on A.parent_id=B.id" + where
        get_accesss = access.get_by_sql_no_count(sql)
        if not get_accesss:
            raise IdNotExist(f"系统中不存在 Access查询关键字 为 {access_id} 的Access结果.")
        return resp_200(data=get_accesss, msg=f"查询到了 Access查询关键字 为 {access_id} 的Access结果.")
    else:
        return resp_400()

@router.post("/settype", response_model=ResultModel[AccessOut], summary='添加Access信息')
def update_apppr_type(*, db: Session = Depends(get_db), access_in: AccessType) -> Any:
    if access_in.id == 0:
        raise IdNotExist(f"缺少id.")
    if access_in.is_check == 0 or access_in.is_check == 1:
        get_access = access.get(db, id=access_in.id)
        alter_access = access.update(db, db_obj=get_access, obj_in=access_in)
        return resp_200(data=alter_access, msg=f"更新了 id 为 {access_in.id} 的Access属性信息.")
    else:
        raise IdNotExist(f"缺少参数.")

@router.post("/settype1", response_model=ResultModel[AccessOut], summary='添加Access信息')
def update_apppr_type(*, db: Session = Depends(get_db), access_in: AccessType1) -> Any:
    if access_in.id == 0:
        raise IdNotExist(f"缺少id.")
    if access_in.is_menu == 0 or access_in.is_menu == 1:
        get_access = access.get(db, id=access_in.id)
        alter_access = access.update(db, db_obj=get_access, obj_in=access_in)
        return resp_200(data=alter_access, msg=f"更新了 id 为 {access_in.id} 的Access属性信息.")
    else:
        raise IdNotExist(f"缺少参数.")

@router.post("/setupdatetype", response_model=ResultModel[AccessOut], summary='添加Access更新属性信息')
def update_apppr_update_type(*, db: Session = Depends(get_db), access_in: AccessUpdateType) -> Any:
    if access_in.id == 0:
        raise IdNotExist(f"缺少id.")
    if access_in.access_update_type == 0 or access_in.access_update_type == 1:
        get_access = access.get(db, id=access_in.id)
        alter_access = access.update(db, db_obj=get_access, obj_in=access_in)
        return resp_200(data=alter_access, msg=f"更新了 id 为 {access_in.id} 的Access更新属性信息.")
    else:
        raise IdNotExist(f"缺少参数.")

@router.post("/accessexist", response_model=ResultModel[AccessOut], summary='判断是否存在name')
def update_access_exist(*, access_in: AccessCodeCheck) -> Any:
    if access_in.id == 0:#新增
        if access_in.access_code == "":
            raise IdNotExist(f"缺少权限编号.")
        name = access_in.access_code
        sqlcount = "select count(id) as countid from access where access_code = '" + name + "'"
        get_access = access.get_by_sql_is_exist(sqlcount)
        if get_access == 0:
            return resp_200(data=get_access, msg=f"查询了 权限编号为 {access_in.access_code} 的信息,此权限编号在数据库中不存在，可以添加.")
        else:
            return {'code': -1, 'data': get_access, 'msg': 'access权限编号已经存在，不能重复添加一样的权限编号！'}
    else:#编辑
        if access_in.access_code == "":
            raise IdNotExist(f"缺少权限编号.")
        name = access_in.access_code
        sqlcount = "select count(id) as countid from access where access_code = '" + name + "' and id <> " + str(access_in.id)
        get_access = access.get_by_sql_is_exist(sqlcount)
        if get_access == 0:
            return resp_200(data=get_access, msg=f"查询了 权限编号为 {access_in.access_code} 的信息,此权限编号在数据库中不存在，可以添加.")
        else:
            return {'code': -1, 'data': get_access, 'msg': 'access权限编号已经存在，不能重复添加一样的权限编号！'}

@router.post("/accessnewexist", response_model=ResultModel[AccessOut], summary='判断是否存在权限编号')
def update_access_new_exist(*, access_in: AccessCodeCheckNoid) -> Any:
    if access_in.access_code == "":
        raise IdNotExist(f"缺少权限编号.")
    sqlcount = "select count(id) as countid from access where access_code = '" + access_in.access_code + "'"
    get_access = access.get_by_sql_is_exist(sqlcount)
    if get_access == 0:
        return resp_200(data=get_access, msg=f"查询了 权限编号为 {access_in.access_code} 的信息,此权限编号在数据库中不存在，可以添加.")
    else:
        return {'code': -1, 'data': get_access, 'msg': 'access权限编号已经存在，不能重复添加一样的权限编号！'}