# from enum import Enum
from flask import request, current_app
from flask_restx import Resource, Namespace, fields
import jwt
import time
import logging
from BLL.aug import AugBll
from Kernel.JsonConverter import JsonConverter
from Kernel.RequestHandler import RequestHandler
from common import create_parser
from fta_response import FtaResult
from icecream import ic

ns_aug = Namespace('aug', description='aug 訊號數值相關')
MachineNameList = ['19', '20', '21', 'C1']
IntervalUnitList = ['DAY', 'HOUR', 'MINUTE']

aug_group_interval_filter_model = ns_aug.model('aug_group_interval_filter_model', {
    'MachineName': fields.String(required=True, description='機台名稱', default='20'),
    'TagName': fields.String(required=True, description='Tag名稱', default='PMSP_A'),
    'DtFrom': fields.String(required=False, description='查詢起時', default='2024-08-20 00:00:00'),
    'DtTo': fields.String(required=False, description='查詢迄時', default='2024-09-01 00:00:00'),
    'IntervalValue': fields.String(required=False, description='取樣間隔', default='1', example='1'),
    'IntervalUnit': fields.String(required=False, description='取樣間隔單位 DAY, HOUR, MINUTE', default='HOUR', example='HOUR'),
    'ReelNoCsv': fields.String(required=False, description='紙捲號碼CSV', default='T4090909', example='W4050505')
})

aug_group_raw_filter_model = ns_aug.model('aug_group_raw_filter_model', {
    'MachineName': fields.String(required=True, description='機台名稱', default='21'),
    'TagName': fields.String(required=True, description='Tag名稱', default='P21-BW1-RL'),
    'DtFrom': fields.String(required=False, description='查詢起時'),
    'DtTo': fields.String(required=False, description='查詢迄時'),
    'ReelNoCsv': fields.String(required=True, description='紙捲號碼CSV', default='W4050505', example='W4050505'),
    'PaperCode': fields.String(required=False, description='紙別代碼'),
    'BaseWeight': fields.String(required=False, description='基重')
})

aug_group_reel_avg_filter_model = ns_aug.model('aug_group_reel_avg_filter_model', {
    'MachineName': fields.String(required=True, description='機台名稱', default='21'),
    'TagName': fields.String(required=False, description='Tag名稱'),
    'ReelNoCsv': fields.String(required=True, description='紙捲號碼CSV', default='W4050505', example='W4050505'),
    'PaperCode': fields.String(required=False, description='紙別代碼'),
    'BaseWeight': fields.String(required=False, description='基重'),
    # 'Category': fields.String(required=False, description='訊號類別'),
    # 'STime': fields.String(required=False, description='紙捲生產起時'),
    # 'ETime': fields.String(required=False, description='紙捲生產迄時'),
})

aug_tag_raw_filter_model = ns_aug.model('aug_tag_raw_filter_model', {
    'MachineName': fields.String(required=True, description='機台名稱', default='21'),
    'TagName': fields.String(required=True, description='Tag名稱', default='P21-BW1-RL'),
    'DtFrom': fields.String(required=False, description='查詢起時'),
    'DtTo': fields.String(required=False, description='查詢迄時'),
    'ReelNoCsv': fields.String(required=True, description='紙捲號碼CSV', default='W4050505', example='W4050505'),
    'PaperCode': fields.String(required=False, description='紙別代碼'),
    'BaseWeight': fields.String(required=False, description='基重')
})

parser_group_interval = create_parser(aug_group_interval_filter_model)
parser_group_raw = create_parser(aug_group_raw_filter_model)
parser_group_reel_avg = create_parser(aug_group_reel_avg_filter_model)
parser_tag_raw = create_parser(aug_tag_raw_filter_model)


@ns_aug.route('/group/interval/')
class GroupInterval(Resource):
    @ns_aug.expect(parser_group_interval)
    # @ns_permission_cross_department.marshal_with(fta_response, as_list=True) #輸出自動轉model
    @ns_aug.doc(
        params={'MachineName': {'in': 'query', 'enum': MachineNameList},
                'IntervalUnit': {'in': 'query', 'enum': IntervalUnitList}},
        description='''
查詢 AUG tag_name 的群組原始值 特定時間區間取樣
TagName以iolist name 為主
19號紙機 CARL塗後厚度(um)
20號紙機 BWRL, CoatingWeight塗佈量(GSM), ODRL_A塗後絕乾(GSM), ODSP_A塗前絕乾(GSM), PMRL_A塗後水分(%), PMRL捲取前(加濕後)水分(%), PMSP_A塗前水分(%)
21號紙機 CoatingWeight塗佈量(GSM), P21-BW1-RL塗後基重(GSM), P21-BW1-SP塗前基重(GSM), P21-MO1-RL塗後水份(%), P21-MO1-SP塗前水份(%)
C1塗佈機 CM8_MP1成品掃瞄架水份(%),CM8_MP2第一台掃描架塗後水份(%)

取樣間隔單位 DAY, HOUR, MINUTE
輸出data.Content

    {
        "schema": {
            "fields": [
            {
                "name": "fta_dtm",
                "type": "string"
            },
            {
                "name": "relno",
                "type": "string"
            },
            {
                "name": "ptype",
                "type": "string"
            },
            {
                "name": "gramg",
                "type": "number"
            },
            {
                "name": "G01",
                "type": "number"
            },
            {
                "name": "G02",
                "type": "number"
            },
            ...
            ...
            {
                "name": "G73",
                "type": "number"
            }
            ]
        },
        "data": []
    }
        ''',
        responses={
            200: 'OK',
            400: 'Bad Request'
        }
    )
    def get(self):
        msg = f'{request.method} {request.url_rule.rule} {request.remote_addr}'
        try:
            data = RequestHandler.handle_get_request(self, current_app, msg, request, parser_group_interval)
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

        data['user_id'] = data['jwt']["FTAId"] if data.get('jwt') and data['jwt'].get("FTAId") else ""
        data['ReelNo'] = data['ReelNoCsv'].split(',')

        try:
            # productionbll = ProductionInfoBll()
            bll = AugBll()
            start_time = time.time()
            rst = bll.browse_group_interval(data)
            # custom_field_types = {
            #     "fta_dtm": "DATE",
            #     "relno": "string",
            #     "ptype": "string"
            # }
            rstt = JsonConverter.dict_array_to_table_json_dict(rst)
            end_time = time.time()
            execution_time = round((end_time - start_time) * 1000, 2)
            output = FtaResult(rstt, execution_time, True).to_dict()
            # ic(output)
            return output, output['status_code']
        except Exception as e:
            msg = f'{self.__class__.__name__} |An error occurred: {str(e)}'
            ic(msg)
            logging.debug(msg)

            return {'message': msg}, 500


@ns_aug.route('/group/raw/')
class Group(Resource):
    @ns_aug.expect(parser_group_raw)
    # @ns_permission_cross_department.marshal_with(fta_response, as_list=True) #輸出自動轉model
    @ns_aug.doc(
        params={'MachineName': {'in': 'query', 'enum': MachineNameList}},
        description='''
查詢 AUG tag_name 的群組原始值
TagName以iolist name 為主
19號紙機 CARL塗後厚度(um)
20號紙機 BWRL, CoatingWeight塗佈量(GSM), ODRL_A塗後絕乾(GSM), ODSP_A塗前絕乾(GSM), PMRL_A塗後水分(%), PMRL捲取前(加濕後)水分(%), PMSP_A塗前水分(%)
21號紙機 CoatingWeight塗佈量(GSM), P21-BW1-RL塗後基重(GSM), P21-BW1-SP塗前基重(GSM), P21-MO1-RL塗後水份(%), P21-MO1-SP塗前水份(%)
C1塗佈機 CM8_MP1成品掃瞄架水份(%),CM8_MP2第一台掃描架塗後水份(%)

輸出data.Content

    {
        "schema": {
            "fields": [
            {
                "name": "fta_dtm",
                "type": "string"
            },
            {
                "name": "relno",
                "type": "string"
            },
            {
                "name": "ptype",
                "type": "string"
            },
            {
                "name": "gramg",
                "type": "number"
            },
            {
                "name": "G01",
                "type": "number"
            },
            {
                "name": "G02",
                "type": "number"
            },
            ...
            ...
            {
                "name": "G73",
                "type": "number"
            }
            ]
        },
        "data": []
    }
        ''',
        responses={
            200: 'OK',
            400: 'Bad Request'
        }
    )
    def get(self):
        msg = f'{request.method} {request.url_rule.rule} {request.remote_addr}'
        try:
            data = RequestHandler.handle_get_request(self, current_app, msg, request, parser_group_raw)
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

        data['user_id'] = data['jwt']["FTAId"] if data.get('jwt') and data['jwt'].get("FTAId") else ""
        data['ReelNo'] = data['ReelNoCsv'].split(',')

        try:
            bll = AugBll()
            start_time = time.time()
            rst = bll.browse(data)
            # custom_field_types = {
            #     "fta_dtm": "DATE",
            #     "relno": "string",
            #     "ptype": "string"
            # }
            rstt = JsonConverter.dict_array_to_table_json_dict(rst)
            end_time = time.time()
            execution_time = round((end_time - start_time) * 1000, 2)
            output = FtaResult(rstt, execution_time, True).to_dict()
            # ic(output)
            return output, output['status_code']
        except Exception as e:
            msg = f'{self.__class__.__name__} |An error occurred: {str(e)}'
            ic(msg)
            logging.debug(msg)

            return {'message': msg}, 500


@ns_aug.route('/group/reel_avg')
class GroupAvg(Resource):
    @ns_aug.expect(parser_group_reel_avg)
    # @ns_permission_cross_department.marshal_with(fta_response, as_list=True) #輸出自動轉model
    @ns_aug.doc(
        params={'MachineName': {'in': 'query', 'enum': MachineNameList}},
        description='''
查詢 AUG tag_name 的群組平均值
TagName以iolist name 為主
19號紙機 CARL塗後厚度(um)
20號紙機 BWRL, CoatingWeight塗佈量(GSM), ODRL_A塗後絕乾(GSM), ODSP_A塗前絕乾(GSM), PMRL_A塗後水分(%), PMRL捲取前(加濕後)水分(%), PMSP_A塗前水分(%)
21號紙機 CoatingWeight塗佈量(GSM), P21-BW1-RL塗後基重(GSM), P21-BW1-SP塗前基重(GSM), P21-MO1-RL塗後水份(%), P21-MO1-SP塗前水份(%)
C1塗佈機 CM8_MP1成品掃瞄架水份(%),CM8_MP2第一台掃描架塗後水份(%)

輸出data.Content

    [
        {
            "relno": "紙捲號碼",
            "ptype": "紙別",
            "gramg": "基重",
            "stime": "起時",
            "etime": "迄時",
            "G01": "時間點",
            "G02": "時間點",
            ...
            ...

            "Category": "TagName"
        }
    ]

*註：群組數量超過3位數者，G01->G001*
        ''',
        responses={
            200: 'OK',
            400: 'Bad Request'
        }
    )
    def get(self):
        msg = f'{request.method} {request.url_rule.rule} {request.remote_addr}'
        try:
            data = RequestHandler.handle_get_request(self, current_app, msg, request, parser_group_reel_avg)
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

        data['user_id'] = data['jwt']["FTAId"] if data.get('jwt') and data['jwt'].get("FTAId") else ""
        data['ReelNo'] = data['ReelNoCsv'].split(',')

        try:
            bll = AugBll()
            start_time = time.time()
            rst = bll.browse_reel(data)
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


@ns_aug.route('/tag/raw/')
class Tag(Resource):
    @ns_aug.expect(parser_tag_raw)
    # @ns_permission_cross_department.marshal_with(fta_response, as_list=True) #輸出自動轉model
    @ns_aug.doc(
        params={'MachineName': {'in': 'query', 'enum': MachineNameList}},
        description='''
查詢 AUG tag_name 的TAG原始值
TagName以iolist name 為主
19號紙機 CARL塗後厚度(um)
20號紙機 BWRL, CoatingWeight塗佈量(GSM), ODRL_A塗後絕乾(GSM), ODSP_A塗前絕乾(GSM), PMRL_A塗後水分(%), PMRL捲取前(加濕後)水分(%), PMSP_A塗前水分(%)
21號紙機 CoatingWeight塗佈量(GSM), P21-BW1-RL塗後基重(GSM), P21-BW1-SP塗前基重(GSM), P21-MO1-RL塗後水份(%), P21-MO1-SP塗前水份(%)
C1塗佈機 CM8_MP1成品掃瞄架水份(%),CM8_MP2第一台掃描架塗後水份(%)

輸出data.Content

    {
        "schema": {
            "fields": [
            {
                "name": "fta_dtm",
                "type": "string"
            },
            {
                "name": "relno",
                "type": "string"
            },
            {
                "name": "ptype",
                "type": "string"
            },
            {
                "name": "gramg",
                "type": "number"
            },
            {
                "name": "Tag001",
                "type": "number"
            },
            {
                "name": "Tag002",
                "type": "number"
            },
            ...
            ...
            {
                "name": "Tag512",
                "type": "number"
            }
            ]
        },
        "data": []
    }
        ''',
        responses={
            200: 'OK',
            400: 'Bad Request'
        }
    )
    def get(self):
        msg = f'{request.method} {request.url_rule.rule} {request.remote_addr}'
        try:
            data = RequestHandler.handle_get_request(self, current_app, msg, request, parser_group_raw)
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

        data['user_id'] = data['jwt']["FTAId"] if data.get('jwt') and data['jwt'].get("FTAId") else ""
        data['ReelNo'] = data['ReelNoCsv'].split(',')

        try:
            bll = AugBll()
            start_time = time.time()
            rst = bll.browseTag(data)
            # custom_field_types = {
            #     "fta_dtm": "DATE",
            #     "relno": "string",
            #     "ptype": "string"
            # }
            rstt = JsonConverter.dict_array_to_table_json_dict(rst)
            end_time = time.time()
            execution_time = round((end_time - start_time) * 1000, 2)
            output = FtaResult(rstt, execution_time, True).to_dict()
            # ic(output)
            return output, output['status_code']
        except Exception as e:
            msg = f'{self.__class__.__name__} |An error occurred: {str(e)}'
            ic(msg)
            logging.debug(msg)

            return {'message': msg}, 500


@ns_aug.route('/tag/exceed-limit/reel-statistics')
class Tag(Resource):
    @ns_aug.expect(parser_tag_raw)
    # @ns_permission_cross_department.marshal_with(fta_response, as_list=True) #輸出自動轉model
    @ns_aug.doc(
        params={'MachineName': {'in': 'query', 'enum': MachineNameList}},
        description='''
查詢 AUG tag 超標統計


輸出data.Content

    {
        "schema": {
            "fields": [
            {
                "name": "fta_dtm",
                "type": "string"
            },
            {
                "name": "relno",
                "type": "string"
            },
            {
                "name": "ptype",
                "type": "string"
            },
            {
                "name": "gramg",
                "type": "number"
            },
            {
                "name": "Tag001",
                "type": "number"
            },
            {
                "name": "Tag002",
                "type": "number"
            },
            ...
            ...
            {
                "name": "Tag512",
                "type": "number"
            }
            ]
        },
        "data": []
    }
        ''',
        responses={
            200: 'OK',
            400: 'Bad Request'
        }
    )
    def get(self):
        msg = f'{request.method} {request.url_rule.rule} {request.remote_addr}'
        try:
            data = RequestHandler.handle_get_request(self, current_app, msg, request, parser_group_raw)
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

        data['user_id'] = data['jwt']["FTAId"] if data.get('jwt') and data['jwt'].get("FTAId") else ""
        data['ReelNo'] = data['ReelNoCsv'].split(',')

        try:
            bll = AugBll()
            start_time = time.time()
            rst = bll.browseTag(data)
            # custom_field_types = {
            #     "fta_dtm": "DATE",
            #     "relno": "string",
            #     "ptype": "string"
            # }
            rstt = JsonConverter.dict_array_to_table_json_dict(rst)
            end_time = time.time()
            execution_time = round((end_time - start_time) * 1000, 2)
            output = FtaResult(rstt, execution_time, True).to_dict()
            # ic(output)
            return output, output['status_code']
        except Exception as e:
            msg = f'{self.__class__.__name__} |An error occurred: {str(e)}'
            ic(msg)
            logging.debug(msg)

            return {'message': msg}, 500
