import json
import os
from flask import request, current_app
from flask_restx import Resource, Namespace, fields
import jwt
import time
import logging
from BLL.permission import PermissionBll
from Model.permission import permission_query_filter_dto, permission_edit_dto, permission_copy_dto
from common import create_parser, GetJwtPayload, set_security
from fta_response import FtaResult

ns_permission = Namespace('permission', description='permission 權限相關')

permission_filter_model = ns_permission.model('PermissionDto.permission_filter', permission_query_filter_dto)
permission_edit_model = ns_permission.model('PermissionDto.permission_edit', permission_edit_dto)
permission_edit_array_model = ns_permission.model('PermissionDto.permission_edit_array', {
    'user_id': fields.String(required=True, description='user_id'),
    'up_function': fields.String(required=True, description='up_function'),
    'Content': fields.List(fields.Nested(permission_edit_model), required=False, description='Content'),
})
permission_delete_model = ns_permission.model('PermissionDto.permission_delete', {
    'user_id': fields.String(required=True, description='user_id'),
    'function': fields.String(required=True, description='up_function'),
    'machine': fields.String(required=True, description='machine'),
})
permission_copy_model = ns_permission.model('PermissionDto.permission_copy', permission_copy_dto)
parser = create_parser(permission_filter_model)


@ns_permission.route('/')
class Permission(Resource):
    @ns_permission.expect(parser)
    # @ns_permission.marshal_with(fta_response, as_list=True) #輸出自動轉model
    @ns_permission.doc(description='查詢權限',
                       responses={200: 'OK',
                                  400: 'Bad Request'})
    def get(self):
        logging.info(f'{request.method} {request.url_rule.rule}')
        try:
            json_path_security = os.path.join(current_app.config['folders']['temproot'], 'security.json')
            # logging.info(f'json_path_security: {json_path_security}')
            with open(json_path_security, 'r') as file2:
                data = json.load(file2)
                self.key = data["Jwt"]["Key"]
                self.aud = data["Jwt"]["Audience"]
        except Exception as e:
            msg = f'{self.__class__.__name__} |An error occurred: {str(e)}'
            print(msg)
            logging.debug(msg)

            return {'message': msg}, 500

        try:
            data = parser.parse_args()
            data.function_array = []
            if data.function:
                data.function_array = data.function.split(',')

            data.up_function_array = []
            if data.up_function:
                data.up_function_array = data.up_function.split(',')

            data.progm_id_array = []
            if data.progm_id:
                data.progm_id_array = data.progm_id.split(',')

            jwt_token = request.cookies.get('jwt')
            try:
                payload = jwt.decode(jwt_token, self.key, algorithms=['HS256'], audience=self.aud)
            except jwt.ExpiredSignatureError:
                print("JWT签名已过期")
                return {'message': 'Authentication failed'}, 401
            except jwt.PyJWTError as e:
                print(f"JWT异常: {e}")
                return {'message': 'Authentication failed'}, 401

            bll = PermissionBll()
            start_time = time.time()
            rst = bll.read_by_user(data)
            end_time = time.time()
            execution_time = round((end_time - start_time) * 1000, 2)
            output = FtaResult(rst, execution_time, True).to_dict()
            # print(output)
            return output, output['status_code']
        except Exception as e:
            msg = f'{self.__class__.__name__} |An error occurred: {str(e)}'
            print(msg)
            logging.debug(msg)
            return {'message': msg}, 500

    @ns_permission.expect(permission_delete_model)
    @ns_permission.doc(description='刪除特定使用者權限',
                       responses={200: 'OK',
                                  400: 'Bad Request'})
    def delete(self):
        url = f'{request.method} {request.url_rule.rule}?{request.query_string.decode("utf-8")}'
        print(url)
        logging.info(url)
        try:
            set_security(self, current_app)
        except Exception as e:
            msg = f'{self.__class__.__name__} |An error occurred: {str(e)}'
            print(msg)
            logging.debug(msg)

            return {'message': msg}, 500

        data = ns_permission.payload
        # print(f'data: {type(data)}')
        try:
            data['jwt'] = GetJwtPayload(self.security, request)
        except jwt.ExpiredSignatureError:
            print("JWT签名已过期")
            return {'message': 'Authentication failed'}, 401
        except jwt.PyJWTError as e:
            print(f"JWT异常: {e}")
            return {'message': 'Authentication failed'}, 401
        except Exception as e:
            print(f"JWT异常: {e}")
            return {'message': 'Authentication failed'}, 401
        data['musr'] = data['jwt']["FTAId"]
        try:
            bll = PermissionBll()
            start_time = time.time()
            rst = bll.delete(data)
            end_time = time.time()
            execution_time = round((end_time - start_time) * 1000, 2)
            output = FtaResult(rst, execution_time, True).to_dict()
            # print(output)
            return output, output['status_code']
        except Exception as e:
            msg = f'{self.__class__.__name__} |An error occurred: {str(e)}'
            print(msg)
            logging.debug(msg)
            return {'message': msg}, 500

@ns_permission.route('/current')
class CurrentUserPermission(Resource):
    @ns_permission.expect(parser)
    # @ns_permission.marshal_with(fta_response, as_list=True) #輸出自動轉model
    @ns_permission.doc(description='查詢當前使用者權限',
                       responses={200: 'OK',
                                  400: 'Bad Request'})
    def get(self):
        url = f'{request.method} {request.url_rule.rule}?{request.query_string.decode("utf-8")}'
        print(url)
        logging.info(url)
        try:
            set_security(self, current_app)
        except Exception as e:
            msg = f'{self.__class__.__name__} |An error occurred: {str(e)}'
            print(msg)
            logging.debug(msg)

            return {'message': msg}, 500
        data = parser.parse_args()
        print(type(data))
        try:
            data.function_array = []
            if data.function:
                data.function_array = data.function.split(',')

            data.up_function_array = []
            if data.up_function:
                data.up_function_array = data.up_function.split(',')

            data.progm_id_array = []
            if data.progm_id:
                data.progm_id_array = data.progm_id.split(',')

            # jwt_token = request.cookies.get('jwt')
            # if not jwt_token:
            #     # 如果 cookie 中沒有，從 Authorization 標頭中獲取
            #     auth_header = request.headers.get('Authorization')
            #     if auth_header and auth_header.startswith('Bearer '):
            #         jwt_token = auth_header.split(' ')[1]  # 提取 Bearer token 的值

            try:
                data['jwt'] = GetJwtPayload(self.security, request)
                data.user_id = data['jwt'].get("FTAId")
            except jwt.ExpiredSignatureError:
                print("JWT签名已过期")
                return {'message': 'Authentication failed'}, 401
            except jwt.PyJWTError as e:
                print(f"JWT异常: {e}")
                return {'message': 'Authentication failed'}, 401

            bll = PermissionBll()
            start_time = time.time()
            rst = bll.read_by_user(data)
            end_time = time.time()
            execution_time = round((end_time - start_time) * 1000, 2)
            output = FtaResult(rst, execution_time, True).to_dict()
            # print(output)
            return output, output['status_code']
        except Exception as e:
            msg = f'{self.__class__.__name__} |An error occurred: {str(e)}'
            print(msg)
            logging.warning(msg)

            return {'message': msg}, 500


        url = f'{request.method} {request.url_rule.rule}?{request.query_string.decode("utf-8")}'
        print(url)
        logging.info(url)
        try:
            set_security(self, current_app)
        except Exception as e:
            msg = f'{self.__class__.__name__} |An error occurred: {str(e)}'
            print(msg)
            logging.debug(msg)

            return {'message': msg}, 500

        data = ns_permission.payload
        data["user_id"] = id
        # print(f'data: {type(data)}')
        try:
            data['jwt'] = GetJwtPayload(self.security, request)
        except jwt.ExpiredSignatureError:
            print("JWT签名已过期")
            return {'message': 'Authentication failed'}, 401
        except jwt.PyJWTError as e:
            print(f"JWT异常: {e}")
            return {'message': 'Authentication failed'}, 401
        except Exception as e:
            print(f"JWT异常: {e}")
            return {'message': 'Authentication failed'}, 401
        data['busr'] = data['jwt']["FTAId"]
        data['musr'] = data['jwt']["FTAId"]
        try:
            bll = PermissionBll()
            start_time = time.time()
            rst = bll.editbulk(data)
            end_time = time.time()
            execution_time = round((end_time - start_time) * 1000, 2)
            if isinstance(rst, Exception):
                output = FtaResult(rst.args, execution_time).to_dict()
            else:
                output = FtaResult(rst, execution_time, success=True).to_dict()
            print(output)
            return output, output['status_code']

        except Exception as e:
            msg = f'{self.__class__.__name__} |An error occurred: {str(e)}'
            print(msg)
            logging.debug(msg)

@ns_permission.route('/<string:id>')
class UserPermission(Resource):
    @ns_permission.expect(parser)
    # @ns_permission.marshal_with(fta_response, as_list=True) #輸出自動轉model
    @ns_permission.doc(description='查詢特定使用者權限',
                       responses={200: 'OK',
                                  400: 'Bad Request'})
    def get(self, id):
        url = f'{request.method} {request.url_rule.rule}?{request.query_string.decode("utf-8")}'
        print(url)
        logging.info(url)
        try:
            set_security(self, current_app)
        except Exception as e:
            msg = f'{self.__class__.__name__} |An error occurred: {str(e)}'
            print(msg)
            logging.debug(msg)

            return {'message': msg}, 500
        data = parser.parse_args()
        print(type(data))
        try:
            data.user_id = id
            data.function_array = []
            if data.function:
                data.function_array = data.function.split(',')

            data.up_function_array = []
            if data.up_function:
                data.up_function_array = data.up_function.split(',')

            data.progm_id_array = []
            if data.progm_id:
                data.progm_id_array = data.progm_id.split(',')

            # jwt_token = request.cookies.get('jwt')
            # if not jwt_token:
            #     # 如果 cookie 中沒有，從 Authorization 標頭中獲取
            #     auth_header = request.headers.get('Authorization')
            #     if auth_header and auth_header.startswith('Bearer '):
            #         jwt_token = auth_header.split(' ')[1]  # 提取 Bearer token 的值

            try:
                payload = GetJwtPayload(self.security, request)
            except jwt.ExpiredSignatureError:
                print("JWT签名已过期")
                return {'message': 'Authentication failed'}, 401
            except jwt.PyJWTError as e:
                print(f"JWT异常: {e}")
                return {'message': 'Authentication failed'}, 401

            bll = PermissionBll()
            start_time = time.time()
            rst = bll.read_by_user(data)
            end_time = time.time()
            execution_time = round((end_time - start_time) * 1000, 2)
            output = FtaResult(rst, execution_time, True).to_dict()
            # print(output)
            return output, output['status_code']
        except Exception as e:
            msg = f'{self.__class__.__name__} |An error occurred: {str(e)}'
            print(msg)
            logging.debug(msg)

            return {'message': msg}, 500

    @ns_permission.expect(permission_edit_array_model)
    @ns_permission.doc(description='編輯特定使用者權限',
                       responses={200: 'OK',
                                  400: 'Bad Request'})
    def put(self, id):
        url = f'{request.method} {request.url_rule.rule}?{request.query_string.decode("utf-8")}'
        print(url)
        logging.info(url)
        try:
            set_security(self, current_app)
        except Exception as e:
            msg = f'{self.__class__.__name__} |An error occurred: {str(e)}'
            print(msg)
            logging.debug(msg)

            return {'message': msg}, 500

        data = ns_permission.payload
        data["user_id"] = id
        # print(f'data: {type(data)}')
        try:
            data['jwt'] = GetJwtPayload(self.security, request)
        except jwt.ExpiredSignatureError:
            print("JWT签名已过期")
            return {'message': 'Authentication failed'}, 401
        except jwt.PyJWTError as e:
            print(f"JWT异常: {e}")
            return {'message': 'Authentication failed'}, 401
        except Exception as e:
            print(f"JWT异常: {e}")
            return {'message': 'Authentication failed'}, 401
        data['busr'] = data['jwt']["FTAId"]
        data['musr'] = data['jwt']["FTAId"]
        try:
            bll = PermissionBll()
            start_time = time.time()
            rst = bll.editbulk(data)
            end_time = time.time()
            execution_time = round((end_time - start_time) * 1000, 2)
            if isinstance(rst, Exception):
                output = FtaResult(rst.args, execution_time).to_dict()
            else:
                output = FtaResult(rst, execution_time, success=True).to_dict()
            print(output)
            return output, output['status_code']

        except Exception as e:
            msg = f'{self.__class__.__name__} |An error occurred: {str(e)}'
            print(msg)
            logging.debug(msg)


@ns_permission.route('/<string:id>/<string:function>/<string:machine>')
class PermissionDelete(Resource):
    @ns_permission.doc(params={'id': '要刪除權限的使用者id',
                               'function': '要刪除權限的功能代碼',
                               'machine': '要刪除權限的機台代碼'},
                       description='Delete user permission',
                       responses={200: 'OK',
                                  400: 'Bad Request'})
    def delete(self, id, function, machine):
        url = f'{request.method} {request.url_rule.rule}?{request.query_string.decode("utf-8")}'
        print(url)
        logging.info(url)
        try:
            set_security(self, current_app)
        except Exception as e:
            msg = f'{self.__class__.__name__} |An error occurred: {str(e)}'
            print(msg)
            logging.debug(msg)

            return {'message': msg}, 500

        # data = ns_permission.payload
        data = {}
        data["user_id"] = id
        data["function"] = function
        if machine == 'empty':
            data["machine"] = ''
        else:
            data["machine"] = machine
        # print(f'data: {type(data)}')
        try:
            data['jwt'] = GetJwtPayload(self.security, request)
        except jwt.ExpiredSignatureError:
            print("JWT签名已过期")
            return {'message': 'Authentication failed'}, 401
        except jwt.PyJWTError as e:
            print(f"JWT异常: {e}")
            return {'message': 'Authentication failed'}, 401
        except Exception as e:
            print(f"JWT异常: {e}")
            return {'message': 'Authentication failed'}, 401
        data['musr'] = data['jwt']["FTAId"]
        try:
            bll = PermissionBll()
            start_time = time.time()
            rst = bll.delete(data)
            end_time = time.time()
            execution_time = round((end_time - start_time) * 1000, 2)
            output = FtaResult(rst, execution_time, True).to_dict()
            # print(output)
            return output, output['status_code']
        except Exception as e:
            msg = f'{self.__class__.__name__} |An error occurred: {str(e)}'
            print(msg)
            logging.debug(msg)
            return {'message': msg}, 500


@ns_permission.route('/copy/<string:id>')
class UserStatus(Resource):
    @ns_permission.expect(permission_copy_model)
    @ns_permission.doc(params={'id': '要複製權限的使用者id'},
                       description='使用者將會從指定的userid複製同樣的權限',
                       responses={200: 'OK',
                                  400: 'Bad Request'})
    def put(self, id):
        url = f'{request.method} {request.url_rule.rule}?{request.query_string.decode("utf-8")}'
        print(url)
        logging.info(url)
        try:
            set_security(self, current_app)
        except Exception as e:
            msg = f'{self.__class__.__name__} |An error occurred: {str(e)}'
            print(msg)
            logging.debug(msg)

            return {'message': msg}, 500

        data = ns_permission.payload
        data["destination_id"] = id
        # print(f'data: {type(data)}')
        try:
            data['jwt'] = GetJwtPayload(self.security, request)
        except jwt.ExpiredSignatureError:
            print("JWT签名已过期")
            return {'message': 'Authentication failed'}, 401
        except jwt.PyJWTError as e:
            print(f"JWT异常: {e}")
            return {'message': 'Authentication failed'}, 401
        except Exception as e:
            print(f"JWT异常: {e}")
            return {'message': 'Authentication failed'}, 401
        data['busr'] = data['jwt']["FTAId"]
        try:
            bll = PermissionBll()
            start_time = time.time()
            rst = bll.copy(data)
            end_time = time.time()
            execution_time = round((end_time - start_time) * 1000, 2)
            if isinstance(rst, Exception):
                output = FtaResult(rst.args, execution_time).to_dict()
            else:
                output = FtaResult(rst, execution_time, success=True).to_dict()
            print(output)
            return output, output['status_code']

        except Exception as e:
            msg = f'{self.__class__.__name__} |An error occurred: {str(e)}'
            print(msg)
            logging.debug(msg)
