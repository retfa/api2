from DAL.srvbiapa1.ESG_FTA_MODIFY.bianalysisinddaily import BiAnalysisIndDailyDal
from DAL.srvbiapa1.ESG_FTA_MODIFY.bianalysisindmonthly import BiAnalysisIndMonthlyDal
from DAL.srvbiapa1.ESG_FTA_MODIFY.bimachinestopdetails import BiMachineStopDetailsDal
from DAL.srvbiapa1.ESG_FTA_MODIFY.bipmsch import BiPmSchDal
from DAL.srvbiapa1.ESG_FTA_MODIFY.dailymaterialdata import DailyMaterialDataDal
from DAL.srvbiapa1.ESG_FTA_MODIFY.dailyproductiondata import DailyProductionDataDal
from DAL.srvbiapa1.ESG_FTA_MODIFY.uploaddata import UploadDataDal


class BussinessIntelligenceBll:
    def browseBiAnalysisIndDaily(self, data):
        dal = BiAnalysisIndDailyDal()
        rst = dal.query(data)
        print(f'type: {type(rst)}')
        return rst

    def editBiAnalysisIndDaily(self, data):
        dal = BiAnalysisIndDailyDal()
        rst = dal.update(data)
        return rst

    def browseBiAnalysisIndMonthly(self, data):
        dal = BiAnalysisIndMonthlyDal()
        rst = dal.query(data)
        print(f'type: {type(rst)}')
        return rst

    def editBiAnalysisIndMonthly(self, data):
        dal = BiAnalysisIndMonthlyDal()
        rst = dal.update(data)
        return rst

    def browseBiMachineStopDetails(self, data):
        dal = BiMachineStopDetailsDal()
        rst = dal.query(data)
        print(f'type: {type(rst)}')
        return rst

    # def editBiMachineStopDetails(self, data):
    #     dal = BiMachineStopDetailsDal()
    #     rst = dal.update(data)
    #     return rst

    def browseBiPmSch(self, data):
        dal = BiPmSchDal()
        rst = dal.query(data)
        print(f'type: {type(rst)}')
        return rst

    def editBiPmSch(self, data):
        dal = BiPmSchDal()
        rst = dal.update(data)
        return rst

    def browseDailyMaterialData(self, data):
        dal = DailyMaterialDataDal()
        rst = dal.query(data)
        print(f'type: {type(rst)}')
        return rst

    def browseDailyProductionData(self, data):
        dal = DailyProductionDataDal()
        rst = dal.query(data)
        print(f'type: {type(rst)}')
        return rst

    def editDailyProductionData(self, data):
        dal = DailyProductionDataDal()
        rst = dal.update(data)
        return rst

    # def read(self, data):
    #     zmuser_dal = UserDal()
    #     rst = zmuser_dal.select(data)
    #     print(f'type: {type(rst)}')
    #     return rst

    def browseUploadData(self, data):
        dal = UploadDataDal()
        rst = dal.query(data)
        print(f'type: {type(rst)}')
        return rst

    def editUploadData(self, data):
        zmuser_dal = UploadDataDal()
        rst = zmuser_dal.update(data)
        return rst

    # def read(self, data):
    #     zmuser_dal = UserDal()
    #     rst = zmuser_dal.select(data)
    #     print(f'type: {type(rst)}')
    #     return rst
