import json
import logging
import os
from flask import current_app
from sqlalchemy import create_engine, desc, text, String, Integer, DateTime
from sqlalchemy.exc import OperationalError
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.sql import func
from sqlalchemy.orm import mapped_column
from common import get_connection_string
# import re


class Base_add(DeclarativeBase):
    pass


class zdtree_add(Base_add):
    __tablename__ = 'zdtree'
    floor: Mapped[int] = mapped_column(Integer())
    f_code: Mapped[str] = mapped_column(String(20), primary_key=True)
    f_type: Mapped[str] = mapped_column(String(10))
    up_code: Mapped[str] = mapped_column(String(20))
    f_name: Mapped[str] = mapped_column(String(50))
    station: Mapped[str] = mapped_column(String(20))
    busr: Mapped[str] = mapped_column(String(5))


class Base_edit(DeclarativeBase):
    pass


class zdtree_edit(Base_edit):
    __tablename__ = 'zdtree'
    floor: Mapped[int] = mapped_column(Integer())
    f_code: Mapped[str] = mapped_column(String(20), primary_key=True)
    f_type: Mapped[str] = mapped_column(String(10))
    up_code: Mapped[str] = mapped_column(String(20))
    f_name: Mapped[str] = mapped_column(String(50))
    musr: Mapped[str] = mapped_column(String(5))
    mdtm: Mapped[DateTime] = mapped_column(DateTime)


class Base(DeclarativeBase):
    pass


class zdtree_basic(Base):
    __tablename__ = 'zdtree'
    floor: Mapped[int] = mapped_column(Integer())
    f_code: Mapped[str] = mapped_column(String(20), primary_key=True)
    f_type: Mapped[str] = mapped_column(String(10))
    up_code: Mapped[str] = mapped_column(String(20))
    f_name: Mapped[str] = mapped_column(String(50))
    station: Mapped[str] = mapped_column(String(20))
    sub_num: Mapped[int] = mapped_column(Integer())
    file_num: Mapped[int] = mapped_column(Integer())
    busr: Mapped[str] = mapped_column(String(5))
    bdtm: Mapped[DateTime] = mapped_column(DateTime)
    musr: Mapped[str] = mapped_column(String(5))
    mdtm: Mapped[DateTime] = mapped_column(DateTime)


class MenuTreeDal:
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

    def query(self, node):
        try:
            with self.session.begin():
                node_name = f"{node}%"

#                 query = text('''
# SELECT
#         tree.[floor]
#     ,tree.[f_code]
#     ,tree.[up_code]
#     ,tree.[f_name]
#     ,tree.[f_type]
#     ,tree.[station]
#     ,STUFF(
#         (SELECT ',' + CAST(mname AS VARCHAR(10))
#             FROM [AMIS].[dbo].[ampudmc]
#             WHERE station=tree.[station]
#             FOR XML PATH('')), 1, 1, '') AS mname
#     ,prog.progm_id
# FROM [AMIS].[dbo].[zdtree] tree
# LEFT JOIN [AMIS].[dbo].[zdprogm] prog on tree.f_code=prog.f_code
# WHERE tree.[f_code] like :node
# order by floor,tree.f_code
#                 ''')
                query = text('''
SELECT
    tree.[floor]
    ,tree.[f_code]
    ,tree.[up_code]
    ,tree.[f_name]
    ,tree.[f_type]
    ,tree.[station]
    ,STRING_AGG(mname, ',') WITHIN GROUP (ORDER BY mname) AS mname
    ,prog.progm_id
FROM [AMIS].[dbo].[zdtree] tree
LEFT JOIN [AMIS].[dbo].[zdprogm] prog ON tree.f_code = prog.f_code
OUTER APPLY (
    SELECT mname = CAST(amp.mname AS VARCHAR(10))
    FROM [AMIS].[dbo].[ampudmc] amp
    WHERE ',' + tree.station + ',' LIKE CONCAT('%', ',' + amp.station + ',', '%')
) AS m
WHERE tree.[f_code] LIKE :node
GROUP BY tree.[floor], tree.[f_code], tree.[up_code], tree.[f_name], tree.[f_type], tree.[station], prog.progm_id
ORDER BY tree.[floor], tree.[f_code];
                ''')
                result = self.session.execute(query, {'node': node_name})
                # print(result.keys())
                # print(type(result))
                rows = result.fetchall()
                code_dict = {}
                for row in rows:
                    floor = row[0]
                    f_code = row[1]
                    up_code = row[2]
                    f_name = row[3]
                    f_type = row[4]
                    station = row[5]
                    mname = row[6]
                    progm_id = row[7]

                    item = {
                        "Depth": floor,
                        "Code": f_code,
                        "ParentCode": up_code,
                        "Name": f_name,
                        "Type": f_type,
                        "Station": station,
                        "Mname": mname,
                        "ProgramId": progm_id,
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

    def queryroot(self):
        try:
            with self.session.begin():
                query = text('''
                SELECT
                     tree.[floor]
                    ,tree.[f_code]
                    ,tree.[up_code]
                    ,tree.[f_name]
                    ,tree.[f_type]
                FROM [AMIS].[dbo].[zdtree] tree
                WHERE tree.[up_code] ='0'
                order by floor,f_code
                ''')
                result = self.session.execute(query)
                # print(result.keys())
                # print(type(result))
                rows = result.fetchall()
                code_dict = {}
                for row in rows:
                    floor, f_code, up_code, f_name, f_type = row
                    item = {
                        "Depth": floor,
                        "Code": f_code,
                        "ParentCode": up_code,
                        "Name": f_name,
                        "Type": f_type,
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

    def queryall(self):
        try:
            with self.session.begin():
                query = text('''
                SELECT
                     tree.[floor]
                    ,tree.[f_code]
                    ,tree.[up_code]
                    ,tree.[f_name]
                    ,tree.[f_type]
                FROM [AMIS].[dbo].[zdtree] tree
                order by floor,f_code
                ''')
                result = self.session.execute(query)
                # print(result.keys())
                # print(type(result))
                rows = result.fetchall()
                code_dict = {}
                for row in rows:
                    floor, f_code, up_code, f_name, f_type = row
                    item = {
                        "Depth": floor,
                        "Code": f_code,
                        "ParentCode": up_code,
                        "Name": f_name,
                        "Type": f_type,
                        "children": []  # 子项为空列表
                    }
                    code_dict[f_code] = item

                root_items = []
                for f_code, item in code_dict.items():
                    parent_code = item.get("ParentCode")
                    if parent_code == '0':  # 根项目的up_code为0
                        root_items.append(item)
                    else:
                        parent_item = code_dict.get(parent_code)
                        if parent_item:
                            parent_item["children"].append(item)
                        else:
                            root_items.append(item)
                if result:
                    print("Database connection is successful.")
                else:
                    print("Database connection is not working as expected.")
                return root_items
        except OperationalError as e:
            print("Database connection error:", str(e))

    def insert(self, datum):
        # msg = f'{self.__class__.__name__} | DAL insert'
        # logging.debug(msg)
        try:
            if (datum['floor'] == 1):  # 第一層
                with self.session.begin():
                    zdtree = zdtree_add()
                    zdtree.floor = datum['floor']
                    zdtree.f_code = datum['f_code']
                    zdtree.f_type = datum['f_type']
                    zdtree.up_code = 0
                    zdtree.f_name = datum['f_name']
                    zdtree.busr = datum['busr']
                    self.session.add(zdtree)
                    self.session.commit()
                return zdtree.f_code
            else:  # 第一層以外
                with self.session.begin():
                    parent = self.session.query(zdtree_basic).filter_by(
                        f_code=datum['up_code']
                    ).first()
                    if parent is None:
                        return -1

                    children = self.session.query(zdtree_basic).filter_by(
                        up_code=datum['up_code']
                    ).order_by(desc(zdtree_basic.f_code))
                    print(children.count())

                    if (children.count() > 0):
                        sorted_ids = []

                        # 遍歷每個物件
                        for obj in children:
                            # 使用字串替換函數來替換 up_code 部分
                            obj.cid = int(obj.f_code.replace(obj.up_code, ''))
                            sorted_ids.append(obj)

                        # 排序整數陣列
                        sorted_objects = sorted(sorted_ids, key=lambda x: x.cid, reverse=True)  # cid倒序排列
                        maxid = sorted_objects[0].cid
                        new_id_suffix = maxid+1
                    else:
                        new_id_suffix = f"{(datum['floor']-1)}01"
                    logging.debug(f'new_id_suffix={new_id_suffix}')
                    # for child in sorted_objects:
                    #     print(child.cid)

                    zdtree = zdtree_add()
                    zdtree.floor = datum['floor']
                    zdtree.f_code = datum['up_code'] + str(new_id_suffix)
                    zdtree.f_type = datum['f_type']
                    zdtree.up_code = datum['up_code']
                    zdtree.f_name = datum['f_name']
                    if "station" in datum:
                        zdtree.station = datum['station']
                    zdtree.busr = datum['busr']
                    self.session.add(zdtree)

                    childCount = self.session.query(zdtree_basic).filter_by(
                        up_code=datum['up_code'],
                        f_type=datum['f_type']
                    ).count()

                    if parent:
                        parent.sub_num = childCount
                        parent.musr = datum['busr']
                        parent.mdtm = func.sysdatetime()
                        self.session.merge(parent)
                    self.session.commit()
                return zdtree.f_code
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
