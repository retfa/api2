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
class ODRL_A_avg(Base):
    __tablename__ = 'ODRL_A_avg'
    fta_dtm: Mapped[str] = mapped_column(DateTime, primary_key=True)
    relno: Mapped[str] = mapped_column(String(8))
    ptype: Mapped[str] = mapped_column(String(4))
    gramg: Mapped[float] = mapped_column(DECIMAL)
    G001: Mapped[float] = mapped_column(DECIMAL)
    G002: Mapped[float] = mapped_column(DECIMAL)
    G003: Mapped[float] = mapped_column(DECIMAL)
    G004: Mapped[float] = mapped_column(DECIMAL)
    G005: Mapped[float] = mapped_column(DECIMAL)
    G006: Mapped[float] = mapped_column(DECIMAL)
    G007: Mapped[float] = mapped_column(DECIMAL)
    G008: Mapped[float] = mapped_column(DECIMAL)
    G009: Mapped[float] = mapped_column(DECIMAL)
    G010: Mapped[float] = mapped_column(DECIMAL)
    G011: Mapped[float] = mapped_column(DECIMAL)
    G012: Mapped[float] = mapped_column(DECIMAL)
    G013: Mapped[float] = mapped_column(DECIMAL)
    G014: Mapped[float] = mapped_column(DECIMAL)
    G015: Mapped[float] = mapped_column(DECIMAL)
    G016: Mapped[float] = mapped_column(DECIMAL)
    G017: Mapped[float] = mapped_column(DECIMAL)
    G018: Mapped[float] = mapped_column(DECIMAL)
    G019: Mapped[float] = mapped_column(DECIMAL)
    G020: Mapped[float] = mapped_column(DECIMAL)
    G021: Mapped[float] = mapped_column(DECIMAL)
    G022: Mapped[float] = mapped_column(DECIMAL)
    G023: Mapped[float] = mapped_column(DECIMAL)
    G024: Mapped[float] = mapped_column(DECIMAL)
    G025: Mapped[float] = mapped_column(DECIMAL)
    G026: Mapped[float] = mapped_column(DECIMAL)
    G027: Mapped[float] = mapped_column(DECIMAL)
    G028: Mapped[float] = mapped_column(DECIMAL)
    G029: Mapped[float] = mapped_column(DECIMAL)
    G030: Mapped[float] = mapped_column(DECIMAL)
    G031: Mapped[float] = mapped_column(DECIMAL)
    G032: Mapped[float] = mapped_column(DECIMAL)
    G033: Mapped[float] = mapped_column(DECIMAL)
    G034: Mapped[float] = mapped_column(DECIMAL)
    G035: Mapped[float] = mapped_column(DECIMAL)
    G036: Mapped[float] = mapped_column(DECIMAL)
    G037: Mapped[float] = mapped_column(DECIMAL)
    G038: Mapped[float] = mapped_column(DECIMAL)
    G039: Mapped[float] = mapped_column(DECIMAL)
    G040: Mapped[float] = mapped_column(DECIMAL)
    G041: Mapped[float] = mapped_column(DECIMAL)
    G042: Mapped[float] = mapped_column(DECIMAL)
    G043: Mapped[float] = mapped_column(DECIMAL)
    G044: Mapped[float] = mapped_column(DECIMAL)
    G045: Mapped[float] = mapped_column(DECIMAL)
    G046: Mapped[float] = mapped_column(DECIMAL)
    G047: Mapped[float] = mapped_column(DECIMAL)
    G048: Mapped[float] = mapped_column(DECIMAL)
    G049: Mapped[float] = mapped_column(DECIMAL)
    G050: Mapped[float] = mapped_column(DECIMAL)
    G051: Mapped[float] = mapped_column(DECIMAL)
    G052: Mapped[float] = mapped_column(DECIMAL)
    G053: Mapped[float] = mapped_column(DECIMAL)
    G054: Mapped[float] = mapped_column(DECIMAL)
    G055: Mapped[float] = mapped_column(DECIMAL)
    G056: Mapped[float] = mapped_column(DECIMAL)
    G057: Mapped[float] = mapped_column(DECIMAL)
    G058: Mapped[float] = mapped_column(DECIMAL)
    G059: Mapped[float] = mapped_column(DECIMAL)
    G060: Mapped[float] = mapped_column(DECIMAL)
    G061: Mapped[float] = mapped_column(DECIMAL)
    G062: Mapped[float] = mapped_column(DECIMAL)
    G063: Mapped[float] = mapped_column(DECIMAL)
    G064: Mapped[float] = mapped_column(DECIMAL)
    G065: Mapped[float] = mapped_column(DECIMAL)
    G066: Mapped[float] = mapped_column(DECIMAL)
    G067: Mapped[float] = mapped_column(DECIMAL)
    G068: Mapped[float] = mapped_column(DECIMAL)
    G069: Mapped[float] = mapped_column(DECIMAL)
    G070: Mapped[float] = mapped_column(DECIMAL)
    G071: Mapped[float] = mapped_column(DECIMAL)
    G072: Mapped[float] = mapped_column(DECIMAL)
    G073: Mapped[float] = mapped_column(DECIMAL)
    G074: Mapped[float] = mapped_column(DECIMAL)
    G075: Mapped[float] = mapped_column(DECIMAL)
    G076: Mapped[float] = mapped_column(DECIMAL)
    G077: Mapped[float] = mapped_column(DECIMAL)
    G078: Mapped[float] = mapped_column(DECIMAL)
    G079: Mapped[float] = mapped_column(DECIMAL)
    G080: Mapped[float] = mapped_column(DECIMAL)
    G081: Mapped[float] = mapped_column(DECIMAL)
    G082: Mapped[float] = mapped_column(DECIMAL)
    G083: Mapped[float] = mapped_column(DECIMAL)
    G084: Mapped[float] = mapped_column(DECIMAL)
    G085: Mapped[float] = mapped_column(DECIMAL)
    G086: Mapped[float] = mapped_column(DECIMAL)
    G087: Mapped[float] = mapped_column(DECIMAL)
    G088: Mapped[float] = mapped_column(DECIMAL)
    G089: Mapped[float] = mapped_column(DECIMAL)
    G090: Mapped[float] = mapped_column(DECIMAL)
    G091: Mapped[float] = mapped_column(DECIMAL)
    G092: Mapped[float] = mapped_column(DECIMAL)
    G093: Mapped[float] = mapped_column(DECIMAL)
    G094: Mapped[float] = mapped_column(DECIMAL)
    G095: Mapped[float] = mapped_column(DECIMAL)
    G096: Mapped[float] = mapped_column(DECIMAL)
    G097: Mapped[float] = mapped_column(DECIMAL)
    G098: Mapped[float] = mapped_column(DECIMAL)
    G099: Mapped[float] = mapped_column(DECIMAL)
    G100: Mapped[float] = mapped_column(DECIMAL)
    G101: Mapped[float] = mapped_column(DECIMAL)
    G102: Mapped[float] = mapped_column(DECIMAL)
    G103: Mapped[float] = mapped_column(DECIMAL)
    G104: Mapped[float] = mapped_column(DECIMAL)
    G105: Mapped[float] = mapped_column(DECIMAL)
    G106: Mapped[float] = mapped_column(DECIMAL)
    G107: Mapped[float] = mapped_column(DECIMAL)
    G108: Mapped[float] = mapped_column(DECIMAL)
    G109: Mapped[float] = mapped_column(DECIMAL)
    G110: Mapped[float] = mapped_column(DECIMAL)
    G111: Mapped[float] = mapped_column(DECIMAL)
    G112: Mapped[float] = mapped_column(DECIMAL)
    G113: Mapped[float] = mapped_column(DECIMAL)
    G114: Mapped[float] = mapped_column(DECIMAL)
    G115: Mapped[float] = mapped_column(DECIMAL)
    G116: Mapped[float] = mapped_column(DECIMAL)
    G117: Mapped[float] = mapped_column(DECIMAL)
    G118: Mapped[float] = mapped_column(DECIMAL)
    G119: Mapped[float] = mapped_column(DECIMAL)
    G120: Mapped[float] = mapped_column(DECIMAL)

    # bdtm: Mapped[str] = mapped_column(DateTime)


class ODRL_A_avgDal:
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
            cs_name = 'SRVMSDBA2_FTA_TAUG'
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

            if filter.get('DtFrom') is not None:
                filter_conditions.append(ODRL_A_avg.fta_dtm >= filter['DtFrom'])

            if filter.get('DtTo') is not None:
                filter_conditions.append(ODRL_A_avg.fta_dtm < filter['DtTo'])

            print(len(filter.get('ReelNo')))
            if filter.get('ReelNo') is not None and len(filter.get('ReelNo')) > 0:
                # filter_conditions.append(ODRL_A_avg.relno in (filter['ReelNo']))
                filter_conditions.append(ODRL_A_avg.relno.in_(tuple(filter['ReelNo'])))

            if filter.get('ptype') is not None:
                filter_conditions.append(ODRL_A_avg.ptype == filter['ptype'])

            if filter.get('gramg') is not None:
                filter_conditions.append(ODRL_A_avg.gramg == filter['gramg'])

            final_filter_condition = and_(*filter_conditions)
            query = session.query(ODRL_A_avg).filter(final_filter_condition)
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
                filter_conditions.append(ODRL_A_avg.user_id == filter['user_id'])

            if filter.get('progm_id') is not None:
                filter_conditions.append(ODRL_A_avg.progm_id == filter['progm_id'])

            filter_conditions.append(ODRL_A_avg.IsEnabled == 1)
            final_filter_condition = and_(*filter_conditions)
            query = session.query(ODRL_A_avg).filter(final_filter_condition)
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
