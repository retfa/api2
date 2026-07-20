# class Department:
#     class user_login:
#         def __init__(self, login_id, password):
#             self.login_id = login_id
#             self.password = password

#     class user_add:
#         def __init__(self, usr):
#             self.user_id = usr['user_id']
#             self.user_name = usr['user_name']
#             self.dept_no = usr['dept_no']
#             self.group_id = usr['group_id']
#             self.pwd= usr['pwd']
    # class implicit_user_add(user_add):
    #     def __init__(self, usr):
    #         super().__init__(usr)
    #         self.prt='Y'
    #         self.busr=usr['busr']

from flask_restx import fields, Namespace
ns_user = Namespace('user')
user_dto = ns_user.model('User', {
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

user_query_filter_dto = ns_user.model('UserFilter', {
    'id': fields.String(required=False, description='FTA ID'),
    'idhris': fields.String(required=False, description='HRIS ID'),
    'name': fields.String(required=False, description='Name')
})

user_add_dto = ns_user.model('UserAddDto', {
    'user_id': fields.String(required=True, description='使用者代碼'),
    'user_name': fields.String(required=True, description='使用者名稱'),
    'pwd': fields.String(required=True, description='使用者密碼'),
    'dept_no': fields.String(required=True, description='使用者單位代碼'),
    'group_id': fields.String(required=True, description='群組代碼'),
})

user_edit_dto = ns_user.model('UserEditDto', {
    'user_name': fields.String(required=True, description='使用者名稱'),
    'dept_no': fields.String(required=True, description='使用者單位代碼'),
    'group_id': fields.String(required=True, description='群組代碼'),
})