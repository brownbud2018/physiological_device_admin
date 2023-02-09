#!/usr/bin/env python3
# _*_ coding: utf-8 _*_
# @Time : 2022/11/28 19:18
# @Author : wdm
# @desc : 医生控制器接口
import time
from typing import Any, List
from fastapi import APIRouter, Depends, Request, Form
from sqlalchemy import and_, or_
from sqlalchemy.orm import Session

from api.deps import get_db
from schemas import Ecs_professorsUpdate, Ecs_professorsCreate, Ecs_professorsOut, Relation, ResultModel, NewResultModel, Ecs_professorsType, Ecs_professorsDelete, Ecs_professorsMenu
from crud import ecs_professors, access
from models import Ecs_professors, Access
from utils import resp_200, resp_400, IdNotExist, resp_new_200, resp_new_str_200


router = APIRouter()

@router.get("/query", response_model=ResultModel[Ecs_professorsOut], summary='根据 条件 查询医生信息')
def query_ecs_professors(name: str = "", type: int = 0, pageIndex: int = 1, pageSize: int = 10) -> Any:
    where = " where 1=1 "
    if str.strip(name) != "" :
        where = where + " and (ecs_professor_name like '%%" + str(name) + "%%' or ecs_professors_desc like '%%" + str(name) + "%%')"
    else:
        raise IdNotExist(f"查询关键字必须.")
    where = where + " and ecs_professors_status = " + str(type)
    if pageIndex<1:
        raise IdNotExist(f"页数小于1.")
    if pageSize<1:
        raise IdNotExist(f"每页记录数小于1.")
    limit = " limit " + str((pageIndex - 1) * pageSize) + "," + str(pageSize)
    sql = "select * from ecs_professors " + where + limit
    sqlcount = "select count(id) as countid from ecs_professors " + where
    get_ecs_professorss = ecs_professors.get_by_sql(sql, sqlcount)
    if not get_ecs_professorss:
        raise IdNotExist(f"系统中不存在 医生类查询关键字 为 {name} 的医生类结果.")
    return resp_200(data=get_ecs_professorss, msg=f"查询到了 医生类查询关键字 为 {name} 的医生类结果.")

@router.post("/queryandor", response_model=ResultModel[Ecs_professorsOut], summary='根据 条件 查询医生信息')
def query_ecs_professors(name: str = "", type: int = 0, pageIndex: int = 1, pageSize: int = 10, db: Session = Depends(get_db)) -> Any:
    if str.strip(name) != "" :
        if pageIndex<1:
            raise IdNotExist(f"页数小于1.")
        if pageSize<1:
            raise IdNotExist(f"每页记录数小于1.")
        filter_query = and_(
                Ecs_professors.ecs_professors_status == type ,
            )
        filter_query1 = or_(
                Ecs_professors.ecs_professor_name.like('%' + name + '%') ,
                Ecs_professors.ecs_professors_desc.like('%' + name + '%') ,
            )
        get_ecs_professors = ecs_professors.get_by_page_and_or(db, filter_query=filter_query,filter_query1=filter_query1, pageIndex=pageIndex, pageSize=pageSize )
        if not get_ecs_professors:
            raise IdNotExist(f"系统中不存在 条件 为 {name} 的医生结果.")
        return resp_200(data=get_ecs_professors, msg=f"查询到了 条件 为 {name} 的医生结果.")
    else:
        return resp_400()

@router.get("/", response_model=ResultModel[Ecs_professorsOut], summary='查询所有医生(根据页码和每页个数)')
def read_ecs_professorss(db: Session = Depends(get_db), pageIndex: int = 1, pageSize: int = 10) -> Any:
    if pageIndex<1:
        raise IdNotExist(f"页数小于1.")
    if pageSize<1:
        raise IdNotExist(f"每页记录数小于1.")
    get_ecs_professorss = ecs_professors.get_multi(db, pageIndex=pageIndex, pageSize=pageSize)
    return resp_200(data=get_ecs_professorss, msg=f"查询了第 {pageIndex} 页中的 {pageSize} 个医生信息.")

@router.get("/queryweb", response_model=ResultModel[Ecs_professorsOut], summary='根据 条件 查询医生信息')
def query_ecs_professors(professor_name: str = "", professor_sex: int = 99, pageIndex: int = 1, pageSize: int = 10) -> Any:
    where = " where 1=1 "
    if str.strip(professor_name) != "" :
        where = where + " and (`name` like '%%" + str(professor_name) + "%%'" \
                        " or expert like '%%" + str(professor_name) + "%%'" \
                        " or remark like '%%" + str(professor_name) + "%%'" \
                        " or resume like '%%" + str(professor_name) + "%%'" \
                        " or EPC.cat_name like '%%" + str(professor_name) + "%%'" \
                        ")"
    if professor_sex != 99:
        where = where + " and `sex` = " + str(professor_sex)
    if pageIndex<1:
        raise IdNotExist(f"页数小于1.")
    if pageSize<1:
        raise IdNotExist(f"每页记录数小于1.")
    limit = " limit " + str((pageIndex - 1) * pageSize) + "," + str(pageSize)
    sql = "select *,professor_id as id,`name` as professor_name,EPC.cat_name,if(A.cat_id=0,'第三方（春雨医生）','本站') as fromcat from ecs_professors A left join ecs_professors_cat EPC on A.cat_id=EPC.cat_id " + where + limit
    sqlcount = "select count(professor_id) as countid from ecs_professors A left join ecs_professors_cat EPC on A.cat_id=EPC.cat_id " + where
    get_professors = ecs_professors.get_by_sql(sql, sqlcount)
    if not get_professors:
        raise IdNotExist(f"系统中不存在 医生类查询关键字 为 {professor_name} 的医生类结果.")
    return resp_200(data=get_professors, msg=f"查询到了 医生类查询关键字 为 {professor_name} 的医生类结果.")

@router.get("/catqtree", response_model=ResultModel[Ecs_professorsOut], summary='根据 条件 查询主治分类树')
def query_ecs_professors_tree(cat_name: str = "", cat_id: int = 999) -> Any:
    where = " where 1=1 "
    if str.strip(cat_name) != "" :
        where = where + " and (cat_name like '%%" + str(cat_name) + "%%' or cat_desc like '%%" + str(cat_name) + "%%')"
    if cat_id != 999:
        where = where + " and cat_id = " + str(cat_id)
    sql = "select * from ecs_professors_cat " + where
    get_ecs_professorss_cat = ecs_professors.get_by_sql_no_count(sql)
    if not get_ecs_professorss_cat:
        raise IdNotExist(f"系统中不存在 医生类查询关键字 为 {cat_name} 的主治分类结果.")
    #return {'code': 200, 'data': get_ecs_professorss, 'message': f"查询到了 医生类查询关键字 为 {ecs_professor_name} 的医生类结果.", 'type': 'success'}
    return resp_200(data=get_ecs_professorss_cat, msg=f"查询到了主治分类结果.")

@router.get("/qtree", response_model=ResultModel[Ecs_professorsOut], summary='根据 条件 查询医生信息')
def query_ecs_professors_tree(ecs_professor_name: str = "", ecs_professors_cat_id: int = 999) -> Any:
    where = " where 1=1 "
    if str.strip(ecs_professor_name) != "" :
        where = where + " and (name like '%%" + str(ecs_professor_name) + "%%' or expert like '%%" + str(ecs_professor_name) + "%%'"\
                " or title like '%%" + str(ecs_professor_name) + "%%' or email like '%%" + str(ecs_professor_name) + "%%'"\
                " or education like '%%" + str(ecs_professor_name) + "%%' or resume like '%%" + str(ecs_professor_name) + "%%'"\
                " or clinic_name like '%%" + str(ecs_professor_name) + "%%' or hospital like '%%" + str(ecs_professor_name) + "%%'"\
                " or hospital_grade like '%%" + str(ecs_professor_name) + "%%')"
    if ecs_professors_cat_id != 999:
        where = where + " and cat_id = " + str(ecs_professors_cat_id)
    sql = "select *,professor_id as id,`name` as professor_name from ecs_professors " + where
    get_ecs_professorss = ecs_professors.get_by_sql_no_count(sql)
    if not get_ecs_professorss:
        raise IdNotExist(f"系统中不存在 医生类查询关键字 为 {ecs_professor_name} 的医生类结果.")
    #return {'code': 200, 'data': get_ecs_professorss, 'message': f"查询到了 医生类查询关键字 为 {ecs_professor_name} 的医生类结果.", 'type': 'success'}
    return resp_200(data=get_ecs_professorss, msg=f"查询到了医生类结果.")

@router.post("/updatejson", response_model=ResultModel[Ecs_professorsOut], summary='添加医生信息')
def update_ecs_professors_json(*, db: Session = Depends(get_db), ecs_professors_in: Ecs_professorsCreate) -> Any:
    if ecs_professors_in.id != 0:
        professors_add = dict()
        for key,value in ecs_professors_in:
            if key != "id":
                if key != "professor_name":
                    # 赋值字典
                    professors_add[key] = value
                else:
                    professors_add['name'] = value
            else:
                professors_add['professor_id'] = value
        get_ecs_professors = ecs_professors.get_by_professor_id(db, professor_id=ecs_professors_in.id)
        alter_professors = ecs_professors.update(db, db_obj=get_ecs_professors, obj_in=professors_add)
        return resp_new_str_200(data="OK", msg=f"更新了 id 为 {ecs_professors_in.id} 的医生信息.")
    else:
        professors_add = dict()
        for key,value in ecs_professors_in:
            if key == "id":
                pass
            else:
                if key == "professor_name":
                    professors_add['name'] = value
                else:
                    # 赋值字典
                    professors_add[key] = value
        professors_add['reg_time'] = str(time.time())
        add_professors = ecs_professors.create(db, obj_in=professors_add)
        return resp_new_str_200(data="OK", msg=f"添加了新的医生信息.")

@router.post("/updateform", response_model=ResultModel[Ecs_professorsOut], summary='添加医生信息')
def update_ecs_professors_form(*, id: int = Form(...), ecs_professor_name: str = Form(...), ecs_professors_status: int = Form(...), ecs_professors_desc: str = Form(...)) -> Any: #, ecs_professors_in: Ecs_professorsCreate
    print('id'+ str(id))
    print(id)
    print('ecs_professor_name' + str(ecs_professor_name))
    print('ecs_professors_status' + str(ecs_professors_status))
    print('ecs_professors_desc' + str(ecs_professors_desc))
    if id != 0:
        raise IdNotExist(f"修改.")
    else:
        raise IdNotExist(f"ID:{id}新增.")

@router.post("/settype", response_model=ResultModel[Ecs_professorsOut], summary='添加医生信息')
def update_ecs_professors_type(*, db: Session = Depends(get_db), ecs_professors_in: Ecs_professorsType) -> Any:
    if ecs_professors_in.id == 0:
        raise IdNotExist(f"缺少id.")
    if ecs_professors_in.ecs_professors_status == 0 or ecs_professors_in.ecs_professors_status == 1:
        get_ecs_professors = ecs_professors.get(db, id=ecs_professors_in.id)
        alter_ecs_professors = ecs_professors.update(db, db_obj=get_ecs_professors, obj_in=ecs_professors_in)
        return resp_200(data=alter_ecs_professors, msg=f"更新了 id 为 {ecs_professors_in.id} 的医生类型信息.")
    else:
        raise IdNotExist(f"缺少参数.")

@router.delete("/delete", response_model=ResultModel[Ecs_professorsOut], summary='通过 id 删除医生信息')
def delete_ecs_professors(*, db: Session = Depends(get_db), professor_id: Ecs_professorsDelete) -> Any:
    del_ecs_professors = ecs_professors.remove(db, id=professor_id.id)
    '''#filter_query = {'professor_id': professor_id.id}
    filters = {
        Accessecs_professors.professor_id == professor_id.id
    }
    del_accessecs_professors = accessecs_professors.removefield(db, filters)'''
    return resp_200(data=del_ecs_professors, msg=f"删除了 id 为 {professor_id.id} 的医生信息.")