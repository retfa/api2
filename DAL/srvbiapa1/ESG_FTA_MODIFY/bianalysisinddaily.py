import decimal
import logging
import os
import pandas as pd
from flask import current_app
import datetime
from sqlalchemy import UnicodeText, create_engine, String, Integer, DateTime, DECIMAL, and_
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
class BiAnalysisIndDaily(Base):
    __tablename__ = 'BI_Analysis_Ind_Daily'
    ORG_CODE: Mapped[str] = mapped_column(String(3), primary_key=True)
    DATA_DATE: Mapped[datetime.datetime] = mapped_column(DateTime, primary_key=True)
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
class BiAnalysisIndDaily_edit(edit_Base):
    __tablename__ = 'BI_Analysis_Ind_Daily'
    ORG_CODE: Mapped[str] = mapped_column(String(3), primary_key=True)
    DATA_DATE: Mapped[datetime.datetime] = mapped_column(DateTime, primary_key=True)
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
class BiAnalysisIndDaily_edit_log(log_Base):
    __tablename__ = 'BI_Analysis_Ind_Daily_log'
    DATA_DATE: Mapped[datetime.datetime] = mapped_column(DateTime, primary_key=True)
    MACHINE_CODE: Mapped[str] = mapped_column(UnicodeText(20), primary_key=True)
    INDICATORS_CATEGORY: Mapped[str] = mapped_column(UnicodeText(50), primary_key=True)
    INDICATORS_GROUP: Mapped[str] = mapped_column(UnicodeText(50), primary_key=True)
    INDICATORS_NAME: Mapped[str] = mapped_column(UnicodeText(50), primary_key=True)
    MEASURE_VALUE: Mapped[decimal.Decimal] = mapped_column(DECIMAL)
    MEASURE_VALUE_old: Mapped[decimal.Decimal] = mapped_column(DECIMAL)
    department: Mapped[str] = mapped_column(String(20))
    musr: Mapped[str] = mapped_column(String(5))
    mdtm: Mapped[str] = mapped_column(DateTime)
    remark: Mapped[str] = mapped_column(UnicodeText)


class BiAnalysisIndDailyDal:
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
            # filter_condition = text("DATA_DATE < :enddate AND DATA_DATE >= :startdate AND department = :department")
            # query = session.query(BiAnalysisIndDaily).filter(filter_condition).params(
            #     enddate=data['dateTo'],
            #     startdate=data['dateFrom'],
            #     department=data['departmentId']
            # )
            department_ids = [dep.strip() for dep in data['departmentId'].split(",")]

            if len(department_ids) > 0 and department_ids[0] == "all":
                filter_condition = and_(
                    BiAnalysisIndDaily.DATA_DATE < data['dateTo'],
                    BiAnalysisIndDaily.DATA_DATE >= data['dateFrom']
                    # filter_condition_department
                    )
            else:
                filter_condition = and_(
                    BiAnalysisIndDaily.DATA_DATE < data['dateTo'],
                    BiAnalysisIndDaily.DATA_DATE >= data['dateFrom'],
                    BiAnalysisIndDaily.department.in_(department_ids)
                    # filter_condition_department
                    )

            query = session.query(BiAnalysisIndDaily).filter(filter_condition)
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

    def update(self, data: BiAnalysisIndDaily_edit):
        try:
            with self.Session() as session:
                if isinstance(data, list):
                    for datum in data:
                        record = self.fetch_record(session, datum)
                        if record:
                            if (record.MEASURE_VALUE != decimal.Decimal(datum.MEASURE_VALUE) or
                                    record.remark != datum.remark):
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
        return session.query(BiAnalysisIndDaily_edit).filter(
                            and_(
                                BiAnalysisIndDaily_edit.DATA_DATE == datum.DATA_DATE,
                                BiAnalysisIndDaily_edit.MACHINE_CODE == datum.MACHINE_CODE,
                                BiAnalysisIndDaily_edit.INDICATORS_CATEGORY == datum.INDICATORS_CATEGORY,
                                BiAnalysisIndDaily_edit.INDICATORS_GROUP == datum.INDICATORS_GROUP,
                                BiAnalysisIndDaily_edit.INDICATORS_NAME == datum.INDICATORS_NAME
                            )
                        ).first()

    def Log(self, datum, record):
        log = BiAnalysisIndDaily_edit_log()
        log.DATA_DATE = record.DATA_DATE
        log.MACHINE_CODE = record.MACHINE_CODE
        log.INDICATORS_CATEGORY = record.INDICATORS_CATEGORY
        log.INDICATORS_GROUP = record.INDICATORS_GROUP
        log.INDICATORS_NAME = record.INDICATORS_NAME
        log.MEASURE_VALUE_old = record.MEASURE_VALUE
        log.MEASURE_VALUE = datum.MEASURE_VALUE
        log.remark = datum.remark
        log.department = record.department
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
