from DAL.program import ProgramDal


class ProgramBll:
    def browse(self, data):
        return data
        dal = ProgramDal()
        rst = dal.query(data)
        return rst

    def add(self, data):
        dal = ProgramDal()
        rst = dal.insert(data)
        return rst

    def read(self, data):
        return data
        dal = ProgramDal()
        rst = dal.select(data)
        return rst

