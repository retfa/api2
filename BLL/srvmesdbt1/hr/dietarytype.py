from DAL.srvmesdbt1.hr.dietarytype import DietaryTypeDal

class DietaryTypeBll:
    def browse(self, data):
        dal = DietaryTypeDal()
        rst = dal.query()
        print(f'type: {type(rst)}')
        return rst