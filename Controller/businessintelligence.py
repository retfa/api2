import json
import os
from flask import request, current_app
from flask_restx import Resource, Namespace
import jwt
import time
import logging
from BLL.bussinessintelligence import BussinessIntelligenceBll
from Model.businessintelligence import *
from common import GetJwtPayload, set_security, create_parser
from fta_response import FtaResult

ns_businessintelligence = Namespace(
    'businessintelligence', description='BusinessIntelligence 相關')

bussinessintelligence_filter_model = ns_businessintelligence.model(
    'BusinessIntelligenceDto.user_filter', bussinessintelligence_query_filter_dto)

bussinessintelligence_filter_monthly_model = ns_businessintelligence.model(
    'BusinessIntelligenceDto.user_filter_monthly', bussinessintelligence_query_filter_monthly_dto)

bussinessintelligence_bianalysisinddaily_edit_model = ns_businessintelligence.model(
    'BusinessIntelligenceBussinessIntelligenceBIAnalysisIndDailyEditDto.user', bussinessintelligence_bianalysisinddaily_edit_dto)

bussinessintelligence_bianalysisindmonthly_edit_model = ns_businessintelligence.model(
    'BusinessIntelligenceBussinessIntelligenceBIAnalysisIndMonthlyEditDto.user', bussinessintelligence_bianalysisindmonthly_edit_dto)

bussinessintelligence_dailyproductiondata_edit_model = ns_businessintelligence.model(
    'BusinessIntelligenceDailyProductionDataEditDto.user', bussinessintelligence_dailyproductiondata_edit_dto)

bussinessintelligence_uploaddata_edit_model = ns_businessintelligence.model(
    'BusinessIntelligenceUploadDataEditDto.user', bussinessintelligence_uploaddata_edit_dto)

parser = create_parser(bussinessintelligence_filter_model)
# parser_monthly = create_parser(bussinessintelligence_filter_monthly_model)

# @ns_businessintelligence.route('/')
# class BI(Resource):
#     @ns_businessintelligence.expect(parser)
#     # @ns_user.marshal_with(fta_response, as_list=True) #輸出自動轉model
#     @ns_businessintelligence.doc(description='查詢特定使用者',
#                  responses={200: 'OK',
#                             400: 'Bad Request'})
#     def get(self):
#         try:
#             logging.info(f'{request.method} {request.url_rule.rule} {request.remote_addr}')
#             json_path_security = os.path.join(current_app.config['folders']['temproot'], 'security.json')
#             logging.info(f'json_path_security: {json_path_security}')
#             with open(json_path_security, 'r') as file2:
#                 data = json.load(file2)
#                 self.key = data["Jwt"]["Key"]
#                 self.aud = data["Jwt"]["Audience"]
#         except Exception as e:
#             return {'message': f'Controller.user.py |An error occurred: {str(e)}'}, 500
#         try:
#             logging.info('Controller.user.py')
#             data = parser.parse_args()
#             print(f'data:{type(data)}')
#             jwt_token = request.cookies.get('jwt')
#             try:
#                 payload = jwt.decode(jwt_token, self.key, algorithms=['HS256'], audience=self.aud)
#             except jwt.ExpiredSignatureError:
#                 print("JWT签名已过期")
#                 return {'message': 'Authentication failed'}, 401
#             except jwt.PyJWTError as e:
#                 print(f"JWT异常: {e}")
#                 return {'message': 'Authentication failed'}, 401
#
#             bll = UserBll()
#             start_time = time.time()
#             rst = bll.browse(data)
#             end_time = time.time()
#             execution_time = round((end_time - start_time) * 1000, 2)
#             output = FtaResult(rst, execution_time, True).to_dict()
#             # print(output)
#             return output, output['status_code']
#         except Exception as e:
#             return {'message': f'Controller.user.py |An error occurred: {str(e)}'}, 500


@ns_businessintelligence.route('/bianalysisinddaily')
class BiAnalysisIndDaily(Resource):
    @ns_businessintelligence.expect(parser)
    # @ns_user.marshal_with(fta_response, as_list=True) #輸出自動轉model
    @ns_businessintelligence.doc(
        description='''
查詢BI每日指標

輸出data.Content

    [
        {
            "DATA_DATE": "資料日期"
            "DATA_SOURCE": "資料來源"
            "INDICATORS_CATEGORY": "指標分類"
            "INDICATORS_GROUP": "指標群組"
            "INDICATORS_NAME": "指標名稱"
            "LAST_UPDATE_DATE": "最後更新日期"
            "MACHINE_CODE": "機台"
            "MEASURE_VALUE": "指標數值"
            "ORG_CODE": "廠別代碼"
            "Unit": "單位"
            "Is_it_automated": "是否自動產生,非人工手動"
            "bdtm": "建立時間"
            "busr": "建立者"
            "department": "部門Id"
            "mdtm": "修改日期"
            "musr": "修改者"
            "remark": "註"
        }
    ]
        ''',
                                 responses={200: 'OK',
                                            400: 'Bad Request'})
    def get(self):
        print(f'{request.method} {request.url_rule.rule} {request.remote_addr}')
        logging.info(f'{request.method} {request.url_rule.rule} {request.remote_addr}')
        try:
            set_security(self, current_app)
        except Exception as e:
            msg = f'{self.__class__.__name__} |An error occurred: {str(e)}'
            print(msg)
            logging.debug(msg)
            return {'message': msg}, 500

        # parser = None
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
            bll = BussinessIntelligenceBll()
            start_time = time.time()
            rst = bll.browseBiAnalysisIndDaily(data)
            end_time = time.time()
            execution_time = round((end_time - start_time) * 1000, 2)
            output = FtaResult(rst, execution_time, True).to_dict()
            # print(output)
            return output, output['status_code']
        except Exception as e:
            msg = f'{self.__class__.__name__} |An error occurred: {str(e)}'
            print(msg)
            logging.debug(msg)
            return {'message': msg}, 500

    @ns_businessintelligence.expect([bussinessintelligence_bianalysisinddaily_edit_model])
    @ns_businessintelligence.doc(
        description='更新BI每日指標 ',
        responses={200: 'OK',
                   400: 'Bad Request'})
    def patch(self):
        print(f'{request.method} {request.url_rule.rule} {request.remote_addr}')
        logging.info(f'{request.method} {request.url_rule.rule} {request.remote_addr}')
        try:
            set_security(self, current_app)
        except Exception as e:
            msg = f'{self.__class__.__name__} |An error occurred: {str(e)}'
            print(msg)
            logging.debug(msg)

            return {'message': msg}, 500

        data = {}
        data['content'] = ns_businessintelligence.payload
        try:
            data['jwt'] = GetJwtPayload(self.security, request)
        except jwt.ExpiredSignatureError:
            print("JWT签名已过期")
            return {'message': 'Authentication failed'}, 401
        except jwt.PyJWTError as e:
            print(f"JWT异常: {e}")
            return {'message': 'Authentication failed'}, 401
        try:

            if isinstance(data['content'], list):
                instance = []
                for datum in data['content']:
                    datum['musr'] = data['jwt']["FTAId"]
                    instance.append(BussinessIntelligenceDto.implicit_bianalysisinddaily_edit(datum))
            else:
                data['musr'] = data['jwt']["FTAId"]
                instance = BussinessIntelligenceDto.implicit_bianalysisinddaily_edit(data)

            bll = BussinessIntelligenceBll()
            start_time = time.time()
            rst = bll.editBiAnalysisIndDaily(instance)
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


@ns_businessintelligence.route('/bianalysisindmonthly')
class BiAnalysisIndMonthly(Resource):
    @ns_businessintelligence.expect(parser)
    # @ns_user.marshal_with(fta_response, as_list=True) #輸出自動轉model
    @ns_businessintelligence.doc(
        description='''
查詢BI每月指標

輸出data.Content

    [
        {
            "DATA_SOURCE": "資料來源"
            "INDICATORS_CATEGORY": "指標分類"
            "INDICATORS_GROUP": "指標群組"
            "INDICATORS_NAME": "指標名稱"
            "LAST_UPDATE_DATE": "最後更新時間"
            "MACHINE_CODE": "機台"
            "MEASURE_VALUE": "指標數值"
            "ORG_CODE": "廠別代碼"
            "PERIOD_NAME": "期間"
            "Unit": "單位"
            "Is_it_automated": "是否自動產生,非人工手動"
            "bdtm": "建立時間"
            "busr": "建立者"
            "department": "部門Id"
            "mdtm": "修改日期"
            "musr": "修改者"
            "remark": "註"
        }
    ]
''',
        responses={200: 'OK',
                    400: 'Bad Request'})
    def get(self):
        print(f'{request.method} {request.url_rule.rule} {request.remote_addr}')
        logging.info(f'{request.method} {request.url_rule.rule} {request.remote_addr}')
        try:
            set_security(self, current_app)
        except Exception as e:
            msg = f'{self.__class__.__name__} |An error occurred: {str(e)}'
            print(msg)
            logging.debug(msg)
            return {'message': msg}, 500

        # parser = None
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
            bll = BussinessIntelligenceBll()
            start_time = time.time()
            rst = bll.browseBiAnalysisIndMonthly(data)
            end_time = time.time()
            execution_time = round((end_time - start_time) * 1000, 2)
            output = FtaResult(rst, execution_time, True).to_dict()
            # print(output)
            return output, output['status_code']
        except Exception as e:
            msg = f'{self.__class__.__name__} |An error occurred: {str(e)}'
            print(msg)
            logging.debug(msg)
            return {'message': msg}, 500

    @ns_businessintelligence.expect([bussinessintelligence_bianalysisindmonthly_edit_model])
    @ns_businessintelligence.doc(
        description='更新BI每月指標',
        responses={200: 'OK',
                   400: 'Bad Request'})
    def patch(self):
        print(f'{request.method} {request.url_rule.rule} {request.remote_addr}')
        logging.info(f'{request.method} {request.url_rule.rule} {request.remote_addr}')
        try:
            set_security(self, current_app)
        except Exception as e:
            msg = f'{self.__class__.__name__} |An error occurred: {str(e)}'
            print(msg)
            logging.debug(msg)

            return {'message': msg}, 500

        data = {}
        data['content'] = ns_businessintelligence.payload
        try:
            data['jwt'] = GetJwtPayload(self.security, request)
        except jwt.ExpiredSignatureError:
            print("JWT签名已过期")
            return {'message': 'Authentication failed'}, 401
        except jwt.PyJWTError as e:
            print(f"JWT异常: {e}")
            return {'message': 'Authentication failed'}, 401
        try:

            if isinstance(data['content'], list):
                instance = []
                for datum in data['content']:
                    datum['musr'] = data['jwt']["FTAId"]
                    instance.append(BussinessIntelligenceDto.implicit_bianalysisindmonthly_edit(datum))
            else:
                data['musr'] = data['jwt']["FTAId"]
                instance = BussinessIntelligenceDto.implicit_bianalysisindmonthly_edit(data)

            bll = BussinessIntelligenceBll()
            start_time = time.time()
            rst = bll.editBiAnalysisIndMonthly(instance)
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


@ns_businessintelligence.route('/bimachinestopdetails')
class BiMachineStopDetails(Resource):
    @ns_businessintelligence.expect(parser)
    # @ns_user.marshal_with(fta_response, as_list=True) #輸出自動轉model
    @ns_businessintelligence.doc(
        description='''
查詢BI停機紀錄

輸出data.Content

    [
        {
            "ORG_CODE": "廠別代碼",
            "STOP_DATE": "日期",
            "MACHINE_CODE": "機台",
            "STOP_NO": "停車紀錄NO/序號",
            "CATALOG_NAME": "分類名稱",
            "STOP_ITEM_NAME": "停車項目名稱",
            "REASON": "停機內容說明",
            "STOP_MIN": "時間(分)",
            "LAST_UPDATE_DATE": "最後更新時間",
            "Is_it_automated": "是否自動產生,非人工手動"
            "bdtm": "建立時間"
            "busr": "建立者"
            "department": "部門Id"
            "mdtm": "修改日期"
            "musr": "修改者"
        }
    ]
''',
        responses={200: 'OK',
                    400: 'Bad Request'})
    def get(self):
        print(f'{request.method} {request.url_rule.rule} {request.remote_addr}')
        logging.info(f'{request.method} {request.url_rule.rule} {request.remote_addr}')
        try:
            set_security(self, current_app)
        except Exception as e:
            msg = f'{self.__class__.__name__} |An error occurred: {str(e)}'
            print(msg)
            logging.debug(msg)
            return {'message': msg}, 500

        # parser = None
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
            bll = BussinessIntelligenceBll()
            start_time = time.time()
            rst = bll.browseBiMachineStopDetails(data)
            end_time = time.time()
            execution_time = round((end_time - start_time) * 1000, 2)
            output = FtaResult(rst, execution_time, True).to_dict()
            # print(output)
            return output, output['status_code']
        except Exception as e:
            msg = f'{self.__class__.__name__} |An error occurred: {str(e)}'
            print(msg)
            logging.debug(msg)
            return {'message': msg}, 500


@ns_businessintelligence.route('/bipmsch')
class BiPmSch(Resource):
    @ns_businessintelligence.expect(parser)
    # @ns_user.marshal_with(fta_response, as_list=True) #輸出自動轉model
    @ns_businessintelligence.doc(
        description='''
查詢BI紙機日排程

輸出data.Content

    [
        {
            "ORG_CODE": "廠別代碼",
            "PROD_DATE": "歸屬生產日期",
            "PM_NO": "紙機",
            "SCHEDULE_NO": "批號/排程號碼",
            "ITEM_NO": "ERP料號",
            "PAPER_TYPE": "紙別",
            "BASIS_WT": 基重,
            "OP_TIME_BEGIN": "抄造開始時間",
            "OP_TIME_END": "抄造結束時間",
            "RUN_MIN": "運轉時間(分)",
            "TARGET_SPEED": "目標車速",
            "ACTUAL_SPEED": "實際車速",
            "WEIGHT_KG": "重量(KG)",
            "LENGTH_M": "長度(M)",
            "LAST_UPDATE_DATE": "最後更新時間",
            "Is_it_automated": "是否自動產生,非人工手動"
            "bdtm": "建立時間"
            "busr": "建立者"
            "department": "部門Id"
            "mdtm": "修改日期"
            "musr": "修改者"
        }
    ]
    ''',
                                 responses={200: 'OK',
                                            400: 'Bad Request'})
    def get(self):
        print(f'{request.method} {request.url_rule.rule} {request.remote_addr}')
        logging.info(f'{request.method} {request.url_rule.rule} {request.remote_addr}')
        try:
            set_security(self, current_app)
        except Exception as e:
            msg = f'{self.__class__.__name__} |An error occurred: {str(e)}'
            print(msg)
            logging.debug(msg)
            return {'message': msg}, 500

        # parser = None
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
            bll = BussinessIntelligenceBll()
            start_time = time.time()
            rst = bll.browseBiPmSch(data)
            end_time = time.time()
            execution_time = round((end_time - start_time) * 1000, 2)
            output = FtaResult(rst, execution_time, True).to_dict()
            # print(output)
            return output, output['status_code']
        except Exception as e:
            msg = f'{self.__class__.__name__} |An error occurred: {str(e)}'
            print(msg)
            logging.debug(msg)
            return {'message': msg}, 500


@ns_businessintelligence.route('/dailymaterialdata')
class DailyMaterialData(Resource):
    @ns_businessintelligence.expect(parser)
    # @ns_user.marshal_with(fta_response, as_list=True) #輸出自動轉model
    @ns_businessintelligence.doc(
        description='''
查詢BI daily material data

輸出data.Content

    [
        {
            "ID": "唯一識別數",
            "ProductionDate": "生產日期",
            "ProductMaterialNo": "產品料號",
            "EquipmentNo": "設備編號",
            "SourceMaterialNo": "原物料或能資源料號",
            "SourceName": "原物料或能資源名稱",
            "SourceNo": "原物料或能資源編號",
            "Stage": "碳足跡階段",
            "Type": "排放源類別",
            "Value": "使用量",
            "Unit": "單位",
            "Rate": "使用比例",
            "UploadTime": "....",
            "Is_it_automated": "是否自動產生,非人工手動"
            "bdtm": "建立時間"
            "busr": "建立者"
            "department": "部門Id"
            "mdtm": "修改日期"
            "musr": "修改者"
            "remark": "註"
        }
    ]
    ''',
        responses={200: 'OK',
                    400: 'Bad Request'})
    def get(self):
        print(f'{request.method} {request.url_rule.rule} {request.remote_addr}')
        logging.info(f'{request.method} {request.url_rule.rule} {request.remote_addr}')
        try:
            set_security(self, current_app)
        except Exception as e:
            msg = f'{self.__class__.__name__} |An error occurred: {str(e)}'
            print(msg)
            logging.debug(msg)
            return {'message': msg}, 500

        # parser = None
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
            bll = BussinessIntelligenceBll()
            start_time = time.time()
            rst = bll.browseDailyMaterialData(data)
            end_time = time.time()
            execution_time = round((end_time - start_time) * 1000, 2)
            output = FtaResult(rst, execution_time, True).to_dict()
            # print(output)
            return output, output['status_code']
        except Exception as e:
            msg = f'{self.__class__.__name__} |An error occurred: {str(e)}'
            print(msg)
            logging.debug(msg)
            return {'message': msg}, 500


@ns_businessintelligence.route('/dailyproductiondata')
class DailyProductionData(Resource):
    @ns_businessintelligence.expect(parser)
    # @ns_user.marshal_with(fta_response, as_list=True) #輸出自動轉model
    @ns_businessintelligence.doc(
        description='''
查詢BI daily production data

輸出data.Content

    [
        {
            "ID": "ID",
            "ProductionDate": "生產日期",
            "ProductMaterialNo": "產品分類料號",
            "EquipmentNo": "設備編號",
            "Production": "產量//抄造量，單位:公斤",
            "ProductionRate": "產量佔比",
            "Inbound": "ERP 入庫量//單位:公斤",
            "InboundRate": "ERP 入庫量佔比",
            "UploadTime": "....",
            "Is_it_automated": "是否自動產生,非人工手動"
            "bdtm": "建立時間"
            "busr": "建立者"
            "department": "部門Id"
            "mdtm": "修改日期"
            "musr": "修改者"
            "remark": "註"
        }
    ]
''',
        responses={200: 'OK',
                    400: 'Bad Request'})
    def get(self):
        print(f'{request.method} {request.url_rule.rule} {request.remote_addr}')
        logging.info(f'{request.method} {request.url_rule.rule} {request.remote_addr}')
        try:
            set_security(self, current_app)
        except Exception as e:
            msg = f'{self.__class__.__name__} |An error occurred: {str(e)}'
            print(msg)
            logging.debug(msg)
            return {'message': msg}, 500

        # parser = None
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
            bll = BussinessIntelligenceBll()
            start_time = time.time()
            rst = bll.browseDailyProductionData(data)
            end_time = time.time()
            execution_time = round((end_time - start_time) * 1000, 2)
            output = FtaResult(rst, execution_time, True).to_dict()
            # print(output)
            return output, output['status_code']
        except Exception as e:
            msg = f'{self.__class__.__name__} |An error occurred: {str(e)}'
            print(msg)
            logging.debug(msg)
            return {'message': msg}, 500

    @ns_businessintelligence.expect([bussinessintelligence_dailyproductiondata_edit_model])
    @ns_businessintelligence.doc(
        description='更新BI daily production data',
        responses={200: 'OK',
                   400: 'Bad Request'})
    def patch(self):
        print(f'{request.method} {request.url_rule.rule} {request.remote_addr}')
        logging.info(f'{request.method} {request.url_rule.rule} {request.remote_addr}')
        try:
            set_security(self, current_app)
        except Exception as e:
            msg = f'{self.__class__.__name__} |An error occurred: {str(e)}'
            print(msg)
            logging.debug(msg)

            return {'message': msg}, 500

        data = {}
        data['content'] = ns_businessintelligence.payload
        try:
            data['jwt'] = GetJwtPayload(self.security, request)
        except jwt.ExpiredSignatureError:
            print("JWT签名已过期")
            return {'message': 'Authentication failed'}, 401
        except jwt.PyJWTError as e:
            print(f"JWT异常: {e}")
            return {'message': 'Authentication failed'}, 401
        try:

            if isinstance(data['content'], list):
                dailyproductiondata_instance = []
                for datum in data['content']:
                    datum['musr'] = data['jwt']["FTAId"]
                    dailyproductiondata_instance.append(BussinessIntelligenceDto.implicit_dailyproductiondata_edit(datum))
            else:
                data['musr'] = data['jwt']["FTAId"]
                dailyproductiondata_instance = BussinessIntelligenceDto.implicit_dailyproductiondata_edit(data)

            bll = BussinessIntelligenceBll()
            start_time = time.time()
            rst = bll.editDailyProductionData(dailyproductiondata_instance)
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


@ns_businessintelligence.route('/uploaddata')
class UploadData(Resource):
    @ns_businessintelligence.expect(parser)
    # @ns_user.marshal_with(fta_response, as_list=True) #輸出自動轉model
    @ns_businessintelligence.doc(
        description='''
查詢BI upload data

輸出data.Content

    [
        {
            "UID": "唯一識別數",
            "ProdDate": "生產日期",
            "DepartName": "....",
            "ClassName": "....",
            "SubClassName": "....",
            "ItemName": "....",
            "ProcNo": "製程編號",
            "ProcCode": "製程代碼",
            "ProcName": "製程名稱",
            "EquNo": "設備編號",
            "EquCode": "設備代碼",
            "EquName": "設備名稱",
            "IsCHP": "是否為汽電共生",
            "FuelCode": "燃料代碼",
            "FuelName": "燃料名稱",
            "IsBioFuel": "是否屬生質能源",
            "Category": "範疇別",
            "DisType": "排放型式",
            "ItemValue": "實績數值",
            "Unit": "單位",
            "UploadTime": "....",
            "Is_it_automated": "是否自動產生,非人工手動"
            "bdtm": "建立時間"
            "busr": "建立者"
            "department": "部門Id"
            "mdtm": "修改日期"
            "musr": "修改者"
            "remark": "註"
        }
    ]
        ''',
        responses={200: 'OK',
                    400: 'Bad Request'})
    def get(self):
        print(f'{request.method} {request.url_rule.rule} {request.remote_addr}')
        logging.info(f'{request.method} {request.url_rule.rule} {request.remote_addr}')
        try:
            set_security(self, current_app)
        except Exception as e:
            msg = f'{self.__class__.__name__} |An error occurred: {str(e)}'
            print(msg)
            logging.debug(msg)
            return {'message': msg}, 500

        # parser = None
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
            bll = BussinessIntelligenceBll()
            start_time = time.time()
            rst = bll.browseUploadData(data)
            end_time = time.time()
            execution_time = round((end_time - start_time) * 1000, 2)
            output = FtaResult(rst, execution_time, True).to_dict()
            # print(output)
            return output, output['status_code']
        except Exception as e:
            msg = f'{self.__class__.__name__} |An error occurred: {str(e)}'
            print(msg)
            logging.debug(msg)
            return {'message': msg}, 500

    @ns_businessintelligence.expect([bussinessintelligence_uploaddata_edit_model])
    @ns_businessintelligence.doc(
        description='更新UploadData',
        responses={200: 'OK',
                   400: 'Bad Request'})
    def patch(self):
        print(f'{request.method} {request.url_rule.rule} {request.remote_addr}')
        logging.info(f'{request.method} {request.url_rule.rule} {request.remote_addr}')
        try:
            set_security(self, current_app)
        except Exception as e:
            msg = f'{self.__class__.__name__} |An error occurred: {str(e)}'
            print(msg)
            logging.debug(msg)

            return {'message': msg}, 500

        data = {}
        data['content'] = ns_businessintelligence.payload
        try:
            data['jwt'] = GetJwtPayload(self.security, request)
        except jwt.ExpiredSignatureError:
            print("JWT签名已过期")
            return {'message': 'Authentication failed'}, 401
        except jwt.PyJWTError as e:
            print(f"JWT异常: {e}")
            return {'message': 'Authentication failed'}, 401
        try:

            if isinstance(data['content'], list):
                uploaddata_instance = []
                for datum in data['content']:
                    datum['musr'] = data['jwt']["FTAId"]
                    uploaddata_instance.append(BussinessIntelligenceDto.implicit_uploaddata_edit(datum))
            else:
                data['musr'] = data['jwt']["FTAId"]
                uploaddata_instance = BussinessIntelligenceDto.implicit_uploaddata_edit(data)

            bll = BussinessIntelligenceBll()
            start_time = time.time()
            rst = bll.editUploadData(uploaddata_instance)
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
