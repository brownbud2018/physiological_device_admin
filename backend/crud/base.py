#!/usr/bin/env python3
# _*_ coding: utf-8 _*_
# @Time : 2021/10/14 17:00
# @Author : wdm
# @desc : 封装数据库增删改查方法
from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy import func, distinct, and_, or_
from sqlalchemy.orm import Session

from core import verify_password
from models import Base, myBase

from db.session import engine, DBSession

ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: Type[ModelType]):
        """
        CRUD对象的默认方法去 增 查 改 删 (CRUD).

        * `model`: ORM模型类
        * `schema`: 数据验证模型类
        """
        self.model = model

    def get(self, db: Session, *, id: Any) -> Optional[ModelType]:
        """
        通过 ID 获取对象

        :param db: Session
        :param id: ID
        :return: 查询到的orm模型对象
        """
        # table_name = self.model.__tablename__
        # table_id = table_name + '_id'  # 表名_字段名
        # return db.execute(f'select * from {table_name} where {table_id} = {id}').first()

        return db.query(self.model).filter(self.model.id == str(id)).first()

    def getlist(self, sql:str = "") -> dict:
        conn = engine.connect()
        res = conn.execute(sql)
        all_res_list = res.fetchall()
        return all_res_list

    def get_by_filter(self, db: Session, *, filter_query: filter) -> Optional[ModelType]:
        # 通过 filter查询条件 得到查询结果
        return db.query(self.model).filter(filter_query).all()

    def get_by_any(self, db: Session, *, filter_query: or_) -> Optional[ModelType]:
        # 通过 or查询条件 得到查询结果
        return db.query(self.model).filter(filter_query).all()

    def get_by_any_and(self, db: Session, *, filter_query: and_) -> Optional[ModelType]:
        # 通过 and查询条件 得到查询结果
        return db.query(self.model).filter(filter_query).all()

    def get_by_name(self, db: Session, *, name: str) -> Optional[ModelType]:
        # 通过名字得到用户
        return db.query(self.model).filter(self.model.name == name).first()

    def get_by_professor_id(self, db: Session, *, professor_id: Any) -> Optional[ModelType]:
        # 通过professor_id得到医生
        return db.query(self.model).filter(self.model.professor_id == professor_id).first()

    def get_by_device_code(self, db: Session, *, name: str) -> Optional[ModelType]:
        #print("name",name)
        #通过device_code得到用户
        return db.query(self.model).filter(self.model.device_code == name).first()

    def get_by_page_or(self, db: Session, *, filter_query: or_, pageIndex: int = 1, pageSize: int = 10) -> Optional[ModelType]:
        # 通过 filter_query，pageindex,pagesize 得到分页数据
        return db.query(self.model).filter(filter_query).offset((pageIndex - 1) * pageSize).limit(pageSize).all()

    def get_by_page_or_dict(self, db: Session, *, filter_query: or_, pageIndex: int = 1, pageSize: int = 10) -> dict[str, List[ModelType]]:
        # 通过 filter_query,pageindex,pagesize 得到分页数据
        if pageIndex == -1 and pageSize == -1:
            data = db.query(self.model).filter(filter_query).all()
        else:
            data = db.query(self.model).filter(filter_query).offset((pageIndex - 1) * pageSize).limit(pageSize).all()
        count: int = db.query(func.count(distinct(self.model.id))).filter(filter_query).scalar()
        return {'count': count, 'dataList': data}

    def get_by_page_filter(self, db: Session, *, filter_query, pageIndex: int = 1, pageSize: int = 10) -> dict[str, List[ModelType]]:
        # 通过 filter_query，pageindex,pagesize 得到分页数据
        if pageIndex == -1 and pageSize == -1:
            data = db.query(self.model).filter(filter_query).all()
        else:
            data = db.query(self.model).filter(filter_query).offset((pageIndex - 1) * pageSize).limit(pageSize).all()
        count: int = db.query(func.count(distinct(self.model.id))).filter(filter_query).scalar()
        return {'count': count, 'dataList': data}

    def get_by_sql(self, sql:str = "", countsql:str = "") -> dict[str, List[ModelType]]:
        # 通过 filter_query，pageindex,pagesize 得到分页数据
        conn = engine.connect()
        res = conn.execute(sql)
        all_res_list = res.fetchall()

        count = 0   #记录数
        prox = engine.execute(countsql)
        for result in prox:
            for k, v in result.items():
                if k == "countid" :
                    count = v
        result = [dict(zip(result.keys(), result)) for result in all_res_list]
        return {'count': count, 'dataList': result}

    def get_by_sql_is_exist(self, countsql:str = "") -> int:
        count = 0   #记录数
        prox = engine.execute(countsql)
        for result in prox:
            for k, v in result.items():
                if k == "countid" :
                    count = v
        return count

    def get_by_sql_count_int(self, countsql:str = "") -> int:
        count = 0   #记录数
        prox = engine.execute(countsql)
        for result in prox:
            for k, v in result.items():
                if k == "countid" :
                    count = v
        return count

    def get_by_sql_fetchall(self, sql:str = "") -> dict:#原生sql查询：多条记录
        conn = engine.connect()
        res = conn.execute(sql)
        all_res_list = res.fetchall()
        return all_res_list

    def get_by_sql_fetchone(self, sql:str = "") -> Optional[ModelType]:#原生sql查询：单条记录
        conn = engine.connect()
        res = conn.execute(sql)
        all_res_list = res.fetchone()
        return all_res_list

    def get_by_sql_fetchone1(self, sql:str = "") -> [dict]:#原生sql查询：单条记录
        conn = engine.connect()
        res = conn.execute(sql)
        all_res_list = res.fetchall()
        result_dict = [dict(zip(result.keys(), result)) for result in all_res_list]
        return result_dict

    def get_by_sql_no_count(self, sql:str = "") -> List[dict]:
        conn = engine.connect()
        res = conn.execute(sql)
        all_res_list = res.fetchall()
        return all_res_list

    def get_by_sql_count(self, countsql:str = "") -> dict[str, List[ModelType]]:
        count = 0   #记录数
        prox = engine.execute(countsql)
        for result in prox:
            for k, v in result.items():
                if k == "countid" :
                    count = v
        return count

    def get_by_sql_group_concat(self, concatsql:str = "") -> dict[str, List[ModelType]]:
        concat_field = None   #记录数
        prox = engine.execute(concatsql)
        for result in prox:
            for k, v in result.items():
                if k == "concat_field" :
                    concat_field = v
        return concat_field

    def update_by_sql(self, sql:str = "") -> List[dict]:
        conn = engine.connect()
        res = conn.execute(sql)
        return res

    def get_data_by_sql(self, sql:str = "") -> List[dict]:
        conn = engine.connect()
        result = conn.execute(sql)
        cursor = result.cursor
        result_dict  = [dict(zip([field[0].lower() for field in cursor.description], d)) for d in cursor.fetchall()]
        return result_dict

    def get_count_by_sql(self, countsql:str = "") -> int:
        count = 0   #记录数
        prox = engine.execute(countsql)
        for result in prox:
            for k, v in result.items():
                if k == "countid" :
                    count = v
        return count

    def get_by_page_and_or(self, db: Session, filter_query: (), filter_query1: (), pageIndex: int = 1, pageSize: int = 10) -> dict[str, List[ModelType]]:
        # 通过 and_:filter_query，or_:filter_query1，pageindex,pagesize 得到分页数据
        data = db.query(self.model).filter(and_(filter_query)).filter(or_(filter_query1)).offset((pageIndex - 1) * pageSize).limit(pageSize).all()
        count: int = db.query(func.count(distinct(self.model.id))).filter(and_(filter_query)).filter(or_(filter_query1)).scalar()
        return {'count': count, 'dataList': data}

    def get_multi(self, db: Session, *, pageIndex: int = 1, pageSize: int = 10) -> dict[str, List[ModelType]]:
        """
        获取 skip-limit 的对象集

        :param db: Session
        :param pageIndex: 页码 (默认值1)
        :param pageSize: 页码 (默认10)
        :return: 查询到的orm模型对象集
        """
        if pageIndex == -1 and pageSize == -1:
            data = db.query(self.model).all()
        else:
            data = db.query(self.model).offset((pageIndex - 1) * pageSize).limit(pageSize).all()
        count: int = db.query(func.count(distinct(self.model.id))).scalar()
        return {'count': count, 'dataList': data}

    def get_multi_relation(self, db: Session):
        """
        只获取关系字段

        :param db: Session
        :return: 查询到的关系字段
        """
        data = db.query(self.model.id, self.model.name).distinct().all()
        count = db.query(func.count(distinct(self.model.id))).scalar()
        return {'dataList': data, 'count': count}

    def create(self, db: Session, *, obj_in: CreateSchemaType) -> ModelType:
        """
        添加对象

        :param db: Session
        :param obj_in: 创建模型
        :return: orm模型对象
        """
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data)  # type: ignore
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(self, db: Session, *, db_obj: ModelType, obj_in: Union[UpdateSchemaType, Dict[str, Any]]) -> ModelType:
        """
        更新对象

        :param db: Session
        :param db_obj: orm模型对象
        :param obj_in: 更新模型
        :return: orm模型对象
        """
        obj_data = jsonable_encoder(db_obj)
        if isinstance(obj_in, dict):  # 判断对象是否为字典类型
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)  # 排除未设置的元素
        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def remove(self, db: Session, *, id: int) -> ModelType:
        """
        通过 ID 删除对象

        :param db: Session
        :param id: ID
        :return: orm模型对象
        """
        obj = db.query(self.model).get(id)
        db.delete(obj)
        db.commit()
        return obj

    def removefield(self, db: Session, filter_query) -> ModelType:
        """
        通过 int字段和对应值 删除对象
        """
        db.query(self.model).filter(*filter_query).delete()
        #db.query(self.model).filter(self.model.field_name.in_(field_id)).delete()
        db.commit()

    def remove_multi(self, db: Session, *, id_list: list):
        """
        同时删除多个对象

        :param db: Session
        :param id_list: id 列表
        """
        db.query(self.model).filter(self.model.id.in_(id_list)).delete()
        db.commit()

    def delete_by_sql(self, sql:str = "") -> List[dict]:
        # 通过 filter_query，pageindex,pagesize 得到分页数据
        conn = engine.connect()
        res = conn.execute(sql)
        return res

    def authenticate(self, db: Session, *, username: str, password: str) -> Optional[ModelType]:
        """ 验证用户 """
        user = self.get_by_name(db, name=username)
        if not user:
            return None
        if not verify_password(password, user.hashed_password):
            return None
        return user

    def authenticatedevice(self, db: Session, *, username: str, password: str) -> Optional[ModelType]:
        """ 验证用户 """
        user = self.get_by_device_code(db, name=username)
        if not user:
            return None
        if not verify_password(password, user.hashed_password):
            return None
        return user
