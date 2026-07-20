from flask import current_app
from sqlalchemy import create_engine, text
from sqlalchemy.exc import OperationalError
from sqlalchemy.orm import sessionmaker
import pyodbc
import json
import os
import logging
import re
from ldap3 import ALL_ATTRIBUTES, SUBTREE, Server, Connection, ALL, KERBEROS, SAFE_SYNC

from Model.user import UserDto
from common import get_connection_string


class Authentication:
    def __init__(self, folders):
        trace_msg = f'{self.__class__.__name__}'
        print(trace_msg)
        logging.info(trace_msg)
        try:
            json_path = os.path.join(
                current_app.config['folders']['exe'], 'appsettings.json')
            print(f'appsettings.json_path: {json_path}')
            with open(json_path, 'r') as file:
                _config = json.load(file)
            DbHostName = _config["Database"]["HostName"]

            json_path = os.path.join(
                current_app.config['folders']['temproot'], 'connections.json')
            print(f'json_path: {json_path}')
            cs_name = f'{DbHostName}_AMIS'
            print(cs_name)

            connection_string = get_connection_string(json_path, cs_name)
            self.engine = create_engine(connection_string, echo=False)
            session = sessionmaker(bind=self.engine)
            self.session = session()
        except Exception as e:
            msg = f'auth.py |An error occurred: {str(e)}'
            logging.info(msg)
            print(msg)

    def Auth(self, data: UserDto.user_login):
        user = self.CheckByAd(data)
        if user is None:
            user = self.CheckByLocal(data)

        return user

    def CheckByAd(self, data):
        # 設定 AD 伺服器的相關資訊
        AD_SERVER = 'ldap://10.10.1.1'  # Active Directory 伺服器地址
        # 建立伺服器物件並設定安全層級
        server = Server(AD_SERVER, get_info=ALL)
        try:
            conn = Connection(server, fr"yfy\{data.login_id}", data.password, auto_bind=True)

            # 嘗試連線並驗證登入
            if conn.bind():
                print("登入成功")
                # base_dn = "OU=資管組,OU=久堂廠,OU=纖維材料事業部,OU=總經理,OU=中華紙漿股份有限公司,OU=永豐餘控股,OU=Company,DC=yfy,DC=corp"
                # base_dn = "OU=久堂廠,OU=纖維材料事業部,OU=總經理,OU=中華紙漿股份有限公司,OU=永豐餘控股,OU=Company,DC=yfy,DC=corp"
                base_dns = [
                    "OU=久堂廠,OU=纖維材料事業部,OU=總經理,OU=中華紙漿股份有限公司,OU=永豐餘控股,OU=Company,DC=yfy,DC=corp",
                    "OU=久堂廠,OU=Group,OU=TW-久堂廠,OU=YFY_TW,OU=YFY,DC=yfy,DC=corp"
                ]

                search_filter = f"(sAMAccountName={data.login_id})"  # 用戶名的篩選條件
                attributes = ['cn', 'displayname', 'samaccountname', 'distinguishedName', 'employeeID']  # 欲取得的屬性

                results = []  # 儲存查詢結果
                for base_dn in base_dns:
                    # 執行查詢
                    conn.search(search_base=base_dn,
                                search_filter=search_filter,
                                search_scope=SUBTREE,
                                attributes=attributes,
                                get_operational_attributes=False,
                                size_limit=1
                                )
                    results.extend(conn.entries)

                # 顯示查詢結果
                if len(results) == 1:
                    try:
                        with self.session.begin():
                            query = text('''
                SELECT mes.*, AIMS.Sn
                FROM [AMIS].[dbo].[zmuser] mes
                LEFT JOIN [SRVMSDBA1].[AIMSFTAZ].[dbo].[zuser_m] aims
                ON mes.user_id_hris collate Chinese_Traditional_Bopomofo_100_CS_AS_KS_WS = aims.IdHris
                WHERE mes.user_id_hris=:login_id and mes.status='Y'
            ''')
                            result = self.session.execute(
                                query, {'login_id': str(results[0].cn)})
                            row = result.fetchone()
                            if row:
                                user_data = UserDto.user_signedIn(
                                    row.user_id, row.user_id_hris, row.user_name, row.Sn)
                                self.reset_error_counter(data)

                                print(user_data)
                                if result:
                                    print("Database connection is successful.")
                                else:
                                    print(
                                        "Database connection is not working as expected.")
                                return user_data
                            else:
                                self.increase_error_counter(data)
                    except OperationalError as e:
                        print("Database connection error:", str(e))
                    else:
                        print("未找到使用者資訊")

                # 結束連線
                conn.unbind()  # 完成後解除連線
            else:
                print("登入失敗，請檢查使用者名稱或密碼")
        except:
            pass

    def CheckByLocal(self, data):
        try:
            with self.session.begin():
                # patternLocal = r"^[A-Za-z]\d{4}$"  # 匹配5碼工號一個英文字母後接4個數字
                patternHirs = r"^\d{9}$"  # 匹配9碼工號9個數字

                if re.match(patternHirs, data.login_id):
                    query = text('''
    SELECT mes.*, AIMS.Sn
    FROM [AMIS].[dbo].[zmuser] mes
    LEFT JOIN [SRVMSDBA1].[AIMSFTAZ].[dbo].[zuser_m] aims
    ON mes.user_id_hris collate Chinese_Traditional_Bopomofo_100_CS_AS_KS_WS = aims.IdHris
    WHERE mes.user_id_hris=:login_id and mes.pwd=:password and mes.status='Y'
''')
                # elif re.match(patternLocal, data.login_id):
                else:
                    query = text('''
    SELECT mes.*, AIMS.Sn
    FROM [AMIS].[dbo].[zmuser] mes
    LEFT JOIN [SRVMSDBA1].[AIMSFTAZ].[dbo].[zuser_m] aims
    ON mes.user_id_hris collate Chinese_Traditional_Bopomofo_100_CS_AS_KS_WS = aims.IdHris
    WHERE mes.user_id=:login_id and mes.pwd=:password and mes.status='Y'
''')
                result = self.session.execute(
                    query, {'login_id': data.login_id, 'password': data.password})
                row = result.fetchone()
                if row:
                    user_data = UserDto.user_signedIn(
                        row.user_id, row.user_id_hris, row.user_name, row.Sn)
                    self.reset_error_counter(data)

                    print(user_data)
                    if result:
                        print("Database connection is successful.")
                    else:
                        print("Database connection is not working as expected.")
                    return user_data
                else:
                    self.increase_error_counter(data)
        except OperationalError as e:
            print("Database connection error:", str(e))

    def increase_error_counter(self, data: UserDto.user_login):
        try:
            # patternLocal = r"^[A-Za-z]\d{4}$"  # 匹配5碼工號一個英文字母後接4個數字
            patternHris = r"^\d{9}$"  # 匹配9碼工號9個數字
            error_limit = 4
            print(type(error_limit))
            if re.match(patternHris, data.login_id):
                query = text(
                    f"Update [AMIS].[dbo].[zmuser] SET pwderrcount = pwderrcount + 1, status= CASE WHEN pwderrcount >={str(error_limit)} THEN 'L' ELSE status END WHERE user_id_hris=:login_id")
            # elif re.match(patternLocal, data.login_id):
            else:
                query = text(
                    f"Update [AMIS].[dbo].[zmuser] SET pwderrcount = pwderrcount + 1, status= CASE WHEN pwderrcount >={str(error_limit)} THEN 'L' ELSE status END WHERE user_id=:login_id")

            self.session.execute(
                query, {'login_id': data.login_id, 'password': data.password})
        except OperationalError as e:
            print("Database connection error:", str(e))

    def reset_error_counter(self, data: UserDto.user_login):
        try:
            # patternLocal = r"^[A-Za-z]\d{4}$"  # 匹配5碼工號一個英文字母後接4個數字
            patternHris = r"^\d{9}$"  # 匹配9碼工號9個數字

            if re.match(patternHris, data.login_id):
                query = text(
                    "Update [AMIS].[dbo].[zmuser] SET pwderrcount = 0 WHERE user_id_hris=:login_id and pwd=:password")
            # elif re.match(patternLocal, data.login_id):
            else:
                query = text(
                    "Update [AMIS].[dbo].[zmuser] SET pwderrcount = 0 WHERE user_id=:login_id and pwd=:password")

            self.session.execute(
                query, {'login_id': data.login_id, 'password': data.password})
        except OperationalError as e:
            print("Database connection error:", str(e))
