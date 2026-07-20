import json
import os
from flask import request, current_app
from flask_restx import Resource, Namespace, fields
import jwt
import time
import logging
from BLL.permission import PermissionBll
from BLL.permissioncrossdepartment import PermissionCrossDepartmentBll
from Model.permissioncrossdept import permission_cross_department_query_filter_dto, permission_cross_department_user_query_filter_dto, permission_cross_department_edit_dto
from common import create_parser, GetJwtPayload, set_security
from fta_response import FtaResult

ns_permission_cross_department = Namespace('permissioncrossdepartment', description='跨部門權限 相關')

permission_cross_department_filter_model = ns_permission_cross_department.model('PermissionCrossDepartmentDto.permission_cross_department_filter', permission_cross_department_query_filter_dto)
permission_cross_department_user_filter_model = ns_permission_cross_department.model('PermissionCrossDepartmentDto.permission_cross_department_filter', permission_cross_department_user_query_filter_dto)
permission_cross_department_edit_model = ns_permission_cross_department.model('PermissionCrossDepartmentDto.permission_cross_department_edit', permission_cross_department_edit_dto)

parser = create_parser(permission_cross_department_filter_model)
parser_user = create_parser(permission_cross_department_user_filter_model)


@ns_permission_cross_department.route('/')
class PermissionCrossDepartment(Resource):
    @ns_permission_cross_department.expect(parser)
    # @ns_permission_cross_department.marshal_with(fta_response, as_list=True) #輸出自動轉model
    @ns_permission_cross_department.doc(description='查詢權限',
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

            jwt_token = request.cookies.get('jwt')
            try:
                payload = jwt.decode(jwt_token, self.key, algorithms=['HS256'], audience=self.aud)
            except jwt.ExpiredSignatureError:
                print("JWT签名已过期")
                return {'message': 'Authentication failed'}, 401
            except jwt.PyJWTError as e:
                print(f"JWT异常: {e}")
                return {'message': 'Authentication failed'}, 401

            bll = PermissionCrossDepartmentBll()
            start_time = time.time()
            rst = bll.browse(data)
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


@ns_permission_cross_department.route('/<string:id>')
class UserPermissionCrossDepartment(Resource):
    @ns_permission_cross_department.expect(parser_user)
    # @ns_permission_cross_department.marshal_with(fta_response, as_list=True) #輸出自動轉model
    @ns_permission_cross_department.doc(description='查詢特定使用者權限',
                                        responses={200: 'OK',
                                                   400: 'Bad Request'})
    def get(self, id):
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
            data = parser_user.parse_args()
            data.user_id = id

            jwt_token = request.cookies.get('jwt')
            try:
                payload = jwt.decode(jwt_token, self.key, algorithms=['HS256'], audience=self.aud)
            except jwt.ExpiredSignatureError:
                print("JWT签名已过期")
                return {'message': 'Authentication failed'}, 401
            except jwt.PyJWTError as e:
                print(f"JWT异常: {e}")
                return {'message': 'Authentication failed'}, 401

            bll = PermissionCrossDepartmentBll()
            start_time = time.time()
            rst = bll.read(data)
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

    @ns_permission_cross_department.expect(permission_cross_department_edit_model)
    @ns_permission_cross_department.doc(description='編輯特定使用者權限',
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

        data = ns_permission_cross_department.payload
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
        data['musr'] = data['jwt']["FTAId"]
        data['busr'] = data['jwt']["FTAId"]
        try:
            bll = PermissionCrossDepartmentBll()
            start_time = time.time()
            rst = bll.edit(data)
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

    def delete(self, id):
        pass
