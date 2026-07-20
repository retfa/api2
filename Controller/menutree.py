from flask import request, current_app
import flask_restx
# from flask_restx import Resource, Namespace, fields
import jwt
import time
import logging
from BLL.menutree import MenuTreeBll
from common import GetJwtPayload, create_parser, set_security
from fta_response import FtaResult
from Model.menutree import menutree_add_dto

ns_menutree = flask_restx.Namespace('menutree', description='Menutree 結構相關')

menu_model = ns_menutree.model('Menu', {
    'Node': flask_restx.fields.String(required=True, description='Start Node')
})
menutree_add_model = ns_menutree.model('menutreeAddModel', menutree_add_dto)

parser = create_parser(menu_model)


@ns_menutree.route('/')
class MenuTree(flask_restx.Resource):
    @ns_menutree.expect(parser)
    # @api.marshal_with(fta_response, as_list=True) #輸出自動轉model
    @ns_menutree.doc(description='''取得Menu結構資料
    ![desc1](../static/img/desc1.jpg)
    ''',
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
        try:
            data['jwt'] = GetJwtPayload(self.security, request)
        except jwt.ExpiredSignatureError:
            print("JWT签名已过期")
            return {'message': 'Authentication failed'}, 401
        except jwt.PyJWTError as e:
            print(f"JWT异常: {e}")
            return {'message': 'Authentication failed'}, 401

        try:
            bll = MenuTreeBll()
            start_time = time.time()
            rst = bll.browse(data)
            end_time = time.time()
            execution_time = round((end_time - start_time) * 1000, 2)
            resp = FtaResult(rst, execution_time, True).to_dict()
            return resp, resp['status_code']
        except Exception as e:
            msg = f'{self.__class__.__name__} |An error occurred: {str(e)}'
            print(msg)
            logging.debug(msg)

            return {'message': msg}, 500

    @ns_menutree.expect(menutree_add_model)
    @ns_menutree.doc(description='新增目錄',
                     responses={200: 'OK',
                                400: 'Bad Request'})
    def post(self):
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

        data = ns_menutree.payload
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
        try:
            bll = MenuTreeBll()
            start_time = time.time()
            rst = bll.add(data)
            end_time = time.time()
            execution_time = round((end_time - start_time) * 1000, 2)
            if isinstance(rst, Exception):
                output = FtaResult(rst.args, execution_time).to_dict()
            elif rst == -1:
                output = FtaResult(rst, execution_time).to_dict()
            else:
                output = FtaResult(rst, execution_time, success=True).to_dict()
            print(output)
            return output, output['status_code']

        except Exception as e:
            msg = f'{self.__class__.__name__} |An error occurred: {str(e)}'
            print(msg)
            logging.debug(msg)


@ns_menutree.route('/all')
class MenuTreeAll(flask_restx.Resource):
    # @ns_menutree.expect(parser)
    # @api.marshal_with(fta_response, as_list=True) #輸出自動轉model
    @ns_menutree.doc(description='取得Menu結構資料',
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

        data = {"Node": "all"}
        try:
            data['jwt'] = GetJwtPayload(self.security, request)
        except jwt.ExpiredSignatureError:
            print("JWT签名已过期")
            return {'message': 'Authentication failed'}, 401
        except jwt.PyJWTError as e:
            print(f"JWT异常: {e}")
            return {'message': 'Authentication failed'}, 401

        try:
            bll = MenuTreeBll()
            start_time = time.time()
            rst = bll.browse(data)
            end_time = time.time()
            execution_time = round((end_time - start_time) * 1000, 2)
            resp = FtaResult(rst, execution_time, True).to_dict()
            return resp, resp['status_code']
        except Exception as e:
            msg = f'{self.__class__.__name__} |An error occurred: {str(e)}'
            print(msg)
            logging.debug(msg)

            return {'message': msg}, 500
