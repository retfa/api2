import json
import os
from types import SimpleNamespace
from flask import request, current_app
from flask_restx import Resource, Namespace
import jwt
import time
import logging
from BLL.user import UserBll
from Model.user import UserDto, user_query_filter_dto, user_dto, user_add_dto, user_edit_dto, user_status_dto, user_password_dto
from Model.srvmesdbt1.hr.emploee import Emploee, emploee_edit_dto, emploee_add_dto

from common import GetJwtPayload, set_security, create_parser
from fta_response import FtaResult

ns_user = Namespace('user', description='user operations')

user_filter_model = ns_user.model('UserDto.user_filter', user_query_filter_dto)
user_model = ns_user.model('UserDto.user', user_dto)
user_add_model = ns_user.model('UserAddDto.user', user_add_dto)
user_edit_model = ns_user.model('UserEditDto.user', user_edit_dto)
user_status_model = ns_user.model('UserStatusDto.user', user_status_dto)
user_password_model = ns_user.model('UserPasswordDto.user', user_password_dto)
parser = create_parser(user_filter_model)

emploee_edit_model = ns_user.model('EmploeeEditDto.user', emploee_edit_dto)
emploee_add_model = ns_user.model('EmploeeEditDto.user', emploee_add_dto)


@ns_user.route('/hrad6/<string:id>')
class HumanResourceSrvad6(Resource):
    @ns_user.doc(description='從HR ad6查詢特定使用者',
                 responses={200: 'OK',
                            400: 'Bad Request'})
    def get(self, id):
        try:
            logging.info(f'{request.method} {request.url_rule.rule}')
            json_path_security = os.path.join(current_app.config['folders']['temproot'], 'security.json')
            logging.info(f'json_path_security: {json_path_security}')
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
            bll = UserBll()
            start_time = time.time()
            rst = bll.srvad6_hr_read(id)
            end_time = time.time()
            execution_time = round((end_time - start_time) * 1000, 2)
            output = FtaResult(rst, execution_time, True).to_dict()
            print(output)
            return output, output['status_code']
        except Exception as e:
            msg = f'{self.__class__.__name__} |An error occurred: {str(e)}'
            print(msg)
            logging.debug(msg)

            return {'message': msg}, 500


@ns_user.route('/hr')
class HumanResources(Resource):
    @ns_user.expect(parser)
    # @ns_user.marshal_with(fta_response, as_list=True) #輸出自動轉model
    @ns_user.doc(description='查詢特定使用者',
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

        data = {}
        data = parser.parse_args()
        print(type(data))
        try:
            data['jwt'] = GetJwtPayload(self.security, request)
        except jwt.ExpiredSignatureError:
            print("JWT签名已过期")
            return {'message': 'Authentication failed'}, 401
        except jwt.PyJWTError as e:
            print(f"JWT异常: {e}")
            return {'message': 'Authentication failed'}, 401

        try:
            bll = UserBll()
            start_time = time.time()
            rst = bll.hr_browse(data)
            end_time = time.time()
            execution_time = round((end_time - start_time) * 1000, 2)
            output = FtaResult(rst, execution_time, True).to_dict()
            # print(output)
            return output, output['status_code']
        except Exception as e:
            return {'message': f'Controller.user.py |An error occurred: {str(e)}'}, 500


@ns_user.route('/hr/<string:idhris>')
class HumanResource(Resource):
    @ns_user.doc(params={'idhris': '使用者hris_id'},
                 description='HR表查詢使用者',
                 responses={200: 'OK',
                            400: 'Bad Request'})
    def get(self, idhris):
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

        data = {}
        print(type(data))
        try:
            data['jwt'] = GetJwtPayload(self.security, request)
        except jwt.ExpiredSignatureError:
            print("JWT签名已过期")
            return {'message': 'Authentication failed'}, 401
        except jwt.PyJWTError as e:
            print(f"JWT异常: {e}")
            return {'message': 'Authentication failed'}, 401

        try:
            bll = UserBll()
            start_time = time.time()
            rst = bll.hr_read(idhris)
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

            return {'message': msg}, 500

    @ns_user.expect(emploee_edit_model)
    @ns_user.doc(params={'idhris': '使用者hris_id'},
                 description='HR表修改資料',
                 responses={200: 'OK',
                            400: 'Bad Request'})
    def patch(self, idhris):
        print(f'{request.method} {request.url_rule.rule}')
        logging.info(f'{request.method} {request.url_rule.rule}')
        try:
            set_security(self, current_app)
        except Exception as e:
            msg = f'{self.__class__.__name__} |An error occurred: {str(e)}'
            print(msg)
            logging.debug(msg)

            return {'message': msg}, 500

        try:
            data = ns_user.payload
            print(f'data:{type(data)}')
            try:
                data['jwt'] = GetJwtPayload(self.security, request)
            except jwt.ExpiredSignatureError:
                print("JWT签名已过期")
                return {'message': 'Authentication failed'}, 401
            except jwt.PyJWTError as e:
                print(f"JWT异常: {e}")
                return {'message': 'Authentication failed'}, 401
            data['Emp_ID'] = idhris
            data['ModifyBy'] = data['jwt']["FTAId"]

            emploee_instance = Emploee.emploee_edit(data)

            bll = UserBll()
            start_time = time.time()
            rst = bll.hr_edit(emploee_instance)
            end_time = time.time()
            execution_time = round((end_time - start_time) * 1000, 2)
            if isinstance(rst, Exception):
                output = FtaResult(rst.args, execution_time).to_dict()
            else:
                output = FtaResult(rst, execution_time, success=True).to_dict()
            print(output)
            return output, output['status_code']
        except jwt.ExpiredSignatureError:
            print("JWT签名已过期")
            return {'message': 'Authentication failed'}, 401
        except jwt.PyJWTError as e:
            print(f"JWT异常: {e}")
            return {'message': 'Authentication failed'}, 401
        except Exception as e:
            return {'message': f'ERRor, {e}'}

    @ns_user.expect(emploee_add_model)
    @ns_user.doc(params={'idhris': '使用者hris_id'},
                 description='HR表新增資料',
                 responses={200: 'OK',
                            400: 'Bad Request'})
    def post(self, idhris):
        print(f'{request.method} {request.url_rule.rule}')
        logging.info(f'{request.method} {request.url_rule.rule}')
        try:
            set_security(self, current_app)
        except Exception as e:
            msg = f'{self.__class__.__name__} |An error occurred: {str(e)}'
            print(msg)
            logging.debug(msg)

            return {'message': msg}, 500

        try:
            data = ns_user.payload
            print(f'data:{type(data)}')
            try:
                data['jwt'] = GetJwtPayload(self.security, request)
            except jwt.ExpiredSignatureError:
                print("JWT签名已过期")
                return {'message': 'Authentication failed'}, 401
            except jwt.PyJWTError as e:
                print(f"JWT异常: {e}")
                return {'message': 'Authentication failed'}, 401
            data['Emp_ID'] = idhris
            data['CreateBy'] = data['jwt']["FTAId"]

            emploee_instance = Emploee.emploee_add(data)

            bll = UserBll()
            start_time = time.time()
            rst = bll.hr_add(emploee_instance)
            end_time = time.time()
            execution_time = round((end_time - start_time) * 1000, 2)
            if isinstance(rst, Exception):
                output = FtaResult(rst.args, execution_time).to_dict()
            else:
                output = FtaResult(rst, execution_time, success=True).to_dict()
            print(output)
            return output, output['status_code']
        except jwt.ExpiredSignatureError:
            print("JWT签名已过期")
            return {'message': 'Authentication failed'}, 401
        except jwt.PyJWTError as e:
            print(f"JWT异常: {e}")
            return {'message': 'Authentication failed'}, 401
        except Exception as e:
            return {'message': f'ERRor, {e}'}


@ns_user.route('/')
class Users(Resource):
    @ns_user.expect(parser)
    # @ns_user.marshal_with(fta_response, as_list=True) #輸出自動轉model
    @ns_user.doc(description='查詢特定使用者',
                 responses={200: 'OK',
                            400: 'Bad Request'})
    def get(self):
        try:
            logging.info(f'{request.method} {request.url_rule.rule}')
            json_path_security = os.path.join(current_app.config['folders']['temproot'], 'security.json')
            logging.info(f'json_path_security: {json_path_security}')
            with open(json_path_security, 'r') as file2:
                data = json.load(file2)
                self.key = data["Jwt"]["Key"]
                self.aud = data["Jwt"]["Audience"]
        except Exception as e:
            return {'message': f'Controller.user.py |An error occurred: {str(e)}'}, 500
        try:
            logging.info('Controller.user.py')
            data = parser.parse_args()
            print(f'data:{type(data)}')
            jwt_token = request.cookies.get('jwt')
            try:
                payload = jwt.decode(jwt_token, self.key, algorithms=['HS256'], audience=self.aud)
            except jwt.ExpiredSignatureError:
                print("JWT签名已过期")
                return {'message': 'Authentication failed'}, 401
            except jwt.PyJWTError as e:
                print(f"JWT异常: {e}")
                return {'message': 'Authentication failed'}, 401

            bll = UserBll()
            start_time = time.time()
            rst = bll.browse(data)
            end_time = time.time()
            execution_time = round((end_time - start_time) * 1000, 2)
            output = FtaResult(rst, execution_time, True).to_dict()
            # print(output)
            return output, output['status_code']
        except Exception as e:
            return {'message': f'Controller.user.py |An error occurred: {str(e)}'}, 500

    @ns_user.expect(user_add_model)
    @ns_user.doc(description='Add user',
                 responses={200: 'OK',
                            400: 'Bad Request'})
    def post(self):
        try:
            logging.info(f'{request.method} {request.url_rule.rule}')
            json_path_security = os.path.join(current_app.config['folders']['temproot'], 'security.json')
            logging.info(f'json_path_security: {json_path_security}')
            with open(json_path_security, 'r') as file2:
                data = json.load(file2)
                self.key = data["Jwt"]["Key"]
                self.aud = data["Jwt"]["Audience"]
        except Exception as e:
            return {'message': f'menu.py |An error occurred: {str(e)}'}, 500
        try:
            jwt_token = request.cookies.get('jwt')
            print(jwt)
            try:
                payload = jwt.decode(jwt_token, self.key, algorithms=['HS256'],
                                     audience=self.aud)
            except jwt.ExpiredSignatureError:
                print("JWT签名已过期")
                return {'message': 'Authentication failed'}, 401
            except jwt.PyJWTError as e:
                print(f"JWT异常: {e}")
                return {'message': 'Authentication failed'}, 401

            logging.info(f'{request.method} {request.url_rule.rule}')
            data = ns_user.payload
            data['busr'] = payload["FTAId"]
            print(type(data))
            zmuser_instance = UserDto.implicit_user_add(data)
            print(zmuser_instance)
            bll = UserBll()
            start_time = time.time()
            rst = bll.add(zmuser_instance)
            end_time = time.time()
            execution_time = round((end_time - start_time) * 1000, 2)
            if isinstance(rst, Exception):
                output = FtaResult(rst.args, execution_time).to_dict()
            else:
                if rst == -1:
                    output = FtaResult(rst, execution_time,
                                       success=False).to_dict()
                else:
                    output = FtaResult(rst, execution_time,
                                       success=True).to_dict()
            print(output)
            return output, output['status_code']

        except Exception as e:
            return {'message': f'ERRor, {e}'}


@ns_user.route('/<string:id>')
class User(Resource):
    @ns_user.doc(params={'id': '要查詢資料的使用者id'},
                 description='查詢特定使用者',
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

            bll = UserBll()
            start_time = time.time()
            rst = bll.read(id)
            end_time = time.time()
            execution_time = round((end_time - start_time) * 1000, 2)
            output = FtaResult(rst, execution_time, True).to_dict()
            print(output)
            return output, output['status_code']
        except Exception as e:
            return {'message': f'Controller.user.py |An error occurred: {str(e)}'}, 500

    @ns_user.expect(user_edit_model)
    @ns_user.doc(params={'id': '要修改資料的使用者id'},
                 description='Edit user properties',
                 responses={200: 'OK',
                            400: 'Bad Request'})
    def patch(self, id):
        print(f'{request.method} {request.url_rule.rule}')
        logging.info(f'{request.method} {request.url_rule.rule}')
        try:
            set_security(self, current_app)
        except Exception as e:
            msg = f'{self.__class__.__name__} |An error occurred: {str(e)}'
            print(msg)
            logging.debug(msg)

            return {'message': msg}, 500

        try:
            data = ns_user.payload
            print(f'data:{type(data)}')
            try:
                data['jwt'] = GetJwtPayload(self.security, request)
            except jwt.ExpiredSignatureError:
                print("JWT签名已过期")
                return {'message': 'Authentication failed'}, 401
            except jwt.PyJWTError as e:
                print(f"JWT异常: {e}")
                return {'message': 'Authentication failed'}, 401
            data['user_id'] = id
            data['musr'] = data['jwt']["FTAId"]

            zmuser_instance = UserDto.implicit_user_edit(data)

            bll = UserBll()
            start_time = time.time()
            rst = bll.edit(zmuser_instance)
            end_time = time.time()
            execution_time = round((end_time - start_time) * 1000, 2)
            if isinstance(rst, Exception):
                output = FtaResult(rst.args, execution_time).to_dict()
            else:
                output = FtaResult(rst, execution_time, success=True).to_dict()
            print(output)
            return output, output['status_code']
        except jwt.ExpiredSignatureError:
            print("JWT签名已过期")
            return {'message': 'Authentication failed'}, 401
        except jwt.PyJWTError as e:
            print(f"JWT异常: {e}")
            return {'message': 'Authentication failed'}, 401
        except Exception as e:
            return {'message': f'ERRor, {e}'}


@ns_user.route('/password/<string:id>')
class UserPassword(Resource):
    @ns_user.expect(user_password_model)
    @ns_user.doc(params={'id': '要更改密碼的使用者id'},
                 description='更改使用者密碼，只能更改登入者自己',
                 responses={200: 'OK',
                            400: 'Bad Request'})
    def patch(self, id):
        print(f'{request.method} {request.url_rule.rule}')
        logging.info(f'{request.method} {request.url_rule.rule}')
        try:
            set_security(self, current_app)
        except Exception as e:
            msg = f'{self.__class__.__name__} |An error occurred: {str(e)}'
            print(msg)
            logging.debug(msg)

            return {'message': msg}, 500

        try:
            data = ns_user.payload
            try:
                data.jwt = GetJwtPayload(self.security, request)
            except jwt.ExpiredSignatureError:
                print("JWT签名已过期")
                return {'message': 'Authentication failed'}, 401
            except jwt.PyJWTError as e:
                print(f"JWT异常: {e}")
                return {'message': 'Authentication failed'}, 401

            data['user_id'] = id
            data['musr'] = data.jwt["FTAId"]

            zmuser_instance = UserDto.implicit_user_password_edit(data)

            bll = UserBll()
            start_time = time.time()
            rst = bll.password_edit(zmuser_instance)
            end_time = time.time()
            execution_time = round((end_time - start_time) * 1000, 2)
            if isinstance(rst, Exception):
                output = FtaResult(rst.args, execution_time).to_dict()
            else:
                output = FtaResult(rst, execution_time, success=True).to_dict()
            print(output)
            return output, output['status_code']
        except jwt.ExpiredSignatureError:
            print("JWT签名已过期")
            return {'message': 'Authentication failed'}, 401
        except jwt.PyJWTError as e:
            print(f"JWT异常: {e}")
            return {'message': 'Authentication failed'}, 401
        except Exception as e:
            return {'message': f'ERRor, {e}'}


@ns_user.route('/password/reset<string:id>')
class UserPasswordReset(Resource):
    # @ns_user.expect(user_status_model)
    @ns_user.doc(params={'id': '要重設密碼的使用者id'},
                 description='重設使用者密碼',
                 responses={200: 'OK',
                            400: 'Bad Request'})
    def patch(self, id):
        print(f'{request.method} {request.url_rule.rule}')
        logging.info(f'{request.method} {request.url_rule.rule}')
        try:
            set_security(self, current_app)
        except Exception as e:
            msg = f'{self.__class__.__name__} |An error occurred: {str(e)}'
            print(msg)
            logging.debug(msg)

            return {'message': msg}, 500

        try:
            data = SimpleNamespace(jwt=None)
            try:
                data.jwt = GetJwtPayload(self.security, request)
            except jwt.ExpiredSignatureError:
                print("JWT签名已过期")
                return {'message': 'Authentication failed'}, 401
            except jwt.PyJWTError as e:
                print(f"JWT异常: {e}")
                return {'message': 'Authentication failed'}, 401

            data['user_id'] = id
            data['musr'] = data.jwt["FTAId"]

            zmuser_instance = UserDto.implicit_user_password_edit(data)

            bll = UserBll()
            start_time = time.time()
            rst = bll.password_reset(zmuser_instance)
            end_time = time.time()
            execution_time = round((end_time - start_time) * 1000, 2)
            if isinstance(rst, Exception):
                output = FtaResult(rst.args, execution_time).to_dict()
            else:
                output = FtaResult(rst, execution_time, success=True).to_dict()
            print(output)
            return output, output['status_code']
        except jwt.ExpiredSignatureError:
            print("JWT签名已过期")
            return {'message': 'Authentication failed'}, 401
        except jwt.PyJWTError as e:
            print(f"JWT异常: {e}")
            return {'message': 'Authentication failed'}, 401
        except Exception as e:
            return {'message': f'ERRor, {e}'}

    
@ns_user.route('/status/<string:id>')
class UserStatus(Resource):
    # @ns_user.doc(params={'id': '要查詢資料的使用者id'},
    #              description='查詢特定使用者',
    #              responses={200: 'OK',
    #                         400: 'Bad Request'})
    # def get(self,id):
    #     try:
    #         logging.info(f'{request.method} {request.url_rule.rule}')
    #         json_path_security = os.path.join(current_app.config['folders']['temproot'], 'security.json')
    #         logging.info(f'json_path_security: {json_path_security}')
    #         with open(json_path_security, 'r') as file2:
    #             data = json.load(file2)
    #             self.key = data["Jwt"]["Key"]
    #             self.aud = data["Jwt"]["Audience"]
    #     except Exception as e:
    #         return {'message': f'Controller.user.py |An error occurred: {str(e)}'}, 500
    #     try:
    #         logging.info('Controller.user.py')
    #         data = parser.parse_args()
    #         jwt_token = request.cookies.get('jwt')
    #         try:
    #             payload = jwt.decode(jwt_token, self.key, algorithms=['HS256'],audience=self.aud)
    #         except jwt.ExpiredSignatureError:
    #             print("JWT签名已过期")
    #             return {'message': 'Authentication failed'}, 401
    #         except jwt.PyJWTError as e:
    #             print(f"JWT异常: {e}")
    #             return {'message': 'Authentication failed'}, 401

    #         bll=UserBll()
    #         start_time = time.time()
    #         rst = bll.read(id)
    #         end_time = time.time()
    #         execution_time = round((end_time - start_time) * 1000, 2)
    #         output=FtaResult(rst,execution_time,True).to_dict()
    #         print(output)
    #         return output, output['status_code']
    #     except Exception as e:
    #         return {'message': f'Controller.user.py |An error occurred: {str(e)}'}, 500

    @ns_user.expect(user_status_model)
    @ns_user.doc(params={'id': '要啟停用的使用者id'},
                 description='啟/停用使用者',
                 responses={200: 'OK',
                            400: 'Bad Request'})
    def patch(self, id):
        print(f'{request.method} {request.url_rule.rule}')
        logging.info(f'{request.method} {request.url_rule.rule}')
        try:
            set_security(self, current_app)
        except Exception as e:
            msg = f'{self.__class__.__name__} |An error occurred: {str(e)}'
            print(msg)
            logging.debug(msg)

            return {'message': msg}, 500

        try:
            data = ns_user.payload
            print(f'data: {type(data)}')
            try:
                data['jwt'] = GetJwtPayload(self.security, request)
            except jwt.ExpiredSignatureError:
                print("JWT签名已过期")
                return {'message': 'Authentication failed'}, 401
            except jwt.PyJWTError as e:
                print(f"JWT异常: {e}")
                return {'message': 'Authentication failed'}, 401

            data['user_id'] = id
            data['musr'] = data['jwt']["FTAId"]

            zmuser_instance = UserDto.implicit_user_status_edit(data)

            bll = UserBll()
            start_time = time.time()
            rst = bll.status_edit(zmuser_instance)
            end_time = time.time()
            execution_time = round((end_time - start_time) * 1000, 2)
            if isinstance(rst, Exception):
                output = FtaResult(rst.args, execution_time).to_dict()
            else:
                output = FtaResult(rst, execution_time, success=True).to_dict()
            print(output)
            return output, output['status_code']
        except jwt.ExpiredSignatureError:
            print("JWT签名已过期")
            return {'message': 'Authentication failed'}, 401
        except jwt.PyJWTError as e:
            print(f"JWT异常: {e}")
            return {'message': 'Authentication failed'}, 401
        except Exception as e:
            return {'message': f'ERRor, {e}'}
