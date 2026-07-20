import json
import logging
import os
import pandas as pd
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
from common import add_to_dict, get_connection_string
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
    user_id_hris: Mapped[str] = mapped_column(String(5))
    user_name: Mapped[str] = mapped_column(String(50))
    original_name: Mapped[str] = mapped_column(String(50))
    pwd: Mapped[str] = mapped_column(String(10))
    department_id: Mapped[str] = mapped_column(String(50))
    dept_no: Mapped[str] = mapped_column(String(50))
    email: Mapped[str] = mapped_column(String(50))
    group_id: Mapped[str] = mapped_column(String(5))
    prt: Mapped[str] = mapped_column(String(1))
    busr: Mapped[str] = mapped_column(String(5))
    assume_date: Mapped[datetime.datetime] = mapped_column(DateTime)
    job_title: Mapped[str] = mapped_column(String(5))
    job_rank: Mapped[int] = mapped_column(Integer())

    @validates('group_id')
    def validate_group_id(self, key, value):
        if value not in [item.name for item in GroupIdEnum]:
            raise ValueError("group_id must be ADM, OFE, or OPR")
        return value


class Base(DeclarativeBase):
    pass


@add_to_dict
class zmuser(Base):
    __tablename__ = 'zmuser'
    user_id: Mapped[str] = mapped_column(String(5), primary_key=True)
    user_id_hris: Mapped[str] = mapped_column(String(9))
    user_name: Mapped[str] = mapped_column(String(50))
    original_name: Mapped[str] = mapped_column(String(50))
    pwd: Mapped[str] = mapped_column(String(10))
    department_id: Mapped[str] = mapped_column(String(50))
    dept_no: Mapped[str] = mapped_column(String(50))
    email: Mapped[str] = mapped_column(String(50))
    group_id: Mapped[str] = mapped_column(String(5))
    prt: Mapped[str] = mapped_column(String(1))
    pmdtm: Mapped[str] = mapped_column(DateTime)
    status: Mapped[str] = mapped_column(String(1))
    busr: Mapped[str] = mapped_column(String(5))
    bdtm: Mapped[str] = mapped_column(DateTime)
    musr: Mapped[str] = mapped_column(String(5))
    mdtm: Mapped[datetime.datetime] = mapped_column(DateTime)
    pwderrcount: Mapped[int] = mapped_column(Integer)
    accession_state: Mapped[int] = mapped_column(Integer)
    no_pay_status: Mapped[int] = mapped_column(Integer)
    assume_date: Mapped[datetime.datetime] = mapped_column(DateTime)
    leave_date: Mapped[datetime.datetime] = mapped_column(DateTime)
    job_title: Mapped[str] = mapped_column(String(20))
    job_rank: Mapped[int] = mapped_column(Integer)
    last_sync: Mapped[str] = mapped_column(DateTime)

    @validates('group_id')
    def validate_group_id(self, key, value):
        if value not in [item.name for item in GroupIdEnum]:
            raise ValueError("group_id must be ADM, OFE, or OPR")
        return value


class UserDal:
    def __init__(self):
        trace_msg = f'{self.__class__.__name__}'
        print(trace_msg)
        logging.info(trace_msg)
        try:
            json_path = os.path.join(current_app.config['folders']['exe'], 'appsettings.json')
            print(f'appsettings.json_path: {json_path}')
            with open(json_path, 'r') as file:
                _config = json.load(file)
            DbHostName = _config["Database"]["HostName"]

            json_path = os.path.join(current_app.config['folders']['temproot'], 'connections.json')
            print(f'json_path: {json_path}')
            cs_name = f'{DbHostName}_AMIS'
            print(cs_name)

            connection_string = get_connection_string(json_path, cs_name)
            self.engine = create_engine(connection_string, echo=False)
            self.Session = sessionmaker(bind=self.engine)

        except Exception as e:
            msg = f'{self.__class__.__name__} |An error occurred: {str(e)}'
            print(msg)
            logging.debug(msg)

    def query(self, filter):
        try:
            session = self.Session()
            # conditions = []
            cond = []
            params = {}
            if filter.id:
                # conditions.append(zmuser.user_id.ilike(f"%{filter.id}%"))
                cond.append("a.user_id like :id")
                params['id'] = f"%{filter.id}%"

            if filter.idhris:
                # conditions.append(zmuser.user_id_hris.ilike(f"%{filter.idhris}%"))
                cond.append("a.user_id_hris like :idhris")
                params['idhris'] = f"%{filter.idhris}%"

            if filter.name:
                # conditions.append(zmuser.user_name.ilike(f"%{filter.name}%"))
                cond.append("a.user_name like :name")
                params['name'] = f"%{filter.name}%"

            # if not conditions:
            #     rst = session.query(zmuser)
            # else:
            #     rst = session.query(zmuser).filter(*conditions)

            query = '''
select a.*,b.user_name as busr_name from zmuser a join zmuser b on a.busr = b.user_id
                '''
            if cond:
                # 使用 AND 運算符將條件組合在一起
                where_clause = " AND ".join(cond)
                query = f"{query} WHERE {where_clause}"

            rst = session.execute(text(query), params)
            # sql = rst.statement.compile(dialect=self.engine.dialect)
            # print(sql)

            # Convert the query result to a DataFrame
            result_df = pd.DataFrame(rst.fetchall(), columns=rst.keys())
            # print(result_df)
            # print(result_df.dtypes)

            result_df.astype({
                'accession_state': 'Int64',
                'no_pay_status': 'Int64',
                'job_rank': 'Int64',
            })
            # result_df[['job_rank', 'no_pay_status']].astype(pd.Int16Dtype())
            # print(result_df.dtypes)

            session.close()

            # Format datetime attributes
            float_columns = result_df.select_dtypes(include=['float64']).columns
            # print(float_columns)
            # print(result_df.dtypes["job_rank"])
            for f_col in float_columns:
                result_df[f_col] = result_df.apply(lambda x: x[f_col] if not pd.isna(x[f_col]) else -1, axis=1)
                result_df.loc[:, f_col] = result_df.loc[:, f_col].replace(-1, None)
            # print(result_df.dtypes["job_rank"])
            datetime_columns = result_df.select_dtypes(include=['datetime64[ns]']).columns
            # print(datetime_columns)
            datetime_columns = datetime_columns.union(pd.Index(['bdtm', 'last_sync']))
            # print(datetime_columns)
            for column in datetime_columns:
                result_df[column] = result_df.apply(lambda x: x[column].strftime(
                    '%Y-%m-%d %H:%M:%S') if not pd.isna(x[column]) else None, axis=1)

            result_df = result_df.drop(columns=['pwd', 'pwderrcount'])

            # Convert DataFrame to a list of dictionaries
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

    def insert(self, user):
        try:
            session = self.Session()
            zmusr = zmuser_add()
            zmusr.user_id = user.user_id
            zmusr.user_id_hris = user.user_id_hris
            zmusr.user_name = user.user_name
            zmusr.original_name = user.original_name
            zmusr.pwd = user.pwd
            zmusr.department_id = user.department_id
            if hasattr(user, 'dept_no'):
                zmusr.dept_no = user.dept_no
            zmusr.group_id = user.group_id
            zmusr.email = user.email
            zmusr.assume_date = user.assume_date
            zmusr.job_title = user.job_title
            zmusr.job_rank = user.job_rank
            zmusr.prt = user.prt
            zmusr.busr = user.busr
            session.add(zmusr)
            session.commit()
            return zmusr.user_id
        except OperationalError as e:
            msg = f'{self.__class__.__name__} |An connection error occurred: {str(e)}'
            print(msg)
            logging.debug(msg)
            return -1
        except Exception as e:
            msg = f'{self.__class__.__name__} |An error occurred: {str(e)}'
            print(msg)
            logging.debug(msg)
            return -1
        finally:
            session.close()

    def reset_password(self, user):
        try:
            session = self.Session()
            zmusr = session.query(zmuser).filter_by(user_id=user.user_id).first()
            zmusr.pwd = 'a0000000'
            zmusr.musr = user.musr
            zmusr.mdtm = func.sysdatetime()
            session.merge(zmusr)
            session.commit()

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

    def update_password(self, user):
        try:
            session = self.Session()
            zmusr = session.query(zmuser).filter_by(user_id=user.user_id).first()
            zmusr.pwd = user.new_password
            zmusr.musr = user.musr
            zmusr.mdtm = func.sysdatetime()
            session.merge(zmusr)
            session.commit()

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

    def update_status(self, user):
        try:
            session = self.Session()
            zmusr = session.query(zmuser).filter_by(user_id=user.user_id).first()
            zmusr.status = user.status if user.status == 'Y' else 'N'
            zmusr.musr = user.musr
            zmusr.mdtm = func.sysdatetime()
            session.merge(zmusr)
            session.commit()

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

    def update(self, user):
        try:
            session = self.Session()
            zmusr = session.query(zmuser).filter_by(user_id=user.user_id).first()

            if hasattr(user, 'user_id_hris'):
                zmusr.user_id_hris = user.user_id_hris
            if hasattr(user, 'user_name'):
                zmusr.user_name = user.user_name
            if hasattr(user, 'original_name'):
                zmusr.original_name = user.original_name
            if hasattr(user, 'department_id'):
                zmusr.department_id = user.department_id
            if hasattr(user, 'dept_no'):
                zmusr.dept_no = user.dept_no
            if hasattr(user, 'group_id'):
                zmusr.group_id = user.group_id
            if hasattr(user, 'prt'):
                zmusr.prt = user.prt
            if hasattr(user, 'email'):
                zmusr.email = user.email
            if hasattr(user, 'accession_state'):
                zmusr.accession_state = user.accession_state
            if hasattr(user, 'no_pay_status'):
                zmusr.no_pay_status = user.no_pay_status
            if hasattr(user, 'assume_date'):
                zmusr.assume_date = user.assume_date
            if hasattr(user, 'leave_date'):
                zmusr.leave_date = user.leave_date
            if hasattr(user, 'assume_date'):
                zmusr.assume_date = user.assume_date
            if hasattr(user, 'job_title'):
                zmusr.job_title = user.job_title
            if hasattr(user, 'job_rank'):
                zmusr.job_rank = user.job_rank
            zmusr.musr = user.musr
            zmusr.mdtm = func.sysdatetime()
            session.merge(zmusr)
            session.commit()

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

    def select(self, quser_id):
        try:
            session = self.Session()
            rst = session.query(zmuser).filter_by(user_id=quser_id).first()
            session.commit()
            return rst.to_dict()

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
