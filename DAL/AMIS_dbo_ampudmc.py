import json
import logging
import os
import pandas as pd

from flask import current_app
from sqlalchemy import create_engine, text
from sqlalchemy.exc import OperationalError
from sqlalchemy.orm import sessionmaker
from common import get_connection_string


class AMIS_dbo_ampudmc_Dal:
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
            self.engine = create_engine(connection_string, echo=False)
            session = sessionmaker(bind=self.engine)
            self.session = session()
        except Exception as e:
            msg = f'menu_engine.py |An error occurred: {str(e)}'
            logging.info(msg)
            print(msg)

    def query(self, filter):
        try:
            with self.session.begin():
                cond = []
                params = {}
                if filter.station:
                    cond.append("station = :station")
                    params['station'] = f"{filter.station}"

                if filter.production_line:
                    cond.append("pm =  :pm")
                    params['pm'] = f"{filter.production_line}"

                if filter.name:
                    cond.append("mname = :mname")
                    params['mname'] = f"{filter.name}"

                query = '''
    SELECT [station]
        ,[pm]
        ,[mname]
        ,[chsnm]
        ,[btable]
        ,[stop_yn]
        ,[status]
        ,[cls_sn]
        ,[busr]
        ,[bdtm]
        ,[musr]
        ,[mdtm]
    FROM [AMIS].[dbo].[ampudmc]
                    '''
                if cond:
                    # 使用 AND 運算符將條件組合在一起
                    where_clause = " AND ".join(cond)
                    query = f"{query} WHERE {where_clause}"

                rst = self.session.execute(text(query), params)

                # Convert the query result to a DataFrame
                result_df = pd.DataFrame(rst.fetchall(), columns=rst.keys())
                # print(result_df)
                # print(result_df.dtypes)

                # Format datetime attributes
                float_columns = result_df.select_dtypes(include=['float64']).columns
                # print(float_columns)
                # print(result_df.dtypes["job_rank"])
                for f_col in float_columns:
                    result_df[f_col] = result_df.apply(lambda x: x[f_col] if not pd.isna(x[f_col]) else -1, axis=1)
                    result_df.loc[:, f_col] = result_df.loc[:, f_col].replace(-1, None)
                # print(result_df.dtypes["job_rank"])
                datetime_columns = result_df.select_dtypes(include=['datetime64[ns]']).columns
                # print(datetime_columns)
                for column in datetime_columns:
                    result_df[column] = result_df.apply(
                        lambda x: x[column].strftime('%Y-%m-%d %H:%M:%S') if not pd.isna(x[column]) else None,
                        axis=1
                    )

                # 移除欄位
                result_df = result_df.drop(['busr', 'bdtm', 'musr', 'mdtm'], axis=1)

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

    def queryroot(self, userid):
        try:
            with self.session.begin():
                query = text('''
                SELECT
                     tree.[floor]
                    ,tree.[f_code]
                    ,tree.[up_code]
                    ,tree.[f_name]
                    ,prog.url
                FROM [AMIS].[dbo].[zdtree] tree
                LEFT JOIN [AMIS].[dbo].[zdpermi] permi on tree.f_code=permi.f_code
                LEFT JOIN [AMIS].[dbo].[zdprogm] prog on tree.f_code=prog.f_code
                where permi.user_id=:userid
                and tree.[up_code] ='0'
                order by floor,f_code
                ''')
                result = self.session.execute(query, {'userid': userid})
                # print(result.keys())
                # print(type(result))
                rows = result.fetchall()
                code_dict = {}
                for row in rows:
                    floor, f_code, up_code, f_name, url = row
                    item = {
                        "Depth": floor,
                        "Code": f_code,
                        "ParentCode": up_code,
                        "Name": f_name,
                        "Url": url,
                        "children": []  # 子项为空列表
                    }
                    code_dict[f_code] = item

                root_items = []
                for f_code, item in code_dict.items():
                    parent_code = item.get("ParentCode")
                    if parent_code == '0':  # 根项目的up_code为0
                        pass
                    else:
                        parent_item = code_dict.get(parent_code)
                        if parent_item:
                            parent_item["children"].append(item)
                    root_items.append(item)
                if result:
                    print("Database connection is successful.")
                else:
                    print("Database connection is not working as expected.")
                return root_items
        except OperationalError as e:
            print("Database connection error:", str(e))
