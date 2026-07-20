from flask_restx import fields, Namespace


class PermissionCrossDepartment:
    def __init__(self):
        pass

    class filter:
        def __init__(self, userid, progid):
            self.user_id = userid
            self.progm_id = progid


ns_permission_cross_department = Namespace('permission_cross_department')

permission_cross_department_query_filter_dto = ns_permission_cross_department.model('PermissionCrossDepartmentFilter', {
    'user_id': fields.String(required=False, description='user_id'),
    'progm_id': fields.String(required=False, description='program id'),
})

permission_cross_department_user_query_filter_dto = ns_permission_cross_department.model('PermissionCrossDepartmentFilter', {
    'progm_id': fields.String(required=False, description='program id'),
})

permission_cross_department_edit_dto = ns_permission_cross_department.model('PermissionCrossDepartmentEditDto', {
    'progm_id': fields.String(required=False, description='program id'),
    'departments': fields.String(required=False, description='departments'),
})