# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['diagonal-PASEF_slope_checker.py'],
    pathex=[],
    binaries=[],
    datas=[('C:\\Users\\tobias.kroniger\\OneDrive - Bruker Physik GmbH\\Dokumente\\Python\\diagonal-PASEF_Slope_Checker_Final\\v0.1.1\\logo.ico', '.')],
    hiddenimports=[],
    hookspath=['.'],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='diagonal-PASEF_slope_checker',
    debug=False,
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
    icon=['logo.ico'],
)
