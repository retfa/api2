from flask import request, current_app
from flask_restx import Resource, Namespace, fields
import jwt
import time
import logging
from BLL.machine import MachineBll
from Model.machine import pmEnum
from common import GetJwtPayload, set_security, create_parser, add_to_dict, get_connection_string
from fta_response import FtaResult

ns_machine = Namespace('machine', description='機台操作相關')
stationList = ["M", "R", "C", "E", "W", "F", "B", "S", "T", "H", "P", "A", "D", "STK", "U", "W"]
production_lineList = ["R", "S", "T", "W", "A"]
nameList = ["18", "19", "20", "21",
            "R1", "RT",
            "C1", "C2", "C7",
            "EA", "EB", "EC", "ED", "E3", "EO", "EP", "EQ", "ER",
            "WA", "WB", "WR", "WS", "WJ", "WE", "WW",
            "DA",
            "BA",
            "SA", "SB", "SC", "SD", "SH", "SI", "SL", "SF",
            "TB", "TD",
            "H1", "H3", "HN",
            "PB", "PC", "PD",
            "M", "N", "P",
            ]

machine_filter_model = ns_machine.model('machine_filter', {
    'station': fields.String(required=False, description='站別 EX:M 抄紙'),
    'production_line': fields.Raw(enum=[member.name for member in pmEnum], required=False, description='生產線 EX:T 20號機'),
    'name': fields.String(required=False, description='名稱 EX:EO 壓光機')
})

parser = create_parser(machine_filter_model)


@ns_machine.route('/')
class MachineController(Resource):
    @ns_machine.expect(parser)
    # @api.marshal_with(fta_response, as_list=True) #輸出自動轉model
    @ns_machine.doc(
        params={'station': {'in': 'query', 'enum': stationList},
                'production_line': {'in': 'query', 'enum': production_lineList},
                'name': {'in': 'query', 'enum': nameList},
                },
        description='''
取得機台資料

輸出data.Content

    [
        {
            "station": "站別",
            "pm": "生產線",
            "mname": "名稱",
            "chsnm": "中文名稱",
            "btable": "資料表",
            "stop_yn": "目前機台停車狀態",
            "status": "機台使用狀態",
            "cls_sn": "機台停用原因"
        }
    ]
        ''',
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
