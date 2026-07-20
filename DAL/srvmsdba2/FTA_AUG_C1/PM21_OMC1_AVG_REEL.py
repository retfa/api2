import json
import logging
import os
import pandas as pd
import pyodbc
import datetime
from flask import current_app
from sqlalchemy import and_, create_engine, String, Integer, DateTime, Boolean, DECIMAL
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
class PM21_OMC1_AVG_REEL(Base):
    __tablename__ = 'PM21_OMC1_AVG_REEL'
    relno: Mapped[str] = mapped_column(String(8), primary_key=True)
    ptype: Mapped[str] = mapped_column(String(4))
    gramg: Mapped[float] = mapped_column(DECIMAL)
    stime: Mapped[str] = mapped_column(DateTime)
    etime: Mapped[str] = mapped_column(DateTime)
    G01: Mapped[float] = mapped_column(DECIMAL)
    G02: Mapped[float] = mapped_column(DECIMAL)
    G03: Mapped[float] = mapped_column(DECIMAL)
    G04: Mapped[float] = mapped_column(DECIMAL)
    G05: Mapped[float] = mapped_column(DECIMAL)
    G06: Mapped[float] = mapped_column(DECIMAL)
    G07: Mapped[float] = mapped_column(DECIMAL)
    G08: Mapped[float] = mapped_column(DECIMAL)
    G09: Mapped[float] = mapped_column(DECIMAL)
    G10: Mapped[float] = mapped_column(DECIMAL)
    G11: Mapped[float] = mapped_column(DECIMAL)
    G12: Mapped[float] = mapped_column(DECIMAL)
    G13: Mapped[float] = mapped_column(DECIMAL)
    G14: Mapped[float] = mapped_column(DECIMAL)
    G15: Mapped[float] = mapped_column(DECIMAL)
    G16: Mapped[float] = mapped_column(DECIMAL)
    G17: Mapped[float] = mapped_column(DECIMAL)
    G18: Mapped[float] = mapped_column(DECIMAL)
    G19: Mapped[float] = mapped_column(DECIMAL)
    G20: Mapped[float] = mapped_column(DECIMAL)
    G21: Mapped[float] = mapped_column(DECIMAL)
    G22: Mapped[float] = mapped_column(DECIMAL)
    G23: Mapped[float] = mapped_column(DECIMAL)
    G24: Mapped[float] = mapped_column(DECIMAL)
    G25: Mapped[float] = mapped_column(DECIMAL)
    G26: Mapped[float] = mapped_column(DECIMAL)
    G27: Mapped[float] = mapped_column(DECIMAL)
    G28: Mapped[float] = mapped_column(DECIMAL)
    G29: Mapped[float] = mapped_column(DECIMAL)
    G30: Mapped[float] = mapped_column(DECIMAL)
    G31: Mapped[float] = mapped_column(DECIMAL)
    G32: Mapped[float] = mapped_column(DECIMAL)
    G33: Mapped[float] = mapped_column(DECIMAL)
    G34: Mapped[float] = mapped_column(DECIMAL)
    G35: Mapped[float] = mapped_column(DECIMAL)
    G36: Mapped[float] = mapped_column(DECIMAL)
    G37: Mapped[float] = mapped_column(DECIMAL)
    G38: Mapped[float] = mapped_column(DECIMAL)
    G39: Mapped[float] = mapped_column(DECIMAL)
    G40: Mapped[float] = mapped_column(DECIMAL)
    G41: Mapped[float] = mapped_column(DECIMAL)
    G42: Mapped[float] = mapped_column(DECIMAL)
    G43: Mapped[float] = mapped_column(DECIMAL)
    G44: Mapped[float] = mapped_column(DECIMAL)
    G45: Mapped[float] = mapped_column(DECIMAL)
    G46: Mapped[float] = mapped_column(DECIMAL)
    G47: Mapped[float] = mapped_column(DECIMAL)
    G48: Mapped[float] = mapped_column(DECIMAL)
    G49: Mapped[float] = mapped_column(DECIMAL)
    G50: Mapped[float] = mapped_column(DECIMAL)
    G51: Mapped[float] = mapped_column(DECIMAL)
    G52: Mapped[float] = mapped_column(DECIMAL)
    G53: Mapped[float] = mapped_column(DECIMAL)
    G54: Mapped[float] = mapped_column(DECIMAL)
    G55: Mapped[float] = mapped_column(DECIMAL)
    G56: Mapped[float] = mapped_column(DECIMAL)
    G57: Mapped[float] = mapped_column(DECIMAL)
    G58: Mapped[float] = mapped_column(DECIMAL)
    G59: Mapped[float] = mapped_column(DECIMAL)
    G60: Mapped[float] = mapped_column(DECIMAL)
    G61: Mapped[float] = mapped_column(DECIMAL)
    G62: Mapped[float] = mapped_column(DECIMAL)
    G63: Mapped[float] = mapped_column(DECIMAL)
    G64: Mapped[float] = mapped_column(DECIMAL)
    G65: Mapped[float] = mapped_column(DECIMAL)
    G66: Mapped[float] = mapped_column(DECIMAL)
    G67: Mapped[float] = mapped_column(DECIMAL)
    G68: Mapped[float] = mapped_column(DECIMAL)
    G69: Mapped[float] = mapped_column(DECIMAL)
    G70: Mapped[float] = mapped_column(DECIMAL)
    G71: Mapped[float] = mapped_column(DECIMAL)
    Category: Mapped[str] = mapped_column(String(50))
    # bdtm: Mapped[str] = mapped_column(DateTime)


class PM21_OMC1_AVG_REELDal:
    def __init__(self):
        trace_msg = f'{self.__class__.__name__}'
        print(trace_msg)
        logging.info(trace_msg)
        try:
            # json_path = os.path.join(current_app.config['folders']['exe'], 'appsettings.json')
            # print(f'appsettings.json_path: {json_path}')
            # with open(json_path, 'r') as file:
            #     _config = json.load(file)
            # DbHostName = _config["Database"]["HostName"]

            json_connections_path = os.path.join(current_app.config['folders']['temproot'], 'connections.json')
            print(f'json_path: {json_connections_path}')
            cs_name = 'SRVMSDBA2_FTA_AUG_C1'
            print(cs_name)

            connection_string = get_connection_string(json_connections_path, cs_name)
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

            # if filter.get('DtFrom') is not None:
            #     filter_conditions.append(PM21_OMC1_AVG_REEL.fta_dtm >= filter['DtFrom'])

            # if filter.get('DtTo') is not None:
            #     filter_conditions.append(PM21_OMC1_AVG_REEL.fta_dtm < filter['DtTo'])

            print(len(filter.get('ReelNo')))
            if filter.get('ReelNo') is not None and len(filter.get('ReelNo')) > 0:
                # filter_conditions.append(BW1RL_avg.relno in (filter['ReelNo']))
                filter_conditions.append(PM21_OMC1_AVG_REEL.relno.in_(tuple(filter['ReelNo'])))

            if filter.get('PaperCode') is not None:
                filter_conditions.append(PM21_OMC1_AVG_REEL.ptype == filter['PaperCode'])

            if filter.get('BaseWeight') is not None:
                filter_conditions.append(PM21_OMC1_AVG_REEL.gramg == filter['BaseWeight'])

            if filter.get('Category') is not None:
                filter_conditions.append(PM21_OMC1_AVG_REEL.Category == filter['Category'])

            final_filter_condition = and_(*filter_conditions)
            query = session.query(PM21_OMC1_AVG_REEL).filter(final_filter_condition)
            result_df = pd.read_sql(query.statement, session.bind)
            print(f'records: {len(result_df.index)}')
            datetime_columns = result_df.select_dtypes(include=['datetime64[ns]']).columns
            print(f'datetime_columns: {datetime_columns}')
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

    def select(self, filter):
        try:
            session = self.Session()
            filter_conditions = []

            if filter.get('user_id') is not None:
                filter_conditions.append(BW1RL_avg.user_id == filter['user_id'])

            if filter.get('progm_id') is not None:
                filter_conditions.append(BW1RL_avg.progm_id == filter['progm_id'])

            filter_conditions.append(BW1RL_avg.IsEnabled == 1)
            final_filter_condition = and_(*filter_conditions)
            query = session.query(BW1RL_avg).filter(final_filter_condition)
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
