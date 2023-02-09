#!/usr/bin/env python3
# _*_ coding: utf-8 _*_
# @Time : 2022/3/4 11:42
# @Author : wdm
# @desc : 上传图片 https://fastapi.tiangolo.com/zh/tutorial/request-files/?h=up#uploadfile
# @desc : 大文件分片上传 https://v3u.cn/a_id_175
import shutil
import os
import datetime
import time
from pathlib import Path
from tempfile import NamedTemporaryFile
from fastapi import APIRouter, Depends, File, UploadFile, Request, Form
from sqlalchemy.orm import Session

import crud
from core import settings
from api.deps import get_db, get_current_user
from models import Admin
from utils import logger, resp_200, IdNotExist
from utils.create_dir import create_dir

from typing import List

router = APIRouter()

@router.post("/upload/file", summary="上传头像")
async def upload_image(
        file: UploadFile = File(...),
        db: Session = Depends(get_db),
        current_user: Admin = Depends(get_current_user)
):
    static_path = create_dir(settings.STATIC_DIR)
    logger.info(f"用户 {current_user.name} 正在上传图片 {file.filename}.")
    try:
        suffix = Path(file.filename).suffix
        with NamedTemporaryFile(delete=False, suffix=suffix, dir=static_path) as tmp:
            shutil.copyfileobj(file.file, tmp)
            tmp_file_name = Path(tmp.name).name
    finally:
        file.file.close()
    user = crud.admin.update(db, db_obj=current_user,
                             obj_in={'image': f"{settings.BASE_URL}/{settings.STATIC_DIR}/{tmp_file_name}"})
    return resp_200(data=user, msg='上传成功！')

@router.post("/upload/filetest", summary="上传test文件")
async def upload_log(
        file: UploadFile = File(...),
        current_user: Admin = Depends(get_current_user)
):
    static_path = create_dir(settings.STATIC_DIR + "/upload")
    logger.info(f"用户 {current_user.name} 正在上传文件 {file.filename}.")
    try:
        suffix = Path(file.filename).suffix
        with NamedTemporaryFile(delete=False, suffix=suffix, dir=static_path) as tmp:
            shutil.copyfileobj(file.file, tmp)
            tmp_file_name = Path(tmp.name).name
    finally:
        file.file.close()
    os.chmod(f"{settings.STATIC_DIR}/upload/{tmp_file_name}",0o664)#0o664、0o400
    user = "ID:" + str(current_user.id) + ",头像：" + str(current_user.image) + ",名称：" + str(current_user.name)
    cur_time = datetime.datetime.now()
    date_str = cur_time.strftime('%y%m%d')
    time_str = cur_time.strftime('%H%M%S')
    data = {
        'up_code': 'Up' + date_str + time_str,
        'user_id': current_user.id,
        'up_image': f"{settings.STATIC_DIR}/upload/{tmp_file_name}",
    }
    #add_log = devicelog.create(db, obj_in=data)
    backdata = {'user': user, 'file_temp': f"{settings.STATIC_DIR}/upload/{tmp_file_name}", 'create_data': data}
    return resp_200(data=backdata, msg='上传成功！')

@router.post('/upfile1/')
async def up_f1(request:Request,upload_list:List[UploadFile]=File(...)):
    # 获取文件名称列表
    file_names=[dd.filename for dd in upload_list]

    # 获取文件大小列表
    file_sizes=[round(len(ds.read())/1024,2) for ds in [dd.file for dd in upload_list]]

    # 获取文件类型列表
    file_types=[dd.content_type for dd in upload_list]

    # 获取文件对象列表
    filesss = [dd for dd in upload_list]

    # 根据文件个数进行遍历，使用列表索引
    for ss in range(len(file_names)):

        # 指定文件保存路径（使用源文件名称），当前路径下的file目录下
        pth = 'file\\{}'.format(file_names[ss])

        with open(pth, 'wb') as f:
            # @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
            # 每次读取1Mb写入
            for i in iter(lambda : filesss[ss].file.read(1024*1024),b''):
                f.write(i)
            # @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@

    return resp_200(
        data=
        {
            "request":request,
            "file_names":file_names,
            "file_sizes":file_sizes,
            "file_types":file_types
        }, msg='上传成功！')

@router.post("/upload/uploadfile")
async def upload_big_file(file: UploadFile = File(...), chunknumber: str = Form(...), identifier: str = Form(...)):#分片上传文件【用唯一标志符+分片序号】作为文件名
    if len(chunknumber) == 0 or len(identifier) == 0:
        return {"eroor": "没有传递相关参数"}
    task = identifier                           # 获取文件唯一标识符
    chunk = chunknumber                         # 获取该分片在所有分片中的序号【客户端设定】
    filename = '%s%s' % (task,chunk)           # 构成该分片唯一标识符
    contents = await file.read()                #异步读取文件
    with open(f"{settings.STATIC_DIR}/uploads/{filename}", "wb") as f:
        f.write(contents)
    return {"filename": file.filename}


@router.post("/upload/mergefile")
async def mergefile(identifier: str = Form(...), filename: str = Form(...), chunkstar: int = Form(...)):#根据唯一标识符合并文件
    if len(filename) == 0 or len(identifier) == 0:
        return {"eroor": "没有传递相关参数"}
    target_filename = filename      # 获取上传文件的文件名【保存的文件名】
    task = identifier              # 获取文件的唯一标识符
    chunk = chunkstar              # 分片序号开始的序号默认=0
    if os.path.isfile(f"{settings.STATIC_DIR}/uploads/{target_filename}"):#如果客户端传递过来的文件名在服务器上已经存在，那么另外新建一个【时间戳.后缀名】文件
        t = time.time()                                         #时间戳
        timeUnix = str(round(t * 1000))                         #毫秒级时间戳
        filesuffix = os.path.splitext(target_filename)[1]       #后缀名
        target_filename = timeUnix + filesuffix                 #新文件名【时间戳.后缀名】
    error_i = 0
    chunkfilename = ""
    with open(f"{settings.STATIC_DIR}/uploads/{target_filename}", 'wb') as target_file:  # 创建新文件
        while True:#循环把分片文件写入新建的文件
            if os.path.isfile(f"{settings.STATIC_DIR}/uploads/{task}{chunk}"):#存在这个文件
                try:
                    #分片文件名
                    chunkfilename = f"{settings.STATIC_DIR}/uploads/{task}{chunk}"
                    # 按序打开每个分片
                    source_file = open(chunkfilename, 'rb')
                    # 读取分片内容写入新文件
                    target_file.write(source_file.read())
                    source_file.close()
                except IOError:#当分片标志chunk累加到最后，文件夹里面不存在{task}{chunk}文件时，退出循环
                    break
                os.remove(f"{settings.STATIC_DIR}/uploads/{task}{chunk}")#删除分片文件
            else:#【如果分片文件上传中途出错，导致中间缺少某个分片文件，跳过它，不退出循环，直到累计缺少次数大于3次，再跳出循环】
                error_i += 1
                if error_i > 3:
                    break
            chunk += 1
    os.chmod(f"{settings.STATIC_DIR}/uploads/{target_filename}",0o664)#linux设置权限0o664、0o400
    return {"code":200, "filename": f"{settings.STATIC_DIR}/uploads/{target_filename}"}

@router.post("/upload/removefile")
async def removefile(identifier: str = Form(...), chunkstar: int = Form(...)):#根据唯一标识符删除文件
    if len(identifier) == 0:
        return {"eroor": "没有传递相关参数"}
    task = identifier              # 获取文件的唯一标识符
    chunk = chunkstar              # 分片序号开始的序号默认=0
    while True:#循环把分片文件删除
        try:
            #分片文件名
            del_filename = f"{settings.STATIC_DIR}/uploads/{task}{chunk}"
            os.remove(del_filename)#删除分片文件
        except IOError:#当分片标志chunk累加到最后，文件夹里面不存在{task}{chunk}文件时，退出循环
            break
        chunk += 1
    return {"code":200, "msg": '删除成功'}