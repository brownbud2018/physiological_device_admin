#!/usr/bin/env python3
# _*_ coding: utf-8 _*_
# @Time : 2022/11/28 19:18
# @Author : wdm
# @desc : device表接口

from typing import Any, List
from fastapi import APIRouter, Depends, Request, File, UploadFile, Form
from sqlalchemy import and_, or_
from sqlalchemy.orm import Session

from schemas import DeviceUpdate, DeviceCreate, DeviceOut, DeviceDelete, ResultModel, DeviceType, DeviceCodeCheck, DeviceCodeCheckNoid, DevicePwd, ProvincesOut, CitiesOut
from crud import device, adminauthclass, provinces, cities
from utils import resp_200, resp_400, IdNotExist, logger
from models import Device, Adminauthclass, Provinces, Cities

import shutil
from core import settings
from utils.create_dir import create_dir
from pathlib import Path
from tempfile import NamedTemporaryFile
from device.deps import get_db, get_current_user1

from core import get_password_hash
router = APIRouter()

@router.post("/query", response_model=ResultModel[DeviceOut], summary='根据 条件 查询设备号信息')
def query_device(productId: int = 0, pageIndex: int = 1, pageSize: int = 10) -> Any:
    where = " where 1=1 "
    if productId != 0 :
        where = where + " and product_id = " + str(productId)
    else:
        raise IdNotExist(f"设备类ID必须.")
    if pageIndex<1:
        raise IdNotExist(f"页数小于1.")
    if pageSize<1:
        raise IdNotExist(f"每页记录数小于1.")
    limit = " limit " + str((pageIndex - 1) * pageSize) + "," + str(pageSize)
    sql = "select * from device " + where + limit
    sqlcount = "select count(id) as countid from device " + where
    get_device = device.get_by_sql(sql, sqlcount)
    if not get_device:
        raise IdNotExist(f"系统中不存在 设备类ID 为 {productId} 的设备号结果.")
    return resp_200(data=get_device, msg=f"查询到了 设备类ID 为 {productId} 的设备号结果.")

@router.post("/querybyproductid", response_model=ResultModel[DeviceOut], summary='根据 条件 查询设备号信息')
def query_device_id(productId: int = 0, pageIndex: int = 1, pageSize: int = 10, db: Session = Depends(get_db)) -> Any:
    if productId != 0 :
        filter_query = (Device.product_id == productId)
        get_device = device.get_by_page_filter(db, filter_query=filter_query, pageIndex=pageIndex, pageSize=pageSize )
        if not get_device:
            raise IdNotExist(f"系统中不存在 设备类ID 为 {productId} 的设备号结果.")
        return resp_200(data=get_device, msg=f"查询到了 设备类ID 为 {productId} 的设备号结果.")
    else:
        return resp_400()

@router.post("/querybyname", response_model=ResultModel[DeviceOut], summary='根据 条件 查询设备号信息')
def query_device_name(name: str = "", pageIndex: int = 1, pageSize: int = 10, db: Session = Depends(get_db)) -> Any:
    if str.strip(name) != "" :
        filter_query = or_ (
             Device.device_code.like('%' + name + '%') ,
             Device.name.like('%' + name + '%') ,
             Device.version.like('%' + name + '%') ,
            )
        get_device = device.get_by_page_filter(db, filter_query=filter_query, pageIndex=pageIndex, pageSize=pageSize )
        if not get_device:
            raise IdNotExist(f"系统中不存在 条件 为 {name} 的设备号结果.")
        return resp_200(data=get_device, msg=f"查询到了 条件 为 {name} 的设备号结果.")
    else :
        raise IdNotExist(f"没有传递 条件 值.")

@router.get("/", response_model=ResultModel[DeviceOut], summary='查询所有设备号(根据页码和每页个数)')
def read_devices(db: Session = Depends(get_db), pageIndex: int = 1, pageSize: int = 10) -> Any:
    get_devices = device.get_multi(db, pageIndex=pageIndex, pageSize=pageSize)
    return resp_200(data=get_devices, msg=f"查询了第 {pageIndex} 页中的 {pageSize} 个设备号信息.")

@router.post("/upload/file/log", summary="上传log")
async def upload_log(
        file: UploadFile = File(...),
        current_user: Device = Depends(get_current_user1)
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
    user = "ID:" + str(current_user.id) + ",编号：" + str(current_user.device_code) + ",名称：" + str(current_user.name)
    backdata = {'user': user, 'file_temp': f"{settings.STATIC_DIR}/log/{tmp_file_name}"}
    #user = crud.admin.update(db, db_obj=current_user,
    #                         obj_in={'image': f"{settings.BASE_URL}/{settings.STATIC_DIR}/{tmp_file_name}"})
    return resp_200(data=backdata, msg='上传成功！')

@router.get("/queryprovince", response_model=ResultModel[ProvincesOut], summary='根据 条件 查询省份列表')
def query_province(
        province: str = "", pageIndex: int = 1, pageSize: int = 100
        ) -> Any:
    where = " where 1=1 "
    if province != "":
        where = where + " and province like '%" + str(province) + "%'"
    if pageIndex<1:
        raise IdNotExist(f"页数小于1.")
    if pageSize<1:
        raise IdNotExist(f"每页记录数小于1.")
    order = " order by A.id"
    limit = " limit " + str((pageIndex - 1) * pageSize) + "," + str(pageSize)
    sql = "select A.* from provinces A" + where + order + limit
    sqlcount = "select count(A.id) as countid from provinces A " + where
    get_provinces = provinces.get_by_sql(sql, sqlcount)
    if not get_provinces:
        raise IdNotExist(f"系统中不存在 device查询关键字 为 {province} 的省份结果.")
    return resp_200(data=get_provinces, msg=f"查询到了 省份查询关键字 为 {province} 的省份结果.")

@router.get("/queryprovincecity", response_model=ResultModel[ProvincesOut], summary='根据 条件 查询省份城市列表')
def query_provincecity(
        db: Session = Depends(get_db),
        ) -> Any:
    get_provinces = provinces.getlist("select * from provinces")
    if not get_provinces:
        raise IdNotExist(f"系统中不存在 省份列表结果.")
    province_list = []
    province_city_ary = {}
    i = 0
    for item in get_provinces:
        i += 1
        province_list.append({"id":item['provinceid'], "label":item['province'], "value":item['provinceid'], "key":item['provinceid']})
        province_item_list = []
        get_cities = cities.getlist("select * from cities where provinceid = '" + item['provinceid'] + "'")
        j = 0
        for item1 in get_cities:
            j += 1
            province_item_list.append({"value":item1['cityid'], "label":item1['city'], "key":item1['cityid']})

        #print('province_item_list', province_item_list)
        province_city_ary[item['provinceid']] = province_item_list
    #print('province_list', province_list)
    print('province_city_ary', province_city_ary)
    outdata = {"province":province_list, "city":province_city_ary}
    return resp_200(data=outdata, msg=f"查询到了 省份城市结果.")

@router.get("/querycity", response_model=ResultModel[CitiesOut], summary='根据 条件 查询城市列表')
def query_city(
        city: str = "", pageIndex: int = 1, pageSize: int = 500
        ) -> Any:
    where = " where 1=1 "
    if city != "":
        where = where + " and city like '%" + str(city) + "%'"
    if pageIndex<1:
        raise IdNotExist(f"页数小于1.")
    if pageSize<1:
        raise IdNotExist(f"每页记录数小于1.")
    order = " order by A.id"
    limit = " limit " + str((pageIndex - 1) * pageSize) + "," + str(pageSize)
    sql = "select A.* from cities A" + where + order + limit
    sqlcount = "select count(A.id) as countid from cities A " + where
    get_citys = cities.get_by_sql(sql, sqlcount)
    if not get_citys:
        raise IdNotExist(f"系统中不存在 device查询关键字 为 {city} 的device结果.")
    return resp_200(data=get_citys, msg=f"查询到了 省份查询关键字 为 {city} 的device结果.")

@router.get("/queryweb", response_model=ResultModel[DeviceOut], summary='根据 条件 查询device信息')
def query_device(
        db: Session = Depends(get_db),
        device_name: str = "", productId: int = 0,
        pageIndex: int = 1, pageSize: int = 10,
        current_user: Device = Depends(get_current_user1)
        ) -> Any:
    where = " where 1=1 "
    if str.strip(str(current_user.id)) != "" :
        auth_class_id_ary = []
        auth_class_id_str = ""
        filter_query = and_(
             Adminauthclass.admin_id == current_user.id ,
            )
        get_adminauthclass = adminauthclass.get_by_filter(db, filter_query=filter_query)
        if get_adminauthclass:
            for item in get_adminauthclass:
                auth_class_id_ary.append(item.auth_class_id)
        if len(auth_class_id_ary) > 1:
            #auth_class_id_str = ",".join(auth_class_id_ary)
            auth_class_id_str = ",".join('%s' %id for id in auth_class_id_ary)
        else:
            if len(auth_class_id_ary) == 1:
                auth_class_id_str = str(auth_class_id_ary[0])
        if auth_class_id_str != "":
            where = where + " and A.device_auth_class_id in (" + auth_class_id_str + ")"
    if str.strip(device_name) != "" :
        where = where + " and (name like '%%" + str(device_name) + "%%'"
        where = where + " or version like '%%" + str(device_name) + "%%'"
        where = where + " or ota_name like '%%" + str(device_name) + "%%'"
        where = where + " or prod_name like '%%" + str(device_name) + "%%'"
        where = where + " or device_code like '%%" + str(device_name) + "%%'"
        where = where + " or address like '%%" + str(device_name) + "%%')"
    if productId != 0:
        where = where + " and product_id = " + str(productId)
    if pageIndex<1:
        raise IdNotExist(f"页数小于1.")
    if pageSize<1:
        raise IdNotExist(f"每页记录数小于1.")
    order = " order by A.id"
    limit = " limit " + str((pageIndex - 1) * pageSize) + "," + str(pageSize)
    sql = "select A.*,B.prod_name,C.ota_name,D.class_name,E.province,F.city from device A left join product B on A.product_id=B.id"\
          " left join otamain C on A.device_ota=C.id left join authclass D on A.device_auth_class_id=D.id "\
          " left join provinces E on A.provinceid = E.provinceid "\
          " left join cities F on A.cityid = F.cityid "\
          + where + order + limit
    sqlcount = "select count(A.id) as countid from device A left join product B on A.product_id=B.id left join otamain C on A.device_ota=C.id left join authclass D on A.device_auth_class_id=D.id " + where
    get_devices = device.get_by_sql(sql, sqlcount)
    if not get_devices:
        raise IdNotExist(f"系统中不存在 device查询关键字 为 {device_name} 的device结果.")
    return resp_200(data=get_devices, msg=f"查询到了 device查询关键字 为 {device_name} 的device结果.")

@router.post("/updatejson", response_model=ResultModel[DeviceOut], summary='添加设备信息')
def update_device_json(*, db: Session = Depends(get_db), device_in: DeviceCreate) -> Any:
    if device_in.id != 0:
        get_device = device.get(db, id=device_in.id)
        if get_device.device_code == device_in.device_code:
            #没有修改device_code
            #device_code编号=提交的device_code编号
            alter_device = device.update(db, db_obj=get_device, obj_in=device_in)
            return resp_200(data=alter_device, msg=f"更新了 id 为 {device_in.id} 的设备信息【未修改设备编号】.")
        else:
            #修改了device_code
            # 查找device表里面有没有device_code对应的记录
            get_device1 = device.get_by_device_code(db, name=device_in.device_code)
            if get_device1:
                #device_code编号已存在
                raise IdNotExist(f"设备编号：{device_in.device_code}已经在数据库中存在了.")
            alter_device = device.update(db, db_obj=get_device, obj_in=device_in)
            return resp_200(data=alter_device, msg=f"更新了 id 为 {device_in.id} 的设备信息【包括设备编号】.")
    else:
        get_device = device.get_by_device_code(db, name=device_in.device_code)#查找device表里面有没有device_code对应的记录
        if get_device:
            #device_code编号已经存，则返回错误
            raise IdNotExist(f"设备编号：{device_in.device_code}已经在数据库中存在了.")
        prod_in = dict()
        for key,value in device_in:
            if key != "id":
                # 赋值字典
                prod_in[key] = value
        add_device = device.create(db, obj_in=prod_in)
        return resp_200(data=add_device, msg=f"添加了 id 为 {add_device.id} 的设备信息.")

@router.post("/updateform", response_model=ResultModel[DeviceOut], summary='添加设备信息')
def update_device_form(*, id: int = Form(...), prod_code: str = Form(...), prod_name: str = Form(...), prod_type: int = Form(...), prod_image: str = Form(...), prod_remark: str = Form(...)) -> Any: #, device_in: ProductCreate
    print('id'+ str(id))
    print(id)
    print('prod_code' + str(prod_code))
    print('prod_name' + str(prod_name))
    print('prod_type' + str(prod_type))
    print('prod_image' + str(prod_image))
    print('prod_remark' + str(prod_remark))
    if id != 0:
        raise IdNotExist(f"修改.")
    else:
        raise IdNotExist(f"ID:{id}新增.")

@router.post("/settype", response_model=ResultModel[DeviceOut], summary='添加device信息')
def update_device_type(*, db: Session = Depends(get_db), device_in: DeviceType) -> Any:
    if device_in.id == 0:
        raise IdNotExist(f"缺少id.")
    if device_in.is_active == 0 or device_in.is_active == 1:
        get_device = device.get(db, id=device_in.id)
        alter_device = device.update(db, db_obj=get_device, obj_in=device_in)
        return resp_200(data=alter_device, msg=f"更新了 id 为 {device_in.id} 的device激活信息.")
    else:
        raise IdNotExist(f"缺少参数.")

@router.delete("/delete", response_model=ResultModel[DeviceOut], summary='通过 id 删除设备信息')
def delete_device(*, db: Session = Depends(get_db), device_id: DeviceDelete) -> Any:
    del_device = device.remove(db, id=device_id.id)
    return resp_200(data=del_device, msg=f"删除了 id 为 {device_id.id} 的设备信息.")

@router.get("/querybyid", response_model=ResultModel[DeviceOut], summary='根据 条件 查询device信息')
def query_device_id(device_id: int = 0) -> Any:
    where = " where 1=1 "
    if device_id != 0 :
        where = where + " and A.id=" + str(device_id)
        sql = "select A.*,B.prod_name from device A left join product B on A.product_id=B.id " + where
        get_devices = device.get_by_sql_no_count(sql)
        if not get_devices:
            raise IdNotExist(f"系统中不存在 device查询关键字 为 {device_id} 的device结果.")
        return resp_200(data=get_devices, msg=f"查询到了 device查询关键字 为 {device_id} 的device结果.")
    else:
        return resp_400()

@router.post("/deviceexist", response_model=ResultModel[DeviceOut], summary='判断是否存在device_code')
def update_device_exist(*, device_in: DeviceCodeCheck) -> Any:
    if device_in.id == 0:#新增
        if device_in.device_code == "":
            raise IdNotExist(f"缺少编号.")
        name = device_in.device_code
        sqlcount = "select count(id) as countid from device where device_code = '" + name + "'"
        get_device = device.get_by_sql_is_exist(sqlcount)
        if get_device == 0:
            return resp_200(data=get_device, msg=f"查询了 编号为 {device_in.device_code} 的信息,此编号在数据库中不存在，可以添加.")
        else:
            return {'code': -1, 'data': get_device, 'msg': 'device编号已经存在，不能重复添加一样的编号！'}
    else:#编辑
        if device_in.device_code == "":
            raise IdNotExist(f"缺少编号.")
        name = device_in.device_code
        sqlcount = "select count(id) as countid from device where device_code = '" + name + "' and id <> " + str(device_in.id)
        get_device = device.get_by_sql_is_exist(sqlcount)
        if get_device == 0:
            return resp_200(data=get_device, msg=f"查询了 编号为 {device_in.device_code} 的信息,此编号在数据库中不存在，可以添加.")
        else:
            return {'code': -1, 'data': get_device, 'msg': 'device编号已经存在，不能重复添加一样的编号！'}

@router.post("/devicenewexist", response_model=ResultModel[DeviceOut], summary='判断是否存在device_code')
def update_device_new_exist(*, device_in: DeviceCodeCheckNoid) -> Any:
    if device_in.device_code == "":
        raise IdNotExist(f"缺少编号.")
    sqlcount = "select count(id) as countid from device where device_code = '" + device_in.device_code + "'"
    get_device = device.get_by_sql_is_exist(sqlcount)
    if get_device == 0:
        return resp_200(data=get_device, msg=f"查询了 编号为 {device_in.device_code} 的信息,此编号在数据库中不存在，可以添加.")
    else:
        return {'code': -1, 'data': get_device, 'msg': 'device编号已经存在，不能重复添加一样的编号！'}

@router.post("/changepwd", response_model=ResultModel[DeviceOut], summary='添加项目信息')
def update_device_changepwd(*, db: Session = Depends(get_db), device_in: DevicePwd) -> Any:
    if device_in.id == 0:
        raise IdNotExist(f"缺少id.")
    if device_in.hashed_password == "":
        raise IdNotExist(f"缺少密码.")
    else:
        hashed_password = get_password_hash(device_in.hashed_password)
        device_in.hashed_password = hashed_password
        get_project = device.get(db, id=device_in.id)
        alter_project = device.update(db, db_obj=get_project, obj_in=device_in)
        return resp_200(data=alter_project, msg=f"更新了 id 为 {device_in.id} 的项目类型信息.")

