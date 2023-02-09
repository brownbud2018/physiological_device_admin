#!/usr/bin/env python3
# _*_ coding: utf-8 _*_
# @Time : 2022/5/10 13:41
# @Author : ming
# @desc : 公用函数，方法，
import os
import sys


def get_project_root():
    curPath = os.path.abspath(os.path.dirname(__file__))
    backPath = ''
    if 'win32' in sys.platform:
        backPath = curPath.replace('\\utils','')
    elif 'linux' in sys.platform:
        backPath = curPath.replace('/utils','')
    return backPath
