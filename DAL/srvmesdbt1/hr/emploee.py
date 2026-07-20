import json
import logging
import os
import datetime
from flask import current_app
from sqlalchemy import create_engine, String, Integer, DateTime
from sqlalchemy.exc import OperationalError
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.sql import func
from Kernel.Helpers import Exclude_Fields
from common import add_to_dict, get_connection_string


class Base(DeclarativeBase):
    pass


@add_to_dict
class employee(Base):
    __tablename__ = 'emploee'
    Emp_Guid: Mapped[str] = mapped_column(String(36))
    COM: Mapped[str] = mapped_column(String(1))
    Emp_ID: Mapped[str] = mapped_column(String(9))
    Email: Mapped[str] = mapped_column(String(255))
    Emp_Name: Mapped[str] = mapped_column(String(20))
    Emp_EName: Mapped[str] = mapped_column(String(100))
    Department_ID: Mapped[str] = mapped_column(String(24))
    Department_ID2: Mapped[str] = mapped_column(String(1024))
    Job_Title: Mapped[str] = mapped_column(String(100))
    Assume_Date: Mapped[datetime.datetime] = mapped_column(DateTime)
    Leave_Date: Mapped[datetime.datetime] = mapped_column(DateTime)
    CreateDate: Mapped[str] = mapped_column(DateTime)
    AccessionState: Mapped[int] = mapped_column(Integer)
    NoPayStatus: Mapped[int] = mapped_column(Integer)
    jobrank: Mapped[int] = mapped_column(Integer)
    cellphone1: Mapped[str] = mapped_column(String(100))
    cellphone2: Mapped[str] = mapped_column(String(100))
    officephone: Mapped[str] = mapped_column(String(100))
    emp_id_hr: Mapped[str] = mapped_column(String(5), primary_key=True)
    last_sync: Mapped[datetime.datetime] = mapped_column(DateTime)
    shift: Mapped[str] = mapped_column(String(1))
    CreateBy: Mapped[str] = mapped_column(String(5))
    ModifyDate: Mapped[str] = mapped_column(DateTime)
    ModifyBy: Mapped[str] = mapped_column(String(5))


class EmploeeDal:
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
            msg = f'{self.__class__.__name__} |An error occurred: {str(e)}'
            print(msg)
            logging.debug(msg)

    def insert(self, emp: employee):
        try:
            session = self.Session()
            emploeeObj = employee()
            for key, value in vars(emp).items():
                print(f'{key} {value}')
                setattr(emploeeObj, key, value)
            emploeeObj.CreateDate = func.sysdatetime()
            session.add(emploeeObj)
            session.commit()

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

    def update(self, emp: employee):
        try:
            session = self.Session()
            emploeeObj = session.query(employee).filter_by(Emp_ID=emp.Emp_ID).first()
            for key, value in vars(emp).items():
                print(f'{key} {value}')
                setattr(emploeeObj, key, value)
            emploeeObj.ModifyDate = func.sysdatetime()
            session.merge(emploeeObj)
            session.commit()

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

    def select(self, quser_id):
        try:
            session = self.Session()
            rst = session.query(employee).filter_by(Emp_ID=quser_id).first()
            session.commit()
            return rst.to_dict()

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

    def query(self, quser):
        try:
            session = self.Session()
            filters = []

            if quser.get("id") is not None:
                filters.append(employee.emp_id_hr == quser["id"])

            if quser.get("idhris") is not None:
                filters.append(employee.Emp_ID == quser["idhris"])

            if quser.get("name") is not None:
                filters.append(employee.Emp_Name == quser["name"])

            rst = session.query(employee).filter(*filters).all()
            session.commit()

            employees_dict = [employee.to_dict() for employee in rst]
            exclude_fields_list = ['CreateBy', 'ModifyDate', 'ModifyBy']

            filtered_employees = Exclude_Fields(employees_dict, exclude_fields_list)
            return filtered_employees

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