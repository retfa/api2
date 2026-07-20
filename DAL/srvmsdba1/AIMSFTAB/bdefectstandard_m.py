import logging
import os
import pandas as pd
from flask import current_app
from sqlalchemy import and_, create_engine, String, Integer, Boolean, DECIMAL
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
class bdefectstandard_m(Base):
    __tablename__ = 'bdefectstandard_m'
    Sn: Mapped[int] = mapped_column(Integer, primary_key=True)

    MachineCode: Mapped[str] = mapped_column(String(50))
    PaperCode: Mapped[str] = mapped_column(String(4))
    BaseWeight: Mapped[float] = mapped_column(DECIMAL)
    ProductWeight: Mapped[float] = mapped_column(DECIMAL)
    TagName: Mapped[str] = mapped_column(String(255))
    TimeSpan: Mapped[int] = mapped_column(Integer)
    Method: Mapped[str] = mapped_column(String(255))
    Mode: Mapped[str] = mapped_column(String(255))
    LimitType: Mapped[str] = mapped_column(String(255))
    ValueFloat: Mapped[float] = mapped_column(DECIMAL)
    SchedulerExpression: Mapped[str] = mapped_column(String(255))    
    IsEnabled: Mapped[bool] = mapped_column(Boolean)


class bdefectstandard_mDal:
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
            cs_name = 'SRVMSDBA1_AIMSFTAB'
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

            # if filter.get('DtFrom') is not None:
            #     filter_conditions.append(bdefectstandard_m.fta_dtm >= filter['DtFrom'])

            # if filter.get('DtTo') is not None:
            #     filter_conditions.append(bdefectstandard_m.fta_dtm < filter['DtTo'])

            if filter.get('MachineCode') is not None:
                filter_conditions.append(bdefectstandard_m.MachineCode == filter['MachineCode'])

            if filter.get('PaperCode') is not None:
                filter_conditions.append(bdefectstandard_m.PaperCode == filter['PaperCode'])

            if filter.get('BaseWeight') is not None:
                filter_conditions.append(bdefectstandard_m.BaseWeight == filter['BaseWeight'])

            if filter.get('ProductWeight') is not None:
                filter_conditions.append(bdefectstandard_m.BaseWeight == filter['ProductWeight'])

            if filter.get('TagName') is not None:
                filter_conditions.append(bdefectstandard_m.TagName == filter['TagName'])
            timeSpan = filter.get('TimeSpan')
            if isinstance(timeSpan, int) and timeSpan > 0:
                filter_conditions.append(bdefectstandard_m.TimeSpan == filter['TimeSpan'])

            if filter.get('Method') is not None:
                filter_conditions.append(bdefectstandard_m.Method == filter['Method'])

            if filter.get('Mode') is not None:
                filter_conditions.append(bdefectstandard_m.Mode == filter['Mode'])

            if filter.get('LimitType') is not None:
                filter_conditions.append(bdefectstandard_m.LimitType == filter['LimitType'])

            if filter.get('SchedulerExpression') is not None:
                filter_conditions.append(bdefectstandard_m.SchedulerExpression == filter['SchedulerExpression'])

            final_filter_condition = and_(*filter_conditions)
            query = session.query(bdefectstandard_m).filter(final_filter_condition)
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
