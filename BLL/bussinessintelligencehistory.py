from DAL.permicrossdepartment import PermissionCrossDepartmentDal
from DAL.srvbiapa1.BI_FTA.bianalysisinddaily import BiAnalysisIndDailyDal
from DAL.srvbiapa1.BI_FTA.bianalysisindmonthly import BiAnalysisIndMonthlyDal
from DAL.srvbiapa1.BI_FTA.bimachinestopdetails import BiMachineStopDetailsDal
from DAL.srvbiapa1.BI_FTA.bipmsch import BiPmSchDal
from DAL.srvbiapa1.ESG_FTA.dailymaterialdata import DailyMaterialDataDal
from DAL.srvbiapa1.ESG_FTA.dailyproductiondata import DailyProductionDataDal
from DAL.srvbiapa1.ESG_FTA.uploaddata import UploadDataDal


class BussinessIntelligenceHistoryBll:
    def browseBiAnalysisIndDaily(self, data):
        data["progm_id"] = 'PB010I1'
        dalPermiCrossDept = PermissionCrossDepartmentDal()
        data["departments"] = dalPermiCrossDept.query(data)
        dal = BiAnalysisIndDailyDal()
        rst = dal.query(data)
        print(f'type: {type(rst)}')
        return rst

    def browseBiAnalysisIndMonthly(self, data):
        data["progm_id"] = 'PB010I1'
        dalPermiCrossDept = PermissionCrossDepartmentDal()
        data["departments"] = dalPermiCrossDept.query(data)
        dal = BiAnalysisIndMonthlyDal()
        rst = dal.query(data)
        print(f'type: {type(rst)}')
        return rst

    def browseBiMachineStopDetails(self, data):
        data["progm_id"] = 'PB010I1'
        dalPermiCrossDept = PermissionCrossDepartmentDal()
        data["departments"] = dalPermiCrossDept.query(data)
        dal = BiMachineStopDetailsDal()
        rst = dal.query(data)
        print(f'type: {type(rst)}')
        return rst

    def browseBiPmSch(self, data):
        data["progm_id"] = 'PB010I1'
        dalPermiCrossDept = PermissionCrossDepartmentDal()
        data["departments"] = dalPermiCrossDept.query(data)
        dal = BiPmSchDal()
        rst = dal.query(data)
        print(f'type: {type(rst)}')
        return rst

    def browseDailyMaterialData(self, data):
        data["progm_id"] = 'OB010I1'
        dalPermiCrossDept = PermissionCrossDepartmentDal()
        data["departments"] = dalPermiCrossDept.query(data)
        dal = DailyMaterialDataDal()
        rst = dal.query(data)
        print(f'type: {type(rst)}')
        return rst

    def browseDailyProductionData(self, data):
        data["progm_id"] = 'OB010I1'
        dalPermiCrossDept = PermissionCrossDepartmentDal()
        data["departments"] = dalPermiCrossDept.query(data)
        dal = DailyProductionDataDal()
        rst = dal.query(data)
        print(f'type: {type(rst)}')
        return rst

    def browseUploadData(self, data):
        data["progm_id"] = 'OB010I1'
        dalPermiCrossDept = PermissionCrossDepartmentDal()
        data["departments"] = dalPermiCrossDept.query(data)
        dal = UploadDataDal()
        rst = dal.query(data)
        print(f'type: {type(rst)}')
        return rst

