import decimal
import logging
import os
import pandas as pd
from flask import current_app
import datetime
from sqlalchemy import and_, create_engine, String, Integer, DateTime, Float, DECIMAL
from sqlalchemy.exc import OperationalError
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.sql import func
from sqlalchemy import text
from common import add_to_dict, get_connection_string


class Base(DeclarativeBase):
    pass


@add_to_dict
class BiMachineStopDetails(Base):
    __tablename__ = 'BI_MACHINE_STOP_DETAILS'
    ORG_CODE: Mapped[str] = mapped_column(String(3), primary_key=True)
    STOP_DATE: Mapped[datetime.datetime] = mapped_column(DateTime, primary_key=True)
    MACHINE_CODE: Mapped[str] = mapped_column(String(10))
    STOP_NO: Mapped[str] = mapped_column(String(20), primary_key=True)
    CATALOG_NAME: Mapped[str] = mapped_column(String(20))
    STOP_ITEM_NAME: Mapped[str] = mapped_column(String(20))
    REASON: Mapped[str] = mapped_column(String(1000))
    STOP_MIN: Mapped[int] = mapped_column(Integer)
    LAST_UPDATE_DATE: Mapped[datetime.datetime] = mapped_column(DateTime)
    department: Mapped[str] = mapped_column(String(20))
    busr: Mapped[str] = mapped_column(String(5))
    bdtm: Mapped[datetime.datetime] = mapped_column(DateTime)
    musr: Mapped[str] = mapped_column(String(5))
    mdtm: Mapped[datetime.datetime] = mapped_column(DateTime)
    Is_it_automated: Mapped[int] = mapped_column(Integer)


class edit_Base(DeclarativeBase):
    pass


@add_to_dict
class BiMachineStopDetails_edit(edit_Base):
    __tablename__ = 'BI_MACHINE_STOP_DETAILS'
    ORG_CODE: Mapped[str] = mapped_column(String(3), primary_key=True)
    STOP_DATE: Mapped[datetime.datetime] = mapped_column(DateTime, primary_key=True)
    MACHINE_CODE: Mapped[str] = mapped_column(String(10))
    STOP_NO: Mapped[str] = mapped_column(String(20), primary_key=True)
    CATALOG_NAME: Mapped[str] = mapped_column(String(20))
    STOP_ITEM_NAME: Mapped[str] = mapped_column(String(20))
    REASON: Mapped[str] = mapped_column(String(1000))
    STOP_MIN: Mapped[float] = mapped_column(Float)
    LAST_UPDATE_DATE: Mapped[datetime.datetime] = mapped_column(DateTime)
    department: Mapped[str] = mapped_column(String(20))
    musr: Mapped[str] = mapped_column(String(5))
    mdtm: Mapped[datetime.datetime] = mapped_column(DateTime)
    Is_it_automated: Mapped[int] = mapped_column(Integer)


class log_Base(DeclarativeBase):
    pass


@add_to_dict
class BiMachineStopDetails_edit_log(log_Base):
    __tablename__ = 'BI_MACHINE_STOP_DETAILS_log'
    ID: Mapped[int] = mapped_column(Integer)
    ProductionDate: Mapped[datetime.datetime] = mapped_column(DateTime)
    ItemName: Mapped[str] = mapped_column(String(20), primary_key=True)
    ItemValue: Mapped[float] = mapped_column(Float)
    ItemValue_old: Mapped[float] = mapped_column(Float)
    department: Mapped[str] = mapped_column(String(20))
    musr: Mapped[str] = mapped_column(String(5))
    mdtm: Mapped[str] = mapped_column(DateTime)


class BiMachineStopDetailsDal:
    def __init__(self):
        trace_msg = f'{self.__class__.__name__}'
        print(trace_msg)
        logging.info(trace_msg)
        try:
            json_path = os.path.join(current_app.config['folders']['temproot'], 'connections.json')
            logging.info(f'json_path: {json_path}')
            cs_name = 'SRVBIAPA1_ESG_FTA_MODIFY'
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
            # filter_condition = text("STOP_DATE < :enddate AND STOP_DATE >= :startdate AND department = :department")
            # query = session.query(BiMachineStopDetails).filter(filter_condition).params(
            #     enddate=data['dateTo'],
            #     startdate=data['dateFrom'],
            #     department=data['departmentId']
            # )
            department_ids = [dep.strip() for dep in data['departmentId'].split(",")]

            if len(department_ids) > 0 and department_ids[0] == "all":
                filter_condition = and_(
                    BiMachineStopDetails.STOP_DATE < data['dateTo'],
                    BiMachineStopDetails.STOP_DATE >= data['dateFrom'],
                    # filter_condition_department
                    )
            else:
                filter_condition = and_(
                    BiMachineStopDetails.STOP_DATE < data['dateTo'],
                    BiMachineStopDetails.STOP_DATE >= data['dateFrom'],
                    BiMachineStopDetails.department.in_(department_ids)
                    # filter_condition_department
                    )

            query = session.query(BiMachineStopDetails).filter(filter_condition)
            result_df = pd.read_sql(query.statement, session.bind)
            # print(result_df)
            float_columns = result_df.select_dtypes(include=['float64']).columns
            # print(float_columns)
            for f_col in float_columns:
                result_df[f_col] = result_df.apply(lambda x: x[f_col] if not pd.isna(x[f_col]) else -1, axis=1)
                result_df.loc[:, f_col] = result_df.loc[:, f_col].replace(-1, None)

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

    def Log(self, datum, record):
        log = BiMachineStopDetails_edit_log()
        log.UID = record.UID
        log.ProdDate = record.ProdDate
        log.ItemName = record.ItemName
        log.department = record.department
        log.ItemValue_old = record.ItemValue
        log.ItemValue = datum.ItemValue
        log.musr = datum.musr
        log.mdtm = func.sysdatetime()
        return log
    
    # def select(self, quser_id):
    #     try:
    #         session = self.Session()
    #         rst = session.query(dininguser).filter_by(user_id=quser_id).first()
    #         session.commit()
    #         return rst.to_dict()

    #     except OperationalError as e:
    #         msg = f'{self.__class__.__name__} |An connection error occurred: {str(e)}'
    #         print(msg)
    #         logging.debug(msg)
    #         return e
    #     except Exception as e:
    #         msg = f'{self.__class__.__name__} |An error occurred: {str(e)}'
    #         print(msg)
    #         logging.debug(msg)
    #         return e
    #     finally:
    #         session.close()
