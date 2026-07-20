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
class DailyMaterialData(Base):
    __tablename__ = 'DailyMaterialData'
    ID: Mapped[int] = mapped_column(Integer, primary_key=True)
    ProductionDate: Mapped[datetime.datetime] = mapped_column(DateTime)
    ProductMaterialNo: Mapped[str] = mapped_column(UnicodeText(40))
    EquipmentNo: Mapped[str] = mapped_column(UnicodeText(240))
    SourceMaterialNo: Mapped[str] = mapped_column(UnicodeText(40))
    SourceName: Mapped[str] = mapped_column(UnicodeText(240))
    SourceNo: Mapped[str] = mapped_column(UnicodeText(40))
    Stage: Mapped[int] = mapped_column(Integer)
    Type: Mapped[int] = mapped_column(Integer)
    Value: Mapped[decimal.Decimal] = mapped_column(DECIMAL(18, 4))
    Unit: Mapped[int] = mapped_column(Integer)
    Rate: Mapped[decimal.Decimal] = mapped_column(DECIMAL(18, 5))
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


# @add_to_dict
# class DailyProductionData_edit(edit_Base):
#     __tablename__ = 'DailyProductionData'
#     ID: Mapped[int] = mapped_column(Integer)
#     ProductionDate: Mapped[datetime.datetime] = mapped_column(DateTime)
#     ProductMaterialNo: Mapped[str] = mapped_column(UnicodeText(40))
#     EquipmentNo: Mapped[str] = mapped_column(UnicodeText(240))
#     Production: Mapped[float] = mapped_column(DECIMAL)
#     ProductionRate: Mapped[float] = mapped_column(DECIMAL)
#     Inbound: Mapped[float] = mapped_column(DECIMAL)
#     InboundRate: Mapped[float] = mapped_column(DECIMAL)
#     UploadTime: Mapped[datetime.datetime] = mapped_column(DateTime)
#     department: Mapped[str] = mapped_column(String(20))
#     musr: Mapped[str] = mapped_column(String(5))
#     mdtm: Mapped[datetime.datetime] = mapped_column(DateTime)
#     Is_it_automated: Mapped[int] = mapped_column(Integer)
#     remark: Mapped[str] = mapped_column(UnicodeText)


# class log_Base(DeclarativeBase):
#     pass


# @add_to_dict
# class DailyProductionData_edit_log(log_Base):
#     __tablename__ = 'DailyProductionData_log'
#     ID: Mapped[int] = mapped_column(Integer)
#     ProductionDate: Mapped[datetime.datetime] = mapped_column(DateTime)
#     ItemName: Mapped[str] = mapped_column(String(20))
#     ItemValue: Mapped[float] = mapped_column(Float)
#     ItemValue_old: Mapped[float] = mapped_column(Float)
#     department: Mapped[str] = mapped_column(String(20))
#     musr: Mapped[str] = mapped_column(String(5))
#     mdtm: Mapped[str] = mapped_column(DateTime)


class DailyMaterialDataDal:
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
            department_ids = [dep.strip() for dep in data['departmentId'].split(",")]

            # filter_condition_department = UploadData.department.in_(department_ids)

            # filter_condition = and_(
            #     DailyProductionData.ProductionDate < data['dateTo'],
            #     DailyProductionData.ProductionDate >= data['dateFrom'],
            #     DailyProductionData.department.in_(department_ids)
            #     # filter_condition_department
            # )
            if len(department_ids) > 0 and department_ids[0] == "all":
                filter_condition = and_(
                    DailyMaterialData.ProductionDate < data['dateTo'],
                    DailyMaterialData.ProductionDate >= data['dateFrom']
                    # filter_condition_department
                    )
            else:
                filter_condition = and_(
                    DailyMaterialData.ProductionDate < data['dateTo'],
                    DailyMaterialData.ProductionDate >= data['dateFrom'],
                    DailyMaterialData.department.in_(department_ids)
                    # filter_condition_department
                    )

            query = session.query(DailyMaterialData).filter(filter_condition)
            result_df = pd.read_sql(query.statement, session.bind)
            print(f'length: {len(result_df.index)}')
            columns = result_df.dtypes
            print(columns)
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

    # def update(self, data: DailyProductionData_edit):
    #     try:
    #         with self.Session() as session:
    #             if isinstance(data, list):
    #                 for datum in data:
    #                     record = session.query(DailyProductionData_edit).filter_by(ID=datum.ID).first()
    #                     if record:
    #                         if record.Production != datum.Production or record.Inbound != datum.Inbound or record.remark != datum.remark:
    #                             # if record.Production != datum.Production:
    #                             #     logP = self.LogProduction(datum, record)

    #                             # if record.Inbound != datum.Inbound:
    #                             #     logI = self.LogInbound(datum, record)

    #                             # if record.remark != datum.remark:
    #                             #     logP = self.LogProduction(datum, record)
    #                             #     logI = self.LogInbound(datum, record)

    #                             record.Production = datum.Production
    #                             record.Inbound = datum.Inbound
    #                             record.remark = datum.remark
    #                             record.musr = datum.musr
    #                             record.mdtm = func.sysdatetime()
    #                             session.merge(record)
    #                             # if logP:
    #                             #     session.add(logP)
    #                             # if logI:
    #                             #     session.add(logI)
    #             else:
    #                 record = session.query(DailyProductionData_edit).filter_by(ID=data.ID).first()
    #                 if record:
    #                     if record.Production != datum.Production or record.Inbound != datum.Inbound or record.remark != datum.remark:
    #                         # if record.Production != data.Production:
    #                         #     logP = self.LogProduction(data, record)

    #                         # if record.Inbound != data.Inbound:
    #                         #     logI = self.LogInbound(data, record)

    #                         # if record.remark != data.remark:
    #                         #     logP = self.LogProduction(data, record)
    #                         #     logI = self.LogInbound(data, record)

    #                         record.Production = data.Production
    #                         record.Inbound = data.Inbound
    #                         record.remark = data.remark
    #                         record.musr = data.musr
    #                         record.mdtm = func.sysdatetime()
    #                         session.merge(record)
    #                         # if logP:
    #                         #     session.add(logP)
    #                         # if logI:
    #                         #     session.add(logI)
    #             session.commit()

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

    # def LogProduction(self, datum, record):
    #     log = DailyProductionData_edit_log()
    #     log.ID = record.ID
    #     log.ProductionDate = record.ProductionDate
    #     log.ItemName = "Production"
    #     log.department = record.department
    #     log.ItemValue_old = record.Production
    #     log.ItemValue = datum.Production
    #     log.musr = datum.musr
    #     log.mdtm = func.sysdatetime()
    #     return log

    # def LogInbound(self, datum, record):
    #     log = DailyProductionData_edit_log()
    #     log.ID = record.ID
    #     log.ProductionDate = record.ProductionDate
    #     log.ItemName = "Inbound"
    #     log.department = record.department
    #     log.ItemValue_old = record.Inbound
    #     log.ItemValue = datum.Inbound
    #     log.musr = datum.musr
    #     log.mdtm = func.sysdatetime()
    #     return log

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
