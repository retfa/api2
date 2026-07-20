class hdtree:
    class hr:
        def __init__(self, hrobj):
            self.chsnm = hrobj.chsnm
            self.team_no = hrobj.team_no
            self.dept = hrobj.dept
            self.og_status = hrobj.og_status
            self.dept_name = hrobj.dept_name
        
        def to_dict(self):
            dict = {
                'chsnm' : self.chsnm,
                'team_no' : self.team_no,
                'dept' : self.dept,
                'og_status' : self.og_status,
                'dept_name' : self.dept_name
                }
            return dict
        
# from flask_restx import fields, Namespace
# ns_user = Namespace('hdtree')