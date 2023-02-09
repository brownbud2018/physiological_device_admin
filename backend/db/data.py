#!/usr/bin/env python3
# _*_ coding: utf-8 _*_
# @Time : 2021/9/25 23:00
# @Author : wdm
# @desc : 测试数据
from datetime import date

adminData = [
    {'name': 'admin', 'is_active': True, 'user_type': True,
     'hashed_password': '$2b$12$fSWir4aZ2fVI1jZLAjvltOmW/S0XV5s3C5VeoYlKYtkpBmDQipPJa'},
]

accessData = [
    {'id': 1, 'access_code': 'admin', 'access_name': '管理员中心', 'parent_id': 0, 'access_image': 'static/author.jpg', 'is_check': 0, 'is_menu': 1, 'access_desc': '管理员中心', 'access_remark': '管理员中心备注'},
    {'id': 2, 'access_code': 'adminmanager', 'access_name': '管理员管理', 'parent_id': 1, 'access_image': 'static/author.jpg', 'is_check': 0, 'is_menu': 1, 'access_desc': '管理员管理', 'access_remark': '备注'},
    {'id': 3, 'access_code': 'rolemanager', 'access_name': '角色管理', 'parent_id': 1, 'access_image': 'static/author.jpg', 'is_check': 0, 'is_menu': 1, 'access_desc': '角色管理', 'access_remark': '备注'},
]

roleData = [
    {'id': 1, 'role_name': '管理员角色', 'role_status': 1, 'role_desc': '描述'},
    {'id': 2, 'role_name': '客服角色', 'role_status': 1, 'role_desc': '描述'},
    {'id': 3, 'role_name': '医生角色', 'role_status': 1, 'role_desc': '描述'},
]

projectData = [
    {'id': 1, 'pro_code': 'FT101', 'pro_name': '医疗项目', 'pro_image': 'static/author.jpg', 'pro_type': 0, 'pro_remark': '这是测试项目'},
]

productData = [
    {'id': 1, 'prod_code': 'FT101-D1', 'prod_name': 'FT101医院医生版', 'prod_image': 'static/author.jpg', 'project_id': 1, 'pro_remark': '这是医院医生版'},
    {'id': 2, 'prod_code': 'FT101-D2', 'prod_name': 'FT101社区医生版', 'prod_image': 'static/author.jpg', 'project_id': 1, 'pro_remark': '这是社区医生版'},
    {'id': 3, 'prod_code': 'FT101-H1', 'prod_name': 'FT101家庭专业版', 'prod_image': 'static/author.jpg', 'project_id': 1, 'pro_remark': '这是家庭专业版'},
    {'id': 4, 'prod_code': 'FT101-H2', 'prod_name': 'FT101家庭普通版', 'prod_image': 'static/author.jpg', 'project_id': 1, 'pro_remark': '这是家庭普通版'},
]

deviceData = [
    {'device_code': 'FT101D10001', 'name': '医疗平板1', 'version': 'V1.0.1', 'product_id': 1, 'address':'广东省深圳市', 'image': 'static/author.jpg',
     'is_active': 1, 'device_level': 0, 'device_ota': 1, 'device_auth_class_id': 1, 'hashed_password': '$2b$12$fSWir4aZ2fVI1jZLAjvltOmW/S0XV5s3C5VeoYlKYtkpBmDQipPJa'},
    {'device_code': 'FT101D10002', 'name': '医疗平板2', 'version': 'V1.0.1', 'product_id': 1, 'address':'广东省深圳市', 'image': 'static/author.jpg',
     'is_active': 1, 'device_level': 1, 'device_ota': 1, 'device_auth_class_id': 1, 'hashed_password': '$2b$12$fSWir4aZ2fVI1jZLAjvltOmW/S0XV5s3C5VeoYlKYtkpBmDQipPJa'},
    {'device_code': 'FT101D20001', 'name': '医疗平板3', 'version': 'V1.0.1', 'product_id': 2, 'address':'广东省深圳市', 'image': 'static/author.jpg',
     'is_active': 1, 'device_level': 2, 'device_ota': 2, 'device_auth_class_id': 2, 'hashed_password': '$2b$12$fSWir4aZ2fVI1jZLAjvltOmW/S0XV5s3C5VeoYlKYtkpBmDQipPJa'},
    {'device_code': 'FT101D20002', 'name': '医疗平板4', 'version': 'V1.0.1', 'product_id': 2, 'address':'广东省深圳市', 'image': 'static/author.jpg',
     'is_active': 1, 'device_level': 0, 'device_ota': 2, 'device_auth_class_id': 2, 'hashed_password': '$2b$12$fSWir4aZ2fVI1jZLAjvltOmW/S0XV5s3C5VeoYlKYtkpBmDQipPJa'},
    {'device_code': 'FT101H10001', 'name': '医疗平板5', 'version': 'V1.0.1', 'product_id': 3, 'address':'广东省深圳市', 'image': 'static/author.jpg',
     'is_active': 1, 'device_level': 1, 'device_ota': 3, 'device_auth_class_id': 3, 'hashed_password': '$2b$12$fSWir4aZ2fVI1jZLAjvltOmW/S0XV5s3C5VeoYlKYtkpBmDQipPJa'},
    {'device_code': 'FT101H10002', 'name': '医疗平板6', 'version': 'V1.0.1', 'product_id': 3, 'address':'广东省深圳市', 'image': 'static/author.jpg',
     'is_active': 1, 'device_level': 2, 'device_ota': 3, 'device_auth_class_id': 3, 'hashed_password': '$2b$12$fSWir4aZ2fVI1jZLAjvltOmW/S0XV5s3C5VeoYlKYtkpBmDQipPJa'},
    {'device_code': 'FT101H20001', 'name': '医疗平板7', 'version': 'V1.0.1', 'product_id': 4, 'address':'广东省深圳市', 'image': 'static/author.jpg',
     'is_active': 1, 'device_level': 0, 'device_ota': 4, 'device_auth_class_id': 4, 'hashed_password': '$2b$12$fSWir4aZ2fVI1jZLAjvltOmW/S0XV5s3C5VeoYlKYtkpBmDQipPJa'},
    {'device_code': 'FT101H20002', 'name': '医疗平板8', 'version': 'V1.0.1', 'product_id': 4, 'address':'广东省深圳市', 'image': 'static/author.jpg',
     'is_active': 1, 'device_level': 1, 'device_ota': 4, 'device_auth_class_id': 4, 'hashed_password': '$2b$12$fSWir4aZ2fVI1jZLAjvltOmW/S0XV5s3C5VeoYlKYtkpBmDQipPJa'},
]

otamainData = [
    {'id': 1, 'ota_code': 'FT101D001', 'ota_name': '医院医生版', 'ota_image': 'static/author.jpg', 'ota_package': 'com.njyaocheng.health', 'ota_type': 1, 'ota_update_type': 0, 'ota_info': '医院医生版简介1', 'ota_score': 3.4, 'ota_download_amount': 13800000000, 'ota_company': '吉祥星', 'ota_desc': 'OTAEN1描述', 'ota_remark': '这就是个测试医院医生版OTA'},
    {'id': 2, 'ota_code': 'FT101D002', 'ota_name': '社区医生版', 'ota_image': 'static/author.jpg', 'ota_package': 'com.njyaocheng.health', 'ota_type': 1, 'ota_update_type': 0, 'ota_info': '社区医生版简介2', 'ota_score': 2.3, 'ota_download_amount': 15400000000, 'ota_company': '吉祥星', 'ota_desc': '社区医生版描述', 'ota_remark': '这就是个测试社区医生版OTA'},
    {'id': 3, 'ota_code': 'FT101H001', 'ota_name': '家庭专业版', 'ota_image': 'static/author.jpg', 'ota_package': 'com.njyaocheng.health', 'ota_type': 1, 'ota_update_type': 0, 'ota_info': '家庭专业版简介1', 'ota_score': 2.3, 'ota_download_amount': 15400000000, 'ota_company': '吉祥星', 'ota_desc': '家庭专业版描述', 'ota_remark': '这就是个测试家庭专业版OTA'},
    {'id': 4, 'ota_code': 'FT101H002', 'ota_name': '家庭普通版', 'ota_image': 'static/author.jpg', 'ota_package': 'com.njyaocheng.health', 'ota_type': 1, 'ota_update_type': 0, 'ota_info': '家庭普通版简介2', 'ota_score': 2.3, 'ota_download_amount': 15400000000, 'ota_company': '吉祥星', 'ota_desc': '家庭普通版描述', 'ota_remark': '这就是个测试家庭普通版OTA'},
]

otaversionData = [
    {'id': 1, 'ota_v_code': 'FT101D1-V1.0.1', 'ota_v_name': '医院医生版V1.0.1', 'ota_v_image': 'static/author.jpg', 'ota_v_file': 'static/apk/2022/ota_v7_V0.0.11.zip', 'ota_v_md5': 'f3a9db4b9d48f57da45ed0c2953a797d', 'ota_v_updateInfo': 'repair settings crash', 'ota_main_id': 1, 'ota_v_default': 0, 'ota_v_remark': 'OTA版本备注1'},
    {'id': 2, 'ota_v_code': 'FT101D1-V1.0.2', 'ota_v_name': '医院医生版V1.0.2', 'ota_v_image': 'static/author.jpg', 'ota_v_file': 'static/apk/2022/ota_v7_V0.0.11.zip', 'ota_v_md5': 'f3a9db4b9d48f57da45ed0c2953a797d', 'ota_v_updateInfo': 'improve wifi connect', 'ota_main_id': 1, 'ota_v_default': 1, 'ota_v_remark': 'OTA版本备注2'},
    {'id': 3, 'ota_v_code': 'FT101D2-V1.0.1', 'ota_v_name': '社区医生版V1.0.1', 'ota_v_image': 'static/author.jpg', 'ota_v_file': 'static/apk/2022/ota_v7_V0.0.11.zip', 'ota_v_md5': 'f3a9db4b9d48f57da45ed0c2953a797d', 'ota_v_updateInfo': 'repair settings crash', 'ota_main_id': 2, 'ota_v_default': 0, 'ota_v_remark': 'OTA版本备注3'},
    {'id': 4, 'ota_v_code': 'FT101D2-V1.0.2', 'ota_v_name': '社区医生版V1.0.2', 'ota_v_image': 'static/author.jpg', 'ota_v_file': 'static/apk/2022/ota_v7_V0.0.11.zip', 'ota_v_md5': 'f3a9db4b9d48f57da45ed0c2953a797d', 'ota_v_updateInfo': 'improve wifi connect', 'ota_main_id': 2, 'ota_v_default': 1, 'ota_v_remark': 'OTA版本备注4'},
    {'id': 5, 'ota_v_code': 'FT101H1-V1.0.1', 'ota_v_name': '家庭专业版V1.0.1', 'ota_v_image': 'static/author.jpg', 'ota_v_file': 'static/apk/2022/ota_v7_V0.0.11.zip', 'ota_v_md5': 'f3a9db4b9d48f57da45ed0c2953a797d', 'ota_v_updateInfo': 'improve wifi connect', 'ota_main_id': 3, 'ota_v_default': 0, 'ota_v_remark': 'OTA版本备注5'},
    {'id': 6, 'ota_v_code': 'FT101H1-V1.0.2', 'ota_v_name': '家庭专业版V1.0.2', 'ota_v_image': 'static/author.jpg', 'ota_v_file': 'static/apk/2022/ota_v7_V0.0.11.zip', 'ota_v_md5': 'f3a9db4b9d48f57da45ed0c2953a797d', 'ota_v_updateInfo': 'repair settings crash', 'ota_main_id': 3, 'ota_v_default': 1, 'ota_v_remark': 'OTA版本备注6'},
    {'id': 7, 'ota_v_code': 'FT101H2-V1.0.1', 'ota_v_name': '家庭普通版V1.0.1', 'ota_v_image': 'static/author.jpg', 'ota_v_file': 'static/apk/2022/ota_v7_V0.0.11.zip', 'ota_v_md5': 'f3a9db4b9d48f57da45ed0c2953a797d', 'ota_v_updateInfo': 'improve wifi connect', 'ota_main_id': 4, 'ota_v_default': 0, 'ota_v_remark': 'OTA版本备注7'},
    {'id': 8, 'ota_v_code': 'FT101H2-V1.0.2', 'ota_v_name': '家庭普通版V1.0.2', 'ota_v_image': 'static/author.jpg', 'ota_v_file': 'static/apk/2022/ota_v7_V0.0.11.zip', 'ota_v_md5': 'f3a9db4b9d48f57da45ed0c2953a797d', 'ota_v_updateInfo': 'improve wifi connect', 'ota_main_id': 4, 'ota_v_default': 1, 'ota_v_remark': 'OTA版本备注8'},
]

authclassData = [
    {'id': 1, 'class_code': 'FT101D1001', 'class_name': '医院医生版授权类', 'class_image': 'static/author.jpg', 'class_desc': '医院医生版权限组合', 'class_remark': '医院医生版权限组合'},
    {'id': 2, 'class_code': 'FT101D2002', 'class_name': '社区医生版授权类', 'class_image': 'static/author.jpg', 'class_desc': '社区医生版权限组合', 'class_remark': '社区医生版权限组合'},
    {'id': 3, 'class_code': 'FT101H1001', 'class_name': '家庭专业版授权类', 'class_image': 'static/author.jpg', 'class_desc': '家庭专业版权限组合', 'class_remark': '家庭专业版权限组合'},
    {'id': 4, 'class_code': 'FT101H2002', 'class_name': '家庭普通版授权类', 'class_image': 'static/author.jpg', 'class_desc': '家庭普通版权限组合', 'class_remark': '家庭普通版权限组合'},
]

authdetailData = [
    {'id': 1, 'detail_code': 'Auth001', 'detail_name': '画面缩放权限', 'detail_image': 'static/author.jpg', 'detail_type': 0,  'detail_desc': '画面缩放', 'detail_remark': '画面缩放'},
    {'id': 2, 'detail_code': 'Auth002', 'detail_name': '画面平移权限', 'detail_image': 'static/author.jpg', 'detail_type': 1, 'detail_desc': '画面平移', 'detail_remark': '画面平移'},
    {'id': 3, 'detail_code': 'Auth003', 'detail_name': 'log自动保存上传', 'detail_image': 'static/author.jpg', 'detail_type': 0, 'detail_desc': 'log自动保存上传', 'detail_remark': 'log自动保存上传'},
    {'id': 4, 'detail_code': 'Auth004', 'detail_name': '非基础功能', 'detail_image': 'static/author.jpg', 'detail_type': 0, 'detail_desc': '非基础功能', 'detail_remark': '非基础功能'},
]

authclassanddetailData = [
    {'id': 1, 'class_id': 1, 'detail_id': 2},
    {'id': 2, 'class_id': 1, 'detail_id': 3},
    {'id': 3, 'class_id': 1, 'detail_id': 4},
    {'id': 4, 'class_id': 2, 'detail_id': 1},
    {'id': 5, 'class_id': 2, 'detail_id': 3},
    {'id': 6, 'class_id': 2, 'detail_id': 4},
    {'id': 7, 'class_id': 3, 'detail_id': 2},
    {'id': 8, 'class_id': 3, 'detail_id': 4},
    {'id': 9, 'class_id': 4, 'detail_id': 1},
    {'id': 10, 'class_id': 4, 'detail_id': 2},
]

devicelogData = [
    {'id': 1, 'log_code': 'Log001', 'device_id': 1, 'log_image': 'static/log/tmp4bel9nr4.jpg'},
    {'id': 2, 'log_code': 'Log002', 'device_id': 2, 'log_image': 'static/log/tmp4bel9nr4.jpg'},
    {'id': 3, 'log_code': 'Log003', 'device_id': 3, 'log_image': 'static/log/tmp4bel9nr4.jpg'},
    {'id': 4, 'log_code': 'Log004', 'device_id': 4, 'log_image': 'static/log/tmp4bel9nr4.jpg'},
    {'id': 5, 'log_code': 'Log005', 'device_id': 5, 'log_image': 'static/log/tmp4bel9nr4.jpg'},
    {'id': 6, 'log_code': 'Log006', 'device_id': 6, 'log_image': 'static/log/tmp4bel9nr4.jpg'},
    {'id': 7, 'log_code': 'Log007', 'device_id': 6, 'log_image': 'static/log/tmp4bel9nr4.jpg'},
    {'id': 8, 'log_code': 'Log008', 'device_id': 7, 'log_image': 'static/log/tmp4bel9nr4.jpg'},
    {'id': 9, 'log_code': 'Log009', 'device_id': 7, 'log_image': 'static/log/tmp4bel9nr4.jpg'},
]

statisticsData = [
    {'id': 1, 'stat_code': 'tongji001', 'stat_name': '画面缩放功能使用次数统计', 'prod_id': 1, 'stat_num': 100, 'stat_remark': '画面缩放功能使用次数统计'},
    {'id': 2, 'stat_code': 'tongji002', 'stat_name': '微信使用次数统计', 'prod_id': 1, 'stat_num': 999, 'stat_remark': '微信使用次数统计'},
    {'id': 3, 'stat_code': 'tongji003', 'stat_name': '画面平移功能使用次数统计', 'prod_id': 2, 'stat_num': 111, 'stat_remark': '画面平移功能使用次数统计'},
    {'id': 4, 'stat_code': 'tongji004', 'stat_name': '京东使用次数统计', 'prod_id': 2, 'stat_num': 158, 'stat_remark': '京东使用次数统计'},
    {'id': 5, 'stat_code': 'tongji005', 'stat_name': '爱奇艺使用次数统计', 'prod_id': 3, 'stat_num': 158, 'stat_remark': '爱奇艺使用次数统计'},
    {'id': 6, 'stat_code': 'tongji006', 'stat_name': '极光tv使用次数统计', 'prod_id': 4, 'stat_num': 147, 'stat_remark': '极光tv使用次数统计'},
]

exceluploadData = [
    {'id': 1, 'excel_code': 'excel001', 'excel_name': '第一批试产机器导入excel', 'excel_address': 'static/excel001.xlsx', 'is_import': 0, 'excel_remark': '测试上传Excel',
     'name': '医疗平板1', 'device_ota': 1, 'version': 'V7-1.0.1', 'product_id': 1, 'address':'广东省深圳市', 'image': 'static/author.jpg',
     'is_active': 1, 'device_level': 0, 'device_auth_class_id': 1, 'hashed_password': '123'
     },
    {'id': 2, 'excel_code': 'excel002', 'excel_name': '第二批试产机器导入excel', 'excel_address': 'static/excel002.xlsx', 'is_import': 0, 'excel_remark': '测试上传Excel',
     'name': '医疗平板2', 'device_ota': 1, 'version': 'V7-1.0.1', 'product_id': 1, 'address':'广东省深圳市', 'image': 'static/author.jpg',
     'is_active': 1, 'device_level': 0, 'device_auth_class_id': 1, 'hashed_password': '123'
     },
]