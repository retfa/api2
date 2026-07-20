# -*- mode: python ; coding: utf-8 -*-
import os
import datetime
from PyInstaller.utils.hooks import collect_all

SETUP_DIR=r'C:\Project\@Web\flaskApi\MES' 
directories = ['Model', 'Controller', 'DAL', 'BLL', 'Kernel']
python_files = []

for directory in directories:
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.py'):
                python_files.append(os.path.join(root, file))

datas = [
    ('connections.json', '.'),
    ('security.json', '.'),
    ('common.py', '.'),
    ('socketio_handler.py', '.'),
    (r'Kernel\JsonConverter.py', '.'),
    (r'Kernel\RequestHandler.py', '.'),
    ('fta_response.py', '.'),
]

for directory in directories:
    datas.append((directory, directory))

# Collect all data and submodules for jwt
flask_restx_all = collect_all('flask_restx')
jwt_all = collect_all('jwt')
sqlalchemy_all = collect_all('sqlalchemy')
icecream_all = collect_all('icecream')

hiddenimports = [
    'flask', 'json', 'os', 'uuid', 'datetime', 'sys', 'logging', 
    'flask_restx', 'flask_socketio', 'pyodbc', 'pillow', 
    'selenium', 'flask_socketio'
] + flask_restx_all[1] + jwt_all[1] + sqlalchemy_all[1] + icecream_all[1]

datas += flask_restx_all[0] + jwt_all[0] + sqlalchemy_all[0] + icecream_all[0]


a = Analysis(
    ['app.py','common.py','fta_response.py']+ python_files,
    pathex=[SETUP_DIR],
    binaries=[],
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)
pyz = PYZ(a.pure)

# 生成當前日期和時間
current_time = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
# 定義動態的應用名稱
# app_name = f'api2_{current_time}'
app_name = f'api2'

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name=app_name,
    debug=True,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name=app_name,
)
