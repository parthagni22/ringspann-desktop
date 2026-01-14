# -*- mode: python ; coding: utf-8 -*-

import os

a = Analysis(
    ['main.py'],
    pathex=['backend'],  # Add backend to search path
    binaries=[],
    datas=[
        ('backend/app', 'backend/app'),  # Copy backend/app
        ('frontend/dist', 'web'),  # Copy built frontend to 'web' directory
        ('backend/venv/Lib/site-packages/eel/eel.js', 'web'),  # Copy eel.js to web directory
    ],
    hiddenimports=['sqlalchemy', 'eel', 'bottle', 'bcrypt._bcrypt', 'logging'],
    hookspath=[],
    runtime_hooks=[],
    excludes=[],
    cipher=None,
)

pyz = PYZ(a.pure, a.zipped_data)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='QuotationSystem',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,  # Enable console temporarily to see errors
    icon='icon.ico'
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='QuotationSystem'
)