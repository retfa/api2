import logging
import os
import pandas as pd
from flask import current_app
from sqlalchemy import and_, create_engine
from sqlalchemy.exc import OperationalError
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import DeclarativeBase
from common import add_to_dict, get_connection_string
from DAL.srvmsdba2.TableBaseClass import RawTableBase_21


class Base(DeclarativeBase):
    pass


@add_to_dict
class MO1RL_raw_avg(Base, RawTableBase_21):
    __tablename__ = 'MO1RL_raw_avg'


class MO1RL_raw_avgDal:
    def __init__(self):
        trace_msg = f'{self.__class__.__name__}'
        print(trace_msg)
        logging.info(trace_msg)
        try:
            # json_path = os.path.join(current_app.config['folders']['exe'], 'appsettings.json')
            # print(f'appsettings.json_path: {json_path}')
            # with open(json_path, 'r') as file:
            #     _config = json.load(file)
            # DbHostName = _config["Database"]["HostName"]

            json_connections_path = os.path.join(current_app.config['folders']['temproot'], 'connections.json')
            print(f'json_path: {json_connections_path}')
            cs_name = 'SRVMSDBA2_FTA_AUG'
            print(cs_name)

            connection_string = get_connection_string(json_connections_path, cs_name)
            self.engine = create_engine(connection_string, echo=True)
            self.Session = sessionmaker(bind=self.engine)

        except Exception as e:
            msg = f'{self.__class__.__name__} |An error occurred: {str(e)}'
            print(msg)
            logging.debug(msg)

    def query(self, filter):
        try:
            session = self.Session()
            filter_conditions = []

            if filter.get('DtFrom') is not None:
                filter_conditions.append(MO1RL_raw_avg.fta_dtm >= filter['DtFrom'])

            if filter.get('DtTo') is not None:
                filter_conditions.append(MO1RL_raw_avg.fta_dtm < filter['DtTo'])

            print(len(filter.get('ReelNo')))
            if filter.get('ReelNo') is not None and len(filter.get('ReelNo')) > 0:
                # filter_conditions.append(MO1RL_raw_avg.relno in (filter['ReelNo']))
                filter_conditions.append(MO1RL_raw_avg.relno.in_(tuple(filter['ReelNo'])))

            if filter.get('ptype') is not None:
                filter_conditions.append(MO1RL_raw_avg.ptype == filter['ptype'])

            if filter.get('gramg') is not None:
                filter_conditions.append(MO1RL_raw_avg.gramg == filter['gramg'])

            final_filter_condition = and_(*filter_conditions)
            query = session.query(MO1RL_raw_avg).filter(final_filter_condition)
            result_df = pd.read_sql(query.statement, session.bind)
            print(f'records: {len(result_df.index)}')
            datetime_columns = result_df.select_dtypes(include=['datetime64[ns]']).columns
            print(f'datetime_columns: {datetime_columns}')
            for column in datetime_columns:
                result_df[column] = result_df.apply(lambda x: x[column].strftime('%Y-%m-%d %H:%M:%S')
                                                    if not pd.isna(x[column]) else None, axis=1)
            session.close()

            # Convert DataFrame to a list of dictionaries
            result_dict_list_df = result_df.to_dict(orient='records')

            return result_dict_list_df
        except OperationalError as e:
            msg = f'{self.__class__.__name__} |An connection error occurred: {str(e)}'
            print(msg)
            logging.debug(msg)
        except Exception as e:
            msg = f'{self.__class__.__name__} |An error occurred: {str(e)}'
            print(msg)
            logging.debug(msg)
        finally:
            session.close()

    def select(self, filter):
        try:
            session = self.Session()
            filter_conditions = []

            if filter.get('user_id') is not None:
                filter_conditions.append(MO1RL_raw_avg.user_id == filter['user_id'])

            if filter.get('progm_id') is not None:
                filter_conditions.append(MO1RL_raw_avg.progm_id == filter['progm_id'])

            filter_conditions.append(MO1RL_raw_avg.IsEnabled == 1)
            final_filter_condition = and_(*filter_conditions)
            query = session.query(MO1RL_raw_avg).filter(final_filter_condition)
            result_df = pd.read_sql(query.statement, session.bind)
            datetime_columns = result_df.select_dtypes(include=['datetime64[ns]']).columns
            print(datetime_columns)
            for column in datetime_columns:
                result_df[column] = result_df.apply(lambda x: x[column].strftime('%Y-%m-%d %H:%M:%S')
                                                    if not pd.isna(x[column]) else None, axis=1)
            session.close()

            # Convert DataFrame to a list of dictionaries
            result_dict_list_df = result_df.to_dict(orient='records')

            return result_dict_list_df
        except OperationalError as e:
            msg = f'{self.__class__.__name__} |An connection error occurred: {str(e)}'
            print(msg)
            logging.debug(msg)
        except Exception as e:
            msg = f'{self.__class__.__name__} |An error occurred: {str(e)}'
            print(msg)
            logging.debug(msg)
        finally:
            session.close()
