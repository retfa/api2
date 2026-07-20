# from enum import Enum
from flask import request, current_app
import flask_restx
# from flask_restx import Resource, Namespace, fields

import jwt
import time
from datetime import datetime
import logging
# from BLL.consumption import consumptionBll, consumptionReelBll
from BLL.skyeye import SkyeyeBll, SkyeyeCategoryBll, SkyeyeImageBll, SkyeyeImageRealtimeBll, SkyeyeJudgeBll, SkyeyeReelRealtimeBll, skyeyeRealtimeBll, SkyeyeReelBll
from BLL.wintriss import wintrissBll, wintrissRealtimeBll, wintrissReelBll, wintrissImageBll
from Kernel.JsonConverter import JsonConverter
from Kernel.RequestHandler import RequestHandler
from common import create_parser
from fta_response import FtaResult
from icecream import ic

ns_skyeye = flask_restx.Namespace('skyeye', description='skyeye 相關')

defect_category_filter_model = ns_skyeye.model('defect_category_filter_model', {
    'MachineName': flask_restx.fields.String(required=True, description='機台名稱', default='20'),

    'ExportFormat': flask_restx.fields.String(required=False, description='輸出類別// json(default), tablejson'),
})

defect_filter_model = ns_skyeye.model('defect_filter_model', {
    'MachineName': flask_restx.fields.String(required=True, description='機台名稱', default='20'),
    'ReelNo': flask_restx.fields.String(required=True, description='紙捲號碼', default='T4072801'),
    'SkyeyeCategoryCsv': flask_restx.fields.String(required=False, description='瑕疵類別Csv'),
    'CategoryCsv': flask_restx.fields.String(required=False, description='瑕疵類別Csv'),
    'ShowLarge': flask_restx.fields.Boolean(required=False, description='秀Wintriss大瑕疵'),
    'ShowMedium': flask_restx.fields.Boolean(required=False, description='秀Wintriss中瑕疵'),
    'ShowSmall': flask_restx.fields.Boolean(required=False, description='秀Wintriss小瑕疵'),

    'ExportFormat': flask_restx.fields.String(required=False, description='輸出類別// json(default), tablejson'),
})

defect_realtime_filter_model = ns_skyeye.model('defect_realtime_filter_model', {
    'MachineName': flask_restx.fields.String(required=True, description='機台名稱', default='20'),
    'CategoryCsv': flask_restx.fields.String(required=False, description='瑕疵類別Csv'),
    # 'OnlyLarge': flask_restx.fields.Boolean(required=False, description='不秀Wintriss中、小瑕疵'),
    'ShowLarge': flask_restx.fields.Boolean(required=False, description='秀Wintriss大瑕疵'),
    'ShowMedium': flask_restx.fields.Boolean(required=False, description='秀Wintriss中瑕疵'),
    'ShowSmall': flask_restx.fields.Boolean(required=False, description='秀Wintriss小瑕疵'),

    'ExportFormat': flask_restx.fields.String(required=False, description='輸出類別// json(default), tablejson'),
})

defect_reel_statistics_filter_model = ns_skyeye.model('defect_reel_statistics_filter_model', {
    'MachineName': flask_restx.fields.String(required=True, description='機台名稱', default='20'),
    'ReelNoCsv': flask_restx.fields.String(required=True, description='紙捲號碼Csv', default='T4072801,T4072802,T4072803'),
    'CategoryCsv': flask_restx.fields.String(required=False, description='瑕疵類別Csv'),

    'ExportFormat': flask_restx.fields.String(required=False, description='輸出類別// json(default), tablejson'),
})

defect_reel_statistics_realtime_filter_model = ns_skyeye.model('defect_reel_statistics_realtime_filter_model', {
    'MachineName': flask_restx.fields.String(required=True, description='機台名稱', default='20'),
    'CategoryCsv': flask_restx.fields.String(required=False, description='瑕疵類別Csv'),

    'ExportFormat': flask_restx.fields.String(required=False, description='輸出類別// json(default), tablejson'),
})

defect_image_filter_model = ns_skyeye.model('defect_image_filter_model', {
    'MachineName': flask_restx.fields.String(required=True, description='機台名稱'),
    'ReelNo': flask_restx.fields.String(required=True, description='紙捲號碼'),
    'CategoryCsv': flask_restx.fields.String(required=False, description='瑕疵類別Csv'),

    'ShowLarge': flask_restx.fields.Boolean(required=False, description='秀Wintriss大瑕疵'),
    'ShowMedium': flask_restx.fields.Boolean(required=False, description='秀Wintriss中瑕疵'),
    'ShowSmall': flask_restx.fields.Boolean(required=False, description='秀Wintriss小瑕疵'),

    'RangeXStart': flask_restx.fields.Float(required=False, description='X區間起'),
    'RangeXEnd': flask_restx.fields.Float(required=False, description='X區間迄'),
    'RangeYStart': flask_restx.fields.Float(required=False, description='Y區間起'),
    'RangeYEnd': flask_restx.fields.Float(required=False, description='Y區間迄'),

    'ExportFormat': flask_restx.fields.String(required=False, description='輸出類別// json(default), tablejson'),
})

defect_image_uuid_filter_model = ns_skyeye.model('defect_image_uuid_filter_model', {
    'MachineName': flask_restx.fields.String(required=True, description='機台名稱'),
    'ReelNo': flask_restx.fields.String(required=True, description='紙捲號碼'),
    'Uuid': flask_restx.fields.List(flask_restx.fields.String, required=True, description='Uuid array'),

    'ExportFormat': flask_restx.fields.String(required=False, description='輸出類別// json(default), tablejson'),
})

defect_image_realtime_filter_model = ns_skyeye.model('defect_image_realtime_filter_model', {
    'MachineName': flask_restx.fields.String(required=True, description='機台名稱'),
    'CategoryCsv': flask_restx.fields.String(required=False, description='瑕疵類別Csv'),

    'ShowLarge': flask_restx.fields.Boolean(required=False, description='秀Wintriss大瑕疵'),
    'ShowMedium': flask_restx.fields.Boolean(required=False, description='秀Wintriss中瑕疵'),
    'ShowSmall': flask_restx.fields.Boolean(required=False, description='秀Wintriss小瑕疵'),
    
    'RangeXStart': flask_restx.fields.Float(required=False, description='X區間起'),
    'RangeXEnd': flask_restx.fields.Float(required=False, description='X區間迄'),
    'RangeYStart': flask_restx.fields.Float(required=False, description='Y區間起'),
    'RangeYEnd': flask_restx.fields.Float(required=False, description='Y區間迄'),

    'ExportFormat': flask_restx.fields.String(required=False, description='輸出類別// json(default), tablejson'),
})

defect_judge_filter_model = ns_skyeye.model('defect_judge_filter_model', {
    'MachineName': flask_restx.fields.String(required=True, description='機台名稱'),
    'Image': flask_restx.fields.String(required=True, description='影像資料'),
    # 'Uuid': flask_restx.fields.String(required=True, description='判定圖片UUID'),
    # 'FileName': flask_restx.fields.String(required=True, description='判定圖片檔名'),
    # 'IsOk': flask_restx.fields.Boolean(required=False, description='判定結果正確'),
    # 'SkyeyeCategory': flask_restx.fields.String(required=True, description='判定瑕疵類別'),
    # 'SkyeyeDefectName': flask_restx.fields.String(required=True, description='判定瑕疵名稱'),
    # 'Comment': flask_restx.fields.String(required=False, description='判定瑕疵名稱'),
})

defect_category_filter_parser = create_parser(defect_category_filter_model)
defect_filter_parser = create_parser(defect_filter_model)
defect_realtime_filter_parser = create_parser(defect_realtime_filter_model)
defect_reel_statistics_filter_parser = create_parser(defect_reel_statistics_filter_model)
defect_reel_statistics_realtime_filter_parser = create_parser(defect_reel_statistics_realtime_filter_model)
defect_image_filter_parser = create_parser(defect_image_filter_model)
defect_image_uuid_filter_parser = create_parser(defect_image_uuid_filter_model)
defect_image_realtime_filter_parser = create_parser(defect_image_realtime_filter_model)
defect_judge_filter_parser = create_parser(defect_judge_filter_model)


@ns_skyeye.route('/defect')
class Defect(flask_restx.Resource):
    @ns_skyeye.expect(defect_filter_parser)
    # @ns_permission_cross_department.marshal_with(fta_response, as_list=True) #輸出自動轉model
    @ns_skyeye.doc(
        params={'ShowLarge': {'in': 'query', 'enum': ['true', 'false']},
                'ShowMedium': {'in': 'query', 'enum': ['true', 'false']},
                'ShowSmall': {'in': 'query', 'enum': ['true', 'false']},
                },
        description='''
查詢機台指定紙捲號碼的瑕疵

輸出data.Content

    [
        {
            "uuid":"",
            "jobKey":"",
            "flawId":"",
            "flawKey":"",
            "ftaDtm": "時間點",
            "skyeyeCategory":"skyeye瑕疵類別",
            "categoryName":"瑕疵名稱",
            "x":"x座標",
            "y":"y座標",
            "width":"寬(m)",
            "length":"長(m)",
            "area":"面積(m^2)",
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
            data = RequestHandler.handle_get_request(self, current_app, msg, request, defect_filter_parser)
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
        data['SkyeyeCategory'] = []
        if 'ReelNoCsv' in data and data['ReelNoCsv'] is not None:
            data['ReelNo'] = data['ReelNoCsv'].split(',')

        if 'SkyeyeCategoryCsv' in data and data['SkyeyeCategoryCsv'] is not None:
            data['SkyeyeCategory'] = data['SkyeyeCategoryCsv'].split(',')

        if 'CategoryCsv' in data and data['CategoryCsv'] is not None:
            data['Category'] = data['CategoryCsv'].split(',')
            for cat in data['Category']:
                if '_' in cat:  # 確保可以拆分
                    sub_category = cat.split('_')[0]
                    # 如果 sub_category 不在 data['SkyeyeCategory'] 中，才新增
                    if sub_category not in data['SkyeyeCategory']:
                        data['SkyeyeCategory'].append(sub_category)
        # # if 'SkyeyeCategoryCsv' in data and data['SkyeyeCategoryCsv'] is not None:
        # #     data['SkyeyeCategory'] = data['SkyeyeCategoryCsv'].split(',')
        # # if 'CategoryCsv' in data and data['CategoryCsv'] is not None:
        # #     data['Category'] = data['CategoryCsv'].split(',')
        # else:
        #     if 'DtFrom' in data and data['DtFrom'] is not None and 'DtTo' in data and data['DtTo'] is not None:
        #         pass
        #     elif 'Duration' in data and data['Duration'] is not None:
        #         current_time = time.time()
        #         data['DtTo'] = datetime.fromtimestamp(current_time).strftime('%Y-%m-%d %H:%M:00')
        #         data['DtFrom'] = datetime.fromtimestamp(current_time - data['Duration'] * 60).strftime('%Y-%m-%d %H:%M:00')

        try:
            rst = None
            bll = SkyeyeBll()
            start_time = time.time()
            rst = bll.ReadFromDb(data)

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


@ns_skyeye.route('/defect_realtime')
class DefectRealtime(flask_restx.Resource):
    @ns_skyeye.expect(defect_realtime_filter_parser)
    # @ns_permission_cross_department.marshal_with(fta_response, as_list=True) #輸出自動轉model
    @ns_skyeye.doc(
        params={'ShowLarge': {'in': 'query', 'enum': ['true', 'false']},
                'ShowMedium': {'in': 'query', 'enum': ['true', 'false']},
                'ShowSmall': {'in': 'query', 'enum': ['true', 'false']},
                },
        description='''
查詢機台即時的瑕疵

輸出data.Content

    [
        {
            "uuid":"",
            "jobKey":"",
            "flawId":"",
            "flawKey":"",
            "ftaDtm": "時間點",
            "skyeyeCategory":"skyeye瑕疵類別",
            "categoryName":"瑕疵名稱",
            "x":"x座標",
            "y":"y座標",
            "width":"寬(m)",
            "length":"長(m)",
            "area":"面積(m^2)",
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
            data = RequestHandler.handle_get_request(self, current_app, msg, request, defect_realtime_filter_parser)
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
        data['SkyeyeCategory'] = []
        if 'ReelNoCsv' in data and data['ReelNoCsv'] is not None:
            data['ReelNo'] = data['ReelNoCsv'].split(',')

        if 'SkyeyeCategoryCsv' in data and data['SkyeyeCategoryCsv'] is not None:
            data['SkyeyeCategory'] = data['SkyeyeCategoryCsv'].split(',')

        if 'CategoryCsv' in data and data['CategoryCsv'] is not None:
            data['Category'] = data['CategoryCsv'].split(',')
            for cat in data['Category']:
                if '_' in cat:  # 確保可以拆分
                    sub_category = cat.split('_')[0]
                    # 如果 sub_category 不在 data['SkyeyeCategory'] 中，才新增
                    if sub_category not in data['SkyeyeCategory']:
                        data['SkyeyeCategory'].append(sub_category)
        # else:
        #     if 'DtFrom' in data and data['DtFrom'] is not None and 'DtTo' in data and data['DtTo'] is not None:
        #         pass
        #     elif 'Duration' in data and data['Duration'] is not None:
        #         current_time = time.time()
        #         data['DtTo'] = datetime.fromtimestamp(current_time).strftime('%Y-%m-%d %H:%M:00')
        #         data['DtFrom'] = datetime.fromtimestamp(current_time - data['Duration'] * 60).strftime('%Y-%m-%d %H:%M:00')

        try:
            rst = None
            bll = skyeyeRealtimeBll()
            start_time = time.time()
            rst = bll.ReadFromDb(data)

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


@ns_skyeye.route('/defect/reel_statistics')
class DefectReelStatistics(flask_restx.Resource):
    @ns_skyeye.expect(defect_reel_statistics_filter_parser)
    # @ns_permission_cross_department.marshal_with(fta_response, as_list=True) #輸出自動轉model
    @ns_skyeye.doc(
        # params={'TagName': {'in': 'query', 'enum': TagNameList},
        #         },
        description='''
查詢機台指定紙捲號碼的瑕疵統計值

輸出data.Content

    [
        {
            "relno": "紙捲號碼",
            "污點":int,
            "破孔":int,
            ...
            ...
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
            data = RequestHandler.handle_get_request(self, current_app, msg, request, defect_reel_statistics_filter_parser)
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
        # if 'DtFrom' in data and data['DtFrom'] is not None and 'DtTo' in data and data['DtTo'] is not None:
        #     pass
        # elif 'Duration' in data and data['Duration'] is not None:
        #     current_time = time.time()
        #     data['DtTo'] = datetime.fromtimestamp(current_time).strftime('%Y-%m-%d %H:%M:00')
        #     data['DtFrom'] = datetime.fromtimestamp(current_time - data['Duration'] * 60).strftime('%Y-%m-%d %H:%M:00')

        if 'ReelNoCsv' in data and data['ReelNoCsv'] is not None:
            data['ReelNo'] = data['ReelNoCsv'].split(',')
        if 'CategoryCsv' in data and data['CategoryCsv'] is not None:
            data['Category'] = data['CategoryCsv'].split(',')

        try:
            rst = None
            bll = SkyeyeReelBll()
            start_time = time.time()
            rst = bll.ReadFromDb(data)

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


@ns_skyeye.route('/defect/reel_statistics_realtime')
class DefectReelStatisticsRealtime(flask_restx.Resource):
    @ns_skyeye.expect(defect_reel_statistics_realtime_filter_parser)
    # @ns_permission_cross_department.marshal_with(fta_response, as_list=True) #輸出自動轉model
    @ns_skyeye.doc(
        # params={'TagName': {'in': 'query', 'enum': TagNameList},
        #         },
        description='''
查詢機台指定紙捲號碼的瑕疵統計值

輸出data.Content

    [
        {
            "relno": "紙捲號碼",
            "污點":int,
            "破孔":int,
            ...
            ...
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
            data = RequestHandler.handle_get_request(self, current_app, msg, request, defect_reel_statistics_realtime_filter_parser)
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
        if 'CategoryCsv' in data and data['CategoryCsv'] is not None:
            data['Category'] = data['CategoryCsv'].split(',')

        try:
            rst = None
            bll = SkyeyeReelRealtimeBll()
            start_time = time.time()
            rst = bll.ReadFromDb(data)

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


@ns_skyeye.route('/defect/image')
class DefectImage(flask_restx.Resource):
    @ns_skyeye.expect(defect_image_filter_parser)
    # @ns_permission_cross_department.marshal_with(fta_response, as_list=True) #輸出自動轉model
    @ns_skyeye.doc(
        params={'ShowLarge': {'in': 'query', 'enum': ['true', 'false']},
                'ShowMedium': {'in': 'query', 'enum': ['true', 'false']},
                'ShowSmall': {'in': 'query', 'enum': ['true', 'false']},
                },
        description='''
查詢瑕疵影像檔及識別資訊

輸出data.Content

    [
        {
            "ftaDtm": "時間點",
            "fileName": "檔名"
            "jobKey":"",
            "flawId":,
            "flawKey":,
            "x":"x座標",
            "y":"y座標",
            "width":"寬(m)",
            "length":"長(m)",
            "area":"面積(m^2)",
            "rect":{
                "wintrissDefectName": "Wintriss瑕疵名稱",
                "categoryName": "瑕疵名稱",
                "topLeftX":"左上點X座標",
                "topLeftY":"左上點Y座標",
                "bottomRightX":"右下點X座標",
                "bottomRightY":"右下點Y座標",
            }
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
            data = RequestHandler.handle_get_request(self, current_app, msg, request, defect_image_filter_parser)
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
        data['SkyeyeCategory'] = []

        if 'ReelNoCsv' in data and data['ReelNoCsv'] is not None:
            data['ReelNo'] = data['ReelNoCsv'].split(',')

        if 'SkyeyeCategoryCsv' in data and data['SkyeyeCategoryCsv'] is not None:
            data['SkyeyeCategory'] = data['SkyeyeCategoryCsv'].split(',')

        if 'CategoryCsv' in data and data['CategoryCsv'] is not None:
            data['Category'] = data['CategoryCsv'].split(',')
            for cat in data['Category']:
                if '_' in cat:  # 確保可以拆分
                    sub_category = cat.split('_')[0]
                    # 如果 sub_category 不在 data['SkyeyeCategory'] 中，才新增
                    if sub_category not in data['SkyeyeCategory']:
                        data['SkyeyeCategory'].append(sub_category)

        try:
            rst = None
            bll = SkyeyeImageBll()
            start_time = time.time()
            rst = bll.ReadFromDb(data)
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

@ns_skyeye.route('/defect/image/uuid')
class DefectImageUuid(flask_restx.Resource):
    @ns_skyeye.doc(
        params={
            'MachineName': {
                'description': '機台名稱',
                'in': 'query',
                'type': 'string',
                'required': True
            },
            'ReelNo': {
                'description': '紙捲號碼',
                'in': 'query',
                'type': 'string',
                'required': True
            },
            'Uuid': {
                'description': 'UUID 陣列，可多次指定 ?Uuid=abc&Uuid=def',
                'in': 'query',
                'type': 'array',
                'items': {'type': 'string'},
                'collectionFormat': 'multi',
                'required': True
            },
            'ExportFormat': {
                'description': '輸出格式（json｜tablejson）',
                'in': 'query',
                'type': 'string',
                'enum': ['json', 'tablejson'],
                'required': False
            }
        },
        description='''
查詢瑕疵影像檔及識別資訊

輸出data.Content

    [
        {
            "ftaDtm": "時間點",
            "fileName": "檔名"
            "jobKey":"",
            "flawId":,
            "flawKey":,
            "x":"x座標",
            "y":"y座標",
            "width":"寬(m)",
            "length":"長(m)",
            "area":"面積(m^2)",
            "rect":{
                "wintrissDefectName": "Wintriss瑕疵名稱",
                "categoryName": "瑕疵名稱",
                "topLeftX":"左上點X座標",
                "topLeftY":"左上點Y座標",
                "bottomRightX":"右下點X座標",
                "bottomRightY":"右下點Y座標",
            }
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
            data = RequestHandler.handle_get_request(self, current_app, msg, request, defect_image_uuid_filter_parser)
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
        # data['SkyeyeCategory'] = []

        # if 'ReelNoCsv' in data and data['ReelNoCsv'] is not None:
        #     data['ReelNo'] = data['ReelNoCsv'].split(',')

        # if 'SkyeyeCategoryCsv' in data and data['SkyeyeCategoryCsv'] is not None:
        #     data['SkyeyeCategory'] = data['SkyeyeCategoryCsv'].split(',')

        # if 'CategoryCsv' in data and data['CategoryCsv'] is not None:
        #     data['Category'] = data['CategoryCsv'].split(',')
        #     for cat in data['Category']:
        #         if '_' in cat:  # 確保可以拆分
        #             sub_category = cat.split('_')[0]
        #             # 如果 sub_category 不在 data['SkyeyeCategory'] 中，才新增
        #             if sub_category not in data['SkyeyeCategory']:
        #                 data['SkyeyeCategory'].append(sub_category)

        try:
            rst = None
            bll = SkyeyeImageBll()
            start_time = time.time()
            rst = bll.ReadFromDbUuid(data)
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

@ns_skyeye.route('/defect/image_realtime')
class DefectImageRealtime(flask_restx.Resource):
    @ns_skyeye.expect(defect_image_realtime_filter_parser)
    # @ns_permission_cross_department.marshal_with(fta_response, as_list=True) #輸出自動轉model
    @ns_skyeye.doc(
        params={'ShowLarge': {'in': 'query', 'enum': ['true', 'false']},
                'ShowMedium': {'in': 'query', 'enum': ['true', 'false']},
                'ShowSmall': {'in': 'query', 'enum': ['true', 'false']},
                },
        description='''
查詢瑕疵影像檔及識別資訊

輸出data.Content

    [
        {
            "ftaDtm": "時間點",
            "fileName": "檔名"
            "jobKey":"",
            "flawId":,
            "flawKey":,
            "x":"x座標",
            "y":"y座標",
            "width":"寬(m)",
            "length":"長(m)",
            "area":"面積(m^2)",
            "rect":{
                "wintrissDefectName": "Wintriss瑕疵名稱",
                "categoryName": "瑕疵名稱",
                "topLeftX":"左上點X座標",
                "topLeftY":"左上點Y座標",
                "bottomRightX":"右下點X座標",
                "bottomRightY":"右下點Y座標",
            }
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
            data = RequestHandler.handle_get_request(self, current_app, msg, request, defect_image_realtime_filter_parser)
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
        data['SkyeyeCategory'] = []

        if 'ReelNoCsv' in data and data['ReelNoCsv'] is not None:
            data['ReelNo'] = data['ReelNoCsv'].split(',')

        if 'SkyeyeCategoryCsv' in data and data['SkyeyeCategoryCsv'] is not None:
            data['SkyeyeCategory'] = data['SkyeyeCategoryCsv'].split(',')

        if 'CategoryCsv' in data and data['CategoryCsv'] is not None:
            data['Category'] = data['CategoryCsv'].split(',')
            for cat in data['Category']:
                if '_' in cat:  # 確保可以拆分
                    sub_category = cat.split('_')[0]
                    # 如果 sub_category 不在 data['SkyeyeCategory'] 中，才新增
                    if sub_category not in data['SkyeyeCategory']:
                        data['SkyeyeCategory'].append(sub_category)

        try:
            rst = None
            bll = SkyeyeImageRealtimeBll()
            start_time = time.time()
            rst = bll.ReadFromDb(data)
            # statistics = {}
            # statistics['一般汙點'] = sum(1 for obj in rst for rect in obj['rect'] if rect['defectName'] == '一般汙點')
            # statistics['烘缸塗料屑'] = sum(1 for obj in rst for rect in obj['rect'] if rect['defectName'] == '烘缸塗料屑')
            if data["ExportFormat"] == "tablejson":
                rst = JsonConverter.dict_array_to_table_json_dict(rst)
            # rest = {}
            # rest['data'] = rst
            # rest['statistics'] = statistics
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


@ns_skyeye.route('/defect/category')
class DefectCategory(flask_restx.Resource):
    @ns_skyeye.expect(defect_category_filter_parser)
    # @ns_permission_cross_department.marshal_with(fta_response, as_list=True) #輸出自動轉model
    @ns_skyeye.doc(
        # params={'TagName': {'in': 'query', 'enum': TagNameList},
        #         },
        description='''
查詢機台瑕疵分類清單

輸出data.Content

    [
        {
            "primaryCategory": "瑕疵主類",
            "defectName": "瑕疵名稱",
            "order":"排列順序",
            "isEnabled":"是否預設",
            "symbol":"圖形", //circle, rect, roundRect, triangle, diamond, pin, arrow, none
            "color":"顏色", //#RRGGBBAA, #RRGGBB, colorname
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
            data = RequestHandler.handle_get_request(self, current_app, msg, request, defect_category_filter_parser)
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
            bll = SkyeyeCategoryBll()
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


@ns_skyeye.route('/defect/judge')
class DefectJudge(flask_restx.Resource):
    @ns_skyeye.expect(defect_judge_filter_parser)
    # @ns_permission_cross_department.marshal_with(fta_response, as_list=True) #輸出自動轉model
    @ns_skyeye.doc(
        # params={'TagName': {'in': 'query', 'enum': TagNameList},
        #         },
        description='''
判定圖片結果
        ''',
        responses={
            200: 'OK',
            400: 'Bad Request'
        }
    )
    def post(self):
        msg = f'{request.method} {request.url_rule.rule} {request.remote_addr}'
        try:
            data = RequestHandler.handle_get_request(self, current_app, msg, request, defect_judge_filter_parser)
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
            bll = SkyeyeJudgeBll()
            start_time = time.time()
            rst = bll.add(data)
            # if data["ExportFormat"] == "tablejson":
            #     rst = JsonConverter.dict_array_to_table_json_dict(rst)
            end_time = time.time()
            execution_time = round((end_time - start_time) * 1000, 2)
            if isinstance(rst, tuple):
                ic(rst[1])
                output = FtaResult(rst[0], execution_time, False, rst[1]).to_dict()
            else:
                output = FtaResult(rst, execution_time, True).to_dict()
            return output, output['status_code']
        except Exception as e:
            msg = f'{self.__class__.__name__} |An error occurred: {str(e)}'
            ic(msg)
            logging.debug(msg)
            return {'message': msg}, 500


@ns_skyeye.route('/rulealarm')
class RuleAlarm(flask_restx.Resource):
    @ns_skyeye.expect(defect_category_filter_parser)
    # @ns_permission_cross_department.marshal_with(fta_response, as_list=True) #輸出自動轉model
    @ns_skyeye.doc(
        # params={'TagName': {'in': 'query', 'enum': TagNameList},
        #         },
        description='''
查詢機台瑕疵分類清單

輸出data.Content

    [
        {
            "primaryCategory": "瑕疵主類",
            "defectName": "瑕疵名稱",
            "order":"排列順序",
            "isEnabled":"是否預設",
            "symbol":"圖形", //circle, rect, roundRect, triangle, diamond, pin, arrow, none
            "color":"顏色", //#RRGGBBAA, #RRGGBB, colorname
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
            data = RequestHandler.handle_get_request(self, current_app, msg, request, defect_category_filter_parser)
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
            bll = SkyeyeCategoryBll()
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
