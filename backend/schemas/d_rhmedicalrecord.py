#!/usr/bin/env python3
# _*_ coding: utf-8 _*_
# @Time : 2021/9/22 9:59
# @Author : wdm
# @desc : d_rhmedicalrecord 关系表模型
from pydantic import BaseModel, Field

class D_rhmedicalrecordIn(BaseModel):
    """ 共享模型字段 """
    id: int = Field(...)

class D_rhmedicalrecordCreate(BaseModel):
    """ 添加数据时的字段验证 """
    id: int = Field(...)
    dmuserid: int = Field(...)
    url: str = Field(example='病历上传图片地址（逗号分割上传多张图片）')
    recordid: int = Field(...)
    recordname: str = Field(example='检测项目名')
    deviceid: str = Field(example='设备编号')
    descr: str = Field(example='病历描述说明')

class D_rhmedicalrecordUpdate(D_rhmedicalrecordIn):
    """ 更新数据的字段验证 """
    pass


class D_rhmedicalrecordOut(D_rhmedicalrecordCreate):
    """ 查询数据的字段验证 """

    class Config:
        orm_mode = True  # 是否使用orm模型(个人理解: 放行,不验证)

class D_rhmedicalrecordDelete(BaseModel):
    """ 添加数据时的字段验证 """
    id: int = Field(...)
