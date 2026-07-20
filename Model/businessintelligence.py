class BussinessIntelligenceDto:
    def __init__(self):
        pass

    class query_filter:
        def __init__(self, dateFrom, dateTo, departmentId):
            self.dateFrom = dateFrom
            self.dateTo = dateTo
            self.departmentId = departmentId

    class bianalysisinddaily_edit:
        def __init__(self, record):
            print(f'record: {type(record)}')
            if 'DATA_DATE' in record and record['DATA_DATE'] is not None:
                self.DATA_DATE = record['DATA_DATE']
            if 'MACHINE_CODE' in record and record['MACHINE_CODE'] is not None:
                self.MACHINE_CODE = record['MACHINE_CODE']
            if 'INDICATORS_CATEGORY' in record and record['INDICATORS_CATEGORY'] is not None:
                self.INDICATORS_CATEGORY = record['INDICATORS_CATEGORY']
            if 'INDICATORS_GROUP' in record and record['INDICATORS_GROUP'] is not None:
                self.INDICATORS_GROUP = record['INDICATORS_GROUP']
            if 'INDICATORS_NAME' in record and record['INDICATORS_NAME'] is not None:
                self.INDICATORS_NAME = record['INDICATORS_NAME']
            if 'MEASURE_VALUE' in record and record['MEASURE_VALUE'] is not None:
                self.MEASURE_VALUE = record['MEASURE_VALUE']
            if 'remark' in record:
                self.remark = record['remark']

    class implicit_bianalysisinddaily_edit(bianalysisinddaily_edit):
        def __init__(self, record):
            super().__init__(record)
            self.musr = record['musr']

    class bianalysisindmonthly_edit:
        def __init__(self, record):
            print(f'record: {type(record)}')
            if 'PERIOD_NAME' in record and record['PERIOD_NAME'] is not None:
                self.PERIOD_NAME = record['PERIOD_NAME']
            if 'MACHINE_CODE' in record and record['MACHINE_CODE'] is not None:
                self.MACHINE_CODE = record['MACHINE_CODE']
            if 'INDICATORS_CATEGORY' in record and record['INDICATORS_CATEGORY'] is not None:
                self.INDICATORS_CATEGORY = record['INDICATORS_CATEGORY']
            if 'INDICATORS_GROUP' in record and record['INDICATORS_GROUP'] is not None:
                self.INDICATORS_GROUP = record['INDICATORS_GROUP']
            if 'INDICATORS_NAME' in record and record['INDICATORS_NAME'] is not None:
                self.INDICATORS_NAME = record['INDICATORS_NAME']
            if 'MEASURE_VALUE' in record and record['MEASURE_VALUE'] is not None:
                self.MEASURE_VALUE = record['MEASURE_VALUE']
            if 'remark' in record:
                self.remark = record['remark']

    class implicit_bianalysisindmonthly_edit(bianalysisindmonthly_edit):
        def __init__(self, record):
            super().__init__(record)
            self.musr = record['musr']

    class dailyproductiondata_edit:
        def __init__(self, record):
            print(f'record: {type(record)}')
            if 'ID' in record and record['ID'] is not None:
                self.ID = record['ID']
            if 'Production' in record and record['Production'] is not None:
                self.Production = record['Production']
            if 'Inbound' in record and record['Inbound'] is not None:
                self.Inbound = record['Inbound']
            if 'remark' in record:
                self.remark = record['remark']

    class implicit_dailyproductiondata_edit(dailyproductiondata_edit):
        def __init__(self, record):
            super().__init__(record)
            self.musr = record['musr']

    class uploaddata_edit:
        def __init__(self, record):
            print(f'record: {type(record)}')
            if 'UID' in record and record['UID'] is not None:
                self.UID = record['UID']
            # if record.get('ProdDate'):
            #     self.ProdDate = record['ProdDate']
            # if record.get('DepartName'):
            #     self.DepartName = record['DepartName']
            # if record.get('ClassName'):
            #     self.ClassName = record['ClassName']
            # if record.get('SubClassName'):
            #     self.SubClassName = record['SubClassName']
            # if record.get('ItemName'):
            #     self.ItemName = record['ItemName']
            # if record.get('m_id'):
            #     self.m_id = record['m_id']
            # if record.get('ProcNo'):
            #     self.ProcNo = record['ProcNo']
            # if record.get('ProcCode'):
            #     self.ProcCode = record['ProcCode']
            # if record.get('ProcName'):
            #     self.ProcName = record['ProcName']
            # if record.get('EquNo'):
            #     self.EquNo = record['EquNo']
            # if record.get('EquCode'):
            #     self.EquCode = record['EquCode']
            # if record.get('EquName'):
            #     self.EquName = record['EquName']
            # if record.get('IsCHP'):
            #     self.IsCHP = record['IsCHP']
            # if record.get('FuelCode'):
            #     self.FuelCode = record['FuelCode']
            # if record.get('FuelName'):
            #     self.FuelName = record['FuelName']
            # if record.get('IsBioFuel'):
            #     self.IsBioFuel = record['IsBioFuel']
            # if record.get('Category'):
            #     self.Category = record['Category']
            # if record.get('DisType'):
            #     self.DisType = record['DisType']
            if 'ItemValue' in record and record['ItemValue'] is not None:
                self.ItemValue = record['ItemValue']
            # if record.get('Unit'):
            #     self.Unit = record['Unit']
            # if record.get('UploadTime'):
            #     self.UploadTime = record['UploadTime']
            # if record.get('department'):
            #     self.department = record['department']
            if 'remark' in record:
                self.remark = record['remark']

    class implicit_uploaddata_edit(uploaddata_edit):
        def __init__(self, record):
            super().__init__(record)
            self.musr = record['musr']



from flask_restx import fields, Namespace
ns_businessintelligence = Namespace('businessintelligence')

bussinessintelligence_query_filter_dto = ns_businessintelligence.model('BussinessIntelligenceFilterDto', {
    'dateFrom': fields.DateTime(required=True, description='起日yyyy-mm-dd'),
    'dateTo': fields.DateTime(required=True, description='迄日yyyy-mm-dd'),
    'departmentId': fields.String(required=True, description='單位'),
})

bussinessintelligence_query_filter_monthly_dto = ns_businessintelligence.model('BussinessIntelligenceFilterMonthlyDto', {
    'dateFrom': fields.DateTime(required=True, description='起月yyyy-mm'),
    'departmentId': fields.String(required=True, description='單位'),
})

bussinessintelligence_bianalysisinddaily_edit_dto = ns_businessintelligence.model('BussinessIntelligenceBIAnalysisIndDailyEditDto', {
    'DATA_DATE': fields.String(required=True, description=''),
    'MACHINE_CODE': fields.String(required=True, description=''),
    'INDICATORS_CATEGORY': fields.String(required=True, description=''),
    'INDICATORS_GROUP': fields.String(required=True, description=''),
    'INDICATORS_NAME': fields.String(required=True, description=''),
    'MEASURE_VALUE': fields.Float(required=True, description=''),
    'remark': fields.String(required=True, description=''),
})

bussinessintelligence_bianalysisindmonthly_edit_dto = ns_businessintelligence.model('BussinessIntelligenceBIAnalysisIndMonthlyEditDto', {
    'PERIOD_NAME': fields.String(required=True, description=''),
    'MACHINE_CODE': fields.String(required=True, description=''),
    'INDICATORS_CATEGORY': fields.String(required=True, description=''),
    'INDICATORS_GROUP': fields.String(required=True, description=''),
    'INDICATORS_NAME': fields.String(required=True, description=''),
    'MEASURE_VALUE': fields.Float(required=True, description=''),
    'remark': fields.String(required=True, description=''),
})

bussinessintelligence_dailyproductiondata_edit_dto = ns_businessintelligence.model('BussinessIntelligenceDailyProductionDataEditDto', {
    'ID': fields.Integer(required=True, description=''),
    'Production': fields.Float(required=True, description=''),
    'Inbound': fields.Float(required=True, description=''),
    'remark': fields.String(required=True, description=''),
})
bussinessintelligence_uploaddata_edit_dto = ns_businessintelligence.model('BussinessIntelligenceUploadDataEditDto', {
    'UID': fields.Integer(required=True, description=''),
    # 'ProdDate': fields.DateTime(required=True, description=''),
    # 'DepartName': fields.String(required=True, description=''),
    # 'ClassName': fields.String(required=True, description=''),
    # 'SubClassName': fields.String(required=True, description=''),
    # 'ItemName': fields.String(required=True, description=''),
    # 'm_id': fields.String(required=True, description=''),
    # 'ProcNo': fields.String(required=True, description=''),
    # 'ProcCode': fields.String(required=True, description=''),
    # 'ProcName': fields.String(required=True, description=''),
    # 'EquNo': fields.String(required=True, description=''),
    # 'EquCode': fields.String(required=True, description=''),
    # 'EquName': fields.String(required=True, description=''),
    # 'IsCHP': fields.Boolean(required=True, description=''),
    # 'FuelCode': fields.String(required=True, description=''),
    # 'FuelName': fields.String(required=True, description=''),
    # 'IsBioFuel': fields.Boolean(required=True, description=''),
    # 'Category': fields.String(required=True, description=''),
    # 'DisType': fields.String(required=True, description=''),
    'ItemValue': fields.Float(required=True, description=''),
    # 'Unit': fields.String(required=True, description=''),
    # 'UploadTime': fields.DateTime(required=True, description=''),
    # 'department': fields.String(required=True, description=''),
    'remark': fields.String(required=True, description=''),
})
