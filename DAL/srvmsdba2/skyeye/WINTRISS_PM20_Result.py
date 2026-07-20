import logging
import os
import pandas as pd
from flask import current_app
from sqlalchemy import and_, create_engine, String, Integer, Boolean, DECIMAL, text
from sqlalchemy.exc import OperationalError
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from common import add_to_dict, get_connection_string
from icecream import ic


class Base(DeclarativeBase):
    pass


# @add_to_dict
# class FTA_PM20_consumption(Base):
#     __tablename__ = 'FTA_PM20_consumption'
#     Sn: Mapped[int] = mapped_column(Integer, primary_key=True)
#     relno: Mapped[str] = mapped_column(String(20))
#     ptype: Mapped[str] = mapped_column(String(4))
#     gramg: Mapped[float] = mapped_column(DECIMAL)
#     ProductWeight: Mapped[float] = mapped_column(DECIMAL)
#     category: Mapped[str] = mapped_column(String(255))


class WINTRISS_PM20_Result:
    def __init__(self):
        trace_msg = f'{self.__class__.__name__}'
        ic(trace_msg)
        logging.info(trace_msg)
        try:
            # json_path = os.path.join(current_app.config['folders']['exe'], 'appsettings.json')
            # ic(f'appsettings.json_path: {json_path}')
            # with open(json_path, 'r') as file:
            #     _config = json.load(file)
            # DbHostName = _config["Database"]["HostName"]

            json_connections_path = os.path.join(current_app.config['folders']['temproot'], 'connections.json')
            ic(f'json_path: {json_connections_path}')
            cs_name = 'SRVMSBA2_FTA_EN_Summary'
            ic(cs_name)

            connection_string = get_connection_string(json_connections_path, cs_name)
            self.engine = create_engine(connection_string, echo=True)
            self.Session = sessionmaker(bind=self.engine)

        except Exception as e:
            msg = f'{self.__class__.__name__} |An error occurred: {str(e)}'
            ic(msg)
            logging.debug(msg)

    def query(self, filter):
        try:
            session = self.Session()
            filter_conditions = []
            filter_conditions.append("RowNum = 1")
            if filter.get('DtFrom') is not None and filter.get('DtTo') is not None:
                filter_conditions.append("fta_dtm >:pdateStart AND fta_dtm<=:pdateEnd")

            if filter.get('ReelNo') is not None and len(filter.get('ReelNo')) > 0:
                filter_conditions.append("relno IN ({})".format(",".join("'{}'".format(reel) for reel in filter['ReelNo'])))

            if filter.get('PaperCode') is not None:
                filter_conditions.append("ptype = :ptype")

            if filter.get('BaseWeight') is not None:
                filter_conditions.append("gramg = :gramg")

            sqlcmd = f"""
;WITH RankedData
AS
(
	SELECT [fta_dtm]
      ,[value]
      ,[relno]
      ,[ptype]
      ,[gramg]
      ,[category]                                                                                                                                                                                   
	,      ROW_NUMBER() OVER (PARTITION BY DATEPART(YEAR, fta_dtm), DATEPART(MONTH, fta_dtm), DATEPART(DAY, fta_dtm), DATEPART(HOUR, fta_dtm), DATEPART(MINUTE, fta_dtm) ORDER BY fta_dtm DESC) AS RowNum
	FROM [FTA_EN_Summary].[dbo].[FTA_PM20_consumption]
	WHERE category=:category
)
SELECT fta_dtm, value, relno, ptype, gramg, category
FROM RankedData
            """
            if filter_conditions:
                sqlcmd += " WHERE " + " AND ".join(filter_conditions)
            sqlcmd += " ORDER BY fta_dtm"
            ic(sqlcmd)
            sql_query = text(sqlcmd)
            params = {
                'category': filter['TagName'],
                'pdateStart': filter['DtFrom'],
                'pdateEnd': filter['DtTo'],
                'ptype': filter['PaperCode'],
                'gramg': filter['BaseWeight'],
            }
            result_df = pd.read_sql(sql_query, session.bind, params=params)

            ic(f'records: {len(result_df.index)}')
            ic(result_df)
            datetime_columns = result_df.select_dtypes(include=['datetime64[ns]']).columns
            ic(datetime_columns)
            for column in datetime_columns:
                result_df[column] = result_df.apply(lambda x: x[column].strftime('%Y-%m-%d %H:%M:%S')
                                                    if not pd.isna(x[column]) else None, axis=1)
            session.close()

            # Convert DataFrame to a list of dictionaries
            result_dict_list_df = result_df.to_dict(orient='records')

            return result_dict_list_df
        except OperationalError as e:
            msg = f'{self.__class__.__name__} |An connection error occurred: {str(e)}'
            ic(msg)
            logging.debug(msg)
        except Exception as e:
            msg = f'{self.__class__.__name__} |An error occurred: {str(e)}'
            ic(msg)
            logging.debug(msg)
        finally:
            session.close()
