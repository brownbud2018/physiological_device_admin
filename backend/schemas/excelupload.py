#!/usr/bin/env python3
# _*_ coding: utf-8 _*_
# @Time : 2021/9/22 9:59
# @Author : wdm
# @desc : Excel上传表模型
from pydantic import BaseModel, Field

class ExceluploadIn(BaseModel):
    """ 共享模型字段 """
    id: int = Field(...)
    excel_code: str = Field(min_length=1, max_length=20, example='上传Excel文件编号')
    excel_name: str = Field(min_length=1, max_length=30, example='用途名称')
    excel_address: str = Field(min_length=1, max_length=60, example='上传地址')
    #is_import: int = Field(...)
    excel_remark: str = Field(...)
    name: str = Field(min_length=1, max_length=30, example='设备类名称')
    device_ota: int = Field(...)
    version: str = Field(...)
    product_id: int = Field(...)
    address: str = Field(...)
    image: str = Field(...)
    is_active: int = Field(...)
    device_level: int = Field(default=0)
    device_auth_class_id: int = Field(default=0)
    hashed_password: str = Field(...)

class ExceluploadCreate(ExceluploadIn):
    """ 添加数据时的字段验证 """
    #pass
    id: int = Field(...)


class ExceluploadUpdate(ExceluploadIn):
    """ 更新数据的字段验证 """
    pass


class ExceluploadOut(BaseModel):
    """ 查询数据的字段验证 """
    id: int
    excel_code: str
    excel_name: str
    excel_address: str
    is_import: int
    excel_remark: str

    class Config:
        orm_mode = True  # 是否使用orm模型(个人理解: 放行,不验证)

class ExceluploadDelete(BaseModel):
    """ 添加数据时的字段验证 """
    id: int = Field(...)

class ExceluploadType(BaseModel):
    id: int
    is_import: int

class ExceluploadImport(BaseModel):
    id: int