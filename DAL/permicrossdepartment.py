import json
import logging
import os
import pandas as pd
import pyodbc
import datetime
from flask import current_app
from sqlalchemy import and_, create_engine, String, Integer, DateTime, Boolean
from sqlalchemy.exc import OperationalError
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.sql import func
from common import add_to_dict, get_connection_string


class Base_add(DeclarativeBase):
    pass


class zdpermicrossdept_add(Base_add):
    __tablename__ = 'zdpermicrossdept'
    Sn: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[str] = mapped_column(String(9))
    progm_id: Mapped[str] = mapped_column(String(20))
    departments: Mapped[str] = mapped_column(String(100))
    IsEnabled: Mapped[bool] = mapped_column(Boolean)
    busr: Mapped[str] = mapped_column(String(5))


class Base(DeclarativeBase):
    pass


@add_to_dict
class zdpermicrossdept(Base):
    __tablename__ = 'zdpermicrossdept'
    Sn: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[str] = mapped_column(String(9))
    progm_id: Mapped[str] = mapped_column(String(20))
    departments: Mapped[str] = mapped_column(String(100))
    IsEnabled: Mapped[bool] = mapped_column(Boolean)
    busr: Mapped[str] = mapped_column(String(5))
    bdtm: Mapped[str] = mapped_column(DateTime)
    musr: Mapped[str] = mapped_column(String(5))
    mdtm: Mapped[datetime.datetime] = mapped_column(DateTime)


class PermissionCrossDepartmentDal:
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
            self.engine = create_engine(connection_string, echo=True)
            self.Session = sessionmaker(bind=self.engine)

        except Exception as e:
            msg = f'{self.__class__.__name__} |An error occurred: {str(e)}'
            print(msg)
            logging.debug(msg)

    def query(self, filter):
        try:
            session = self.Session()
            filter_conditions = []

            if filter.get('user_id') is not None:
                filter_conditions.append(zdpermicrossdept.user_id == filter['user_id'])

            if filter.get('progm_id') is not None:
                filter_conditions.append(zdpermicrossdept.progm_id == filter['progm_id'])

            filter_conditions.append(zdpermicrossdept.IsEnabled == 1)
            final_filter_condition = and_(*filter_conditions)
            query = session.query(zdpermicrossdept).filter(final_filter_condition)
            result_df = pd.read_sql(query.statement, session.bind)
            datetime_columns = result_df.select_dtypes(include=['datetime64[ns]']).columns
            print(datetime_columns)
            for column in datetime_columns:
                result_df[column] = result_df.apply(lambda x: x[column].strftime('%Y-%m-%d %H:%M:%S')
                                                    if not pd.isna(x[column]) else None, axis=1)
            session.close()

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
            # zmusr=zmuser_add()
            # zmusr.user_id = user.user_id
            # zmusr.user_name = user.user_name
            # zmusr.pwd = user.pwd
            # zmusr.dept_no = user.dept_no
            # zmusr.group_id = user.group_id
            # zmusr.prt=user.prt
            # zmusr.busr=user.busr
            # session.add(zmusr)
            # session.commit()

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

    def update(self, data):
        try:
            session = self.Session()
            zpermicrossdept = session.query(zdpermicrossdept).filter_by(
                user_id=data["user_id"],
                progm_id=data["progm_id"]
            ).first()
            if zpermicrossdept:
                zpermicrossdept.departments = data["departments"]
                if hasattr(data, "IsEnabled"):
                    zpermicrossdept.IsEnabled = data["IsEnabled"]
                zpermicrossdept.musr = data["musr"]
                zpermicrossdept.mdtm = func.sysdatetime()
                session.merge(zpermicrossdept)
            session.commit()
            return data

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

    def upsert(self, data):
        try:
            session = self.Session()
            zpermicrossdept = session.query(zdpermicrossdept).filter_by(
                user_id=data["user_id"],
                progm_id=data["progm_id"]
            ).first()
            if zpermicrossdept:
                zpermicrossdept.departments = data["departments"]
                if hasattr(data, "IsEnabled"):
                    zpermicrossdept.IsEnabled = data["IsEnabled"]
                zpermicrossdept.musr = data["musr"]
                zpermicrossdept.mdtm = func.sysdatetime()
                session.merge(zpermicrossdept)
            else:
                zpermicrossdept = zdpermicrossdept_add()
                zpermicrossdept.user_id = data["user_id"]
                zpermicrossdept.progm_id = data["progm_id"]
                zpermicrossdept.departments = data["departments"]
                zpermicrossdept.IsEnabled = 1
                zpermicrossdept.busr = data["busr"]
                session.add(zpermicrossdept)

            session.commit()
            return data

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

    def select(self, filter):
        try:
            session = self.Session()
            filter_conditions = []

            if filter.get('user_id') is not None:
                filter_conditions.append(zdpermicrossdept.user_id == filter['user_id'])

            if filter.get('progm_id') is not None:
                filter_conditions.append(zdpermicrossdept.progm_id == filter['progm_id'])

            filter_conditions.append(zdpermicrossdept.IsEnabled == 1)
            final_filter_condition = and_(*filter_conditions)
            query = session.query(zdpermicrossdept).filter(final_filter_condition)
            result_df = pd.read_sql(query.statement, session.bind)
            datetime_columns = result_df.select_dtypes(include=['datetime64[ns]']).columns
            print(datetime_columns)
            for column in datetime_columns:
                result_df[column] = result_df.apply(lambda x: x[column].strftime('%Y-%m-%d %H:%M:%S')
                                                    if not pd.isna(x[column]) else None, axis=1)
            session.close()

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

    # def delete_by_upcode(self, data):
    #     try:
    #         session = self.Session()
    #         filter_condition = and_(
    #             zpermission.user_id == data['user_id'],
    #             zpermission.up_code == data['up_code']
    #         )
    #         matched_data = session.query(zpermission).filter(filter_condition).all()

    #         for data in matched_data:
    #             session.delete(data)

    #         session.commit()
    #         return None
    #     except OperationalError as e:
    #         msg = f'{self.__class__.__name__} |An connection error occurred: {str(e)}'
    #         print(msg)
    #         logging.debug(msg)

    #     except Exception as e:
    #         msg = f'{self.__class__.__name__} |An error occurred: {str(e)}'
    #         print(msg)
    #         logging.debug(msg)

    #     finally:
    #         session.close()
