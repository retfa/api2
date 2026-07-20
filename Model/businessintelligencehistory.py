class BussinessIntelligenceHistoryDto:
    def __init__(self):
        pass

    class query_filter:
        def __init__(self, dateFrom, dateTo, departmentId):
            self.dateFrom = dateFrom
            self.dateTo = dateTo
            self.departmentId = departmentId


from flask_restx import fields, Namespace
ns_businessintelligencehistory = Namespace('businessintelligence')

bussinessintelligencehistory_query_filter_dto = ns_businessintelligencehistory.model('BussinessIntelligenceFilterDto', {
    'dateFrom': fields.DateTime(required=True, description='起日')
})

bussinessintelligencehistory_query_filter_monthly_dto = ns_businessintelligencehistory.model('BussinessIntelligenceFilterMonthlyDto', {
    'dateFrom': fields.DateTime(required=True, description='起月'),
})
