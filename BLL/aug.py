from DAL.srvmsdba2.FTA_AUG.BW1RL_avg import BW1RL_avgDal
from DAL.srvmsdba2.FTA_AUG.BW1RL_raw_avg import BW1RL_raw_avgDal
from DAL.srvmsdba2.FTA_AUG.BW1SP_avg import BW1SP_avgDal
from DAL.srvmsdba2.FTA_AUG.BW1SP_raw_avg import BW1SP_raw_avgDal
from DAL.srvmsdba2.FTA_AUG.MO1RL_avg import MO1RL_avgDal
from DAL.srvmsdba2.FTA_AUG.MO1RL_raw_avg import MO1RL_raw_avgDal
from DAL.srvmsdba2.FTA_AUG.MO1SP_avg import MO1SP_avgDal
from DAL.srvmsdba2.FTA_AUG.MO1SP_raw_avg import MO1SP_raw_avgDal
from DAL.srvmsdba2.FTA_AUG.PM21_AUG_AVG_REEL import PM21_AUG_AVG_REELDal
from DAL.srvmsdba2.FTA_AUG.PM21_CoatingWeight import PM21_CoatingWeightDal
from DAL.srvmsdba2.FTA_AUG.PM21_CoatingWeight_raw import PM21_CoatingWeight_rawDal
from DAL.srvmsdba2.FTA_AUG_C1.CM8_MP1_avg import CM8_MP1_avgDal
from DAL.srvmsdba2.FTA_AUG_C1.CM8_MP2_avg import CM8_MP2_avgDal
from DAL.srvmsdba2.FTA_AUG_C1.PM21_OMC1_AVG_REEL import PM21_OMC1_AVG_REELDal
from DAL.srvmsdba2.FTA_SAUG.CARL_avg import CARL_avgDal
from DAL.srvmsdba2.FTA_SAUG.PM19_AUG_AVG_REEL import PM19_AUG_AVG_REELDal
from DAL.srvmsdba2.FTA_TAUG.BWRL_avg import BWRL_avgDal
from DAL.srvmsdba2.FTA_TAUG.BWRL_raw_avg import BWRL_raw_avgDal
from DAL.srvmsdba2.FTA_TAUG.ODRL_A_avg import ODRL_A_avgDal
from DAL.srvmsdba2.FTA_TAUG.ODRL_A_raw_avg import ODRL_A_raw_avgDal
from DAL.srvmsdba2.FTA_TAUG.ODSP_A_avg import ODSP_A_avgDal
from DAL.srvmsdba2.FTA_TAUG.ODSP_A_raw_avg import ODSP_A_raw_avgDal
from DAL.srvmsdba2.FTA_TAUG.PM20_AUG_AVG_REEL import PM20_AUG_AVG_REELDal
from DAL.srvmsdba2.FTA_TAUG.PM20_CoatingWeight import PM20_CoatingWeightDal
from DAL.srvmsdba2.FTA_TAUG.PM20_CoatingWeight_raw import PM20_CoatingWeight_rawDal
from DAL.srvmsdba2.FTA_TAUG.PMRL_A_avg import PMRL_A_avgDal
from DAL.srvmsdba2.FTA_TAUG.PMRL_A_raw_avg import PMRL_A_raw_avgDal
from DAL.srvmsdba2.FTA_TAUG.PMRL_avg import PMRL_avgDal
from DAL.srvmsdba2.FTA_TAUG.PMRL_raw_avg import PMRL_raw_avgDal
from DAL.srvmsdba2.FTA_TAUG.PMSP_A_avg import PMSP_A_avgDal
from DAL.srvmsdba2.FTA_TAUG.PMSP_A_raw_avg import PMSP_A_raw_avgDal


class AugBll:
    def browse(self, data):
        if data.MachineName == "19":
            dal = FTA_SAUGBll.group_raw_dal(data.TagName)
        elif data.MachineName == "20":
            dal = FTA_TAUGBll.group_raw_dal(data.TagName)
        elif data.MachineName == "21":
            dal = FTA_AUGBll.group_raw_dal(data.TagName)
        elif data.MachineName == "C1":
            dal = FTA_AUG_C1Bll.group_raw_dal(data.TagName)
        else:
            dal = None

        if dal is None:
            return None
        rst = dal.query(data)
        return rst

    def browse_group_interval(self, data):
        if data.MachineName == "19":
            dal = FTA_SAUGBll.group_raw_interval_dal(data.TagName)
        elif data.MachineName == "20":
            dal = FTA_TAUGBll.group_raw_interval_dal(data.TagName)
        elif data.MachineName == "21":
            dal = FTA_AUGBll.group_raw_interval_dal(data.TagName)
        elif data.MachineName == "C1":
            dal = FTA_AUG_C1Bll.group_raw_interval_dal(data.TagName)
        else:
            dal = None

        if dal is None:
            return None
        rst = dal.query_interval(data)
        return rst

    def browse_reel(self, data):
        if data.MachineName == "19":
            dal = FTA_SAUGBll.reel_group_raw_dal(data)
        elif data.MachineName == "20":
            dal = FTA_TAUGBll.reel_group_raw_dal(data)
        elif data.MachineName == "21":
            dal = FTA_AUGBll.reel_group_raw_dal(data)
        elif data.MachineName == "C1":
            dal = FTA_AUG_C1Bll.reel_group_raw_dal(data)
        else:
            dal = None

        if dal is None:
            return None
        rst = dal.query(data)
        return rst

    def browseTag(self, data):
        # if data.MachineName == "19":
        #     dal = FTA_SAUGBll.group_raw_dal(data.TagName)
        # el
        if data.MachineName == "20":
            dal = FTA_TAUGBll.tag_raw_dal(data.TagName)
        elif data.MachineName == "21":
            dal = FTA_AUGBll.tag_raw_dal(data.TagName)
        # elif data.MachineName == "C1":
        #     dal = FTA_AUG_C1Bll.group_raw_dal(data.TagName)
        else:
            dal = None

        if dal is None:
            return None
        rst = dal.query(data)
        return rst


class FTA_SAUGBll:
    @staticmethod
    def group_raw_dal(argument: str):
        switcher = {
            "CARL": CARL_avgDal(),
        }
        return switcher.get(argument, None)

    @staticmethod
    def reel_group_raw_dal(data):
        tag_names = ["CARL"]
        if data.TagName in tag_names:
            data.Category = data.TagName
        return PM19_AUG_AVG_REELDal()


class FTA_TAUGBll:
    @staticmethod
    def group_raw_interval_dal(argument: str):
        switcher = {
            "BWRL": BWRL_avgDal(),
            "CoatingWeight": PM20_CoatingWeightDal(),
            "ODRL_A": ODRL_A_avgDal(),
            "ODSP_A": ODSP_A_avgDal(),
            "PMRL_A": PMRL_A_avgDal(),
            "PMRL": PMRL_avgDal(),
            "PMSP_A": PMSP_A_avgDal(),
        }
        return switcher.get(argument, None)

    @staticmethod
    def group_raw_dal(argument: str):
        switcher = {
            "BWRL": BWRL_avgDal(),
            "CoatingWeight": PM20_CoatingWeightDal(),
            "ODRL_A": ODRL_A_avgDal(),
            "ODSP_A": ODSP_A_avgDal(),
            "PMRL_A": PMRL_A_avgDal(),
            "PMRL": PMRL_avgDal(),
            "PMSP_A": PMSP_A_avgDal(),
        }
        return switcher.get(argument, None)

    @staticmethod
    def reel_group_raw_dal(data):
        # if data.TagName == "BWRL":
        #     data.Category = "BWRL"
        #     return PM20_AUG_AVG_REELDal()
        # elif data.TagName == "CoatingWeight":
        #     data.Category = "CoatingWeight"
        #     return PM20_AUG_AVG_REELDal()
        # elif data.TagName == "ODSP_A":
        #     data.Category = "ODSP_A"
        #     return PM20_AUG_AVG_REELDal()
        # elif data.TagName == "ODRL_A":
        #     data.Category = "ODRL_A"
        #     return PM20_AUG_AVG_REELDal()
        # elif data.TagName == "PMRL_A":
        #     data.Category = "PMRL_A"
        #     return PM20_AUG_AVG_REELDal()
        # elif data.TagName == "PMRL":
        #     data.Category = "PMRL"
        #     return PM20_AUG_AVG_REELDal()
        # elif data.TagName == "PMSP_A":
        #     data.Category = "PMSP_A"
        #     return PM20_AUG_AVG_REELDal()
        # else:
        #     return PM20_AUG_AVG_REELDal()
        tag_names = ["BWRL", "CoatingWeight", "ODSP_A", "ODRL_A", "PMRL_A", "PMRL", "PMSP_A"]
        if data.TagName in tag_names:
            data.Category = data.TagName
        return PM20_AUG_AVG_REELDal()

    @staticmethod
    def tag_raw_dal(argument: str):
        switcher = {
            "BWRL": BWRL_raw_avgDal(),
            "CoatingWeight": PM20_CoatingWeight_rawDal(),
            "ODRL_A": ODRL_A_raw_avgDal(),
            "ODSP_A": ODSP_A_raw_avgDal(),
            "PMRL_A": PMRL_A_raw_avgDal(),
            "PMRL": PMRL_raw_avgDal(),
            "PMSP_A": PMSP_A_raw_avgDal(),
        }
        return switcher.get(argument, None)


class FTA_AUGBll:
    @staticmethod
    def group_raw_interval_dal(argument: str):
        switcher = {
            "P21-BW1-SP": BW1SP_avgDal(),
            "P21-BW1-RL": BW1RL_avgDal(),
            "P21-MO1-SP": MO1SP_avgDal(),
            "P21-MO1-RL": MO1RL_avgDal(),
            "CoatingWeight": PM21_CoatingWeightDal(),
        }
        return switcher.get(argument, None)
    
    @staticmethod
    def group_raw_dal(argument: str):
        switcher = {
            "P21-BW1-SP": BW1SP_avgDal(),
            "P21-BW1-RL": BW1RL_avgDal(),
            "P21-MO1-SP": MO1SP_avgDal(),
            "P21-MO1-RL": MO1RL_avgDal(),
            "CoatingWeight": PM21_CoatingWeightDal(),
        }
        return switcher.get(argument, None)

    @staticmethod
    def reel_group_raw_dal(data):
        tag_names = ["P21-BW1-SP", "P21-BW1-RL", "P21-MO1-SP", "P21-MO1-RL", "CoatingWeight"]
        if data.TagName in tag_names:
            data.Category = data.TagName
        return PM21_AUG_AVG_REELDal()

    @staticmethod
    def tag_raw_dal(argument: str):
        switcher = {
            "P21-BW1-SP": BW1SP_raw_avgDal(),
            "P21-BW1-RL": BW1RL_raw_avgDal(),
            "P21-MO1-SP": MO1SP_raw_avgDal(),
            "P21-MO1-RL": MO1RL_raw_avgDal(),
            "CoatingWeight": PM21_CoatingWeight_rawDal(),
        }
        return switcher.get(argument, None)


class FTA_AUG_C1Bll:
    @staticmethod
    def group_raw_dal(argument: str):
        switcher = {
            "CM8_MP1": CM8_MP1_avgDal(),
            "CM8_MP2": CM8_MP2_avgDal(),
        }
        return switcher.get(argument, None)

    @staticmethod
    def reel_group_raw_dal(data):
        tag_names = ["CM8_MP1", "CM8_MP2"]
        if data.TagName in tag_names:
            data.Category = data.TagName
        return PM21_OMC1_AVG_REELDal()
