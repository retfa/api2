# from enum import Enum
from flask import request, current_app
from flask_restx import Resource, Namespace, fields
import jwt
import time
import logging
from BLL.paperqualitystandardaims import PaperQualityStandardAimsBll
from Kernel.JsonConverter import JsonConverter
from Kernel.RequestHandler import RequestHandler
from common import create_parser
from fta_response import FtaResult
from icecream import ic

ns_paperqualitystandardaims = Namespace('paperqualitystandardaims', description='paperqualitystandardaims 相關')
LimitTypeList = ['HH', 'H', 'L', 'LL']
ModeList = ['Moving', 'Scheduler']
MethodList = ['Raw', 'Avg', 'Sum', 'Max', 'Min', 'Sd', 'Avg', '2Sigma']

paperqualitystandardaims_filter_model = ns_paperqualitystandardaims.model('paperqualitystandardaims_filter_model', {
    'MachineName': fields.String(required=True, description='機台名稱', default='21'),
    'TagName': fields.String(required=True, description='Tag名稱', default='P21-BW1-RL'),
    'PaperCode': fields.String(required=False, description='紙別代碼'),
    'BaseWeight': fields.Float(required=False, description='基重'),
    'TimeSpan': fields.Float(required=False, description='時長(秒)', default=1),
    'Method': fields.String(required=False, description='統計方式// Raw 原始值, Avg 平均值, Sum 累計值, Max 最大值, Min 最小值, Sd 標準差, 2Sigma 2σ值', default='Raw'),
    'Mode': fields.String(required=False, description='模式// Moving 最新區間, Scheduler 每排程', default='Moving'),
    'LimitType': fields.String(required=False, description='限別'),
    'ExportFormat': fields.String(required=False, description='輸出類別// json(default), tablejson'),
})

paperqualitystandardaims_filter_parser = create_parser(paperqualitystandardaims_filter_model)


@ns_paperqualitystandardaims.route('/')
class PaperQualityStandardAims(Resource):
    @ns_paperqualitystandardaims.expect(paperqualitystandardaims_filter_parser)
    # @ns_permission_cross_department.marshal_with(fta_response, as_list=True) #輸出自動轉model
    @ns_paperqualitystandardaims.doc(
        params={'LimitType': {'in': 'query', 'enum': LimitTypeList},
                'Mode': {'in': 'query', 'enum': ModeList},
                'Method': {'in': 'query', 'enum': MethodList}
                },
        description='''查詢 紙張品質標準 限值
        TagName以iolist name 為主
        19號紙機 CARL塗後厚度(um)
        20號紙機 BWRL, CoatingWeight塗佈量(GSM), ODRL_A塗後絕乾(GSM), ODSP_A塗前絕乾(GSM), PMRL_A塗後水分(%), PMRL捲取前(加濕後)水分(%), PMSP_A塗前水分(%)
        21號紙機 CoatingWeight塗佈量(GSM), P21-BW1-RL塗後基重(GSM), P21-BW1-SP塗前基重(GSM), P21-MO1-RL塗後水份(%), P21-MO1-SP塗前水份(%)
        C1塗佈機 CM8_MP1成品掃瞄架水份(%),CM8_MP2第一台掃描架塗後水份(%)
        ''',
        responses={
            200: 'OK',
            400: 'Bad Request'
        }
    )
    def get(self):
        msg = f'{request.method} {request.url_rule.rule} {request.remote_addr}'
        try:
            data = RequestHandler.handle_get_request(self, current_app, msg, request, paperqualitystandardaims_filter_parser)
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
            bll = PaperQualityStandardAimsBll()
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
