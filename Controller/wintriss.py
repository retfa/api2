# from enum import Enum
from flask import request, current_app
import flask_restx
# from flask_restx import Resource, Namespace, fields

import jwt
import time
from datetime import datetime
import logging
# from BLL.consumption import consumptionBll, consumptionReelBll
from BLL.wintriss import wintrissBll, wintrissRealtimeBll, wintrissReelBll, wintrissImageBll
from Kernel.JsonConverter import JsonConverter
from Kernel.RequestHandler import RequestHandler
from common import create_parser
from fta_response import FtaResult
from icecream import ic

ns_wintriss = flask_restx.Namespace('wintriss', description='wintriss 相關')

current_length_filter_model = ns_wintriss.model('current_length_filter_model', {
    'MachineName': flask_restx.fields.String(required=True, description='機台名稱', default='20'),

    'ExportFormat': flask_restx.fields.String(required=False, description='輸出類別// json(default), tablejson'),
})


current_length_filter_parser = create_parser(current_length_filter_model)



@ns_wintriss.route('/length_realtime')
class DefectCategory(flask_restx.Resource):
    @ns_wintriss.expect(current_length_filter_parser)
    # @ns_permission_cross_department.marshal_with(fta_response, as_list=True) #輸出自動轉model
    @ns_wintriss.doc(
        # params={'TagName': {'in': 'query', 'enum': TagNameList},
        #         },
        description='''
查詢機台瑕疵分類清單

輸出data.Content

    [
        {
            "length": int,
        }
    ]
        ''',
        responses={
            200: 'OK',
            400: 'Bad Request'
        }
    )
    def get(self):
        msg = f'{request.method} {request.url_rule.rule} {request.remote_addr}'
        try:
            data = RequestHandler.handle_get_request(self, current_app, msg, request, current_length_filter_parser)
        except jwt.ExpiredSignatureError:
            ic("JWT簽名已過期")
            return {'message': 'Authentication failed'}, 401
        except jwt.PyJWTError as e:
            ic(f"JWT異常: {e}")
            return {'message': 'Authentication failed'}, 401
        except Exception as e:
            msg = f'{self.__class__.__name__} |An error occurred: {str(e)}'
            ic(msg)
            logging.debug(msg)
            return {'message': msg}, 500

        data['current_login_id'] = data['jwt']["FTAId"]

        try:
            rst = None
            bll = wintrissBll()
            start_time = time.time()
            rst = bll.getLength(data)
            if data["ExportFormat"] == "tablejson":
                rst = JsonConverter.dict_array_to_table_json_dict(rst)
            end_time = time.time()
            execution_time = round((end_time - start_time) * 1000, 2)
            output = FtaResult(rst, execution_time, True).to_dict()
            # ic(output)
            return output, output['status_code']
        except Exception as e:
            msg = f'{self.__class__.__name__} |An error occurred: {str(e)}'
            ic(msg)
            logging.debug(msg)
            return {'message': msg}, 500
