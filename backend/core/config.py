#!/usr/bin/env python3
# _*_ coding: utf-8 _*_
# @Time : 2021/9/19 17:02
# @Author : wdm
# @desc : éç½®æä»¶
import secrets
from typing import Union, List
from pydantic import BaseSettings, AnyHttpUrl

project_desc = """
    ð ç®¡çåæ¥å£æ±æ» ð
    â¨ è´¦å·: admin â¨
    â¨ å¯ç : 123 â¨
    â¨ æé(scopes): admin â¨
"""


class Settings(BaseSettings):
    BASE_URL: AnyHttpUrl = "http://127.0.0.1:9889"  # å¼åç¯å¢

    STATIC_DIR: str = 'static'  # éææä»¶ç®å½

    PROJECT_DESC: str = project_desc  # æè¿°
    PROJECT_VERSION: Union[int, str] = 4.8  # çæ¬

    API_PREFIX: str = "/api"  # æ¥å£åç¼

    CORS_ORIGINS: List[AnyHttpUrl] = ["http://localhost:3000"]  # è·¨åè¯·æ±"http://localhost:3000", "http://8.136.82.204:8001"

    GLOBAL_ENCODING: str = 'utf-8'  # å¨å±ç¼ç 

    # DATABASE_URI: str = "sqlite:///./sql_app.db"  # Sqlite
    DATABASE_URI: str = "mysql://root:root@localhost:3306/ft101?charset=utf8"  # æ¬å°MySQL
    # DATABASE_URI: str = "postgresql://postgres:123456@localhost:5432/postgres"  # PostgreSQL
    DATABASE_ECHO: bool = False  # æ¯å¦æå°æ°æ®åºæ¥å¿ (å¯çå°åå»ºè¡¨ãè¡¨æ°æ®å¢å æ¹æ¥çä¿¡æ¯)

    REDIS_URI: str = "redis://:123456@localhost:6379/1"  # æ¬å°redis

    SECRET_KEY: str = secrets.token_urlsafe(32)  # å¯é¥
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 1  # tokenè¿ææ¶é´: 60 minutes * 24 hours * 1 days = 1 days

    LOGGER_DIR: str = "logs"  # æ¥å¿æä»¶å¤¹å
    LOGGER_NAME: str = '{time:YYYY-MM-DD_HH-mm-ss}.log'  # æ¥å¿æä»¶å (æ¶é´æ ¼å¼)
    LOGGER_LEVEL: str = 'DEBUG'  # æ¥å¿ç­çº§: ['DEBUG' | 'INFO']
    LOGGER_ROTATION: str = "12:00"  # æ¥å¿åç: æ æ¶é´æ®µ/æä»¶å¤§å° ååæ¥å¿. ä¾å¦ ["500 MB" | "12:00" | "1 week"]
    LOGGER_RETENTION: str = "7 days"  # æ¥å¿ä¿ççæ¶é´: è¶åºå°å é¤ææ©çæ¥å¿. ä¾å¦ ["1 days"]

    # æéæ°æ® (æ ¼å¼å¡å¿ä¸º {'åç§°', 'æè¿°'})
    PERMISSION_DATA: List[dict] = [{'admin': 'ç®¡çåæé'}, {'device': 'è®¾å¤å®¢æ·ç«¯'}]

    class Config:
        case_sensitive = True  # åºåå¤§å°å


settings = Settings()
