class Permission:
    def __init__(self, user_id, user_acc, username):
        self.user_id = user_id
        self.user_acc = user_acc
        self.username = username

    class user_filter:
        def __init__(self, codes):
            self.codes = codes


from flask_restx import fields, Namespace # noqa: E402
ns_permission = Namespace('permission')

permission_query_filter_dto = ns_permission.model('PermissionFilter', {
    'function': fields.String(required=False, description='function'),
    'up_function': fields.String(required=False, description='up of function'),
    'progm_id': fields.String(required=False, description='program id'),
})

permission_edit_dto = ns_permission.model('PermissionEditDto', {
    'Havepermission': fields.String(required=True, description='Permission status'),
    'sid': fields.Integer(required=False, description='SID'),
    'user_id': fields.String(required=False, description='User ID'),
    'mname': fields.String(required=False, description='MName'),
    'progm_id': fields.String(required=False, description='Progm ID'),
    'up_code': fields.String(required=False, description='Up Code'),
    'f_code': fields.String(required=False, description='F Code'),
    'st_func': fields.String(required=False, description='St Func'),
    'sp_func': fields.String(required=False, description='Sp Func'),
    'func_print': fields.String(required=False, description='Func Print'),
    'func_edit': fields.String(required=False, description='Func Edit'),
    'func_sign': fields.String(required=False, description='Func Sign'),
    'func_detail': fields.String(required=False, description='Func Detail'),
    'func_download': fields.String(required=False, description='Func Download'),
    'func_other': fields.String(required=False, description='Func Other')
})

permission_copy_dto = ns_permission.model('PermissionCopyDto', {
    'source_id': fields.String(required=True, description='Permission status')
})