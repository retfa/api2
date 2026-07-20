from DAL.menutree import MenuTreeDal


class MenuTreeBll:
    def browse(self, data):
        dal = MenuTreeDal()
        if data['Node'] == '0':
            return dal.queryroot()
        if data['Node'] == 'all':
            return dal.queryall()
        else:
            return dal.query(node=data['Node'])

    def add(self, data):
        dal = MenuTreeDal()
        return dal.insert(datum=data)
