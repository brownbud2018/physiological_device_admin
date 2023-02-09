#!/usr/bin/env python3
# _*_ coding: utf-8 _*_
# @Time : 2022/1/6 14:29
# @Author : wdm
# @desc : 中间件 https://fastapi.tiangolo.com/tutorial/middleware/
from fastapi import FastAPI, Request
from sqlalchemy.exc import OperationalError
from aioredis.exceptions import ConnectionError

from utils import logger, resp_500


# 权限验证 https://www.cnblogs.com/mazhiyong/p/13433214.html
# 得到真实ip https://stackoverflow.com/questions/60098005/fastapi-starlette-get-client-real-ip
# nginx 解决跨域请求 https://segmentfault.com/a/1190000019227927

def register_middleware(app: FastAPI):
    """ 请求拦截与响应拦截 TODO 此处捕获异常失败 """

    @app.middleware("http")
    async def intercept(request: Request, call_next):
        logger.info(f"访问记录:IP:{request.client.host}-method:{request.method}-url:{request.url}")
        try:
            await request.app.state.redis.incr('request_num')  # redis 请求数量 (自增 1)
            return await call_next(request)  # 返回请求(跳过token)
        except ConnectionError as e:
            logger.error(f'redis连接失败！-- {e}')
            return resp_500(msg=f'redis连接失败！')
        except OperationalError as e:
            logger.error(f'数据库连接失败！-- {e}')
            return resp_500(msg=f'redis数据库连接失败！')

    '''def do_you_need_transcoding(target_single_str):
        special_character_list = ['+', ' ', '/', '?', '%', '#', '&', '=']
        if target_single_str in special_character_list:
            # ord转ASCII, hex转16进制
            return ''.join(('%', hex(ord(target_single_str))[2:]))
        else:
            # 无需处理, 返回原字符
            return target_single_str'''