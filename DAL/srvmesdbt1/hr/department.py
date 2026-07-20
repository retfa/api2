import json
import logging
import os
import pandas as pd
import datetime
from flask import current_app
from sqlalchemy import create_engine, String, DateTime
from sqlalchemy.exc import OperationalError
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from common import add_to_dict, get_connection_string


class Base(DeclarativeBase):
    pass


@add_to_dict
class department(Base):
    __tablename__ = "department"
    Dept_ID: Mapped[str] = mapped_column(String(24), primary_key=True)
    parent_id: Mapped[str] = mapped_column(String(24))
    dept_name: Mapped[str] = mapped_column(String(255))
    order_no: Mapped[str] = mapped_column(String(5))
    last_sync: Mapped[datetime.datetime] = mapped_column(DateTime)


class DepartmentDal:
    def __init__(self):
        trace_msg = f'{self.__class__.__name__}'
        print(trace_msg)
        logging.info(trace_msg)
        try:
            json_path = os.path.join(current_app.config['folders']['exe'], 'appsettings.json')
            print(f'appsettings.json_path: {json_path}')
            with open(json_path, 'r') as file:
                _config = json.load(file)
            DbHostName = _config["Database"]["HostName"]

            json_path = os.path.join(current_app.config['folders']['temproot'], 'connections.json')
            print(f'json_path: {json_path}')
            cs_name = f'{DbHostName}_HR'
            print(cs_name)

            connection_string = get_connection_string(json_path, cs_name)
            self.engine = create_engine(connection_string, echo=False)
            self.Session = sessionmaker(bind=self.engine)

        except Exception as e:
            msg = f"{self.__class__.__name__} |An error occurred: {str(e)}"
            print(msg)
            logging.debug(msg)

    def query_hr(self):
        try:
            session = self.Session()
            result_df = pd.read_sql(session.query(department).statement, session.bind)
            # print(result_df)
            datetime_columns = result_df.select_dtypes(
                include=["datetime64[ns]"]
            ).columns
            print(datetime_columns)
            for column in datetime_columns:
                result_df[column] = result_df.apply(
                    lambda x: x[column].strftime("%Y-%m-%d %H:%M:%S")
                    if not pd.isna(x[column])
                    else None,
                    axis=1,
                )
            result_dict_list_df = result_df.to_dict(orient="records")
            # print(result_dict_list_df)
            return result_dict_list_df

        except OperationalError as e:
            msg = f"{self.__class__.__name__} |An connection error occurred: {str(e)}"
            print(msg)
            logging.debug(msg)

        except Exception as e:
            msg = f"{self.__class__.__name__} |An error occurred: {str(e)}"
            print(msg)
            logging.debug(msg)

        finally:
            session.close()
