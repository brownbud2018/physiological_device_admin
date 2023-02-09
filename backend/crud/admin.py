#!/usr/bin/env python3
# _*_ coding: utf-8 _*_
# @Time : 2021/11/17 11:05
# @Author : wdm
# @desc : 操作管理员表
from typing import Union, Dict, Any
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from core import get_password_hash
from crud import CRUDBase
from models import Admin
from schemas import AdminCreate, AdminUpdate


class CRUDAdmin(CRUDBase[Admin, AdminCreate, AdminUpdate]):
    def create(self, db: Session, *, obj_in: AdminCreate) -> Admin:
        """
        添加管理员信息

        :param db: Session
        :param obj_in: 管理员添加模型
        :return: 管理员orm模型对象
        """
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(
            name                                = obj_in_data['name'],
            nickname                            = obj_in_data['nickname'],
            role_id                             = obj_in_data['role_id'],
            address                             = obj_in_data['address'],
            image                               = obj_in_data['image'],
            hashed_password                     =get_password_hash(obj_in_data['password']),
            is_active                           = obj_in_data['is_active'],
            user_type                           = obj_in_data['user_type'],
            professor_id                        = obj_in_data['professor_id'],
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(self, db: Session, *, db_obj: Admin, obj_in: Union[AdminUpdate, Dict[str, Any]]) -> Admin:
        """
        更新管理员信息

        :param db: Session
        :param db_obj: 管理员orm模型对象
        :param obj_in: 管理管更新模型
        :return: 管理员orm模型对象
        """
        if isinstance(obj_in, dict):  # 判断对象是否为字典类型
            admin_data = obj_in
        else:
            admin_data = obj_in.dict(exclude_unset=True)
        if 'password' in admin_data.keys():  # 判断输入字典中是否有 password
            if admin_data["password"]:  # 判断是否有密码输入,输入新密码则加密(密码不为空)
                hashed_password = get_password_hash(admin_data["password"])
                del admin_data["password"]
                admin_data["hashed_password"] = hashed_password
        else:
            admin_data.update({'password': ''})  # '' 为原密码
        return super().update(db, db_obj=db_obj, obj_in=admin_data)

    def is_active_def(self, admin: Admin) -> bool:
        """ 验证用户是否登录 """
        return admin.is_active


admin = CRUDAdmin(Admin)
