import decimal
import logging
import os
import pandas as pd
from flask import current_app
import datetime
from sqlalchemy import UnicodeText, and_, create_engine, String, Integer, DateTime, Boolean, Float, DECIMAL
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
    busr: Mapped[str] = mapped_column(String(5))
    bdtm: Mapped[datetime.datetime] = mapped_column(DateTime)
    musr: Mapped[str] = mapped_column(String(5))
    mdtm: Mapped[datetime.datetime] = mapped_column(DateTime)
    Is_it_automated: Mapped[int] = mapped_column(Integer)
    remark: Mapped[str] = mapped_column(UnicodeText)


class edit_Base(DeclarativeBase):
    pass


@add_to_dict
class UploadData_edit(edit_Base):
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
    musr: Mapped[str] = mapped_column(String(5))
    mdtm: Mapped[datetime.datetime] = mapped_column(DateTime)
    remark: Mapped[str] = mapped_column(UnicodeText)


class log_Base(DeclarativeBase):
    pass


@add_to_dict
class UploadData_edit_log(log_Base):
    __tablename__ = 'UploadData_log'
    UID: Mapped[int] = mapped_column(Integer)
    ProdDate: Mapped[datetime.datetime] = mapped_column(DateTime)
    ItemName: Mapped[str] = mapped_column(String(20), primary_key=True)
    ItemValue: Mapped[decimal.Decimal] = mapped_column(DECIMAL)
    ItemValue_old: Mapped[decimal.Decimal] = mapped_column(DECIMAL)
    department: Mapped[str] = mapped_column(String(20))
    musr: Mapped[str] = mapped_column(String(5))
    mdtm: Mapped[str] = mapped_column(DateTime)
    remark: Mapped[str] = mapped_column(UnicodeText)


class UploadDataDal:
    def __init__(self):
        trace_msg = f'{self.__class__.__name__}'
        print(trace_msg)
        logging.info(trace_msg)
        try:
            json_path = os.path.join(current_app.config['folders']['temproot'], 'connections.json')
            logging.info(f'json_path: {json_path}')
            cs_name = 'SRVBIAPA1_ESG_FTA_MODIFY'
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
            department_ids = [dep.strip() for dep in data['departmentId'].split(",")]

            if len(department_ids) > 0 and department_ids[0] == "all":
                filter_condition = and_(
                    UploadData.ProdDate < data['dateTo'],
                    UploadData.ProdDate >= data['dateFrom']
                    # filter_condition_department
                    )
            else:
                filter_condition = and_(
                    UploadData.ProdDate < data['dateTo'],
                    UploadData.ProdDate >= data['dateFrom'],
                    UploadData.department.in_(department_ids)
                    # filter_condition_department
                    )

            query = session.query(UploadData).filter(filter_condition)
            result_df = pd.read_sql(query.statement, session.bind)
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

    def update(self, data: UploadData_edit):
        try:
            with self.Session() as session:
                if isinstance(data, list):
                    for datum in data:
                        record = session.query(UploadData_edit).filter_by(UID=datum.UID).first()
                        if record:
                            if record.ItemValue != decimal.Decimal(datum.ItemValue) or record.remark != datum.remark:
                                log = self.Log(datum, record)
                                record.ItemValue = datum.ItemValue
                                record.remark = datum.remark
                                record.musr = datum.musr
                                record.mdtm = func.sysdatetime()
                                session.merge(record)
                                session.add(log)
                else:
                    record = session.query(UploadData_edit).filter_by(UID=data.UID).first()
                    datum = data
                    if record:
                        if record.ItemValue != datum.ItemValue or record.remark != datum.remark:
                            log = self.Log(datum, record)
                            record.ItemValue = datum.ItemValue
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

    def Log(self, datum: UploadData_edit, record):
        log = UploadData_edit_log()
        log.UID = record.UID
        log.ProdDate = record.ProdDate
        log.ItemName = record.ItemName
        log.department = record.department
        log.ItemValue_old = record.ItemValue
        log.ItemValue = datum.ItemValue
        log.musr = datum.musr
        log.mdtm = func.sysdatetime()
        log.remark = datum.remark
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
