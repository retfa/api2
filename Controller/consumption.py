# from enum import Enum
from flask import request, current_app
import flask_restx
# from flask_restx import Resource, Namespace, fields

import jwt
import time
from datetime import datetime
import logging
# from BLL.consumption import consumptionBll
from BLL.consumption import consumptionBll, consumptionReelBll
from Kernel.JsonConverter import JsonConverter
from Kernel.RequestHandler import RequestHandler
from common import create_parser
from fta_response import FtaResult
from icecream import ic

ns_consumption = flask_restx.Namespace('consumption', description='consumption 相關')
TagNameList = ['steam', 'power']
# TagNameList = ['', 'steam', 'electricity']

consumption_filter_model = ns_consumption.model('consumption_filter_model', {
    'MachineName': flask_restx.fields.String(required=True, description='機台名稱', default='21'),
    'TagName': flask_restx.fields.String(required=True, description='Tag名稱// steam蒸氣, power電力'),
    'DtFrom': flask_restx.fields.String(required=False, description='查詢起時'),
    'DtTo': flask_restx.fields.String(required=False, description='查詢迄時'),
    'Duration': flask_restx.fields.Integer(required=False, description='時長(分鐘)// 無DtFrom及DtTo時，以本值查最後區間，有DtFrom及DtTo時，本值無效', default=1440),

    'ReelNoCsv': flask_restx.fields.String(required=False, description='紙捲號碼CSV'),
    'PaperCode': flask_restx.fields.String(required=False, description='紙別代碼'),
    'BaseWeight': flask_restx.fields.Float(required=False, description='基重'),

    'ExportFormat': flask_restx.fields.String(required=False, description='輸出類別// json(default), tablejson'),
})

consumption_reel_filter_model = ns_consumption.model('consumption_reel_filter_model', {
    'MachineName': flask_restx.fields.String(required=True, description='機台名稱', default='21'),
    'TagName': flask_restx.fields.String(required=False, description='Tag名稱// steam蒸氣, power電力'),
    'ReelNoCsv': flask_restx.fields.String(required=True, description='紙捲號碼CSV'),

    'ExportFormat': flask_restx.fields.String(required=False, description='輸出類別// json(default), tablejson'),
})

consumption_filter_parser = create_parser(consumption_filter_model)
consumption_reel_filter_parser = create_parser(consumption_reel_filter_model)


@ns_consumption.route('/')
class consumption(flask_restx.Resource):
    @ns_consumption.expect(consumption_filter_parser)
    # @ns_permission_cross_department.marshal_with(fta_response, as_list=True) #輸出自動轉model
    @ns_consumption.doc(
        params={'TagName': {'in': 'query', 'enum': TagNameList},
                },
        description='''
查詢 即時單位資源消耗量

輸出data.Content

    [
        {
            "fta_dtm": "時間點",
            "value": 資源耗用量(Unit/ton),
            "relno": "紙捲號碼",
            "ptype": "紙別",
            "gramg": "基重",
            "category": "資源類別"
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
            data = RequestHandler.handle_get_request(self, current_app, msg, request, consumption_filter_parser)
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

        if 'ReelNoCsv' in data and data['ReelNoCsv'] is not None:
            data['ReelNo'] = data['ReelNoCsv'].split(',')
        else:
            if 'DtFrom' in data and data['DtFrom'] is not None and 'DtTo' in data and data['DtTo'] is not None:
                pass
            elif 'Duration' in data and data['Duration'] is not None:
                current_time = time.time()
                data['DtTo'] = datetime.fromtimestamp(current_time).strftime('%Y-%m-%d %H:%M:00')
                data['DtFrom'] = datetime.fromtimestamp(current_time - data['Duration'] * 60).strftime('%Y-%m-%d %H:%M:00')

        try:
            rst = None
            bll = consumptionBll()
            start_time = time.time()
            rst = bll.browse(data)

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


@ns_consumption.route('/reel')
class consumptionReel(flask_restx.Resource):
    @ns_consumption.expect(consumption_reel_filter_parser)
    # @ns_permission_cross_department.marshal_with(fta_response, as_list=True) #輸出自動轉model
    @ns_consumption.doc(
        params={'TagName': {'in': 'query', 'enum': TagNameList},
                },
        description='''
查詢 每紙捲資源消耗量

輸出data.Content

    [
        {
            "relno": "紙捲號碼",
            "ptype": "紙別",
            "gramg": "基重",
            "per_reel": "整捲資源耗用量(kwh/ton)",
            "per_ton": "噸紙資源耗用量(ton/ton)",
            "category": "資源類別"
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
            data = RequestHandler.handle_get_request(self, current_app, msg, request, consumption_reel_filter_parser)
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

        # data['current_login_id'] = data['jwt']["FTAId"]
        # if 'DtFrom' in data and data['DtFrom'] is not None and 'DtTo' in data and data['DtTo'] is not None:
        #     pass
        # elif 'Duration' in data and data['Duration'] is not None:
        #     current_time = time.time()
        #     data['DtTo'] = datetime.fromtimestamp(current_time).strftime('%Y-%m-%d %H:%M:00')
        #     data['DtFrom'] = datetime.fromtimestamp(current_time - data['Duration'] * 60).strftime('%Y-%m-%d %H:%M:00')

        if 'ReelNoCsv' in data and data['ReelNoCsv'] is not None:
            data['ReelNo'] = data['ReelNoCsv'].split(',')

        try:
            rst = None
            bll = consumptionReelBll()
            start_time = time.time()
            rst = bll.browse(data)

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
