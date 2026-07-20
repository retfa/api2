from flask import request, current_app
from flask_restx import Resource, Namespace, fields
import jwt
import time
import logging
from BLL.menu import MenuBll
from common import GetJwtPayload, create_parser, set_security
from fta_response import FtaResult

ns_menu = Namespace('menu', description='Menu 相關')

menu_model = ns_menu.model('Menu', {
    'Node': fields.String(required=True, description='Start Node')
})

parser = create_parser(menu_model)


@ns_menu.route('')
class Menu(Resource):
    # def options(self):
    #     origin = request.headers.get('Origin')
    #     if origin in current_app.config['CORS']['allowed_origins']:
    #         return {'Allow': 'GET, POST, OPTIONS'}, 200, {
    #             'Access-Control-Allow-Origin': origin,
    #             'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
    #             'Access-Control-Allow-Headers': 'Content-Type, Authorization',
    #             'Access-Control-Allow-Credentials': 'true'
    #         }
    #     else:
    #         return {'message': 'Origin not allowed'}, 403

    @ns_menu.expect(parser)
    # @api.marshal_with(fta_response, as_list=True) #輸出自動轉model
    @ns_menu.doc(description='取得Menu資料',
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
            data['jwt'] = GetJwtPayload(self.security, request)
        except jwt.ExpiredSignatureError:
            print("JWT签名已过期")
            return {'message': 'Authentication failed'}, 401
        except jwt.PyJWTError as e:
            print(f"JWT异常: {e}")
            return {'message': 'Authentication failed'}, 401
        try:
            bll = MenuBll()
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