import logging
import os
import pandas as pd
from flask import current_app
from sqlalchemy import create_engine, text, DateTime, Integer, String, Boolean, DECIMAL, SmallInteger, VARCHAR, DateTime, DateTime, Float
from sqlalchemy.dialects.mssql import DATETIMEOFFSET
from sqlalchemy.exc import OperationalError
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from common import add_to_dict, get_connection_string
from icecream import ic


class Base(DeclarativeBase):
    pass


@add_to_dict
class duptjobs(Base):
    __tablename__ = 'duptjobs'

    klKey: Mapped[int] = mapped_column(Integer, primary_key=True, nullable=False)
    Operator: Mapped[str] = mapped_column(String(50), nullable=True)
    CompanyName: Mapped[str] = mapped_column(String(50), nullable=True)
    InspectionType: Mapped[str] = mapped_column(String(50), nullable=True)
    MaterialType: Mapped[str] = mapped_column(String(50), nullable=True)
    OrderNumber: Mapped[str] = mapped_column(String(50), nullable=True)
    JobID: Mapped[str] = mapped_column(String(50), nullable=False)
    StartingDoffSerialNumber: Mapped[int] = mapped_column(Integer, nullable=True)
    Date: Mapped[DateTime] = mapped_column(DateTime, nullable=False)
    fkMCS: Mapped[int] = mapped_column(Integer, nullable=False)
    Comment: Mapped[str] = mapped_column(String(255), nullable=True)
    LastPosition: Mapped[float] = mapped_column(Float, nullable=False)
    LastSpeed: Mapped[float] = mapped_column(Float, nullable=False)
    LastLeftEdge: Mapped[float] = mapped_column(Float, nullable=False)
    LastRightEdge: Mapped[float] = mapped_column(Float, nullable=False)
    Status: Mapped[int] = mapped_column(SmallInteger, nullable=False)
    JobEnd: Mapped[DateTime] = mapped_column(DateTime, nullable=True)
    SourceDB: Mapped[str] = mapped_column(VARCHAR(10), nullable=True)
    FetchDate: Mapped[DateTime] = mapped_column(DateTime, nullable=True)
    JobIDModifiedDate: Mapped[DateTime] = mapped_column(DateTime, nullable=True)
    ModifiedBy: Mapped[int] = mapped_column(Integer, nullable=True)
    ModifiedDate: Mapped[DateTime] = mapped_column(DateTime, nullable=True)
    ModifiedDateOffset: Mapped[DATETIMEOFFSET] = mapped_column(DATETIMEOFFSET, nullable=True)


class duptjobsDal:
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
            cs_name = 'SRVMSDBA1_FlawInspection'
            ic(cs_name)

            connection_string = get_connection_string(json_connections_path, cs_name)
            self.engine = create_engine(connection_string, echo=True)
            self.Session = sessionmaker(bind=self.engine)

        except Exception as e:
            msg = f'{self.__class__.__name__} |An error occurred: {str(e)}'
            ic(msg)
            logging.debug(msg)

    def currentLenth(self, filter):
        try:
            session = self.Session()
            # 自定義 SQL 查詢語句
            sql_query = f"""
SELECT TOP (1)
[LastPosition]
FROM [FlawInspection].[dbo].[duptjobs]
order by Date desc
        """
            # 執行 SQL 查詢
            cond = []
            # cond.append("klKey= @jobKey")
            # cond.append("job.dtTime between @queryStartTime and @queryEndTime")
            params = {}
            # params['JobID'] = f"{data.ReelNo}"

            try:
                where_clause = ""
                if cond and len(cond) > 0:
                    # 使用 AND 運算符將條件組合在一起
                    where_clause = "WHERE " + " AND ".join(cond)
                order_clause = ""
                sql_query = f"{sql_query} {where_clause} {order_clause}"

                result_df = pd.read_sql(text(sql_query), session.bind, params=params)
            except OperationalError as e:
                ic(e)
            except Exception as e:
                ic(e)

            results = []
            session.close()
            # 使用範例：
            results = result_df.to_dict(orient='records')
            return results
    
    
        #     result_dict_list_df = result_df.to_dict(orient='records')

        #     return result_dict_list_df
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


    def query(self, filter):
        try:
            session = self.Session()

            result_df = pd.read_sql(query.statement, session.bind)
            ic(f'records: {len(result_df.index)}')
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
