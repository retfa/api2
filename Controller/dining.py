from flask import request, current_app
from flask_restx import Resource, Namespace, fields
import jwt
import time
import logging
from BLL.srvmesdbt1.hr.dietarytype import DietaryTypeBll
from BLL.srvmesdbt1.hr.dininglocation import DiningLocationBll
from BLL.srvmesdbt1.hr.dininguser import DiningUserBll
from Model.srvmesdbt1.hr.dininguser import DiningUser
from common import GetJwtPayload, set_security
from fta_response import FtaResult

ns_dining = Namespace('dining', description='用餐相關')
user_add_edit_model = ns_dining.model('UserAddEditDto.user', {
    # 'user_id': fields.String(required=False),
    'location_code': fields.String(required=True),
    'dietary_type_code': fields.String(required=False),
})


@ns_dining.route('/location')
class Location(Resource):
    # @ns_dining.expect(parser)
    # @ns_dining.marshal_with(fta_response, as_list=True) #輸出自動轉model
    @ns_dining.doc(description='查詢用餐地點',
                   responses={200: 'OK',
                              400: 'Bad Request'})
    def get(self):
        print(f'{request.method} {request.url_rule.rule}')
        logging.info(f'{request.method} {request.url_rule.rule}')
        try:
            set_security(self, current_app)
        except Exception as e:
            msg = f'{self.__class__.__name__} |An error occurred: {str(e)}'
            print(msg)
            logging.debug(msg)
            return {'message': msg}, 500

        parser = None
        data = {}
        if parser:
            data = parser.parse_args()

        print(f'data:{type(data)}')

        try:
            data['jwt'] = GetJwtPayload(self.security, request)
        except jwt.ExpiredSignatureError:
            print("JWT签名已过期")
            return {'message': 'Authentication failed'}, 401
        except jwt.PyJWTError as e:
            print(f"JWT异常: {e}")
            return {'message': 'Authentication failed'}, 401

        try:
            bll = DiningLocationBll()
            start_time = time.time()
            rst = bll.browse({})
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
            print(e)
            return {'message': f'ERRor, {e}'}


@ns_dining.route('/dietarytype')
class DietaryType(Resource):
    # @ns_dining.expect(parser)
    # @ns_dining.marshal_with(fta_response, as_list=True) #輸出自動轉model
    @ns_dining.doc(description='查詢飲食類別',
                   responses={200: 'OK',
                               400: 'Bad Request'})
    def get(self):
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
            data = {}
            print(f'data:{type(data)}')
            try:
                data['jwt'] = GetJwtPayload(self.security, request)
            except jwt.ExpiredSignatureError:
                print("JWT签名已过期")
                return {'message': 'Authentication failed'}, 401
            except jwt.PyJWTError as e:
                print(f"JWT异常: {e}")
                return {'message': 'Authentication failed'}, 401

            bll = DietaryTypeBll()
            start_time = time.time()
            rst = bll.browse({})
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
            print(e)
            return {'message': f'ERRor, {e}'}


@ns_dining.route('/user/<string:id>')
class UserDiningLocationAndDietaryType(Resource):
    # @ns_dining.expect(parser)
    # @ns_dining.marshal_with(fta_response, as_list=True) #輸出自動轉model
    @ns_dining.doc(
        id='',
        description='查詢使用者用餐地點及飲食類別',
        responses={200: 'OK',
                    400: 'Bad Request'})
    def get(self, id):
        print(f'{request.method} {request.url_rule.rule}')
        logging.info(f'{request.method} {request.url_rule.rule}')
        try:
            set_security(self, current_app)
        except Exception as e:
            msg = f'{self.__class__.__name__} |An error occurred: {str(e)}'
            print(msg)
            logging.debug(msg)
            return {'message': msg}, 500
        data = {}
        print(f'data:{type(data)}')
        try:
            data['jwt'] = GetJwtPayload(self.security, request)
        except jwt.ExpiredSignatureError:
            print("JWT签名已过期")
            return {'message': 'Authentication failed'}, 401
        except jwt.PyJWTError as e:
            print(f"JWT异常: {e}")
            return {'message': 'Authentication failed'}, 401
        try:
            bll = DiningUserBll()
            start_time = time.time()
            rst = bll.read(id)
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
            print(e)
            return {'message': f'ERRor, {e}'}

    @ns_dining.expect(user_add_edit_model)
    @ns_dining.doc(params={'id': '使用者id'},
                   description='HR表修改資料',
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
            data = {}
            for k in user_add_edit_model._schema['properties'].keys():
                if k in ns_dining.payload:
                    data[k] = ns_dining.payload[k]
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

            user_instance = DiningUser.user_add_edit(data)

            bll = DiningUserBll()
            start_time = time.time()
            rst = bll.edit(user_instance)
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

    @ns_dining.expect(user_add_edit_model)
    @ns_dining.doc(params={'id': '使用者id'},
                   description='HR表新增資料',
                   responses={200: 'OK',
                              400: 'Bad Request'})
    def post(self, id):
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
            data = {}
            for k in user_add_edit_model._schema['properties'].keys():
                if k in ns_dining.payload:
                    data[k] = ns_dining.payload[k]
            try:
                data['jwt'] = GetJwtPayload(self.security, request)
            except jwt.ExpiredSignatureError:
                print("JWT签名已过期")
                return {'message': 'Authentication failed'}, 401
            except jwt.PyJWTError as e:
                print(f"JWT异常: {e}")
                return {'message': 'Authentication failed'}, 401
            data['user_id'] = id
            data['busr'] = data['jwt']["FTAId"]
            print(user_add_edit_model._schema['properties'].keys())
            user_instance = DiningUser.user_add_edit(data)

            bll = DiningUserBll()
            start_time = time.time()
            rst = bll.add(user_instance)
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
