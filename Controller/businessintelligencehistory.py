from flask import request, current_app
from flask_restx import Resource, Namespace
import jwt
import time
import logging
from BLL.bussinessintelligencehistory import BussinessIntelligenceHistoryBll
from Model.businessintelligencehistory import *
from common import GetJwtPayload, set_security, create_parser
from fta_response import FtaResult

ns_businessintelligencehistory = Namespace(
    'businessintelligencehistory', description='BusinessIntelligence history 相關')

bussinessintelligencehistory_filter_model = ns_businessintelligencehistory.model(
    'BusinessIntelligenceHistoryDto.user_filter', bussinessintelligencehistory_query_filter_dto)

bussinessintelligencehistory_filter_monthly_model = ns_businessintelligencehistory.model(
    'BusinessIntelligenceHistoryDto.user_filter_monthly', bussinessintelligencehistory_query_filter_monthly_dto)

parser = create_parser(bussinessintelligencehistory_filter_model)
parser_monthly = create_parser(bussinessintelligencehistory_filter_monthly_model)

# @ns_businessintelligencehistory.route('/')
# class BI(Resource):
#     @ns_businessintelligencehistory.expect(parser)
#     # @ns_user.marshal_with(fta_response, as_list=True) #輸出自動轉model
#     @ns_businessintelligencehistory.doc(description='查詢特定使用者',
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


@ns_businessintelligencehistory.route('/bianalysisinddaily')
class BiAnalysisIndDaily(Resource):
    @ns_businessintelligencehistory.expect(parser)
    # @ns_user.marshal_with(fta_response, as_list=True) #輸出自動轉model
    @ns_businessintelligencehistory.doc(
        id='get_bi_analysis_ind_daily_history',
        description='查詢BI每日指標',
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
        data['user_id'] = data['jwt']["FTAId"] if data.get('jwt') and data['jwt'].get("FTAId") else ""

        try:
            bll = BussinessIntelligenceHistoryBll()
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


@ns_businessintelligencehistory.route('/bianalysisindmonthly')
class BiAnalysisIndMonthly(Resource):
    @ns_businessintelligencehistory.expect(parser_monthly)
    # @ns_user.marshal_with(fta_response, as_list=True) #輸出自動轉model
    @ns_businessintelligencehistory.doc(
        id='get_bi_analysis_ind_monthly_history',
        description='查詢BI每月指標',
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
        if parser_monthly:
            data = parser_monthly.parse_args()

        print(f'data:{type(data)}')

        try:
            data['jwt'] = GetJwtPayload(self.security, request)
        except jwt.ExpiredSignatureError:
            print("JWT签名已过期")
            return {'message': 'Authentication failed'}, 401
        except jwt.PyJWTError as e:
            print(f"JWT异常: {e}")
            return {'message': 'Authentication failed'}, 401
        data['user_id'] = data['jwt']["FTAId"] if data.get('jwt') and data['jwt'].get("FTAId") else ""

        try:
            bll = BussinessIntelligenceHistoryBll()
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


@ns_businessintelligencehistory.route('/bimachinestopdetails')
class BiMachineStopDetails(Resource):
    @ns_businessintelligencehistory.expect(parser)
    # @ns_user.marshal_with(fta_response, as_list=True) #輸出自動轉model
    @ns_businessintelligencehistory.doc(
        id='get_bi_machine_stop_details_history',
        description='查詢BI停機紀錄',
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
        data['user_id'] = data['jwt']["FTAId"] if data.get('jwt') and data['jwt'].get("FTAId") else ""

        try:
            bll = BussinessIntelligenceHistoryBll()
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


@ns_businessintelligencehistory.route('/bipmsch')
class BiPmSch(Resource):
    @ns_businessintelligencehistory.expect(parser)
    # @ns_user.marshal_with(fta_response, as_list=True) #輸出自動轉model
    @ns_businessintelligencehistory.doc(
        id='get_bi_pm_sch_history',
        description='查詢BI紙機日排程',
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
        data['user_id'] = data['jwt']["FTAId"] if data.get('jwt') and data['jwt'].get("FTAId") else ""

        try:
            bll = BussinessIntelligenceHistoryBll()
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


@ns_businessintelligencehistory.route('/dailymaterialdata')
class DailyMaterialData(Resource):
    @ns_businessintelligencehistory.expect(parser)
    # @ns_user.marshal_with(fta_response, as_list=True) #輸出自動轉model
    @ns_businessintelligencehistory.doc(
        id='get_daily_material_data_history',
        description='查詢BI daily material data',
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
        data['user_id'] = data['jwt']["FTAId"] if data.get('jwt') and data['jwt'].get("FTAId") else ""

        try:
            bll = BussinessIntelligenceHistoryBll()
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


@ns_businessintelligencehistory.route('/dailyproductiondata')
class DailyProductionData(Resource):
    @ns_businessintelligencehistory.expect(parser)
    # @ns_user.marshal_with(fta_response, as_list=True) #輸出自動轉model
    @ns_businessintelligencehistory.doc(
        id='get_daily_production_data_history',
        description='查詢BI daily production data',
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
        data['user_id'] = data['jwt']["FTAId"] if data.get('jwt') and data['jwt'].get("FTAId") else ""
        
        try:
            bll = BussinessIntelligenceHistoryBll()
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


@ns_businessintelligencehistory.route('/uploaddata')
class UploadData(Resource):
    @ns_businessintelligencehistory.expect(parser)
    # @ns_user.marshal_with(fta_response, as_list=True) #輸出自動轉model
    @ns_businessintelligencehistory.doc(
        id='get_upload_data_history',
        description='查詢BI upload data',
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
        data['user_id'] = data['jwt']["FTAId"] if data.get('jwt') and data['jwt'].get("FTAId") else ""

        try:
            bll = BussinessIntelligenceHistoryBll()
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
