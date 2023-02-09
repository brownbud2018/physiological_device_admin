#!/usr/bin/env python3
# _*_ coding: utf-8 _*_
# @Time : 2021/9/22 9:40
# @Author : wdm
# @desc : 数据模型(类似于TS中的interface)
from .common import GMT, Relation
from .access import AccessCreate, AccessUpdate, AccessOut, AccessDelete, AccessType, AccessUpdateType, AccessType1, AccessUpdateType1, AccessCodeCheck, AccessCodeCheckNoid
from .accessrole import AccessroleCreate, AccessroleUpdate, AccessroleOut, AccessroleDelete
from .admin import AdminCreate, AdminUpdate, AdminOut, AdminDelete, AdminType, AdminType1, AdminCodeCheck, AdminCodeCheckNoid, AdminPwd
from .adminauth import AdminauthclassCreate, AdminauthclassUpdate, AdminauthclassOut, AdminauthclassDelete
from .appclass import AppclassCreate, AppclassUpdate, AppclassOut, AppclassDesc, AppclassDelete
from .apppro import AppproCreate, AppproUpdate, AppproOut, AppproDelete, AppproType, AppproUpdateType
from .appversion import AppversionCreate, AppversionUpdate, AppversionOut, AppversionType, AppversionDelete
from .authclass import AuthclassCreate, AuthclassUpdate, AuthclassOut, AuthclassDelete
from .authclassanddetail import AuthclassanddetailCreate, AuthclassanddetailUpdate, AuthclassanddetailOut, AuthclassanddetailDelete
from .authdetail import AuthdetailCreate, AuthdetailUpdate, AuthdetailOut, AuthdetailType, AuthdetailDelete
from .cities import CitiesCreate, CitiesUpdate, CitiesOut, CitiesDelete
from .d_question import D_questionCreate, D_questionUpdate, D_questionOut, D_questionDelete
from .d_rhmedicalrecord import D_rhmedicalrecordCreate, D_rhmedicalrecordUpdate, D_rhmedicalrecordOut, D_rhmedicalrecordDelete
from .device import DeviceIn, DeviceCreate, DeviceUpdate, DeviceOut, DeviceDelete, DeviceType, DeviceCodeCheck, DeviceCodeCheckNoid, DevicePwd
from .devicelog import DevicelogCreate, DevicelogUpdate, DevicelogOut, DevicelogDelete
from .dm_user import Dm_userCreate, Dm_userUpdate, Dm_userOut, Dm_userDelete, Dm_userType, Dm_userCodeCheck, Dm_userCodeCheckNoid, Dm_userPwd
from .dm_physique import Dm_physiqueCreate, Dm_physiqueUpdate, Dm_physiqueOut, Dm_physiqueDelete
from .ecs_consulting import Ecs_ConsultingCreate, Ecs_ConsultingUpdate, Ecs_ConsultingOut, Ecs_ConsultingDelete
from .ecs_consulting_talklog import Ecs_Consulting_TalklogCreate, Ecs_Consulting_TalklogUpdate, Ecs_Consulting_TalklogOut, Ecs_Consulting_TalklogDelete
from .ecs_professors import Ecs_professorsCreate, Ecs_professorsUpdate, Ecs_professorsOut, Ecs_professorsType, Ecs_professorsDelete, Ecs_professorsMenu
from .excelupload import ExceluploadCreate, ExceluploadUpdate, ExceluploadOut, ExceluploadType, ExceluploadDelete, ExceluploadImport
from .login import Login
from .otamain import OtamainCreate, OtamainUpdate, OtamainOut, OtamainDelete, OtamainType, OtamainUpdateType
from .otaversion import OtaversionCreate, OtaversionUpdate, OtaversionOut, OtaversionDelete, OtaversionType
from .product import ProductCreate, ProductUpdate, ProductOut, ProductDelete
from .productapp import ProductappCreate, ProductappUpdate, ProductappOut, ProductappDelete
from .project import ProjectCreate, ProjectUpdate, ProjectOut, ProjectType, ProjectDelete
from .provinces import ProvincesCreate, ProvincesUpdate, ProvincesOut, ProvincesDelete
from .result import SchemasType, ResultModel, ResultPlusModel, NewResultModel
from .role import RoleCreate, RoleUpdate, RoleOut, RoleType, RoleDelete, RoleMenu
from .statistics import StatisticsCreate, StatisticsUpdate, StatisticsOut, StatisticsDelete
from .todo import TodoId, Todo
from .token import Token, TokenData
