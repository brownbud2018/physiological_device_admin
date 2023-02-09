#!/usr/bin/env python3
# _*_ coding: utf-8 _*_
# @Time : 2022/11/28 19:18
# @Author : wdm
# @desc : 院系表接口
import json
from typing import Any, List, Union, TypeVar, Dict
from fastapi import APIRouter, Depends, Request
from sqlalchemy import and_, or_
from sqlalchemy.orm import Session

from device.deps import get_db, get_current_user1
from schemas import StatisticsUpdate, StatisticsCreate, StatisticsOut, Relation, ResultModel, StatisticsDelete
from crud import statistics
from utils import resp_200, resp_400, IdNotExist

from models import Statistics, Device

from pydantic import BaseModel
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)

router = APIRouter()

@router.post("/query", response_model=ResultModel[StatisticsOut], summary='根据 条件 查询统计信息')
def query_statistics(request: Request, name: str = "", db: Session = Depends(get_db)) -> Any:
    if str.strip(name) != "" :
        filter_query = or_(
             Statistics.prod_code.like('%' + name + '%') ,
             Statistics.prod_name.like('%' + name + '%') ,
             Statistics.prod_remark.like('%' + name + '%') ,
            )
        get_statistics = statistics.get_by_any(db, filter_query=filter_query)
        if not get_statistics:
            raise IdNotExist(f"系统中不存在 条件 为 {name} 的统计结果.")
        return resp_200(data=get_statistics, msg=f"查询到了 条件 为 {name} 的统计结果.")
    else:
        return resp_400()

@router.get("/querybyprodid", response_model=ResultModel[StatisticsOut], summary='根据 条件 查询统计信息')
def query_statistics_id(prodId: int = 0, pageIndex: int = 1, pageSize: int = 10, db: Session = Depends(get_db)) -> Any:
    if prodId != 0 :
        if pageIndex<1:
            raise IdNotExist(f"页数小于1.")
        if pageSize<1:
            raise IdNotExist(f"每页记录数小于1.")
        filter_query = (Statistics.prod_id == prodId)
        get_statistics = statistics.get_by_page_filter(db, filter_query=filter_query, pageIndex=pageIndex, pageSize=pageSize )
        if not get_statistics:
            raise IdNotExist(f"系统中不存在 ID 为 {prodId} 的统计结果.")
        return resp_200(data=get_statistics, msg=f"查询到了 ID 为 {prodId} 的统计结果.")
    else:
        return resp_400()

@router.get("/querybyname", response_model=ResultModel[StatisticsOut], summary='根据 条件 查询统计信息')
def query_statistics_name(name: str = "", pageIndex: int = 1, pageSize: int = 10, db: Session = Depends(get_db)) -> Any:
    if str.strip(name) != "" :
        if pageIndex<1:
            raise IdNotExist(f"页数小于1.")
        if pageSize<1:
            raise IdNotExist(f"每页记录数小于1.")
        filter_query = or_ (
             Statistics.stat_code.like('%' + name + '%') ,
             Statistics.stat_name.like('%' + name + '%') ,
             Statistics.stat_remark.like('%' + name + '%') ,
            )
        get_statistics = statistics.get_by_page_filter(db, filter_query=filter_query, pageIndex=pageIndex, pageSize=pageSize )
        if not get_statistics:
            raise IdNotExist(f"系统中不存在 条件 为 {name} 的统计结果.")
        return resp_200(data=get_statistics, msg=f"查询到了 条件 为 {name} 的统计结果.")
    else :
        raise IdNotExist(f"没有传递 条件 值.")

@router.get("/", response_model=ResultModel[StatisticsOut], summary='查询所有统计(根据页码和每页个数)')
def read_statisticss(db: Session = Depends(get_db), pageIndex: int = 1, pageSize: int = 10) -> Any:
    if pageIndex<1:
        raise IdNotExist(f"页数小于1.")
    if pageSize<1:
        raise IdNotExist(f"每页记录数小于1.")
    get_statisticss = statistics.get_multi(db, pageIndex=pageIndex, pageSize=pageSize)
    return resp_200(data=get_statisticss, msg=f"查询了第 {pageIndex} 页中的 {pageSize} 个统计信息.")

@router.post("/update/num", summary="提交统计次数")
async def update_num(
        *,
        statCode: str = "",
        statName: str = "",
        statRemark: str = "",
        prodId: int = 0,
        statNum: int = 0,
        db: Session = Depends(get_db)
):
    where = " where 1=1 "
    if statCode == "":
        raise IdNotExist(f"没有传递编号参数.")
    if statName == "":
        raise IdNotExist(f"没有传递名称参数.")
    if prodId == 0:
        raise IdNotExist(f"没有传递设备类ID参数.")
    if statNum == 0:
        raise IdNotExist(f"没有传递统计次数参数.")
    if prodId != 0 :
        where = where + " and stat_code = '" + str(statCode) + "' and prod_id = " + str(prodId)
    filter_query = and_(
        Statistics.stat_code == statCode ,
        Statistics.prod_id == prodId
    )
    sql = "select * from statistics " + where
    get_statistics = statistics.get_data_by_sql(sql)
    #get_statistics = statistics.get_data_by_sql(db, filter_query=filter_query)
    indata = {
        'stat_code': statCode,
        'stat_name': statName,
        'stat_remark': statRemark,
        'prod_id': prodId,
        'stat_num': statNum,
    }
    if not get_statistics:
        backstatisticsdata = statistics.create(db, obj_in=indata)
        return resp_200(data=backstatisticsdata, msg='提交统计次数成功！')
    else:
        statNum = statNum + get_statistics[0]['stat_num']
        updatestatisticsdata = db.query(Statistics).filter(filter_query).update({Statistics.stat_num:statNum})
        db.commit()
        if updatestatisticsdata == 1:
            backstatisticsdata = statistics.get_data_by_sql(sql)
            return resp_200(data=backstatisticsdata, msg='提交统计次数成功！')
        else:
            raise IdNotExist(f"提交统计次数出错.")
        #db.refresh(statistics)

@router.get("/queryweb", response_model=ResultModel[StatisticsOut], summary='根据 条件 查询统计信息')
def query_statistics(stat_name: str = "", prod_id: int = 0, pageIndex: int = 1, pageSize: int = 10) -> Any:
    where = " where 1=1 "
    if str.strip(stat_name) != "" :
        where = where + " and (A.stat_code like '%%" + str(stat_name) + "%%'"
        where = where + " or A.stat_name like '%%" + str(stat_name) + "%%'"
        where = where + " or B.prod_code like '%%" + str(stat_name) + "%%'"
        where = where + " or B.prod_name like '%%" + str(stat_name) + "%%')"
    if prod_id != 0:
        where = where + " and A.prod_id = " + str(prod_id)
    if pageIndex<1:
        raise IdNotExist(f"页数小于1.")
    if pageSize<1:
        raise IdNotExist(f"每页记录数小于1.")
    order = " order by A.id"
    limit = " limit " + str((pageIndex - 1) * pageSize) + "," + str(pageSize)
    sql = "select A.*,B.prod_name,B.prod_code from statistics A left join product B on A.prod_id=B.id " + where + order + limit
    sqlcount = "select count(A.id) as countid from statistics A left join product B on A.prod_id=B.id " + where + order
    get_statisticss = statistics.get_by_sql(sql, sqlcount)
    if not get_statisticss:
        raise IdNotExist(f"系统中不存在 统计查询关键字 为 {stat_name} 的统计结果.")
    return resp_200(data=get_statisticss, msg=f"查询到了 统计查询关键字 为 {stat_name} 的统计结果.")

@router.post("/updatejson", response_model=ResultModel[StatisticsOut], summary='添加修改统计信息')
def update_statistics_json(*, db: Session = Depends(get_db), statistics_in: StatisticsCreate) -> Any:
    if statistics_in.id != 0:
        get_statistics = statistics.get(db, id=statistics_in.id)
        alter_statistics = statistics.update(db, db_obj=get_statistics, obj_in=statistics_in)
        return resp_200(data=alter_statistics, msg=f"更新了 id 为 {statistics_in.id} 的统计信息.")
    else:
        stat_in = dict()
        for key,value in statistics_in:
            if key != "id":
                # 赋值字典
                stat_in[key] = value
        add_statistics = statistics.create(db, obj_in=stat_in)
        return resp_200(data=add_statistics, msg=f"添加了 id 为 {add_statistics.id} 的统计信息.")

@router.delete("/delete", response_model=ResultModel[StatisticsOut], summary='通过 id 删除统计信息')
def delete_statistics(*, db: Session = Depends(get_db), statistics_in: StatisticsDelete) -> Any:
    del_statistics = statistics.remove(db, id=statistics_in.id)
    return resp_200(data=del_statistics, msg=f"删除了 id 为 {statistics_in.id} 的统计信息.")
