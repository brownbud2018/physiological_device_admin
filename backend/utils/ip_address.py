#!/usr/bin/env python3
# _*_ coding: utf-8 _*_
# @Time : 2022/3/4 15:21
# @Author : wdm
# @desc : 根据ip获取地址
import re,ast
from urllib import request
from ipaddress import ip_address

from utils import IpError


def verify_ip(ip):
    """ 验证ip格式是否正确 """
    try:
        return str(ip_address(ip))
    except Exception as e:
        raise IpError(f'错误的IP格式！ -- {e}')


def by_ip_get_address(ip) -> str:
    """ 根据ip获取地址 """
    verify_ip(ip)
    flag = "localhost" in ip
    if (flag):
        return "本机地址"
    flag1 = "127.0.0.1" in ip
    if (flag1):
        return "本机ip"
    #url1 = f"http://ip.ws.126.net/ipquery?ip={ip}"
    #搜狐免费查ip返回字符串：var returnCitySN = {"cip": "61.141.77.70", "cid": "440307", "cname": "广东省深圳市龙岗区"};
    #url2 = f"https://pv.sohu.com/cityjson?ip={ip}"
    # 太平洋免费查ip返回字符串：{"ip":"140.246.223.208","pro":"山东省","proCode":"370000","city":"潍坊市","cityCode":"370700","region":"","regionCode":"0","addr":"山东省潍坊市 电信","regionNames":"","err":""}
    #url3 = f"http://whois.pconline.com.cn/ipJson.jsp?json=true&ip={ip}"
    #ip-api免费查ip返回字符串：{"status":"success","country":"中国","countryCode":"CN","region":"SD","regionName":"山东省","city":"济南市","zip":"","lat":36.6533,"lon":117.146,"timezone":"Asia/Shanghai","isp":"Cloud Computing Corporation","org":"Chinanet SD","as":"AS58519 Cloud Computing Corporation","query":"140.246.223.208"}
    url4 = f"http://ip-api.com/json/{ip}?lang=zh-CN"
    #print('url4', url4)
    try:
        req = request.Request(url4)
        response = request.urlopen(req).read().decode('utf-8')  # 获取响应
        #handle_address = re.findall(r'"([^"]*)"', response)
        #return handle_address[0] + handle_address[1]
        handle_address = ast.literal_eval(response)
        if handle_address['status'] == 'success':
            return handle_address['regionName'] + handle_address['city']
        else:
            returnstr = 'IP查询出错，返回的错误内容：' + str(handle_address)
            print("returnstr:", returnstr)
            return returnstr
    except Exception as e:
        returnstr = 'IP查询出错，返回的错误内容：' + str(e)
        print('IP查询出错，返回的错误内容：', e)
        return returnstr
    finally:
        return '广东省深圳市'