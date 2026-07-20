from dataclasses import dataclass
#from enum import Enum
from flask_restx import fields, Namespace


@dataclass
class MenutreeAdd:
    floor: int
    f_code: str
    f_type: str
    up_code: str
    f_name: str
    busr: str


@dataclass
class MenutreeEdit:
    floor: int
    f_type: str
    up_code: str
    f_name: str
    sub_num: int
    file_num: int
    musr: str

# class pmEnum(Enum):
#     S = 1
#     R = 0
#     T = 2
#     W = 3


ns_menutree = Namespace('menutree')
menutree_add_dto = ns_menutree.model('menutree_add_edit', {
    'floor': fields.Integer(required=True, description='層數'),
    'f_code': fields.String(required=True, description='選單目錄代碼'),
    'f_type': fields.String(required=False, description='類別'),
    'up_code': fields.String(required=False, description='上層目錄代碼'),
    'f_name': fields.String(required=True, description='名稱'),
    'station': fields.String(required=False, description='站別')
 })

menutree_edit_dto = ns_menutree.model('menutree_add_edit', {
    'floor': fields.Integer(required=True, description='層數'),
    'f_type': fields.String(required=True, description='類別'),
    'up_code': fields.String(required=True, description='上級代碼'),
    'f_name': fields.String(required=True, description='名稱'),
    'sub_num': fields.Integer(required=True, description='目錄數'),
    'file_num': fields.Integer(required=True, description='檔案數'),
    'station': fields.String(required=False, description='站別')
#    'musr': fields.String(required=True, description='修改人'),
#    'mdtm': fields.DateTime(required=True, description='修改日'),
 })
