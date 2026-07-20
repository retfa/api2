import logging
import os
import pandas as pd
from urllib.parse import quote
import datetime
from flask import current_app
from sqlalchemy import create_engine, text, String, Integer, DateTime
from sqlalchemy.exc import OperationalError
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import validates
from sqlalchemy.orm import mapped_column
from sqlalchemy.sql import func
from common import GetJwtPayload, set_security, create_parser, add_to_dict, get_connection_string
from enum import Enum


class GroupIdEnum(Enum):
    ADM = 0
    OFE = 1
    OPR = 2


class Base_add(DeclarativeBase):
    pass


class zmuser_add(Base_add):
    __tablename__ = 'zmuser'
    user_id: Mapped[str] = mapped_column(String(5), primary_key=True)
    user_name: Mapped[str] = mapped_column(String(50))
    pwd: Mapped[str] = mapped_column(String(10))
    dept_no: Mapped[str] = mapped_column(String(50))
    group_id: Mapped[str] = mapped_column(String(5))
    prt: Mapped[str] = mapped_column(String(1))
    busr: Mapped[str] = mapped_column(String(5))
    
    @validates('group_id')
    def validate_group_id(self, key, value):
        if value not in [item.name for item in GroupIdEnum]:
            raise ValueError("group_id must be ADM, OFE, or OPR")
        return value

# class Base_edit(DeclarativeBase):
#     pass
# class zmuser_edit(Base_edit):
#     __tablename__ = 'zmuser'
#     user_id: Mapped[str] = mapped_column(String(5), primary_key=True)
#     user_name: Mapped[str] = mapped_column(String(50))
#     pwd: Mapped[str] = mapped_column(String(10))
#     dept_no: Mapped[str] = mapped_column(String(50))
#     group_id: Mapped[str] = mapped_column(String(5))
#     musr: Mapped[str] = mapped_column(String(5))
#     mdtm: Mapped[str] = mapped_column(DateTime)


class Base(DeclarativeBase):
    pass

@add_to_dict
class zmuser(Base):
    __tablename__ = 'zmuser'
    user_id: Mapped[str] = mapped_column(String(5), primary_key=True)
    user_name: Mapped[str] = mapped_column(String(50))
    pwd: Mapped[str] = mapped_column(String(10))
    dept_no: Mapped[str] = mapped_column(String(50))
    email: Mapped[str] = mapped_column(String(50))
    group_id: Mapped[str] = mapped_column(String(5))
    prt: Mapped[str] = mapped_column(String(1))
    pmdtm: Mapped[str] = mapped_column(DateTime)
    status: Mapped[datetime.datetime] = mapped_column(String(1))
    busr: Mapped[str] = mapped_column(String(5))
    bdtm: Mapped[str] = mapped_column(DateTime)
    musr: Mapped[str] = mapped_column(String(5))
    mdtm: Mapped[datetime.datetime] = mapped_column(DateTime)
    pwderrcount: Mapped[int] = mapped_column(Integer)
    user_id_hris: Mapped[str] = mapped_column(String(9))
    assume_date: Mapped[datetime.datetime] = mapped_column(DateTime)
    leave_date: Mapped[datetime.datetime] = mapped_column(DateTime)
    job_title: Mapped[str] = mapped_column(String(20))
    job_rank: Mapped[int] = mapped_column(Integer)
    no_pay_status: Mapped[int] = mapped_column(Integer)

    @validates('group_id')
    def validate_group_id(self, key, value):
        if value not in [item.name for item in GroupIdEnum]:
            raise ValueError("group_id must be ADM, OFE, or OPR")
        return value


class DepartmentDal:
    def __init__(self):
        try:
            logging.info(self.__class__.__name__)
            json_path = os.path.join(current_app.config['folders']['temproot'], 'connections.json')
            logging.info(f'json_path: {json_path}')
            cs_name = 'SRVMESDBT1_AMIS'
            connection_string = get_connection_string(json_path, cs_name)
            self.engine = create_engine(connection_string, echo=False)
            self.Session = sessionmaker(bind=self.engine)

        except Exception as e:
            msg = f'{self.__class__.__name__} |An error occurred: {str(e)}'
            print(msg)
            logging.debug(msg)

    def to_dict_zmuser(self, zmuser_object):
        user_dict = {
            'user_id': zmuser_object.user_id,
            'user_name': zmuser_object.user_name,
        }
        return user_dict

    def query_zmuser(self):
        try:
            session = self.Session()
            result_df = pd.DataFrame()
            a = {"dept_no": "A", "dept": "-- 廠內單位 --"}
            ap = {"dept_no": "AP", "dept": "-- 廠內單位(prt) --"}
            result_df = pd.concat([result_df, pd.DataFrame([a]), pd.DataFrame([ap])], ignore_index=True)

            query = text('''
select substring(a.dept_no,1,5) as dept_no,(case when b.dept_2 is null then b.dept_1 else b.dept_1+b.dept_2 end) as dept 
from zmuser a,srvad6.hr.dbo.hmdept b
where a.dept_no=b.dept_no and b.status='Y' group by 
substring(a.dept_no,1,5),(case when b.dept_2 is null then b.dept_1 else b.dept_1+b.dept_2 end)
                ''')

            rst = session.execute(query)
            result_df = pd.concat([result_df, pd.DataFrame(rst.fetchall(), columns=result_df.columns)])
            
            b = { "dept_no": "B", "dept": "-- 非廠內單位 --"}
            bp = { "dept_no": "BP", "dept": "-- 非廠內單位(prt) --"}
            result_df = pd.concat([result_df, pd.DataFrame([b]), pd.DataFrame([bp])], ignore_index=True)
            
            query = text('''
select dept_no, dept_no as dept from zmuser where substring(user_id,1,1)<>'A' group by dept_no
                ''')
            rst = session.execute(query)
            result_df = pd.concat([result_df, pd.DataFrame(rst.fetchall(), columns=result_df.columns)])
            
            result_dict_list_df = result_df.to_dict(orient='records')
            return result_dict_list_df
        
        except OperationalError as e:
            msg = f'{self.__class__.__name__} |An connection error occurred: {str(e)}'
            print(msg)
            logging.debug(msg)

        except Exception as e:
            msg = f'{self.__class__.__name__} |An error occurred: {str(e)}'
            print(msg)
            logging.debug(msg)

        finally:
            session.close()