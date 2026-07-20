from DAL.menu import MenuDal


class MenuBll:
    def browse(self, data):
        dal = MenuDal()
        if data['Node'] == '0':
            return dal.queryroot(userid=data.jwt["FTAId"])
        else:
            return dal.query(userid=data.jwt["FTAId"], node=data['Node'])
