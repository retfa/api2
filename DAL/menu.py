import json
import logging
import os

from flask import current_app
from sqlalchemy import create_engine, text
from sqlalchemy.exc import OperationalError
from sqlalchemy.orm import sessionmaker
from common import get_connection_string


class MenuDal:
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

    def query(self, userid, node):
        try:
            with self.session.begin():
                node_name = f"{node}%"
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
                and tree.[f_code] like :node
                order by floor,f_code
                ''')
                result = self.session.execute(query, {'userid': userid, 'node': node_name})
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
                filtered_result = [obj for obj in root_items if obj["Code"] == node]
                return filtered_result
        except OperationalError as e:
            print("Database connection error:", str(e))

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
