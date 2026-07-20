import json
import logging
import os
import pandas as pd
from flask import current_app
from sqlalchemy import create_engine, String, Integer, DateTime
from sqlalchemy.exc import OperationalError
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.sql import func
from common import add_to_dict, get_connection_string


class Base(DeclarativeBase):
    pass


@add_to_dict
class dininguser(Base):
    __tablename__ = 'dininguser'
    Sn: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[str] = mapped_column(String(3))
    location_code: Mapped[str] = mapped_column(String(3))
    dietary_type_code: Mapped[str] = mapped_column(String(2))
    # stringC: Mapped[str] = mapped_column(String(3))
    # intC: Mapped[int] = mapped_column(Integer)
    # floatC: Mapped[float] = mapped_column(Float)
    # datetimeC: Mapped[datetime.datetime] = mapped_column(DateTime)


class add_edit_Base(DeclarativeBase):
    pass


@add_to_dict
class dininguser_add_edit(add_edit_Base):
    __tablename__ = 'dininguser'
    Sn: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[str] = mapped_column(String(3))
    location_code: Mapped[str] = mapped_column(String(3))
    dietary_type_code: Mapped[str] = mapped_column(String(2))
    busr: Mapped[str] = mapped_column(String(5))
    bdtm: Mapped[str] = mapped_column(DateTime)
    musr: Mapped[str] = mapped_column(String(5))
    mdtm: Mapped[str] = mapped_column(DateTime)
    # stringC: Mapped[str] = mapped_column(String(3))
    # intC: Mapped[int] = mapped_column(Integer)
    # floatC: Mapped[float] = mapped_column(Float)
    # datetimeC: Mapped[datetime.datetime] = mapped_column(DateTime)


class DiningUserDal:
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
            cs_name = f'{DbHostName}_HR'
            print(cs_name)

            connection_string = get_connection_string(json_path, cs_name)
            self.engine = create_engine(connection_string, echo=False)
            self.Session = sessionmaker(bind=self.engine)

        except Exception as e:
            msg = f'{self.__class__.__name__} |An error occurred: {str(e)}'
            print(msg)
            logging.debug(msg)

    def insert(self, tuser: dininguser_add_edit):
        try:
            session = self.Session()
            userObj = dininguser_add_edit()
            for key, value in vars(tuser).items():
                print(f'{key} {value}')
                setattr(userObj, key, value)
            userObj.bdtm = func.sysdatetime()
            session.add(userObj)
            session.commit()

        except OperationalError as e:
            msg = f'{self.__class__.__name__} |An connection error occurred: {str(e)}'
            print(msg)
            logging.debug(msg)
            return e
        except Exception as e:
            msg = f'{self.__class__.__name__} |An error occurred: {str(e)}'
            print(msg)
            logging.debug(msg)
            return e
        finally:
            session.close()

    def query(self, data):
        try:
            session = self.Session()
            result_df = pd.read_sql(session.query(dininguser).statement, session.bind)
            # print(result_df)
            datetime_columns = result_df.select_dtypes(include=['datetime64[ns]']).columns
            print(datetime_columns)
            for column in datetime_columns:
                result_df[column] = result_df.apply(lambda x: x[column].strftime('%Y-%m-%d %H:%M:%S')
                                                    if not pd.isna(x[column]) else None, axis=1)
            result_dict_list_df = result_df.to_dict(orient='records')
            # print(result_dict_list_df)
            return result_dict_list_df

        except OperationalError as e:
            msg = f'{self.__class__.__name__} |An connection error occurred: {str(e)}'
            print(msg)
            logging.debug(msg)
            return e
        except Exception as e:
            msg = f'{self.__class__.__name__} |An error occurred: {str(e)}'
            print(msg)
            logging.debug(msg)
            return e
        finally:
            session.close()

    def update(self, tuser: dininguser_add_edit):
        try:
            session = self.Session()
            user = session.query(dininguser_add_edit).filter_by(user_id=tuser.user_id).first()

            if hasattr(tuser, 'location_code'):
                user.location_code = tuser.location_code
            if hasattr(tuser, 'dietary_type_code'):
                user.dietary_type_code = tuser.dietary_type_code

            user.musr = tuser.musr
            user.mdtm = func.sysdatetime()
            session.merge(user)
            session.commit()

        except OperationalError as e:
            msg = f'{self.__class__.__name__} |An connection error occurred: {str(e)}'
            print(msg)
            logging.debug(msg)
            return e
        except Exception as e:
            msg = f'{self.__class__.__name__} |An error occurred: {str(e)}'
            print(msg)
            logging.debug(msg)
            return e
        finally:
            session.close()

    def select(self, quser_id):
        try:
            session = self.Session()
            rst = session.query(dininguser).filter_by(user_id=quser_id).first()
            session.commit()
            return rst.to_dict()

        except OperationalError as e:
            msg = f'{self.__class__.__name__} |An connection error occurred: {str(e)}'
            print(msg)
            logging.debug(msg)
            return e
        except Exception as e:
            msg = f'{self.__class__.__name__} |An error occurred: {str(e)}'
            print(msg)
            logging.debug(msg)
            return e
        finally:
            session.close()
