#!/usr/bin/env python3
# _*_ coding: utf-8 _*_
# @Time : 2022/1/9 16:48
# @Author : wdm
# @desc : 跨域请求 https://fastapi.tiangolo.com/zh/tutorial/cors/
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from core import settings

#str(origin) for origin in settings.CORS_ORIGINS
def register_cors(app: FastAPI):
    """ 跨域请求 """
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=("GET", "POST", "PUT", "DELETE"),
        allow_headers=("*", "authentication"),
    )
