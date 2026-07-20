from DAL.srvmesdbt1.hr.dininglocation import DiningLocationDal


class DiningLocationBll:
    def browse(self, data):
        dal = DiningLocationDal()
        rst = dal.query()
        print(f'type: {type(rst)}')
        return rst
