# -*- mode: python ; coding: utf-8 -*-
import os
import datetime
from PyInstaller.utils.hooks import collect_submodules, collect_data_files

SETUP_DIR=r'C:\Project\@Web\Api2' 
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

a = Analysis(
    ['app.py','common.py','fta_response.py']+ python_files,
    pathex=[],
    binaries=[],
    datas=datas,
    hiddenimports=['flask', 'json', 'os', 'uuid', 'datetime', 'sys', 'logging', 'flask_restx', 'flask_socketio', 'pyodbc', 'pillow', 'selenium', 'flask_socketio'] + collect_submodules('flask_restx') + collect_submodules('jwt') + collect_submodules('sqlalchemy') + collect_submodules('icecream'),
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False
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
    a.binaries,
    a.datas,
    [],
    name=app_name,
    debug=True,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    version='versioninfo.txt'
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
