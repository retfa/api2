import DAL.dept
import DAL.srvmesdbt1.hr.department


class DepartmentBll:
    def browse_zmuser(self):
        dept_dal = DAL.dept.DepartmentDal()
        rst = dept_dal.query_zmuser()
        return rst

    def browse_hr(self):
        dept_dal = DAL.srvmesdbt1.hr.department.DepartmentDal()
        rst = dept_dal.query_hr()
        return rst
