#!/usr/bin/env python3
# _*_ coding: utf-8 _*_
# @Time : 2021/9/22 9:59
# @Author : wdm
# @desc : 项目表模型
from typing import Optional, Literal
from pydantic import BaseModel, Field

from schemas import GMT


class ProjectIn(BaseModel):
    """ 共享模型字段 """
    id: int = Field(...)
    pro_code: str = Field(min_length=1, max_length=20, example='项目代码')
    pro_name: str = Field(min_length=1, max_length=30, example='项目名称')
    pro_image: str = Field(...)
    pro_type: Literal[0, 1] = Field(default=0, example='项目类型：0.测试项目，1.正式项目')
    pro_remark: str = Field(...)
    """
    pro_code: str = Field(min_length=1, max_length=20, example='编号')
    pro_name: str = Field(min_length=1, max_length=30, example='项目名称')
    pro_image: Optional[str] = Field(min_length=1, max_length=60, example='项目图标')
    name: str = Field(min_length=1, max_length=20, example='名字')
    chairman: str = Field(min_length=1, max_length=10, example='主任名')
    phone: Optional[str] = Field(regex=r'(^\s{0}$)|^(0\d{2,3}-\d{7,8})|(1[34578]\d{9})$', example='主任手机号')
    """

class ProjectCreate(ProjectIn):
    """ 添加数据时的字段验证 """
    #pass
    id: int = Field(...)


class ProjectUpdate(ProjectIn):
    """ 更新数据的字段验证 """
    pass


class ProjectOut(BaseModel):
    """ 查询数据的字段验证 """
    id: int
    pro_code: str
    pro_name: str
    pro_image: str
    pro_type: int
    pro_remark: str

    class Config:
        orm_mode = True  # 是否使用orm模型(个人理解: 放行,不验证)

class ProjectDelete(BaseModel):
    """ 添加数据时的字段验证 """
    id: int = Field(...)

class ProjectType(BaseModel):
    id: int
    pro_type: int