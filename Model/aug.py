from dataclasses import dataclass
from enum import Enum


@dataclass
class AugRaw:
    station: str
    pm: str
    mname: str
    chsnm: str
    btable: str
    stop_yn: str
    status: str
    cls_sn: str


class pmEnum(Enum):
    R = 0
    S = 1
    T = 2
    W = 3
    C1 = 4


from flask_restx import fields, Namespace
ns_aug = Namespace('aug')
user_dto = ns_aug.model('User', {
    'user_id': fields.String(required=True, description='使用者代碼'),
    'user_name': fields.String(required=True, description='使用者名稱'),
    'dept_no': fields.String(required=True, description='使用者單位代碼'),
    'email': fields.String(required=True, description='電子郵件帳號'),
    'group_id': fields.String(required=True, description='群組代碼'),
    'prt': fields.String(required=True, description='不明'),
    'pmdtm': fields.DateTime(required=True, description='密碼修改時間'),
    'status': fields.String(required=True, description='帳號使用狀態'),
    'user_id_hris': fields.String(required=True, description='使用者代碼'),
    'assume_date': fields.DateTime(required=True, description='到職日'),
    'leave_date': fields.DateTime(required=True, description='離職日'),
    'job_title': fields.String(required=True, description='職稱'),
    'job_rank': fields.Integer(required=True, description='職級'),
    'no_pay_status': fields.Integer(required=True, description='留停狀態'),
})
