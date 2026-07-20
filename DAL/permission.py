import json
import logging
import os
import pandas as pd
# from urllib.parse import quote
import datetime
from flask import current_app
from sqlalchemy import and_, bindparam, create_engine, text, String, Integer, DateTime
from sqlalchemy.exc import OperationalError
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
# from sqlalchemy.orm import validates
from sqlalchemy.orm import mapped_column
from sqlalchemy.sql import func
from common import add_to_dict, get_connection_string


class Base(DeclarativeBase):
    pass


@add_to_dict
class zpermission(Base):
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
    func_add: Mapped[str] = mapped_column(String(1))
    func_edit: Mapped[str] = mapped_column(String(1))
    func_delete: Mapped[str] = mapped_column(String(1))
    func_sign: Mapped[str] = mapped_column(String(1))
    func_detail: Mapped[str] = mapped_column(String(1))
    func_download: Mapped[str] = mapped_column(String(1))
    func_other: Mapped[str] = mapped_column(String(1))
    busr: Mapped[str] = mapped_column(String(5))
    bdtm: Mapped[str] = mapped_column(DateTime)
    musr: Mapped[str] = mapped_column(String(5))
    mdtm: Mapped[datetime.datetime] = mapped_column(DateTime)


class PermissionDal:
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
            self.Session = sessionmaker(bind=self.engine)

        except Exception as e:
            msg = f'{self.__class__.__name__} |An error occurred: {str(e)}'
            print(msg)
            logging.debug(msg)

    def query(self, filter):
        try:
            session = self.Session()
            cond = []
            params = {}
            bindparams = []

            if getattr(filter, 'user_id', None) is not None:
                cond.append("perm.user_id=:user_id")
                params['user_id'] = filter.user_id
                bindparams.append(bindparam('user_id', expanding=False))

            if getattr(filter, 'progm_id', None) is not None:
                cond.append("progm.progm_id=:progm_id")
                params['progm_id'] = filter.progm_id
                bindparams.append(bindparam('progm_id', expanding=False))

            up_function_array = getattr(filter, 'up_function_array', None)
            if up_function_array is not None and len(up_function_array) > 0:
                cond.append("perm.up_code IN :param_up_code")
                params['param_up_code'] = filter.up_function_array
                bindparams.append(bindparam('param_up_code', expanding=True))

            function_array = getattr(filter, 'function_array', None)
            if function_array is not None and len(function_array) > 0:
                cond.append("perm.f_code IN :param_f_code")
                params['param_f_code'] = filter.function_array
                bindparams.append(bindparam('param_f_code', expanding=True))

            # if not conditions:
            #     rst = session.query(zmuser)
            # else:
            #     rst = session.query(zmuser).filter(*conditions)
            query = '''
SELECT perm.*,usr.user_name, dept.dept_name, progm.pname , tree.f_name, machine.pm, machine.station
FROM [AMIS].[dbo].[zdpermi] perm
LEFT JOIN [AMIS].[dbo].[zdprogm] progm on perm.f_code=progm.f_code
LEFT JOIN [AMIS].[dbo].[zdtree] tree on perm.up_code=tree.f_code
LEFT JOIN [AMIS].[dbo].[ampudmc] machine on perm.mname=machine.mname
LEFT JOIN [AMIS].[dbo].[zmuser] usr on perm.user_id=usr.user_id
LEFT JOIN [HR].[dbo].[department] dept on usr.department_id collate Chinese_Traditional_Bopomofo_100_CS_AS_KS_WS =dept.Dept_ID
                '''
            if cond:
                # 使用 AND 運算符將條件組合在一起
                where_clause = " AND ".join(cond)
                order_clause = " ORDER BY perm.user_id"
                query = f"{query} WHERE {where_clause} {order_clause}"

            print("SQL Query:", query)
            print("Parameters:", params)

            # Use text function to process the SQL query and replace parameters
            sql_query_with_params = text(query).bindparams(*bindparams)

            # Print the replaced SQL query string
            print('sql_query:', sql_query_with_params)

            rst = session.execute(sql_query_with_params, params)
            # sql = rst.statement.compile(dialect=self.engine.dialect)
            # print(sql)

            # Convert the query result to a DataFrame
            result_df = pd.DataFrame(rst.fetchall(), columns=rst.keys())
            # print(result_df)
            # print(result_df.dtypes)

            datetime_columns = result_df.select_dtypes(include=['datetime64[ns]']).columns
            # print(datetime_columns)
            for column in datetime_columns:
                result_df[column] = result_df.apply(lambda x: x[column].strftime('%Y-%m-%d %H:%M:%S')
                                                    if not pd.isna(x[column]) else None, axis=1)

            session.close()

            # Convert DataFrame to a list of dictionaries
            result_dict_list_df = result_df.to_dict(orient='records')
            # print(result_df)
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

    def insert(self, data):
        try:
            session = self.Session()
            zpermi = zpermission()
            zpermi.sid = 1
            zpermi.user_id = data["user_id"]
            if getattr(data, 'mname', "") is not None:
                zpermi.mname = data["mname"]
            zpermi.up_code = data["up_function"]
            zpermi.f_code = data["f_code"]
            zpermi.st_func = data["st_func"]
            zpermi.sp_func = data["sp_func"]
            zpermi.func_print = data["func_print"]
            zpermi.func_add = data["func_add"]
            zpermi.func_edit = data["func_edit"]
            zpermi.func_delete = data["func_delete"]
            zpermi.func_sign = data["func_sign"]
            zpermi.func_detail = data["func_detail"]
            zpermi.func_download = data["func_download"]
            zpermi.func_other = data["func_other"]
            # zpermi.musr = data["musr"]
            # zpermi.mdtm = func.sysdatetime()
            session.add(zpermi)
            session.commit()

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

    def update(self, data):
        try:
            session = self.Session()
            zpermi = zpermission()
            zpermi.user_id = data["user_id"]
            zpermi.st_func = data["st_func"]
            zpermi.sp_func = data["sp_func"]
            zpermi.func_print = data["func_print"]
            zpermi.func_edit = data["func_edit"]
            zpermi.func_sign = data["func_sign"]
            zpermi.func_detail = data["func_detail"]
            zpermi.func_download = data["func_download"]
            zpermi.func_other = data["func_other"]
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
            rst = session.query(zpermission).filter_by(user_id=user_id).first()
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
                zpermission.user_id == data['user_id'],
                zpermission.up_code == data['up_function']
            )
            matched_data = session.query(zpermission).filter(filter_condition).all()

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

    def insert_by_upcode(self, data):
        try:
            session = self.Session()
            user_id = data["user_id"]
            print(user_id)
            print(type(data["Content"]))
            for index, value in enumerate(data["Content"]):
                print(f'Index: {index}, Value: {value}')
                zpermi = zpermission()
                zpermi.sid = 1
                zpermi.user_id = data["user_id"]
                if getattr(value, 'mname', "") is not None:
                    zpermi.mname = value["mname"]
                zpermi.up_code = data["up_function"]
                zpermi.f_code = value["f_code"]
                zpermi.st_func = value["st_func"]
                zpermi.sp_func = value["sp_func"]
                zpermi.func_print = value["func_print"]
                zpermi.func_add = value["func_add"]
                zpermi.func_edit = value["func_edit"]
                zpermi.func_delete = value["func_delete"]
                zpermi.func_sign = value["func_sign"]
                zpermi.func_detail = value["func_detail"]
                zpermi.func_download = value["func_download"]
                zpermi.func_other = value["func_other"]
                zpermi.busr = data["busr"]
                zpermi.musr = data["musr"]
                zpermi.mdtm = func.sysdatetime()
                session.add(zpermi)

                # print(f'Index: {index}, Value: {value}')
                # zpermi = session.query(zpermission).filter_by(user_id=data["user_id"], f_code=value["f_code"]).first()
                # if zpermi:
                #     zpermi.st_func = value["st_func"]
                #     zpermi.sp_func = value["sp_func"]
                #     zpermi.func_print = value["func_print"]
                #     zpermi.func_edit = value["func_edit"]
                #     zpermi.func_sign = value["func_sign"]
                #     zpermi.func_detail = value["func_detail"]
                #     zpermi.func_download = value["func_download"]
                #     zpermi.func_other = value["func_other"]
                #     zpermi.musr = data["musr"]
                #     zpermi.mdtm = func.sysdatetime()
                #     session.merge(zpermi)
            session.commit()
            return len(data["Content"])

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

    def copy(self, data):
        try:
            session = self.Session()
            query = text('''
DELETE FROM [AMIS].[dbo].[zdpermi]
where user_id=:destination_id;

INSERT INTO zdpermi ( sid, user_id,   mname, progm_id, up_code, f_code, st_func, sp_func, func_print, func_edit, func_sign, func_detail, func_download, func_other, busr )
SELECT                sid, :destination_id, mname, progm_id, up_code, f_code, st_func, sp_func, func_print, func_edit, func_sign, func_detail, func_download, func_other, :busr
FROM [AMIS].[dbo].[zdpermi]
WHERE user_id=:source_id
                ''')
            rst = session.execute(query, data)
            session.commit()
            return rst.rowcount

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

    def delete(self, datum):
        #  msg = f'{self.__class__.__name__} | DAL insert'
        #  logging.debug(msg)
        try:
            session = self.Session()
            permi = session.query(zpermission).filter_by(
                        user_id=datum['user_id'],
                        mname=datum['machine'],
                        f_code=datum['function']
                    ).one()
            if permi:
                session.delete(permi)
                session.commit()
            return datum
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
            session.close()
