#!/usr/bin/env python3
# _*_ coding: utf-8 _*_
# @Time : 2022/11/28 19:18
# @Author : wdm
# @desc : 院系表接口
import os
import stat
import sys
import re
from urllib.parse import quote
from starlette.responses import StreamingResponse
from mimetypes import guess_type
from pathlib import Path
from email.utils import formatdate

from typing import Any, List
from fastapi import APIRouter, Depends, Request, Path as F_Path, Form
from sqlalchemy import and_, or_
from sqlalchemy.orm import Session


from device.deps import get_db
from schemas import OtaversionUpdate, OtaversionCreate, OtaversionOut, Relation, ResultModel, ResultPlusModel, OtaversionDelete, OtaversionType
from crud import otaversion
from utils import resp_200, resp_400, IdNotExist

from models import Otaversion
from utils.function import get_project_root

router = APIRouter()

@router.post("/query", response_model=ResultModel[OtaversionOut], summary='根据 条件 查询OTA版本信息')
def query_otaversion(name: str = "", type: int = 0, otaversionId: int = 0, otamainId: int = 0, pageIndex: int = 1, pageSize: int = 10) -> Any:
    where = " where 1=1 "
    if str.strip(name) != "" :
        where = where + " and (ota_v_code like '%%" + str(name) + "%%' or ota_v_name like '%%" + str(name) + "%%' or ota_v_remark like '%%" + str(name) + "%%')"
    where = where + " and ota_v_default = " + str(type)
    if otaversionId != 0 :
        where = where + " and id = " + str(otaversionId)
    if otamainId != 0 :
        where = where + " and ota_main_id = " + str(otamainId)
    if pageIndex<1:
        raise IdNotExist(f"页数小于1.")
    if pageSize<1:
        raise IdNotExist(f"每页记录数小于1.")
    limit = " limit " + str((pageIndex - 1) * pageSize) + "," + str(pageSize)
    sql = "select * from otaversion " + where + limit
    sqlcount = "select count(id) as countid from otaversion " + where
    get_otaversion = otaversion.get_by_sql(sql, sqlcount)
    if not get_otaversion:
        raise IdNotExist(f"系统中不存在 OTA版本查询关键字 为 综合查询 的OTA版本结果.")
    return resp_200(data=get_otaversion, msg=f"查询到了 综合查询 的OTA版本结果.")

@router.post("/querybyotaversionid", response_model=ResultModel[OtaversionOut], summary='根据 ID条件 查询OTA版本信息')
def query_otaversion_id(otaversionId: int = 0, pageIndex: int = 1, pageSize: int = 10, db: Session = Depends(get_db)) -> Any:
    if otaversionId != 0 :
        if pageIndex<1:
            raise IdNotExist(f"页数小于1.")
        if pageSize<1:
            raise IdNotExist(f"每页记录数小于1.")
        filter_query = (Otaversion.id == otaversionId)
        get_otaversion = otaversion.get_by_page_filter(db, filter_query=filter_query, pageIndex=pageIndex, pageSize=pageSize )
        if not get_otaversion:
            raise IdNotExist(f"系统中不存在 ID 为 {otaversionId} 的OTA版本结果.")
        return resp_200(data=get_otaversion, msg=f"查询到了 ID 为 {otaversionId} 的OTA版本结果.")
    else:
        return resp_400()

@router.post("/querybyotamainid", response_model=ResultModel[OtaversionOut], summary='根据 deviceID 查询OTA信息')
def query_otaversion_id(otamainId: int = 0, pageIndex: int = 1, pageSize: int = 10) -> Any:
    where = " where 1=1 "
    if otamainId != 0 :
        where = where + " and ota_main_id = " + str(otamainId)
    if pageIndex<1:
        raise IdNotExist(f"页数小于1.")
    if pageSize<1:
        raise IdNotExist(f"每页记录数小于1.")
    limit = " limit " + str((pageIndex - 1) * pageSize) + "," + str(pageSize)
    sql = "select * from otaversion " + where + limit
    sqlcount = "select count(id) as countid from otaversion " + where
    get_otaversion = otaversion.get_by_sql(sql, sqlcount)
    if not get_otaversion:
        raise IdNotExist(f"系统中不存在 OTA查询关键字otamainId 为 {otamainId} 的OTA版本结果.")
    return resp_200(data=get_otaversion, msg=f"查询到了otamainId查询 的OTA版本结果.")

@router.post("/querybyname", response_model=ResultModel[OtaversionOut], summary='根据 条件 查询OTA版本信息')
def query_otaversion_name(name: str = "", pageIndex: int = 1, pageSize: int = 10, db: Session = Depends(get_db)) -> Any:
    if str.strip(name) != "" :
        if pageIndex<1:
            raise IdNotExist(f"页数小于1.")
        if pageSize<1:
            raise IdNotExist(f"每页记录数小于1.")
        filter_query = or_ (
             Otaversion.ota_v_code.like('%' + name + '%') ,
             Otaversion.ota_v_name.like('%' + name + '%') ,
             Otaversion.ota_v_remark.like('%' + name + '%') ,
            )
        get_otaversion = otaversion.get_by_page_filter(db, filter_query=filter_query, pageIndex=pageIndex, pageSize=pageSize )
        if not get_otaversion:
            raise IdNotExist(f"系统中不存在 条件 为 {name} 的OTA版本结果.")
        return resp_200(data=get_otaversion, msg=f"查询到了 条件 为 {name} 的OTA版本结果.")
    else :
        raise IdNotExist(f"没有传递 条件 值.")

@router.get("/", response_model=ResultModel[OtaversionOut], summary='查询所有OTA版本(根据页码和每页个数)')
def read_otaversions(db: Session = Depends(get_db), pageIndex: int = 1, pageSize: int = 10) -> Any:
    if pageIndex<1:
        raise IdNotExist(f"页数小于1.")
    if pageSize<1:
        raise IdNotExist(f"每页记录数小于1.")
    get_otaversions = otaversion.get_multi(db, pageIndex=pageIndex, pageSize=pageSize)
    return resp_200(data=get_otaversions, msg=f"查询了第 {pageIndex} 页中的 {pageSize} 个OTA版本信息.")

@router.get("/download")
async def download_file(request: Request, file_name: str = ""):
    base_dir = get_project_root()
    upload_file_path = Path(base_dir)
    file_path = Path(upload_file_path, file_name)
    if not os.path.exists(file_path):
        raise IdNotExist(f"{file_path}文件不存在.")
    # 获取文件的信息
    stat_result = os.stat(file_path)
    content_type, encoding = guess_type(file_path)
    content_type = content_type or 'application/octet-stream'
    # 读取文件的起始位置和终止位置
    range_str = request.headers.get('range', '')
    range_match = re.search(r'bytes=(\d+)-(\d+)', range_str, re.S) or re.search(r'bytes=(\d+)-', range_str, re.S)
    if range_match:
        start_bytes = int(range_match.group(1))
        end_bytes = int(range_match.group(2)) if range_match.lastindex == 2 else stat_result.st_size - 1
    else:
        start_bytes = 0
        end_bytes = stat_result.st_size - 1
    # 这里 content_length 表示剩余待传输的文件字节长度
    content_length = stat_result.st_size - start_bytes if stat.S_ISREG(stat_result.st_mode) else stat_result.st_size
    # 构建文件名称
    name, *suffix = file_name.rsplit('.', 1)
    suffix = f'.{suffix[0]}' if suffix else ''
    filename = quote(f'{name}{suffix}')  # 文件名编码，防止中文名报错
    # 打开文件从起始位置开始分片读取文件
    return StreamingResponse(
        file_iterator(file_path, start_bytes, 1024 * 1024 * 1),  # 每次读取 1M
        media_type=content_type,
        headers={
            'content-disposition': f'attachment; filename="{filename}"',
            'accept-ranges': 'bytes',
            'connection': 'keep-alive',
            'content-length': str(content_length),
            'content-range': f'bytes {start_bytes}-{end_bytes}/{stat_result.st_size}',
            'last-modified': formatdate(stat_result.st_mtime, usegmt=True),
        },
        status_code=206 if start_bytes > 0 else 200
    )


def file_iterator(file_path, offset, chunk_size):
    """
    文件生成器
    :param file_path: 文件绝对路径
    :param offset: 文件读取的起始位置
    :param chunk_size: 文件读取的块大小
    :return: yield
    """
    with open(file_path, 'rb') as f:
        f.seek(offset, os.SEEK_SET)
        while True:
            data = f.read(chunk_size)
            if data:
                yield data
            else:
                break

@router.get("/querybyotaid", response_model=ResultModel[OtaversionOut], summary='根据 条件 查询OTA版本信息')
def query_ota_id(ota_main_id: int = 0, pageIndex: int = 1, pageSize: int = 10, db: Session = Depends(get_db)) -> Any:
    where = " where 1=1 "
    if ota_main_id != 0 :
        where = where + " and A.ota_main_id=" + str(ota_main_id)
        sql = "select A.*,B.ota_name from otaversion A left join otamain B on A.ota_main_id=B.id" + where
        get_otaversion = otaversion.get_by_sql_no_count(sql)
        if not get_otaversion:
            return {'code': -1, 'data': get_otaversion, 'msg': f'系统中不存在 OTAID 为 {ota_main_id} 的版本号结果.'}
        return resp_200(data=get_otaversion, msg=f"查询到了 OTAID 为 {ota_main_id} 的OTA版本结果.")
    else:
        return resp_400()

@router.get("/queryweb", response_model=ResultModel[OtaversionOut], summary='根据 条件 查询otaversion信息')
def query_otaversion(otaversion_name: str = "", ota_main_id: int = 0, pageIndex: int = 1, pageSize: int = 10) -> Any:
    where = " where 1=1 "
    if str.strip(otaversion_name) != "" :
        where = where + " and (ota_v_name like '%%" + str(otaversion_name) + "%%'"
        where = where + " or ota_v_code like '%%" + str(otaversion_name) + "%%'"
        where = where + " or ota_v_remark like '%%" + str(otaversion_name) + "%%'"
        where = where + " or B.ota_name like '%%" + str(otaversion_name) + "%%')"
    if ota_main_id != 0:
        where = where + " and ota_main_id = " + str(ota_main_id)
    if pageIndex<1:
        return {'code': -1, 'data': pageIndex, 'msg': f"页数小于1."}
    if pageSize<1:
        return {'code': -1, 'data': pageSize, 'msg': f"每页记录数小于1."}
    order = " order by A.id"
    limit = " limit " + str((pageIndex - 1) * pageSize) + "," + str(pageSize)
    sql = "select A.*,B.ota_name from otaversion A left join otamain B on A.ota_main_id=B.id " + where + order + limit
    sqlcount = "select count(A.id) as countid from otaversion A left join otamain B on A.ota_main_id=B.id " + where
    get_otaversions = otaversion.get_by_sql(sql, sqlcount)
    if not get_otaversions:
        return {'code': -1, 'data': pageSize, 'msg': f"系统中不存在 otaversion查询关键字 为 {otaversion_name} 的otaversion结果."}
    return resp_200(data=get_otaversions, msg=f"查询到了 otaversion查询关键字 为 {otaversion_name} 的otaversion结果.")

@router.post("/updatejson", response_model=ResultModel[OtaversionOut], summary='添加版本信息')
def update_otaversion_json(*, db: Session = Depends(get_db), otaversion_in: OtaversionCreate) -> Any:
    if otaversion_in.id != 0:
        sqlcount = "select count(id) as countid from otaversion where ota_main_id = " + str(otaversion_in.ota_main_id) + " and id <> " + str(otaversion_in.id)
        get_exist_count = otaversion.get_by_sql_is_exist(sqlcount)
        if get_exist_count == 0:#没有其它存在的版本，就只有这一个版本，那么就改成默认版本
            otaversion_in.ota_v_default = 1
        else:
            if otaversion_in.ota_v_default == 1:#默认版本，相同OTA下的其它版本设置为非默认
                sqlupdate = "update otaversion set ota_v_default = 0 where ota_main_id = " + str(otaversion_in.ota_main_id) + " and id <> " + str(otaversion_in.id)
                get_update = otaversion.update_by_sql(sqlupdate)
        get_otaversion = otaversion.get(db, id=otaversion_in.id)
        alter_otaversion = otaversion.update(db, db_obj=get_otaversion, obj_in=otaversion_in)
        return resp_200(data=alter_otaversion, msg=f"更新了 id 为 {id} 的版本信息.")
    else:
        sqlcount = "select count(id) as countid from otaversion where ota_main_id = " + str(otaversion_in.ota_main_id)
        get_exist_count = otaversion.get_by_sql_is_exist(sqlcount)
        if get_exist_count == 0:#没有其它存在的版本，就只有这一个版本，那么就改成默认版本
            otaversion_in.ota_v_default = 1
        else:
            if otaversion_in.ota_v_default == 1:#默认版本，相同OTA下的其它版本设置为非默认
                sqlupdate = "update otaversion set ota_v_default = 0 where ota_main_id = " + str(otaversion_in.ota_main_id) + " and id <> " + str(otaversion_in.id)
                get_update = otaversion.update_by_sql(sqlupdate)
        version_in = dict()
        for key,value in otaversion_in:
            if key != "id":
                # 赋值字典
                version_in[key] = value
        add_otaversion = otaversion.create(db, obj_in=version_in)
        return resp_200(data=add_otaversion, msg=f"添加了 id 为 {add_otaversion.id} 的版本信息.")

@router.post("/updateform", response_model=ResultModel[OtaversionOut], summary='添加版本信息')
def update_otaversion_form(*, id: int = Form(...), ota_v_code: str = Form(...), ota_v_name: str = Form(...), ota_v_image: str = Form(...), ota_v_file: str = Form(...), ota_main_id: str = Form(...), ota_v_default: int = Form(...), ota_v_remark: str = Form(...)) -> Any:
    print('id'+ str(id))
    print(id)
    if id != 0:
        raise IdNotExist(f"修改.")
    else:
        raise IdNotExist(f"ID:{id}新增.")

@router.post("/settype", response_model=ResultModel[OtaversionOut], summary='添加otaversion信息')
def update_otaversion_type(*, db: Session = Depends(get_db), otaversion_in: OtaversionType) -> Any:
    if otaversion_in.id == 0:
        raise IdNotExist(f"缺少id.")
    if otaversion_in.ota_v_default == 0 or otaversion_in.ota_v_default == 1:
        get_otaversion = otaversion.get(db, id=otaversion_in.id)
        if otaversion_in.ota_v_default == 1:#默认版本，相同OTA下的其它版本设置为非默认
            sqlupdate = "update otaversion set ota_v_default = 0 where ota_main_id = " + str(get_otaversion.ota_main_id) + " and id <> " + str(get_otaversion.id)
            get_update = otaversion.update_by_sql(sqlupdate)
            alter_otaversion = otaversion.update(db, db_obj=get_otaversion, obj_in=otaversion_in)
            return resp_200(data=alter_otaversion, msg=f"更新了 id 为 {otaversion_in.id} 的otaversion默认版本信息.")
        else:
            sqlcount = "select count(id) as countid from otaversion where ota_main_id = " + str(get_otaversion.ota_main_id) + " and id <> " + str(get_otaversion.id)
            get_exist_count = otaversion.get_by_sql_is_exist(sqlcount)
            if get_exist_count == 0:#没有其它存在的版本，就只有这一个版本
                return {'code': -1, 'data': get_otaversion, 'msg': '只有唯一一个版本，不能设置为非默认版本！'}
            else:
                sqlupdate = "update otaversion set ota_v_default = 1 where id in (select a.id from (select max(id) as id from otaversion where ota_main_id = " + str(get_otaversion.ota_main_id) + " and id <> " + str(get_otaversion.id) + ") a)"
                get_update = otaversion.update_by_sql(sqlupdate)
                get_otaversion = otaversion.get(db, id=otaversion_in.id)
                alter_otaversion = otaversion.update(db, db_obj=get_otaversion, obj_in=otaversion_in)
                return resp_200(data=alter_otaversion, msg=f"更新了 id 为 {otaversion_in.id} 的otaversion默认版本信息.")
    else:
        raise IdNotExist(f"缺少参数.")

@router.delete("/delete", response_model=ResultModel[OtaversionOut], summary='通过 id 删除OTA版本信息')
def delete_otaversion(*, db: Session = Depends(get_db), otaversion_id: OtaversionDelete) -> Any:
    get_otaversion = otaversion.get(db, id=otaversion_id.id)
    if get_otaversion.ota_v_default == 1:#如果删除的OTA版本是OTA的【默认版本】，修改当前相同OTA下的其它版本的【ID值最大的记录】设置为默认
        sqlupdate = "update otaversion set ota_v_default = 1 where id in (select a.id from (select max(id) as id from otaversion where ota_main_id = " + str(get_otaversion.ota_main_id) + " and id <> " + str(get_otaversion.id) + ") a)"
        get_update = otaversion.update_by_sql(sqlupdate)
    del_otaversion = otaversion.remove(db, id=otaversion_id.id)
    return resp_200(data=del_otaversion, msg=f"删除了 id 为 {otaversion_id.id} 的OTA版本信息.")

@router.get("/querybyid", response_model=ResultModel[OtaversionOut], summary='根据 条件 查询otaversion信息')
def query_otaversion_id(otaversion_id: int = 0) -> Any:
    where = " where 1=1 "
    if otaversion_id != 0 :
        where = where + " and A.id=" + str(otaversion_id)
        sql = "select A.*,B.ota_name from otaversion A left join otamain B on A.ota_main_id=B.id " + where
        get_otaversions = otaversion.get_by_sql_no_count(sql)
        if not get_otaversions:
            return {'code': -1, 'data': get_otaversions, 'msg': f"系统中不存在 otaversion查询关键字 为 {otaversion_id} 的otaversion结果."}
        return resp_200(data=get_otaversions, msg=f"查询到了 otaversion查询关键字 为 {otaversion_id} 的otaversion结果.")
    else:
        return resp_400()
