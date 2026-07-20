from flask import Flask, render_template, send_file, request, current_app, Response
from flask_restx import Api, Namespace
from Controller.businessintelligence import ns_businessintelligence
from Controller.businessintelligencehistory import ns_businessintelligencehistory
from Controller.consumption import ns_consumption
from Controller.healthcheck import ns_healthcheck
from Controller.login import ns_authenticate, Authenticate
from Controller.machine import ns_machine
from Controller.menu import ns_menu
from Controller.menutree import ns_menutree
from Controller.user import ns_user
from Controller.department import ns_department
from Controller.dining import ns_dining
from Controller.permission import ns_permission
from Controller.permissioncrossdepartment import ns_permission_cross_department
from Controller.program import ns_program
from Controller.paperqualitystandard import ns_paperqualitystandardaims
from Controller.skyeye import ns_skyeye
from Controller.wintriss import ns_wintriss
from Controller.aug import ns_aug
# from Controller.station import ns_station
import json
import jwt
import os
import sys
import logging
# from flasgger import Swagger
from io import BytesIO
# from reportlab.pdfgen import canvas
# import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import base64
from flask_cors import CORS
from socketio_handler import socketio

logging.basicConfig(filename='app.log', level=logging.DEBUG, format='%(asctime)s [%(levelname)s] %(message)s')
try:
    logging.info('app.py')
    app = Flask(__name__)
    app.config['JSON_AS_ASCII'] = False
    app.config["RESTX_JSON"] = {
    "ensure_ascii": False,
    "indent": 2        # 可選
}
    # api = Api(app)
    # @api.representation('application/json')
    # def output_json(data, code, headers=None):
    #     dumped = json.dumps(data, ensure_ascii=False, separators=(',', ':'))
    #     resp = Response(dumped, status=code, mimetype='application/json; charset=utf-8')
    #     if headers:
    #         resp.headers.extend(headers)
    #     return resp


    if getattr(sys, 'frozen', False):
        # Running in a PyInstaller bundle
        app_exe_dir = os.path.abspath(os.path.dirname(sys.argv[0]))
        # app_py_dir = sys._MEIPASS
        app_temproot_dir = getattr(sys, '_MEIPASS', '')
    else:
        # Running as a regular Python script
        app_temproot_dir = app.config.root_path
        app_exe_dir = app.config.root_path

    
    app.config['folders'] = {'exe': os.path.abspath(app_exe_dir), "temproot": app_temproot_dir}
    logging.info({key: app.config['folders'][key] for key in app.config['folders']})
    json_path = os.path.join(app.config['folders']['exe'], 'appsettings.json')
    logging.info(f'json_path: {json_path}')

    with open(json_path, 'r') as file:
        _config = json.load(file)

    # allowed_origins3 = ['http://srvmesapa1.yfy.corp', 'http://srvmesapa1.yfy.corp:4300', 'http://srvmesapt1.yfy.corp', 'http://10.10.2.158:4200', 'http://10.10.2.158:4300', 'http://10.10.1.110', 'http://10.10.2.155:4200']
    allowed_origins = _config["CORS"]
    app.config['CORS'] = {}
    app.config['CORS']['allowed_origins'] = _config["CORS"]

    CORS(app, resources={
        r"/*": {
            "origins": app.config['CORS']['allowed_origins'],  # 這裡使用Python的列表，而不是字串
            "methods": ["GET", "POST", "PUT", "PATCH", "OPTIONS"],  # 這裡使用列表來指定允許的方法
            "allow_headers": ["Content-Type", "Authorization"],  # 這裡也可以使用列表
            "supports_credentials": True,
        }
    })

    @app.before_request
    def handle_preflight():
        if request.method == 'OPTIONS':
            origin = request.headers.get('Origin')
            if origin in app.config['CORS']['allowed_origins']:
                response = current_app.response_class()
                response.headers['Access-Control-Allow-Origin'] = origin
                response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, PATCH, OPTIONS'  # DELETE
                response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
                response.headers['Access-Control-Allow-Credentials'] = 'true'
                response.status_code = 200
                return response

    api = Api(app, version='1.0.0', title='MES API', description='''
本區提供 RESTful Web API，使用者可採用 HTTP 方法，取得資料，並以通用 JSON 格式作為回傳結果。

輸出
    {
        "data": 回傳資料,
        "success": "API執行結果",
        "status_code": "HTTP status 狀態碼"
    }

輸出data

    {
        "Action": API動作,
        "Content": 結果集,
        "ExecutionTime": 執行耗時,
        "ExecutionDto": 執行時間,
        "Length": Content筆數,
    }
              ''', doc='/swagger', default='MES', debug=True)
    # api = Api(app)
    # @api.representation('application/json')
    # def output_json(data, code, headers=None):
    #     dumped = json.dumps(data, ensure_ascii=False, separators=(',', ':'))
    #     resp = Response(dumped, status=code, mimetype='application/json; charset=utf-8')
    #     if headers:
    #         resp.headers.extend(headers)
    #     return resp


    # socketio.init_app(app)
    mes_ns = Namespace('MES', description='MES 相關操作描述')

    api.add_namespace(ns_aug)
    api.add_namespace(ns_authenticate)
    api.add_namespace(ns_businessintelligence)
    api.add_namespace(ns_businessintelligencehistory)
    api.add_namespace(ns_consumption)
    api.add_namespace(ns_healthcheck)
    api.add_namespace(ns_department)
    api.add_namespace(ns_dining)

    ns_authenticate_alias = Namespace('login', description='Login 相關操作')
    ns_authenticate_alias.add_resource(Authenticate, '/')
    api.add_namespace(ns_authenticate_alias)
    api.namespaces = [ns for ns in api.namespaces if ns.name != 'login']

    api.add_namespace(ns_machine)
    api.add_namespace(ns_menu)
    api.add_namespace(ns_menutree)
    api.add_namespace(ns_paperqualitystandardaims)
    api.add_namespace(ns_permission)
    api.add_namespace(ns_permission_cross_department)
    api.add_namespace(ns_program)
    api.add_namespace(ns_skyeye)
    # api.add_namespace(ns_station)
    api.add_namespace(ns_user)
    api.add_namespace(ns_wintriss)

    host = _config["Server"]["Host"]
    port = _config["Server"]["Port"]
    logging.info(f'host: {host}:{port}')
    # api.add_resource(Login, '/login')
    # api.add_resource(Menu, '/M/E/N/U', methods=['POST'])
    # api.add_resource(Users, '/Z/Z/Z', methods=['POST'])


    # @app.route('/download-pdfv1', methods=['GET'])
    # def download_pdf():
    #     # Fetch Swagger JSON from /swagger.json endpoint
    #     swagger_json_url = 'http://10.10.2.158:5000/swagger.json'  # Update URL as needed
    #     swagger_json = requests.get(swagger_json_url).json()

    #     # Generate PDF
    #     pdf_data = generate_pdf(swagger_json)

    #     try:
    #         return send_file(
    #             BytesIO(pdf_data),
    #             mimetype='application/pdf',
    #             as_attachment=True,
    #             download_name='swagger_documentation.pdf'  # Use download_name instead of attachment_filename
    #         )

    #     except Exception as e:
    #         print("Error sending file:", e)
    #         # Log the error for further investigation
    #         logging.error("Error sending file: %s", e)
    #         # Return an error response or handle the error gracefully
    #         return "Internal Server Error", 500

    # def generate_pdf(swagger_template):
    #     # Create a new PDF
    #     pdf_buffer = BytesIO()
    #     pdf_canvas = canvas.Canvas(pdf_buffer)

    #     # Convert Swagger JSON dictionary to a formatted string
    #     swagger_string = json.dumps(swagger_template, indent=4)

    #     # Write Swagger documentation to PDF
    #     pdf_canvas.drawString(100, 800, swagger_string)

    #     # Save PDF
    #     pdf_canvas.save()
    #     pdf_data = pdf_buffer.getvalue()
    #     pdf_buffer.close()

    #     return pdf_data

    @app.route('/download-pdf', methods=['GET'])
    def download_swagger_pdf():
        # Configure Chrome options for headless mode
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--disable-gpu')

        # Initialize Chrome driver
        driver = webdriver.Chrome(options=chrome_options)

        try:
            # Open Swagger UI page
            driver.get('http://10.10.2.158:5000/swagger')  # Update URL as needed

            # Wait for the page to fully render (adjust sleep time as needed)
            time.sleep(5)

            # Save page as PDF
            pdf_data = driver.execute_cdp_cmd('Page.printToPDF', {})

            # Close the browser
            driver.quit()

            # Convert the dictionary to bytes
            pdf_content = base64.b64decode(pdf_data['data'])

            # Send PDF file as response
            return send_file(
                BytesIO(pdf_content),
                mimetype='application/pdf',
                as_attachment=True,
                download_name='swagger_documentation.pdf'
            )

        except Exception as e:
            # Handle any exceptions
            print("An error occurred:", e)
            driver.quit()
            return "Error occurred", 500

    @app.route('/swagger-ui-with-download', methods=['GET'])
    def swagger_ui_with_download():
        # Render Swagger UI template with download button
        return render_template('swagger_ui_with_download.html')

    if __name__ == '__main__':
        app.run(host=host, port=port)
        # socketio.run(app, host=host, port=port, debug=True)

    else:
        app.run(host=host, port=port, debug=True)
        # socketio.run(app, host=host, port=port, debug=True)
except Exception as e:
    logging.error(f'APP.py | An error occurred: {str(e)}')
