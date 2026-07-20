from flask_restx import fields, Namespace


class UserDto:
    def __init__(self, user_id, user_acc, username):
        self.user_id = user_id
        self.user_acc = user_acc
        self.username = username

    class user_login:
        def __init__(self, login_id, password):
            self.login_id = login_id
            self.password = password

    class user_signedIn:
        def __init__(self, FTAId, YFYId, Name, FTASn):
            self.FTAId = FTAId
            self.YFYId = YFYId
            self.Name = Name
            self.FTASn = FTASn

    class user_filter:
        def __init__(self, FTAId, YFYId, Name):
            self.FTAId = FTAId
            self.YFYId = YFYId
            self.Name = Name

    class user_add:
        def __init__(self, usr):
            self.user_id = usr['user_id']
            self.user_id_hris = usr['user_id_hris']
            self.user_name = usr['user_name']
            self.original_name = usr['original_name']
            self.department_id = usr['department_id']
            # self.dept_no = usr['dept_no']
            self.email = usr['email']
            self.group_id = usr['group_id']
            self.pwd = usr['pwd']
            self.assume_date = usr['assume_date']
            self.job_title = usr['job_title']
            self.job_rank = usr['job_rank']

    class implicit_user_add(user_add):
        def __init__(self, usr):
            super().__init__(usr)
            self.prt = 'Y'
            self.busr = usr['busr']

    class user_edit:
        def __init__(self, usr):
            print(f'usr: {type(usr)}')
            if usr.get('user_id_hris'):
                self.user_id_hris = usr['user_id_hris']
            if usr.get('user_name'):
                self.user_name = usr['user_name']
            if usr.get('original_name'):
                self.original_name = usr['original_name']
            if usr.get('department_id'):
                self.department_id = usr['department_id']
            # if usr.get('dept_no'):
            #     self.dept_no = usr['dept_no']
            if usr.get('email'):
                self.email = usr['email']
            if usr.get('group_id'):
                self.group_id = usr['group_id']
            if usr.get('prt'):
                self.prt = usr['prt']
            if usr.get('status'):
                self.status = usr['status']
            if usr.get('accession_state'):
                self.accession_state = usr['accession_state']
            if usr.get('no_pay_status'):
                self.no_pay_status = usr['no_pay_status']
            if usr.get('assume_date'):
                self.assume_date = usr['assume_date']
            if usr.get('leave_date'):
                self.leave_date = usr['leave_date']
            if usr.get('job_title'):
                self.job_title = usr['job_title']
            if usr.get('job_rank'):
                self.job_rank = usr['job_rank']

    class implicit_user_edit(user_edit):
        def __init__(self, usr):
            super().__init__(usr)
            self.user_id = usr['user_id']
            self.musr = usr['musr']

    class user_password_edit:
        def __init__(self, data):
            self.old_password = data['old_password']
            self.new_password = data['new_password']

    class implicit_user_password_edit(user_password_edit):
        def __init__(self, data):
            super().__init__(data)
            self.user_id = data['user_id']
            self.musr = data['musr']

    class user_status_edit:
        def __init__(self, usr):
            self.status = usr['status']

    class implicit_user_status_edit(user_status_edit):
        def __init__(self, usr):
            super().__init__(usr)
            self.user_id = usr['user_id']
            self.musr = usr['musr']


ns_user = Namespace('user')
user_dto = ns_user.model('User', {
    'user_id': fields.String(required=True, description='使用者代碼5'),
    'user_id_hris': fields.String(required=True, description='使用者代碼9'),
    'user_name': fields.String(required=True, description='使用者名稱'),
    'original_name': fields.String(required=True, description='原國籍使用者名稱'),
    'department_id': fields.String(required=True, description='部門代碼'),
    'dept_no': fields.String(required=True, description='部門編號'),
    'email': fields.String(required=True, description='電子郵件帳號'),
    'group_id': fields.String(required=True, description='群組代碼'),
    'prt': fields.String(required=True, description='不明'),
    'pmdtm': fields.DateTime(required=True, description='密碼修改時間'),
    'status': fields.String(required=True, description='帳號使用狀態'),
    'shift': fields.String(required=True, description='班別'),
    'accession_state': fields.Integer(required=True, description='在職狀況'),
    'no_pay_status': fields.Integer(required=True, description='留停狀態'),
    'assume_date': fields.DateTime(required=True, description='到職日'),
    'leave_date': fields.DateTime(required=True, description='離職日'),
    'job_title': fields.String(required=True, description='職稱'),
    'job_rank': fields.Integer(required=True, description='職級'),
    'last_sync': fields.DateTime(required=True, description='最後同步日'),
})

user_query_filter_dto = ns_user.model('UserFilter', {
    'id': fields.String(required=False, description='FTA ID'),
    'idhris': fields.String(required=False, description='HRIS ID'),
    'name': fields.String(required=False, description='Name')
})

user_add_dto = ns_user.model('UserAddDto', {
    'user_id': fields.String(required=True, description='使用者代碼5'),
    'user_id_hris': fields.String(required=True, description='使用者代碼9'),
    'user_name': fields.String(required=True, description='使用者名稱'),
    'original_name': fields.String(required=True, description='原國籍使用者名稱'),
    'pwd': fields.String(required=True, description='使用者密碼'),
    'department_id': fields.String(required=True, description='部門代碼'),
    'dept_no': fields.String(required=False, description='部門編號'),
    'email': fields.String(required=True, description='電子郵件帳號'),
    'group_id': fields.String(required=True, description='群組代碼'),
    'shift': fields.String(required=True, description='班別'),
    'assume_date': fields.String(required=True, description='到職日'),
    'job_title': fields.String(required=True, description='職稱'),
    'job_rank': fields.Integer(required=True, description='職級'),
})

user_edit_dto = ns_user.model('UserEditDto', {
    'user_id_hris': fields.String(required=True, description='使用者代碼9'),
    'user_name': fields.String(required=True, description='使用者名稱'),
    'original_name': fields.String(required=True, description='原國籍使用者名稱'),
    'department_id': fields.String(required=True, description='部門代碼'),
    'dept_no': fields.String(required=True, description='部門編號'),
    'email': fields.String(required=True, description='電子郵件帳號'),
    'group_id': fields.String(required=True, description='群組代碼'),
    'prt': fields.String(required=True, description='不明'),
    'status': fields.String(required=True, description='帳號使用狀態'),
    'shift': fields.String(required=True, description='班別'),
    'accession_state': fields.Integer(required=True, description='在職狀況'),
    'no_pay_status': fields.Integer(required=True, description='留停狀態'),
    'assume_date': fields.String(required=True, description='到職日'),
    'leave_date': fields.DateTime(required=True, description='離職日'),
    'job_title': fields.String(required=True, description='職稱'),
    'job_rank': fields.Integer(required=True, description='職級'),
})

user_password_dto = ns_user.model('UserPasswordDto', {
    'old_password': fields.String(required=True, description='舊密碼'),
    'new_password': fields.String(required=True, description='新密碼'),
})

user_status_dto = ns_user.model('UserStatusDto', {
    'status': fields.String(required=True, description='使用者名稱'),
})
