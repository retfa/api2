from icecream import ic
from DAL.srvmsdba2.FTA_EN_Summary.FTA_PM18_consumption import FTA_PM18_consumptionDal
from DAL.srvmsdba2.FTA_EN_Summary.FTA_PM19_consumption import FTA_PM19_consumptionDal
from DAL.srvmsdba2.FTA_EN_Summary.FTA_PM20_consumption import FTA_PM20_consumptionDal
from DAL.srvmsdba2.FTA_EN_Summary.FTA_PM21_consumption import FTA_PM21_consumptionDal
from DAL.srvmsdba2.FTA_EN_Summary.FTA_PM18_consumption_reel import FTA_PM18_consumption_reelDal
from DAL.srvmsdba2.FTA_EN_Summary.FTA_PM19_consumption_reel import FTA_PM19_consumption_reelDal
from DAL.srvmsdba2.FTA_EN_Summary.FTA_PM20_consumption_reel import FTA_PM20_consumption_reelDal
from DAL.srvmsdba2.FTA_EN_Summary.FTA_PM21_consumption_reel import FTA_PM21_consumption_reelDal


class consumptionBll:
    def browse(self, data):
        mnameMapper = {"18": FTA_PM18_consumptionDal(), "19": FTA_PM19_consumptionDal(),
                       "20": FTA_PM20_consumptionDal(), "21": FTA_PM21_consumptionDal()}
        dal = None
        if 'MachineName' in data and data['MachineName'] in mnameMapper:
            dal = mnameMapper[data['MachineName']]
        else:
            return None

        rst = dal.query(data)
        # ic(type(rst))
        for result in rst:
            # ic(type(result))
            # result['TagName'] = data['TagNameOrigin']
            pass
        return rst


class consumptionReelBll:
    def browse(self, data):
        mnameMapper = {"18": FTA_PM18_consumption_reelDal(), "19": FTA_PM19_consumption_reelDal(),
                       "20": FTA_PM20_consumption_reelDal(), "21": FTA_PM21_consumption_reelDal()}
        dal = None
        if 'MachineName' in data and data['MachineName'] in mnameMapper:
            dal = mnameMapper[data['MachineName']]
        else:
            return None

        rst = dal.query(data)
        # ic(type(rst))
        for result in rst:
            # ic(type(result))
            # result['TagName'] = data['TagNameOrigin']
            pass
        return rst
