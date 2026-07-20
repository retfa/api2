import decimal
import logging
import os
import pandas as pd
from flask import current_app
import datetime
from sqlalchemy import UnicodeText, and_, create_engine, String, Integer, DateTime, Float, DECIMAL
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
class BiAnalysisIndMonthly(Base):
    __tablename__ = 'BI_Analysis_Ind_Monthly'
    ORG_CODE: Mapped[str] = mapped_column(String(3), primary_key=True)
    PERIOD_NAME: Mapped[str] = mapped_column(String(7), primary_key=True)
    DATA_SOURCE: Mapped[str] = mapped_column(String(10))
    MACHINE_CODE: Mapped[str] = mapped_column(UnicodeText(20), primary_key=True)
    INDICATORS_CATEGORY: Mapped[str] = mapped_column(UnicodeText(50), primary_key=True)
    INDICATORS_GROUP: Mapped[str] = mapped_column(UnicodeText(50), primary_key=True)
    INDICATORS_NAME: Mapped[str] = mapped_column(UnicodeText(50), primary_key=True)
    Unit: Mapped[str] = mapped_column(UnicodeText(20))
    MEASURE_VALUE: Mapped[decimal.Decimal] = mapped_column(DECIMAL)
    LAST_UPDATE_DATE: Mapped[datetime.datetime] = mapped_column(DateTime)
    department: Mapped[str] = mapped_column(String(20))
    busr: Mapped[str] = mapped_column(String(5))
    bdtm: Mapped[datetime.datetime] = mapped_column(DateTime)
    musr: Mapped[str] = mapped_column(String(5))
    mdtm: Mapped[datetime.datetime] = mapped_column(DateTime)
    Is_it_automated: Mapped[int] = mapped_column(Integer)
    remark: Mapped[str] = mapped_column(UnicodeText)


class edit_Base(DeclarativeBase):
    pass


@add_to_dict
class BiAnalysisIndMonthly_edit(edit_Base):
    __tablename__ = 'BI_Analysis_Ind_Monthly'
    ORG_CODE: Mapped[str] = mapped_column(String(3), primary_key=True)
    PERIOD_NAME: Mapped[str] = mapped_column(String(7), primary_key=True)
    DATA_SOURCE: Mapped[str] = mapped_column(String(10))
    MACHINE_CODE: Mapped[str] = mapped_column(UnicodeText(20), primary_key=True)
    INDICATORS_CATEGORY: Mapped[str] = mapped_column(UnicodeText(50), primary_key=True)
    INDICATORS_GROUP: Mapped[str] = mapped_column(UnicodeText(50), primary_key=True)
    INDICATORS_NAME: Mapped[str] = mapped_column(UnicodeText(50), primary_key=True)
    Unit: Mapped[str] = mapped_column(UnicodeText(20))
    MEASURE_VALUE: Mapped[decimal.Decimal] = mapped_column(DECIMAL)
    LAST_UPDATE_DATE: Mapped[datetime.datetime] = mapped_column(DateTime)
    department: Mapped[str] = mapped_column(String(20))
    musr: Mapped[str] = mapped_column(String(5))
    mdtm: Mapped[datetime.datetime] = mapped_column(DateTime)
    Is_it_automated: Mapped[int] = mapped_column(Integer)
    remark: Mapped[str] = mapped_column(UnicodeText)


class log_Base(DeclarativeBase):
    pass


@add_to_dict
class BiAnalysisIndMonthly_edit_log(log_Base):
    __tablename__ = 'BI_Analysis_Ind_Monthly_log'
    ID: Mapped[int] = mapped_column(Integer)
    ProductionDate: Mapped[datetime.datetime] = mapped_column(DateTime)
    ItemName: Mapped[str] = mapped_column(String(20), primary_key=True)
    ItemValue: Mapped[float] = mapped_column(Float)
    ItemValue_old: Mapped[float] = mapped_column(Float)
    department: Mapped[str] = mapped_column(String(20))
    musr: Mapped[str] = mapped_column(String(5))
    mdtm: Mapped[str] = mapped_column(DateTime)


class BiAnalysisIndMonthlyDal:
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
            # filter_condition = text("PERIOD_NAME = :startdate AND department = :department")
            # query = session.query(BiAnalysisIndMonthly).filter(filter_condition).params(
            #     enddate=data['dateTo'],
            #     startdate=data['dateFrom'],
            #     department=data['departmentId']
            # )
            department_ids = [dep.strip() for dep in data['departmentId'].split(",")]

            if len(department_ids) > 0 and department_ids[0] == "all":
                filter_condition = and_(
                    BiAnalysisIndMonthly.PERIOD_NAME == data['dateFrom'],
                    # filter_condition_department
                    )
            else:
                filter_condition = and_(
                    BiAnalysisIndMonthly.PERIOD_NAME == data['dateFrom'],
                    BiAnalysisIndMonthly.department.in_(department_ids)
                    # filter_condition_department
                    )

            query = session.query(BiAnalysisIndMonthly).filter(filter_condition)
            result_df = pd.read_sql(query.statement, session.bind)
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

    def update(self, data: BiAnalysisIndMonthly_edit):
        try:
            with self.Session() as session:
                if isinstance(data, list):
                    for datum in data:
                        record = self.fetch_record(session, datum)
                        if record:
                            if record.MEASURE_VALUE != datum.MEASURE_VALUE or record.remark != datum.remark:
                                log = self.Log(datum, record)
                                record.MEASURE_VALUE = datum.MEASURE_VALUE
                                record.remark = datum.remark
                                record.musr = datum.musr
                                record.mdtm = func.sysdatetime()
                                session.merge(record)
                                session.add(log)
                else:
                    datum = data
                    record = self.fetch_record(session, datum)
                    if record:
                        if record.MEASURE_VALUE != datum.MEASURE_VALUE or record.remark != datum.remark:
                            log = self.Log(datum, record)
                            record.MEASURE_VALUE = datum.MEASURE_VALUE
                            record.remark = datum.remark
                            record.musr = datum.musr
                            record.mdtm = func.sysdatetime()
                            session.merge(record)
                            session.add(log)
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

    def fetch_record(self, session, datum):
        return session.query(BiAnalysisIndMonthly_edit).filter(
                            and_(
                                BiAnalysisIndMonthly_edit.PERIOD_NAME == datum.PERIOD_NAME,
                                BiAnalysisIndMonthly_edit.MACHINE_CODE == datum.MACHINE_CODE,
                                BiAnalysisIndMonthly_edit.INDICATORS_CATEGORY == datum.INDICATORS_CATEGORY,
                                BiAnalysisIndMonthly_edit.INDICATORS_GROUP == datum.INDICATORS_GROUP,
                                BiAnalysisIndMonthly_edit.INDICATORS_NAME == datum.INDICATORS_NAME
                            )
                        ).first()

    def Log(self, datum, record):
        log = BiAnalysisIndMonthly_edit_log()
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
