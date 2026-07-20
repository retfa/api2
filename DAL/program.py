import json
import logging
import os
import pandas as pd
# from urllib.parse import quote
import datetime
from flask import current_app
from sqlalchemy import and_, bindparam, create_engine, text, String, Integer, DateTime, Text
from sqlalchemy.exc import OperationalError
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
# from sqlalchemy.orm import validates
from sqlalchemy.orm import mapped_column
from sqlalchemy.sql import func
from common import add_to_dict, get_connection_string
from icecream import ic


class Base_add(DeclarativeBase):
    pass


class zdprogm_add(Base_add):
    __tablename__ = 'zdprogm'
    progm_id: Mapped[str] = mapped_column(String(20), primary_key=True)
    url: Mapped[str] = mapped_column(String(80))
    f_code: Mapped[str] = mapped_column(String(20))
    up_code: Mapped[str] = mapped_column(String(20))
    st_func: Mapped[str] = mapped_column(String(1))
    sp_func: Mapped[str] = mapped_column(String(1))
    pname: Mapped[str] = mapped_column(String(30))
    desc: Mapped[str] = mapped_column(Text)
    busr: Mapped[str] = mapped_column(String(9))


class Base(DeclarativeBase):
    pass


@add_to_dict
class zprogram(Base):
    __tablename__ = 'zdpermi'
    sid: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[str] = mapped_column(String(5), primary_key=True)
    mname: Mapped[str] = mapped_column(String(2), primary_key=True)
    progm_id: Mapped[str] = mapped_column(String(20))
    up_code: Mapped[str] = mapped_column(String(50))
    f_code: Mapped[str] = mapped_column(String(20), primary_key=True)
    st_func: Mapped[str] = mapped_column(String(1))
    sp_func: Mapped[str] = mapped_column(String(1))
    func_print: Mapped[str] = mapped_column(String(1))
    func_edit: Mapped[str] = mapped_column(String(1))
    func_sign: Mapped[str] = mapped_column(String(1))
    func_detail: Mapped[str] = mapped_column(String(1))
    func_download: Mapped[str] = mapped_column(String(1))
    func_other: Mapped[str] = mapped_column(String(1))
    busr: Mapped[str] = mapped_column(String(5))
    bdtm: Mapped[str] = mapped_column(DateTime)
    musr: Mapped[str] = mapped_column(String(5))
    mdtm: Mapped[datetime.datetime] = mapped_column(DateTime)


class ProgramDal:
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
            cs_name = f'{DbHostName}_AMIS'
            print(cs_name)

            connection_string = get_connection_string(json_path, cs_name)
            self.engine = create_engine(connection_string, echo=True)
            Session = sessionmaker(bind=self.engine)
            self.session = Session()
        except Exception as e:
            msg = f'{self.__class__.__name__} |An error occurred: {str(e)}'
            print(msg)
            logging.debug(msg)

    def query(self, filter):
        session = self.session
        try:
            cond = []
            params = {}
            bindparams = []
            if getattr(filter, 'user_id', None) is not None:
                cond.append("user_id=:user_id")
                params['user_id'] = filter.user_id
                bindparams.append(bindparam('user_id', expanding=False))

            up_function_array = getattr(filter, 'up_function_array', None)
            if up_function_array is not None and len(up_function_array) > 0:
                cond.append("up_code IN :param_up_code")
                params['param_up_code'] = filter.up_function_array
                bindparams.append(bindparam('param_up_code', expanding=True))

            function_array = getattr(filter, 'function_array', None)
            if function_array is not None and len(function_array) > 0:
                cond.append("f_code IN :param_f_code")
                params['param_f_code'] = filter.function_array
                bindparams.append(bindparam('param_f_code', expanding=True))

            # if not conditions:
            #     rst = session.query(zmuser)
            # else:
            #     rst = session.query(zmuser).filter(*conditions)
            query = '''
SELECT * FROM [AMIS].[dbo].[zdpermi]
                '''
            if cond:
                # 使用 AND 運算符將條件組合在一起
                where_clause = " AND ".join(cond)
                query = f"{query} WHERE {where_clause}"
            print("SQL Query:", query)
            print("Parameters:", params)

            # Use text function to process the SQL query and replace parameters
            sql_query_with_params = text(query).bindparams(*bindparams)

            # Print the replaced SQL query string
            print('123', sql_query_with_params)

            rst = session.execute(sql_query_with_params, params)
            # sql = rst.statement.compile(dialect=self.engine.dialect)
            # print(sql)

            # Convert the query result to a DataFrame
            result_df = pd.DataFrame(rst.fetchall(), columns=rst.keys())
            print(result_df)
            print(result_df.dtypes)

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
            self.session.close()

    def insert(self, datum):
        try:
            with self.session.begin():
                zdprogm = zdprogm_add()
                zdprogm.progm_id = datum['progm_id']
                zdprogm.url = datum['url']
                zdprogm.f_code = datum['f_code']
                zdprogm.up_code = datum['up_code']
                zdprogm.st_func = datum['st_func']
                zdprogm.sp_func = datum['sp_func']
                zdprogm.pname = datum['pname']
                if "desc" in datum:
                    zdprogm.desc = datum['desc']
                zdprogm.busr = datum['busr']
                self.session.add(zdprogm)
                self.session.commit()
            return zdprogm.progm_id
        except OperationalError as e:
            msg = f'{self.__class__.__name__} |An connection error occurred: {str(e)}'
            print(msg)
            logging.debug(msg)
            return -1
        except Exception as e:
            msg = f'{self.__class__.__name__} |An error occurred: {str(e)}'
            print(msg)
            logging.debug(msg)
            return -1
        finally:
            self.session.close()

    def update(self, data):
        try:
            session = self.Session()
            user_id = data["user_id"]
            print(user_id)
            print(type(data["Content"]))
            for index, value in enumerate(data["Content"]):
                print(f'Index: {index}, Value: {value}')
                zpermi = session.query(zprogram).filter_by(user_id=data["user_id"], f_code=value["f_code"]).first()
                if zpermi:
                    zpermi.st_func = value["st_func"]
                    zpermi.sp_func = value["sp_func"]
                    zpermi.func_print = value["func_print"]
                    zpermi.func_edit = value["func_edit"]
                    zpermi.func_sign = value["func_sign"]
                    zpermi.func_detail = value["func_detail"]
                    zpermi.func_download = value["func_download"]
                    zpermi.func_other = value["func_other"]
                    zpermi.musr = data["musr"]
                    zpermi.mdtm = func.sysdatetime()
                    session.merge(zpermi)
            session.commit()
            return data

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

    def select(self, user_id):
        try:
            session = self.Session()
            # zmusr=zmuser_edit()
            rst = session.query(zprogram).filter_by(user_id=user_id).first()
            session.commit()
            return self.to_dict(rst)

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

    def delete_by_upcode(self, data):
        try:
            session = self.Session()
            filter_condition = and_(
                zprogram.user_id == data['user_id'],
                zprogram.up_code == data['up_function']
            )
            matched_data = session.query(zprogram).filter(filter_condition).all()

            for data in matched_data:
                session.delete(data)

            session.commit()
            return None
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
