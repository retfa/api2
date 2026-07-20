import json
import logging
import os
import pandas as pd
import pyodbc
import datetime
from flask import current_app
from icecream import ic
from sqlalchemy import and_, create_engine, String, Integer, DateTime, Boolean, DECIMAL, text
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
class PM21_CoatingWeight(Base):
    __tablename__ = 'PM21_CoatingWeight'
    fta_dtm: Mapped[str] = mapped_column(DateTime, primary_key=True)
    relno: Mapped[str] = mapped_column(String(8))
    ptype: Mapped[str] = mapped_column(String(4))
    gramg: Mapped[float] = mapped_column(DECIMAL)
    group01: Mapped[float] = mapped_column(DECIMAL)
    group02: Mapped[float] = mapped_column(DECIMAL)
    group03: Mapped[float] = mapped_column(DECIMAL)
    group04: Mapped[float] = mapped_column(DECIMAL)
    group05: Mapped[float] = mapped_column(DECIMAL)
    group06: Mapped[float] = mapped_column(DECIMAL)
    group07: Mapped[float] = mapped_column(DECIMAL)
    group08: Mapped[float] = mapped_column(DECIMAL)
    group09: Mapped[float] = mapped_column(DECIMAL)
    group10: Mapped[float] = mapped_column(DECIMAL)
    group11: Mapped[float] = mapped_column(DECIMAL)
    group12: Mapped[float] = mapped_column(DECIMAL)
    group13: Mapped[float] = mapped_column(DECIMAL)
    group14: Mapped[float] = mapped_column(DECIMAL)
    group15: Mapped[float] = mapped_column(DECIMAL)
    group16: Mapped[float] = mapped_column(DECIMAL)
    group17: Mapped[float] = mapped_column(DECIMAL)
    group18: Mapped[float] = mapped_column(DECIMAL)
    group19: Mapped[float] = mapped_column(DECIMAL)
    group20: Mapped[float] = mapped_column(DECIMAL)
    group21: Mapped[float] = mapped_column(DECIMAL)
    group22: Mapped[float] = mapped_column(DECIMAL)
    group23: Mapped[float] = mapped_column(DECIMAL)
    group24: Mapped[float] = mapped_column(DECIMAL)
    group25: Mapped[float] = mapped_column(DECIMAL)
    group26: Mapped[float] = mapped_column(DECIMAL)
    group27: Mapped[float] = mapped_column(DECIMAL)
    group28: Mapped[float] = mapped_column(DECIMAL)
    group29: Mapped[float] = mapped_column(DECIMAL)
    group30: Mapped[float] = mapped_column(DECIMAL)
    group31: Mapped[float] = mapped_column(DECIMAL)
    group32: Mapped[float] = mapped_column(DECIMAL)
    group33: Mapped[float] = mapped_column(DECIMAL)
    group34: Mapped[float] = mapped_column(DECIMAL)
    group35: Mapped[float] = mapped_column(DECIMAL)
    group36: Mapped[float] = mapped_column(DECIMAL)
    group37: Mapped[float] = mapped_column(DECIMAL)
    group38: Mapped[float] = mapped_column(DECIMAL)
    group39: Mapped[float] = mapped_column(DECIMAL)
    group40: Mapped[float] = mapped_column(DECIMAL)
    group41: Mapped[float] = mapped_column(DECIMAL)
    group42: Mapped[float] = mapped_column(DECIMAL)
    group43: Mapped[float] = mapped_column(DECIMAL)
    group44: Mapped[float] = mapped_column(DECIMAL)
    group45: Mapped[float] = mapped_column(DECIMAL)
    group46: Mapped[float] = mapped_column(DECIMAL)
    group47: Mapped[float] = mapped_column(DECIMAL)
    group48: Mapped[float] = mapped_column(DECIMAL)
    group49: Mapped[float] = mapped_column(DECIMAL)
    group50: Mapped[float] = mapped_column(DECIMAL)
    group51: Mapped[float] = mapped_column(DECIMAL)
    group52: Mapped[float] = mapped_column(DECIMAL)
    group53: Mapped[float] = mapped_column(DECIMAL)
    group54: Mapped[float] = mapped_column(DECIMAL)
    group55: Mapped[float] = mapped_column(DECIMAL)
    group56: Mapped[float] = mapped_column(DECIMAL)
    group57: Mapped[float] = mapped_column(DECIMAL)
    group58: Mapped[float] = mapped_column(DECIMAL)
    group59: Mapped[float] = mapped_column(DECIMAL)
    group60: Mapped[float] = mapped_column(DECIMAL)
    group61: Mapped[float] = mapped_column(DECIMAL)
    group62: Mapped[float] = mapped_column(DECIMAL)
    group63: Mapped[float] = mapped_column(DECIMAL)
    group64: Mapped[float] = mapped_column(DECIMAL)
    group65: Mapped[float] = mapped_column(DECIMAL)
    group66: Mapped[float] = mapped_column(DECIMAL)
    group67: Mapped[float] = mapped_column(DECIMAL)
    group68: Mapped[float] = mapped_column(DECIMAL)
    group69: Mapped[float] = mapped_column(DECIMAL)
    group70: Mapped[float] = mapped_column(DECIMAL)
    group71: Mapped[float] = mapped_column(DECIMAL)
    group72: Mapped[float] = mapped_column(DECIMAL)
    group73: Mapped[float] = mapped_column(DECIMAL)
    # bdtm: Mapped[str] = mapped_column(DateTime)


class PM21_CoatingWeightDal:
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
            cs_name = 'SRVMSDBA2_FTA_AUG'
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
                filter_conditions.append(PM21_CoatingWeight.fta_dtm >= filter['DtFrom'])

            if filter.get('DtTo') is not None:
                filter_conditions.append(PM21_CoatingWeight.fta_dtm < filter['DtTo'])

            print(len(filter.get('ReelNo')))
            if filter.get('ReelNo') is not None and len(filter.get('ReelNo')) > 0:
                # filter_conditions.append(PM21_CoatingWeight.relno in (filter['ReelNo']))
                filter_conditions.append(PM21_CoatingWeight.relno.in_(tuple(filter['ReelNo'])))

            if filter.get('ptype') is not None:
                filter_conditions.append(PM21_CoatingWeight.ptype == filter['ptype'])

            if filter.get('gramg') is not None:
                filter_conditions.append(PM21_CoatingWeight.gramg == filter['gramg'])

            final_filter_condition = and_(*filter_conditions)
            query = session.query(PM21_CoatingWeight).filter(final_filter_condition)
            result_df = pd.read_sql(query.statement, session.bind)
            print(f'records: {len(result_df.index)}')

            datetime_columns = result_df.select_dtypes(include=['datetime64[ns]']).columns
            print(f'datetime_columns: {datetime_columns}')
            for column in datetime_columns:
                result_df[column] = result_df.apply(lambda x: x[column].strftime('%Y-%m-%d %H:%M:%S')
                                                    if not pd.isna(x[column]) else None, axis=1)
            session.close()

            # 原始的欄位名稱
            original_columns = result_df.columns.tolist()

            # 將欄位名稱中的"group"全部改成"G"
            new_columns = [col.replace('group', 'G') for col in original_columns]

            # 使用rename函數將欄位名稱改為新的名稱
            result_df.rename(columns=dict(zip(original_columns, new_columns)), inplace=True)

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
                filter_conditions.append(PM21_CoatingWeight.user_id == filter['user_id'])

            if filter.get('progm_id') is not None:
                filter_conditions.append(PM21_CoatingWeight.progm_id == filter['progm_id'])

            filter_conditions.append(PM21_CoatingWeight.IsEnabled == 1)
            final_filter_condition = and_(*filter_conditions)
            query = session.query(PM21_CoatingWeight).filter(final_filter_condition)
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

    def query_interval(self, filter):
        try:
            session = self.Session()
            filter_conditions = []
            # filter_conditions.append("RowNum = 1")
            if filter.get('DtFrom') is not None and filter.get('DtTo') is not None:
                filter_conditions.append(
                    "fta_dtm >:pdateStart AND fta_dtm<=:pdateEnd")

            if filter.get('ReelNo') is not None and len(filter.get('ReelNo')) > 0:
                filter_conditions.append("relno IN ({})".format(
                    ",".join("'{}'".format(reel) for reel in filter['ReelNo'])))

            if filter.get('PaperCode') is not None:
                filter_conditions.append("ptype = :ptype")

            if filter.get('BaseWeight') is not None:
                filter_conditions.append("gramg = :gramg")

            iu = filter['IntervalUnit']
            match iu:
                case "DAY":
                    sqlcmd = f"""
;WITH PeriodicData AS (
    SELECT *,
           ROW_NUMBER() OVER (
               PARTITION BY DATEPART(YEAR, fta_dtm),
                            DATEPART(MONTH, fta_dtm),
                            (DATEPART(DAY, fta_dtm) / :intervalValue)
               ORDER BY fta_dtm
           ) AS rn
    FROM [FTA_AUG].[dbo].[PM21_CoatingWeight]
    WHERE fta_dtm BETWEEN :dtFrom AND :dtTo
)
SELECT *
FROM PeriodicData
WHERE rn = 1;
            """

                case "HOUR":
                    sqlcmd = f"""
;WITH PeriodicData AS (
    SELECT *,
           ROW_NUMBER() OVER (
               PARTITION BY DATEPART(YEAR, fta_dtm),
                            DATEPART(MONTH, fta_dtm),
                            DATEPART(DAY, fta_dtm),
                            (DATEPART(HOUR, fta_dtm) / :intervalValue)
               ORDER BY fta_dtm
           ) AS rn
    FROM [FTA_AUG].[dbo].[PM21_CoatingWeight]
    WHERE fta_dtm BETWEEN :dtFrom AND :dtTo
)
SELECT *
FROM PeriodicData
WHERE rn = 1;
            """
                case "MINUTE":
                    sqlcmd = f"""
;WITH PeriodicData AS (
    SELECT *,
           ROW_NUMBER() OVER (
               PARTITION BY DATEPART(YEAR, fta_dtm),
                            DATEPART(MONTH, fta_dtm),
                            DATEPART(DAY, fta_dtm),
                            DATEPART(HOUR, fta_dtm),
                            (DATEPART(MINUTE, fta_dtm) / :intervalValue)
               ORDER BY fta_dtm
           ) AS rn
    FROM [FTA_AUG].[dbo].[PM21_CoatingWeight]
    WHERE fta_dtm BETWEEN :dtFrom AND :dtTo
)
SELECT *
FROM PeriodicData
WHERE rn = 1;
            """
                case _:
                    sqlcmd = ""
            # if filter_conditions:
            #     sqlcmd += " WHERE " + " AND ".join(filter_conditions)
            # sqlcmd += " ORDER BY fta_dtm"
            ic(sqlcmd)
            sql_query = text(sqlcmd)
            params = {
                'dtFrom': filter['DtFrom'],
                'dtTo': filter['DtTo'],
                'intervalValue': filter['IntervalValue'],
                'intervalUnit': filter['IntervalUnit'],
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
