# 暫不開發
from flask import request, current_app
from flask_restx import Resource, Namespace, fields
import jwt
import time
import logging
from BLL.machine import *
from Model.machine import *
from common import GetJwtPayload, set_security, create_parser
from fta_response import FtaResult

ns_station = Namespace('station', description='機台站別相關')

station_filter_model = ns_station.model('station_filter', {
    'station': fields.String(required=False, description='站別')
})

parser = create_parser(station_filter_model)


@ns_station.route('/')
class Machine(Resource):
    @ns_station.expect(parser)
    # @api.marshal_with(fta_response, as_list=True) #輸出自動轉model
    @ns_station.doc(description='取得站別機台資料',
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
            bll = MachineBll()
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