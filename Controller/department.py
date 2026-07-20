import json
import os
from flask import request, current_app
from flask_restx import Resource, Namespace
import time
import logging
from BLL.department import DepartmentBll
from fta_response import FtaResult

ns_department = Namespace('department', description='部門操作相關')


@ns_department.route('/')
class Department(Resource):
    def get(self):
        try:
            logging.info(f'{request.method} {request.url_rule.rule}')
            json_path_security = os.path.join(current_app.config['folders']['temproot'], 'security.json')
            logging.info(f'json_path_security: {json_path_security}')
            with open(json_path_security, 'r') as file2:
                data = json.load(file2)
                self.security = {}
                self.security["key"] = data["Jwt"]["Key"]
                self.security["aud"] = data["Jwt"]["Audience"]
        except Exception as e:
            msg = f'{self.__class__.__name__} |An error occurred: {str(e)}'
            print(msg)
            logging.debug(msg)
            return {'message': msg}, 500
        try:
            # jwt_payload = GetJwtPayload(self.security, request)
            bll = DepartmentBll()
            start_time = time.time()
            rst = bll.browse_zmuser()
            end_time = time.time()
            execution_time = round((end_time - start_time) * 1000, 2)
            output = FtaResult(rst, execution_time, True).to_dict()
            return output, output['status_code']
        except Exception as e:
            msg = f'{self.__class__.__name__} |An error occurred: {str(e)}'
            print(msg)
            logging.debug(msg)
            return {'message': msg}, 500

    def post(self):
        pass

    def patch(self):
        pass


@ns_department.route('/hr')
class HrDepartment(Resource):
    def get(self):
        try:
            logging.info(f'{request.method} {request.url_rule.rule}')
            json_path_security = os.path.join(current_app.config['folders']['temproot'], 'security.json')
            logging.info(f'json_path_security: {json_path_security}')
            with open(json_path_security, 'r') as file2:
                data = json.load(file2)
                self.security = {}
                self.security["key"] = data["Jwt"]["Key"]
                self.security["aud"] = data["Jwt"]["Audience"]
        except Exception as e:
            msg = f'{self.__class__.__name__} |An error occurred: {str(e)}'
            print(msg)
            logging.debug(msg)
            return {'message': msg}, 500
        try:
            # jwt_payload = GetJwtPayload(self.security, request)
            bll = DepartmentBll()
            start_time = time.time()
            rst = bll.browse_hr()
            end_time = time.time()
            execution_time = round((end_time - start_time) * 1000, 2)
            output = FtaResult(rst, execution_time, True).to_dict()
            return output, output['status_code']
        except Exception as e:
            msg = f'{self.__class__.__name__} |An error occurred: {str(e)}'
            print(msg)
            logging.debug(msg)
            return {'message': msg}, 500
