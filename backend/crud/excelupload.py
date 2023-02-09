#!/usr/bin/env python3
# _*_ coding: utf-8 _*_
# @Time : 2021/10/28 19:01
# @Author : wdm
# @desc : Excel上传表
from crud import CRUDBase
from models import Excelupload
from schemas import ExceluploadCreate, ExceluploadUpdate


class CRUDExcelupload(CRUDBase[Excelupload, ExceluploadCreate, ExceluploadUpdate]):
    pass


excelupload = CRUDExcelupload(Excelupload)
