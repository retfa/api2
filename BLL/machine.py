from DAL.AMIS_dbo_ampudmc import AMIS_dbo_ampudmc_Dal


class MachineBll:
    def browse(self, data):
        dal = AMIS_dbo_ampudmc_Dal()
        return dal.query(data)
