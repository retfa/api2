import decimal
import logging
import os
import pandas as pd
from flask import current_app
import datetime
from sqlalchemy import UnicodeText, and_, create_engine, String, Integer, DateTime, Boolean, Float, DECIMAL, text
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
class UploadData(Base):
    __tablename__ = 'UploadData'
    UID: Mapped[int] = mapped_column(Integer)
    ProdDate: Mapped[datetime.datetime] = mapped_column(DateTime, primary_key=True)
    DepartName: Mapped[str] = mapped_column(UnicodeText(20), primary_key=True)
    ClassName: Mapped[str] = mapped_column(UnicodeText(20))
    SubClassName: Mapped[str] = mapped_column(UnicodeText(20))
    ItemName: Mapped[str] = mapped_column(UnicodeText(20), primary_key=True)
    ProcNo: Mapped[str] = mapped_column(UnicodeText(20), primary_key=True)
    ProcCode: Mapped[str] = mapped_column(UnicodeText(20), primary_key=True)
    ProcName: Mapped[str] = mapped_column(UnicodeText(20))
    EquNo: Mapped[str] = mapped_column(UnicodeText(20), primary_key=True)
    EquCode: Mapped[str] = mapped_column(UnicodeText(20), primary_key=True)
    EquName: Mapped[str] = mapped_column(UnicodeText(20))
    IsCHP: Mapped[bool] = mapped_column(Boolean, primary_key=True)
    FuelCode: Mapped[str] = mapped_column(UnicodeText(20), primary_key=True)
    FuelName: Mapped[str] = mapped_column(UnicodeText(20))
    IsBioFuel: Mapped[bool] = mapped_column(Boolean, primary_key=True)
    Category: Mapped[str] = mapped_column(UnicodeText(20))
    DisType: Mapped[str] = mapped_column(UnicodeText(20))
    ItemValue: Mapped[decimal.Decimal] = mapped_column(DECIMAL)
    Unit: Mapped[str] = mapped_column(UnicodeText(20))
    UploadTime: Mapped[datetime.datetime] = mapped_column(DateTime)
    department: Mapped[str] = mapped_column(String(20))
    # busr: Mapped[str] = mapped_column(String(5))
    # bdtm: Mapped[datetime.datetime] = mapped_column(DateTime)
    # musr: Mapped[str] = mapped_column(String(5))
    # mdtm: Mapped[datetime.datetime] = mapped_column(DateTime)
    # Is_it_automated: Mapped[int] = mapped_column(Integer)
    # remark: Mapped[str] = mapped_column(UnicodeText)


class UploadDataDal:
    def __init__(self):
        trace_msg = f'{self.__class__.__name__}'
        print(trace_msg)
        logging.info(trace_msg)
        try:
            json_path = os.path.join(current_app.config['folders']['temproot'], 'connections.json')
            logging.info(f'json_path: {json_path}')
            cs_name = 'SRVBIAPA1_ESG_FTA'
            connection_string = get_connection_string(json_path, cs_name)
            self.engine = create_engine(connection_string, echo=True)
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
                    SELECT fin.*, modi.Department
                    FROM [ESG_FTA].[dbo].[UploadData] fin
                    JOIN [ESG_FTA_MODIFY].[dbo].[UploadData] modi ON
                    fin.[ProdDate] = modi.[ProdDate]
                    AND fin.[DepartName] = modi.[DepartName]
                    AND fin.[ClassName] = modi.[ClassName]
                    AND fin.[SubClassName] = modi.[SubClassName]
                    AND fin.[ItemName] = modi.[ItemName]
                    WHERE fin.ProdDate = :date
                """)
            else:
                sql_query = text(f"""
                    SELECT fin.*, modi.Department
                    FROM [ESG_FTA].[dbo].[UploadData] fin
                    JOIN [ESG_FTA_MODIFY].[dbo].[UploadData] modi ON
                    fin.[ProdDate] = modi.[ProdDate]
                    AND fin.[DepartName] = modi.[DepartName]
                    AND fin.[ClassName] = modi.[ClassName]
                    AND fin.[SubClassName] = modi.[SubClassName]
                    AND fin.[ItemName] = modi.[ItemName]
                    WHERE fin.ProdDate = :date
                    AND modi.Department IN ({departments})
                """)
            params = {
                'date': data['dateFrom'],
                # 'departments': ",".join([f"'{item.strip()}'" for item in data['departments'][0]['departments'].split(',')])
            }
            result_df = pd.read_sql(sql_query, session.bind, params=params)
            print(f'length: {len(result_df.index)}')
            float_columns = result_df.select_dtypes(include=['float64']).columns
            # print(float_columns)
            for f_col in float_columns:
                result_df[f_col] = result_df.apply(lambda x: x[f_col] if not pd.isna(x[f_col]) else -1, axis=1)
                result_df.loc[:, f_col] = result_df.loc[:, f_col].replace(-1, None)

            datetime_columns = result_df.select_dtypes(include=['datetime64[ns]']).columns
            # print(datetime_columns)
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
