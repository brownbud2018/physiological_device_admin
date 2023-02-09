#!/usr/bin/env python3
# _*_ coding: utf-8 _*_
# @Time : 2022/11/28 19:18
# @Author : wdm
# @desc : 项目表接口
import json
from typing import Any, List
from fastapi import APIRouter, Depends, Request, Form
from sqlalchemy import and_, or_
from sqlalchemy.orm import Session

from device.deps import get_db
from schemas import ProjectUpdate, ProjectCreate, ProjectOut, Relation, ResultModel, NewResultModel, ProjectType, ProjectDelete
from crud import project
from utils import resp_200, resp_400, IdNotExist, resp_new_200

from models import Project

router = APIRouter()

@router.get("/query", response_model=ResultModel[ProjectOut], summary='根据 条件 查询项目信息')
def query_project(name: str = "", type: int = 0, pageIndex: int = 1, pageSize: int = 10) -> Any:
    where = " where 1=1 "
    if str.strip(name) != "" :
        where = where + " and (pro_code like '%%" + str(name) + "%%' or pro_name like '%%" + str(name) + "%%' or pro_remark like '%%" + str(name) + "%%')"
    else:
        raise IdNotExist(f"查询关键字必须.")
    where = where + " and pro_type = " + str(type)
    if pageIndex<1:
        raise IdNotExist(f"页数小于1.")
    if pageSize<1:
        raise IdNotExist(f"每页记录数小于1.")
    limit = " limit " + str((pageIndex - 1) * pageSize) + "," + str(pageSize)
    sql = "select * from project " + where + limit
    sqlcount = "select count(id) as countid from project " + where
    get_projects = project.get_by_sql(sql, sqlcount)
    if not get_projects:
        raise IdNotExist(f"系统中不存在 项目类查询关键字 为 {name} 的项目类结果.")
    return resp_200(data=get_projects, msg=f"查询到了 项目类查询关键字 为 {name} 的项目类结果.")

@router.post("/queryandor", response_model=ResultModel[ProjectOut], summary='根据 条件 查询项目信息')
def query_project(request: Request, name: str = "", type: int = 0, pageIndex: int = 1, pageSize: int = 10, db: Session = Depends(get_db)) -> Any:
    if str.strip(name) != "" :
        if pageIndex<1:
            raise IdNotExist(f"页数小于1.")
        if pageSize<1:
            raise IdNotExist(f"每页记录数小于1.")
        filter_query = and_(
                Project.pro_type == type ,
            )
        filter_query1 = or_(
                Project.pro_code.like('%' + name + '%') ,
                Project.pro_name.like('%' + name + '%') ,
                Project.pro_remark.like('%' + name + '%') ,
            )
        get_project = project.get_by_page_and_or(db, filter_query=filter_query,filter_query1=filter_query1, pageIndex=pageIndex, pageSize=pageSize )
        if not get_project:
            raise IdNotExist(f"系统中不存在 条件 为 {name} 的项目结果.")
        return resp_200(data=get_project, msg=f"查询到了 条件 为 {name} 的项目结果.")
    else:
        return resp_400()

@router.get("/", response_model=ResultModel[ProjectOut], summary='查询所有项目(根据页码和每页个数)')
def read_projects(db: Session = Depends(get_db), pageIndex: int = 1, pageSize: int = 10) -> Any:
    if pageIndex<1:
        raise IdNotExist(f"页数小于1.")
    if pageSize<1:
        raise IdNotExist(f"每页记录数小于1.")
    get_projects = project.get_multi(db, pageIndex=pageIndex, pageSize=pageSize)
    return resp_200(data=get_projects, msg=f"查询了第 {pageIndex} 页中的 {pageSize} 个项目信息.")

@router.get("/queryweb", response_model=ResultModel[ProjectOut], summary='根据 条件 查询项目信息')
def query_project(pro_name: str = "", pro_type: int = 99, pageIndex: int = 1, pageSize: int = 10) -> Any:
    where = " where 1=1 "
    if str.strip(pro_name) != "" :
        where = where + " and (pro_code like '%%" + str(pro_name) + "%%' or pro_name like '%%" + str(pro_name) + "%%' or pro_remark like '%%" + str(pro_name) + "%%')"
    if pro_type != 99:
        where = where + " and pro_type = " + str(pro_type)
    if pageIndex<1:
        raise IdNotExist(f"页数小于1.")
    if pageSize<1:
        raise IdNotExist(f"每页记录数小于1.")
    limit = " limit " + str((pageIndex - 1) * pageSize) + "," + str(pageSize)
    sql = "select * from project " + where + limit
    sqlcount = "select count(id) as countid from project " + where
    get_projects = project.get_by_sql(sql, sqlcount)
    if not get_projects:
        raise IdNotExist(f"系统中不存在 项目类查询关键字 为 {pro_name} 的项目类结果.")
    return resp_200(data=get_projects, msg=f"查询到了 项目类查询关键字 为 {pro_name} 的项目类结果.")

@router.get("/qtree", response_model=ResultModel[ProjectOut], summary='根据 条件 查询项目信息')
def query_project_tree(pro_name: str = "", pro_type: int = 99) -> Any:
    where = " where 1=1 "
    if str.strip(pro_name) != "" :
        where = where + " and (pro_code like '%%" + str(pro_name) + "%%' or pro_name like '%%" + str(pro_name) + "%%' or pro_remark like '%%" + str(pro_name) + "%%')"
    if pro_type != 99:
        where = where + " and pro_type = " + str(pro_type)
    sql = "select *,id as project_id from project " + where
    get_projects = project.get_by_sql_no_count(sql)
    if not get_projects:
        raise IdNotExist(f"系统中不存在 项目类查询关键字 为 {pro_name} 的项目类结果.")
    #return {'code': 200, 'data': get_projects, 'message': f"查询到了 项目类查询关键字 为 {pro_name} 的项目类结果.", 'type': 'success'}
    return resp_200(data=get_projects, msg=f"查询到了项目类结果.")

@router.get("/qtreedevice", response_model=ResultModel[ProjectOut], summary='根据 条件 查询项目信息')
def query_project_tree(pro_name: str = "", pro_type: int = 99) -> Any:
    where = " where 1=1 "
    if str.strip(pro_name) != "" :
        where = where + " and (pro_code like '%%" + str(pro_name) + "%%' or pro_name like '%%" + str(pro_name) + "%%' or pro_remark like '%%" + str(pro_name) + "%%')"
    if pro_type != 99:
        where = where + " and pro_type = " + str(pro_type)
    sql = "select * from project " + where
    get_projects = project.get_by_sql_fetchall(sql)#List[dict]
    databack = []
    for result in get_projects:
        dicttemp = {}
        for k, v in result.items():
            if k == "id" :
                sql = "select * from product where project_id = " + str(v)
                get_products = project.get_by_sql_fetchall(sql)
                dicttemp[k] = v
                dicttemp["children"] = get_products
            else:
                dicttemp[k] = v
        databack.append(dicttemp)
    if not get_projects:
        raise IdNotExist(f"系统中不存在 项目类查询关键字 为 {pro_name} 的项目类结果.")
    return resp_200(data=databack, msg=f"查询到了项目类结果.")

@router.post("/updatejson", response_model=ResultModel[ProjectOut], summary='添加项目信息')
def update_project_json(*, db: Session = Depends(get_db), project_in: ProjectCreate) -> Any:
    #print(project_in)
    if project_in.id != 0:
        get_project = project.get(db, id=project_in.id)
        alter_project = project.update(db, db_obj=get_project, obj_in=project_in)
        return resp_200(data=alter_project, msg=f"更新了 id 为 {id} 的项目信息.")
    else:
        pro_in = dict()
        for key,value in project_in:
            if key != "id":
                # 赋值字典
                pro_in[key] = value
        add_project = project.create(db, obj_in=pro_in)
        return resp_200(data=add_project, msg=f"添加了 id 为 {add_project.id} 的项目信息.")

@router.post("/updateform", response_model=ResultModel[ProjectOut], summary='添加项目信息')
def update_project_form(*, id: int = Form(...), pro_code: str = Form(...), pro_name: str = Form(...), pro_type: int = Form(...), pro_image: str = Form(...), pro_remark: str = Form(...)) -> Any: #, project_in: ProjectCreate
    print('id'+ str(id))
    print(id)
    print('pro_code' + str(pro_code))
    print('pro_name' + str(pro_name))
    print('pro_type' + str(pro_type))
    print('pro_image' + str(pro_image))
    print('pro_remark' + str(pro_remark))
    if id != 0:
        raise IdNotExist(f"修改.")
    else:
        raise IdNotExist(f"ID:{id}新增.")

@router.post("/settype", response_model=ResultModel[ProjectOut], summary='添加项目信息')
def update_project_type(*, db: Session = Depends(get_db), project_in: ProjectType) -> Any:
    if project_in.id == 0:
        raise IdNotExist(f"缺少id.")
    if project_in.pro_type == 0 or project_in.pro_type == 1:
        get_project = project.get(db, id=project_in.id)
        alter_project = project.update(db, db_obj=get_project, obj_in=project_in)
        return resp_200(data=alter_project, msg=f"更新了 id 为 {project_in.id} 的项目类型信息.")
    else:
        raise IdNotExist(f"缺少参数.")

@router.delete("/delete", response_model=ResultModel[ProjectOut], summary='通过 id 删除项目信息')
def delete_project(*, db: Session = Depends(get_db), pro_id: ProjectDelete) -> Any:
    del_project = project.remove(db, id=pro_id.id)
    return resp_200(data=del_project, msg=f"删除了 id 为 {pro_id.id} 的项目信息.")