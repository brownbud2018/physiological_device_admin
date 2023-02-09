#!/usr/bin/env python3
# _*_ coding: utf-8 _*_
# @Time : 2021/11/17 11:05
# @Author : wdm
# @desc : 操作device表
from typing import Union, Dict, Any
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from core import get_password_hash
from crud import CRUDBase
from models import Device
from schemas import DeviceCreate, DeviceUpdate


class CRUDDevice(CRUDBase[Device, DeviceCreate, DeviceUpdate]):
    def create(self, db: Session, *, obj_in: DeviceCreate) -> Device:
        """
        添加管理员信息

        :param db: Session
        :param obj_in: device添加模型
        :return: device orm模型对象
        """
        obj_in_data = jsonable_encoder(obj_in)
        passwordstr = get_password_hash(obj_in_data['password'])
        db_obj = self.model(
            device_code             = obj_in_data['device_code'],
            name                    = obj_in_data['name'],
            version                 = obj_in_data['version'],
            provinceid              = obj_in_data['provinceid'],
            cityid                  = obj_in_data['cityid'],
            address                 = obj_in_data['address'],
            image                   = obj_in_data['image'],
            product_id              = obj_in_data['product_id'],
            device_ota              = obj_in_data['device_ota'],
            is_active               = obj_in_data['is_active'],
            device_level            = obj_in_data['device_level'],
            device_auth_class_id    = obj_in_data['device_auth_class_id'],
            hashed_password         = get_password_hash(obj_in_data['password'])
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(self, db: Session, *, db_obj: Device, obj_in: Union[DeviceUpdate, Dict[str, Any]]) -> Device:
        """
        更新管理员信息

        :param db: Session
        :param db_obj: device orm模型对象
        :param obj_in: device更新模型
        :return: device orm模型对象
        """
        if isinstance(obj_in, dict):  # 判断对象是否为字典类型
            device_data = obj_in
        else:
            device_data = obj_in.dict(exclude_unset=True)
        if 'password' in device_data.keys():  # 判断输入字典中是否有 password
            if device_data["password"]:  # 判断是否有密码输入,输入新密码则加密(密码不为空)
                hashed_password = get_password_hash(device_data["password"])
                del device_data["password"]
                device_data["hashed_password"] = hashed_password
        else:
            device_data.update({'password': ''})  # '' 为原密码
        return super().update(db, db_obj=db_obj, obj_in=device_data)

    def is_active_def(self, device: Device) -> bool:
        """ 验证用户是否登录 """
        return device.is_active


device = CRUDDevice(Device)
