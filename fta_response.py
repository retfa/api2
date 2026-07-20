import datetime
from flask_restx import fields, Namespace
import pytz

mes_ns = Namespace('mes', description='MES 相关操作描述')
fta_response = mes_ns.model('fta_response', {
    'data': fields.Raw,
    'message': fields.String,
    'status_code': fields.Integer
})


class FtaResult:
    def __init__(self, data=None, execution_time=0, success=False, status_code=None):
        self.data = data
        self.execution_time = execution_time
        self.success = success
        if status_code is None and success is True:
            self.status_code = 200
        else:
            self.status_code = 400

    def to_dict(self):
        # print(type(self.data))
        data_list = []
        if self.data is None:
            pass
        if self.data is False:
            pass
        if self.data == -1:
            pass
        elif isinstance(self.data, list):
            for item in self.data:
                # print(type(item))
                if isinstance(item, list):
                    data_list.append(item.to_dict())
                else:
                    data_list.append(item)
        else:
            data_list = self.data
        # print('length: ' + str(len(data_list)))

        # if len(data_list) != 0:
        #    status_code = 200
        # else:
        #    status_code = 200

        utc_now = datetime.datetime.now(pytz.utc)

        taipei_timezone = pytz.timezone('Asia/Taipei')
        taipei_time = utc_now.astimezone(taipei_timezone).strftime('%Y-%m-%d %H:%M:%S.%f %z')
        taipei_time_formatted = taipei_time[:-2] + ":" + taipei_time[-2:]

        response_dict = {
            'data': {
                'Action': '',
                'Content': data_list,
                'ExecutionTime': f'{self.execution_time} ms',
                'ExecutionDto': taipei_time_formatted
            },
            'success': self.success,
            'status_code': self.status_code
        }

        if data_list and isinstance(data_list, list):
            response_dict["data"]["Length"] = len(data_list)
        return response_dict
