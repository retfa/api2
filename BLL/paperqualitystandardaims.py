from DAL.srvmsdba1.AIMSFTAB.bdefectstandard_m import bdefectstandard_mDal
from icecream import ic


class PaperQualityStandardAimsBll:
    def browse(self, data):
        mnameMapper = {"18": "R", "19": "S", "20": "T", "21": "W", "C1": "C1"}
        tagNameMapper = {}
        tagNameMapper['19'] = {"CARL": "ThicknessAfterCoating", "19": "S", "20": "T", "21": "W", "C1": "C1"}
        tagNameMapper['20'] = {"BWRL": "", "CoatingWeight": "CoatingWeight", "ODRL_A": "AbsoluteDryAfterCoating", "ODSP_A": "none", "PMRL_A": "WaterAfterCoating", "PMRL": "MoistureAfterHumidification", "PMSP_A": "none"}
        tagNameMapper['21'] = {"CoatingWeight": "CoatingWeight", "P21-BW1-RL": "BaseWeightAfterCoating", "P21-BW1-SP": "none", "P21-MO1-RL": "WaterAfterCoating", "P21-MO1-SP": "none"}
        tagNameMapper['C1'] = {"CM8_MP1": "none", "CM8_MP2": "none"}
        if 'MachineName' in data and data['MachineName'] in mnameMapper:
            data['MachineCode'] = mnameMapper[data['MachineName']]

        if 'MachineName' in data and data['MachineName'] in tagNameMapper:
            machine_mapper = tagNameMapper[data['MachineName']]
            if 'TagName' in data and data['TagName'] in machine_mapper:
                data['TagNameOrigin'] = data['TagName']
                data['TagName'] = machine_mapper[data['TagName']]
        else:
            return None
        dal = bdefectstandard_mDal()
        rst = dal.query(data)
        # ic(type(rst))
        for result in rst:
            # ic(type(result))
            result['TagName'] = data['TagNameOrigin']
        return rst
