import logging
import os
import pandas as pd
from flask import current_app
import datetime
from sqlalchemy import UnicodeText, and_, create_engine, String, Integer, DateTime, Float, DECIMAL, text
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
class DailyProductionData(Base):
    __tablename__ = 'DailyProductionData'
    ID: Mapped[int] = mapped_column(Integer)
    ProductionDate: Mapped[datetime.datetime] = mapped_column(DateTime, primary_key=True)
    ProductMaterialNo: Mapped[str] = mapped_column(UnicodeText(40), primary_key=True)
    EquipmentNo: Mapped[str] = mapped_column(UnicodeText(240), primary_key=True)
    Production: Mapped[float] = mapped_column(DECIMAL)
    ProductionRate: Mapped[float] = mapped_column(DECIMAL)
    Inbound: Mapped[float] = mapped_column(DECIMAL)
    InboundRate: Mapped[float] = mapped_column(DECIMAL)
    UploadTime: Mapped[datetime.datetime] = mapped_column(DateTime)
    department: Mapped[str] = mapped_column(String(20))
    # busr: Mapped[str] = mapped_column(String(5))
    # bdtm: Mapped[datetime.datetime] = mapped_column(DateTime)
    # musr: Mapped[str] = mapped_column(String(5))
    # mdtm: Mapped[datetime.datetime] = mapped_column(DateTime)
    # Is_it_automated: Mapped[int] = mapped_column(Integer)
    # remark: Mapped[str] = mapped_column(UnicodeText)


class DailyProductionDataDal:
    def __init__(self):
        trace_msg = f'{self.__class__.__name__}'
        print(trace_msg)
        logging.info(trace_msg)
        try:
            json_path = os.path.join(current_app.config['folders']['temproot'], 'connections.json')
            logging.info(f'json_path: {json_path}')
            cs_name = 'SRVBIAPA1_ESG_FTA'
            connection_string = get_connection_string(json_path, cs_name)
            self.engine = create_engine(connection_string, echo=False)
            self.Session = sessionmaker(bind=self.engine)

        except Exception as e:
            msg = f'{self.__class__.__name__} |An error occurred: {str(e)}'
            print(msg)
            logging.debug(msg)

    def query(self, data):
        try:
            session = self.Session()
            if len(data['departments'])!=0:
                departments = ",".join([f"'{item.strip()}'" for item in data['departments'][0]['departments'].split(',')])
            else:
                return
            if departments == "'all'":
                sql_query = text(f"""
                    SELECT fin.*, department
                    FROM [ESG_FTA].[dbo].[DailyProductionData] fin
                    JOIN [ESG_FTA_MODIFY].[dbo].[DailyProductionData] modi on
                    fin.[ProductionDate]       = modi.[ProductionDate]
                    AND fin.[ProductMaterialNo]	   = modi.[ProductMaterialNo]
                    AND fin.[EquipmentNo]		   = modi.[EquipmentNo]
                    where fin.[ProductionDate] = :date
                """)
            else:
                sql_query = text(f"""
                    SELECT fin.*, department
                    FROM [ESG_FTA].[dbo].[DailyProductionData] fin
                    JOIN [ESG_FTA_MODIFY].[dbo].[DailyProductionData] modi on
                    fin.[ProductionDate]       = modi.[ProductionDate]
                    AND fin.[ProductMaterialNo]	   = modi.[ProductMaterialNo]
                    AND fin.[EquipmentNo]		   = modi.[EquipmentNo]
                    where fin.[ProductionDate] = :date
                    AND Department IN ({departments})
                """)
            params = {
                'date': data['dateFrom'],
                # 'departments': ','.join([f"'{item.strip()}'" for item in data['departments'][0]['departments'].split(',')])
            }
            result_df = pd.read_sql(sql_query, session.bind, params=params)
            print(f'length: {len(result_df.index)}')
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

