class Program:
    def __init__(self, user_id, user_acc, username):
        self.user_id = user_id
        self.user_acc = user_acc
        self.username = username


from flask_restx import fields, Namespace
ns_program = Namespace('program')

program_query_filter_dto = ns_program.model('ProgramFilter', {
    'function': fields.String(required=False, description='function'),
    'up_function': fields.String(required=False, description='up of function'),
    'progm_id': fields.String(required=False, description='program id'),
})

program_add_dto = ns_program.model('ProgramEditDto', {
    'progm_id': fields.String(required=True, description='程式Id', example='ZZZ010Z1'),
    'url': fields.String(required=False, description='URL', example='Z/Z/Z/ZZZ010Z1'),
    'f_code': fields.String(required=False, description='選單目錄代碼', example='ZZZ001101201'),
    'up_code': fields.String(required=False, description='上層目錄代碼', example='Z0001101'),
    'st_func': fields.String(required=False, description='特殊權限標記', example='N'),
    'sp_func': fields.String(required=False, description='特殊權限標記', example='N'),
    'pname': fields.String(required=False, description='程式中文名稱', example='測試名稱'),
    'desc': fields.String(required=False, description='程式功能說明', example='測試說明')
})