from DAL.srvmesdbt1.hr.dininguser import DiningUserDal


class DiningUserBll:
    def browse(self, data):
        dal = DiningUserDal()
        rst = dal.query()
        print(f'type: {type(rst)}')
        return rst

    def read(self, data):
        dal = DiningUserDal()
        rst = dal.select(data)
        return rst

    def add(self, data):
        dal = DiningUserDal()
        rst = dal.insert(data)
        return rst

    def edit(self, data):
        dal = DiningUserDal()
        rst = dal.update(data)
        return rst
