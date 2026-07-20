class Emploee:
    # def __init__(self, user_id, user_acc, username):
    #     self.user_id = user_id
    #     self.user_acc = user_acc
    #     self.username = username

    # class emploee_add:
    #     def __init__(self, usr):
    #         self.user_id = usr['user_id']
    #         self.user_id_hris = usr['user_id_hris']
    #         self.user_name = usr['user_name']
    #         self.original_name = usr['original_name']
    #         self.department_id = usr['department_id']
    #         self.dept_no = usr['dept_no']
    #         self.email = usr['email']
    #         self.group_id = usr['group_id']
    #         self.pwd= usr['pwd']
    #         self.assume_date = usr['assume_date']
    #         self.job_title = usr['job_title']
    #         self.job_rank = usr['job_rank']
    # class implicit_emploee_add(emploee_add):
    #     def __init__(self, usr):
    #         super().__init__(usr)
    #         self.prt='Y'
    #         self.busr=usr['busr']

    class emploee_add:
        def __init__(self, usr):
            # print(f'usr: {type(usr)}')
            for key, value in usr.items():
                setattr(self, key, value)

    class emploee_edit:
        def __init__(self, usr):
            # print(f'usr: {type(usr)}')
            for key, value in usr.items():
                setattr(self, key, value)

    # class implicit_emploee_edit(emploee_edit):
    #     def __init__(self, usr):
    #         super().__init__(usr)
    #         self.ModifyBy=usr['musr']


from flask_restx import fields, Namespace
ns_user = Namespace('user')
emploee_dto = ns_user.model('Emploee', {
    'Emp_Guid': fields.String(required=True),
    'COM': fields.String(required=True),
    'Emp_ID': fields.String(required=True),
    'Email': fields.String(required=True),
    'Emp_Name': fields.String(required=True),
    'Emp_EName': fields.String(required=True),
    'Department_ID': fields.String(required=True),
    'Department_ID2': fields.String(required=True),
    'Job_Title': fields.String(required=True),
    'Assume_Date': fields.DateTime(required=True),
    'Leave_Date': fields.DateTime(required=True),
    'CreateDate': fields.DateTime(required=True),
    'AccessionState': fields.Integer(required=True),
    'NoPayStatus': fields.Integer(required=True),
    'jobrank': fields.Integer(required=True),
    'cellphone1': fields.String(required=True),
    'cellphone2': fields.String(required=True),
    'officephone': fields.String(required=True),
    'emp_id_hr': fields.String(required=True),
    'shift': fields.String(required=True),
})

emploee_add_dto = ns_user.model('EmploeeAddDto', {
    'Email': fields.String(required=False),
    'Emp_Name': fields.String(required=True),
    'Emp_EName': fields.String(required=False),
    'Department_ID': fields.String(required=False),
    'Department_ID2': fields.String(required=False),
    'Job_Title': fields.String(required=False),
    'Assume_Date': fields.DateTime(required=False),
    'Leave_Date': fields.DateTime(required=False),
    'AccessionState': fields.Integer(required=False),
    'NoPayStatus': fields.Integer(required=False),
    'jobrank': fields.Integer(required=False),
    'cellphone1': fields.String(required=False),
    'cellphone2': fields.String(required=False),
    'officephone': fields.String(required=False),
    'emp_id_hr': fields.String(required=True),
    'shift': fields.String(required=False),
})

emploee_edit_dto = ns_user.model('EmploeeEditDto', {
    'Email': fields.String(required=False),
    'Emp_Name': fields.String(required=False),
    'Emp_EName': fields.String(required=False),
    'Department_ID': fields.String(required=False),
    'Department_ID2': fields.String(required=False),
    'Job_Title': fields.String(required=False),
    'Assume_Date': fields.DateTime(required=False),
    'Leave_Date': fields.DateTime(required=False),
    'AccessionState': fields.Integer(required=False),
    'NoPayStatus': fields.Integer(required=False),
    'jobrank': fields.Integer(required=False),
    'cellphone1': fields.String(required=False),
    'cellphone2': fields.String(required=False),
    'officephone': fields.String(required=False),
    'emp_id_hr': fields.String(required=False),
    'shift': fields.String(required=False),
})