import json
import logging
import os
from flask import current_app
from sqlalchemy import create_engine, text, String, Integer
from sqlalchemy.exc import OperationalError
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from Model.srvad6.hr.hdtree import hdtree as HDT
from common import get_connection_string


class Base(DeclarativeBase):
    pass


class hdtree(Base):
    __tablename__ = 'hdtree'
    Sn: Mapped[int] = mapped_column(Integer, primary_key=True)
    IDX: Mapped[int] = mapped_column(Integer)
    OG_MType: Mapped[int] = mapped_column(Integer)
    OG_Msn: Mapped[int] = mapped_column(Integer)
    OG_MID: Mapped[str] = mapped_column(String(50))
    OG_MID_HRIS: Mapped[str] = mapped_column(String(50))
    OG_Name: Mapped[str] = mapped_column(String(100))
    OG_Parent: Mapped[int] = mapped_column(Integer)
    OG_Son: Mapped[int] = mapped_column(Integer)
    OG_level: Mapped[str] = mapped_column(String(100))
    OG_team_sn: Mapped[str] = mapped_column(String(100))
    OG_dept: Mapped[str] = mapped_column(String(100))
    OG_mag: Mapped[str] = mapped_column(String(10))
    OG_Grade: Mapped[int] = mapped_column(Integer)
    OG_status: Mapped[int] = mapped_column(Integer)


class hdtreeDal:
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
            msg = f"{os.path.relpath(__file__,current_app.config['folders']['temproot'])} |An error occurred: {str(e)}"
            logging.info(msg)
            print(msg)

    def to_dict(self, _object):
        user_dict = {
            'Sn': _object.Sn,
            'IDX': _object.IDX,
            'OG_MType': _object.OG_MType,
            'OG_Msn': _object.OG_Msn,
            'OG_MID': _object.OG_MID,
            'OG_MID_HRIS': _object.OG_MID_HRIS,
            'OG_Name': _object.OG_Name,
            'OG_Parent': _object.OG_Parent,
            'OG_Son': _object.OG_Son,
            'OG_level': _object.OG_level,
            'OG_team_sn': _object.OG_team_sn,
            'OG_dept': _object.OG_dept,
            'OG_mag': _object.OG_mag,
            'OG_Grade': _object.OG_Grade,
            'OG_status': _object.OG_status
            }
        return user_dict

    def select(self, user_id):
        try:
            session = self.Session()
            sql_query = text(
                '''
SELECT a.og_name as chsnm, a.og_dept as dept, a.og_team_sn as team_no, a.og_status, b.og_name as dept_name
FROM [srvad6].[hr].[dbo].[hdtree] a
LEFT JOIN [srvad6].[hr].[dbo].[hdtree] b ON b.og_mtype='3' AND b.og_mid=a.og_team_sn
WHERE a.og_mtype NOT IN ('2', '3') AND a.og_mid=:user_id
                '''
            )

            result = session.execute(sql_query, {'user_id': user_id})
            rows = result.fetchall()
            user_objects = [HDT.hr(row).to_dict() for row in rows]
            session.commit()
            return user_objects

        except OperationalError as e:
            print("Database connection error:", str(e))
        except Exception as e:
            print("DAL error:", str(e))
            return e
        finally:
            session.close()
