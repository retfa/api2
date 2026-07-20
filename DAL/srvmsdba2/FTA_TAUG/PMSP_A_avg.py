import json
import logging
import os
import pandas as pd
import pyodbc
import datetime
from flask import current_app
from sqlalchemy import and_, create_engine, String, Integer, DateTime, Boolean, DECIMAL, text
from sqlalchemy.exc import OperationalError
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.sql import func
from common import add_to_dict, get_connection_string
from icecream import ic
from DAL.srvmsdba2.TableBaseClass import GroupTableBase_20


class Base(DeclarativeBase):
    pass


@add_to_dict
class PMSP_A_avg(Base, GroupTableBase_20):
    __tablename__ = 'PMSP_A_avg'


class PMSP_A_avgDal:
    def __init__(self):
        trace_msg = f'{self.__class__.__name__}'
        print(trace_msg)
        logging.info(trace_msg)
        logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)
        try:
            # json_path = os.path.join(current_app.config['folders']['exe'], 'appsettings.json')
            # print(f'appsettings.json_path: {json_path}')
            # with open(json_path, 'r') as file:
            #     _config = json.load(file)
            # DbHostName = _config["Database"]["HostName"]

            json_connections_path = os.path.join(
                current_app.config['folders']['temproot'], 'connections.json')
            print(f'json_path: {json_connections_path}')
            cs_name = 'SRVMSDBA2_FTA_TAUG'
            print(cs_name)

            connection_string = get_connection_string(
                json_connections_path, cs_name)
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
                filter_conditions.append(
                    PMSP_A_avg.fta_dtm >= filter['DtFrom'])

            if filter.get('DtTo') is not None:
                filter_conditions.append(PMSP_A_avg.fta_dtm < filter['DtTo'])

            print(len(filter.get('ReelNo')))
            if filter.get('ReelNo') is not None and len(filter.get('ReelNo')) > 0:
                # filter_conditions.append(PMSP_A_avg.relno in (filter['ReelNo']))
                filter_conditions.append(
                    PMSP_A_avg.relno.in_(tuple(filter['ReelNo'])))

            if filter.get('ptype') is not None:
                filter_conditions.append(PMSP_A_avg.ptype == filter['ptype'])

            if filter.get('gramg') is not None:
                filter_conditions.append(PMSP_A_avg.gramg == filter['gramg'])

            final_filter_condition = and_(*filter_conditions)
            query = session.query(PMSP_A_avg).filter(final_filter_condition)
            result_df = pd.read_sql(query.statement, session.bind)
            print(f'records: {len(result_df.index)}')
            datetime_columns = result_df.select_dtypes(
                include=['datetime64[ns]']).columns
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
                filter_conditions.append(
                    PMSP_A_avg.user_id == filter['user_id'])

            if filter.get('progm_id') is not None:
                filter_conditions.append(
                    PMSP_A_avg.progm_id == filter['progm_id'])

            filter_conditions.append(PMSP_A_avg.IsEnabled == 1)
            final_filter_condition = and_(*filter_conditions)
            query = session.query(PMSP_A_avg).filter(final_filter_condition)
            result_df = pd.read_sql(query.statement, session.bind)
            datetime_columns = result_df.select_dtypes(
                include=['datetime64[ns]']).columns
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

    def query_interval(self, filter):
        try:
            session = self.Session()
            # filter_conditions = []

            iu = filter['IntervalUnit']
            match iu:
                case "DAY":
                    sqlcmd = f"""
;WITH PeriodicData AS (
    SELECT 
        DATEADD(DAY, (DATEDIFF(DAY, 0, fta_dtm) / {int(filter['IntervalValue'])}) * {int(filter['IntervalValue'])}, 0) AS Period,
        MIN(fta_dtm) AS min_dtm
    FROM 
        [FTA_TAUG].[dbo].[PMSP_A_avg]
    WHERE 
        fta_dtm BETWEEN :dtFrom AND :dtTo
    GROUP BY 
        DATEADD(DAY, (DATEDIFF(DAY, 0, fta_dtm) / {int(filter['IntervalValue'])}) * {int(filter['IntervalValue'])}, 0)
)
SELECT 
    *
FROM 
    [FTA_TAUG].[dbo].[PMSP_A_avg] 
INNER JOIN 
    PeriodicData  
    ON fta_dtm = min_dtm
Order by Period
            """
                case "HOUR":
                    sqlcmd = f"""
WITH PeriodicData AS (
    SELECT 
        DATEADD(HOUR, (DATEDIFF(HOUR, 0, fta_dtm) / {int(filter['IntervalValue'])}) * {int(filter['IntervalValue'])}, 0) AS Period,
        MIN(fta_dtm) AS min_dtm
    FROM 
        [FTA_TAUG].[dbo].[PMSP_A_avg]
    WHERE 
        fta_dtm BETWEEN :dtFrom AND :dtTo
    GROUP BY 
        DATEADD(HOUR, (DATEDIFF(HOUR, 0, fta_dtm) / {int(filter['IntervalValue'])}) * {int(filter['IntervalValue'])}, 0)
)
SELECT
    tbl.*
FROM
    [FTA_TAUG].[dbo].[PMSP_A_avg] tbl
INNER JOIN
    PeriodicData pd
    ON tbl.fta_dtm = pd.min_dtm
Order by Period
            """
                case "MINUTE":
                    sqlcmd = f"""
;WITH PeriodicData AS (
    SELECT 
        DATEADD(MINUTE, (DATEDIFF(MINUTE, 0, fta_dtm) / {int(filter['IntervalValue'])}) * {int(filter['IntervalValue'])}, 0) AS Period,
        MIN(fta_dtm) AS min_dtm
    FROM 
        [FTA_TAUG].[dbo].[PMSP_A_avg]
    WHERE 
        fta_dtm BETWEEN :dtFrom AND :dtTo
    GROUP BY 
        DATEADD(MINUTE, (DATEDIFF(MINUTE, 0, fta_dtm) / {int(filter['IntervalValue'])}) * {int(filter['IntervalValue'])}, 0)
)
SELECT 
    *
FROM 
    [FTA_TAUG].[dbo].[PMSP_A_avg] 
INNER JOIN 
    PeriodicData  
    ON fta_dtm = min_dtm
Order by Period
            """
                case _:
                    sqlcmd = "SELECT * FROM [FTA_TAUG].[dbo].[PMSP_A_avg] WHERE 1=0"
            # if filter_conditions:
            #     sqlcmd += " WHERE " + " AND ".join(filter_conditions)
            # sqlcmd += " ORDER BY fta_dtm"
            ic(sqlcmd)
            sql_query = text(sqlcmd)
            params = {
                'dtFrom': filter['DtFrom'],
                'dtTo': filter['DtTo'],
                'intervalValue': int(filter['IntervalValue']),
            }
            result_df = pd.read_sql(sql_query, session.bind, params=params)

            ic(f'records: {len(result_df.index)}')
            ic(result_df)
            datetime_columns = result_df.select_dtypes(
                include=['datetime64[ns]']).columns
            ic(datetime_columns)
            match iu:
                case "DAY":
                    for column in datetime_columns:
                        result_df[column] = result_df.apply(lambda x: x[column].strftime('%Y-%m-%d 00:00:00')
                                                            if not pd.isna(x[column]) else None, axis=1)
                case "HOUR":
                    for column in datetime_columns:
                        result_df[column] = result_df.apply(lambda x: x[column].strftime('%Y-%m-%d %H:00:00')
                                                            if not pd.isna(x[column]) else None, axis=1)
                case "MINUTE":
                    for column in datetime_columns:
                        result_df[column] = result_df.apply(lambda x: x[column].strftime('%Y-%m-%d %H:%M:00')
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
