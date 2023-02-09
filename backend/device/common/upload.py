#!/usr/bin/env python3
# _*_ coding: utf-8 _*_
# @Time : 2022/3/4 11:42
# @Author : wdm
# @desc : 上传图片 https://fastapi.tiangolo.com/zh/tutorial/request-files/?h=up#uploadfile
import shutil
from pathlib import Path
from tempfile import NamedTemporaryFile
from fastapi import APIRouter, Depends, File, UploadFile
from sqlalchemy.orm import Session

import crud
from core import settings
from device.deps import get_db, get_current_user1
from models import Device
from utils import logger, resp_200
from utils.create_dir import create_dir

router = APIRouter()


@router.post("/upload/file/log/", summary="上传头像")
async def upload_log(
        file: UploadFile = File(...),
        db: Session = Depends(get_db),
        current_user: Device = Depends(get_current_user1)
):
    static_path = create_dir(settings.STATIC_DIR)
    logger.info(f"用户 {current_user.name} 正在上传文件 {file.filename}.")
    try:
        suffix = Path(file.filename).suffix
        with NamedTemporaryFile(delete=False, suffix=suffix, dir=static_path) as tmp:
            shutil.copyfileobj(file.file, tmp)
            tmp_file_name = Path(tmp.name).name
    finally:
        file.file.close()
    #user = crud.admin.update(db, db_obj=current_user,
    #                         obj_in={'image': f"{settings.BASE_URL}/{settings.STATIC_DIR}/{tmp_file_name}"})
    return resp_200(data=[], msg='上传成功！')
