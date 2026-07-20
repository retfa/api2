import json
import os
from flask import request, current_app
from flask_restx import Resource, Namespace, fields
import jwt
import time
import logging
from BLL.program import ProgramBll
from Model.program import program_query_filter_dto, program_add_dto
from common import create_parser, GetJwtPayload, set_security
from fta_response import FtaResult

ns_program = Namespace('program', description='program 權限相關')

program_filter_model = ns_program.model('ProgramDto.program_filter', program_query_filter_dto)
program_add_model = ns_program.model('ProgramDto.program_add', program_add_dto)
parser = create_parser(program_filter_model)


@ns_program.route('/')
class Program(Resource):
    # @ns_program.expect(parser)
    # # @ns_program.marshal_with(fta_response, as_list=True) #輸出自動轉model
    # @ns_program.doc(description='查詢權限',
    #                 responses={200: 'OK',
    #                            400: 'Bad Request'})
    # def get(self):
    #     logging.info(f'{request.method} {request.url_rule.rule}')
    #     try:
    #         json_path_security = os.path.join(current_app.config['folders']['temproot'], 'security.json')
    #         # logging.info(f'json_path_security: {json_path_security}')
    #         with open(json_path_security, 'r') as file2:
    #             data = json.load(file2)
    #             self.key = data["Jwt"]["Key"]
    #             self.aud = data["Jwt"]["Audience"]
    #     except Exception as e:
    #         msg = f'{self.__class__.__name__} |An error occurred: {str(e)}'
    #         print(msg)
    #         logging.debug(msg)

    #         return {'message': msg}, 500

    #     try:
    #         data = parser.parse_args()
    #         data.function_array = []
    #         if data.function:
    #             data.function_array = data.function.split(',')

    #         data.up_function_array = []
    #         if data.up_function:
    #             data.up_function_array = data.up_function.split(',')

    #         data.progm_id_array = []
    #         if data.progm_id:
    #             data.progm_id_array = data.progm_id.split(',')

    #         jwt_token = request.cookies.get('jwt')
    #         try:
    #             payload = jwt.decode(jwt_token, self.key, algorithms=['HS256'], audience=self.aud)
    #         except jwt.ExpiredSignatureError:
    #             print("JWT签名已过期")
    #             return {'message': 'Authentication failed'}, 401
    #         except jwt.PyJWTError as e:
    #             print(f"JWT异常: {e}")
    #             return {'message': 'Authentication failed'}, 401

    #         bll = ProgramBll()
    #         start_time = time.time()
    #         rst = bll.read_by_user(data)
    #         end_time = time.time()
    #         execution_time = round((end_time - start_time) * 1000, 2)
    #         output = FtaResult(rst, execution_time, True).to_dict()
    #         # print(output)
    #         return output, output['status_code']
    #     except Exception as e:
    #         msg = f'{self.__class__.__name__} |An error occurred: {str(e)}'
    #         print(msg)
    #         logging.debug(msg)

    #         return {'message': msg}, 500

    @ns_program.expect(program_add_model)
    @ns_program.doc(description='新增程式',
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

        data = ns_program.payload
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
            bll = ProgramBll()
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
