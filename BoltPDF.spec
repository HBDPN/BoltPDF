# -*- mode: python ; coding: utf-8 -*-
#
# BoltPDF — onedir build
#
# Why onedir?  A onefile build extracts ~100 MB of bundled DLLs to a
# temp folder on every launch, which adds 2-5 seconds to startup.
# A onedir build keeps the DLLs on disk next to the exe so they are
# memory-mapped directly — startup is near-instant.
#
# The install flow in pdf_reader.py copies the entire directory
# (not just the exe) into C:\Program Files\BoltPDF.

a = Analysis(
    ['pdf_reader.py'],
    pathex=[],
    binaries=[],
    datas=[('ocr_helper.ps1', '.'), ('boltpdf_icon.png', '.'), ('boltpdf_icon.ico', '.'),
           ('LICENSE', '.'), ('THIRD_PARTY_LICENSES.txt', '.')],
    hiddenimports=['PIL', 'multiprocessing', 'pypdf', 'docx', 'fitz', 'pymupdf',
                   'PyQt6.QtWebEngineWidgets', 'PyQt6.QtWebEngineCore',
                   'PyQt6.QtWebChannel', 'PyQt6.QtNetwork'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        # ── Unused PyQt6 modules ─────────────────────────────────
        'PyQt6.QtDesigner', 'PyQt6.QtHelp',
        'PyQt6.QtMultimedia', 'PyQt6.QtMultimediaWidgets',
        'PyQt6.QtNetworkAuth',
        'PyQt6.QtBluetooth', 'PyQt6.QtNfc',
        'PyQt6.QtSensors', 'PyQt6.QtSerialPort',
        'PyQt6.QtDBus', 'PyQt6.QtSql',
        'PyQt6.QtTest', 'PyQt6.QtXml',
        'PyQt6.QtSvg', 'PyQt6.QtSvgWidgets',
        'PyQt6.Qt3DCore', 'PyQt6.Qt3DRender',
        'PyQt6.Qt3DInput', 'PyQt6.Qt3DLogic',
        'PyQt6.Qt3DExtras', 'PyQt6.Qt3DAnimation',
        'PyQt6.QtRemoteObjects',
        'PyQt6.QtTextToSpeech', 'PyQt6.QtPdf',
        'PyQt6.QtPdfWidgets', 'PyQt6.QtCharts',
        'PyQt6.QtDataVisualization', 'PyQt6.QtStateMachine',
        'PyQt6.QtVirtualKeyboard', 'PyQt6.QtWebSockets',
        'PyQt6.QtSpatialAudio',
        # ── Unused stdlib / third-party modules ──────────────────
        'unittest', 'test', 'tkinter', 'sqlite3',
        'xmlrpc',
        'pydoc', 'doctest', 'ftplib', 'imaplib',
        'smtplib', 'poplib', 'telnetlib',
        'turtle', 'turtledemo', 'curses',
        'lib2to3', 'distutils', 'setuptools',
        'numpy', 'pandas', 'scipy', 'matplotlib',
        'pikepdf',
    ],
    noarchive=False,
    optimize=2,
)

pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,   # onedir — binaries go in COLLECT below
    name='BoltPDF',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=['Qt6WebEngine*', 'Qt6Core*', 'Qt6Gui*', 'Qt6Widget*',
                 'Qt6Network*', 'Qt6OpenGL*', 'Qt6Quick*', 'Qt6Qml*',
                 'Qt6WebChannel*', 'Qt6Positioning*', 'QtWebEngineProcess*',
                 'python3*', 'vcruntime*', 'msvcp*', 'ucrtbase*'],
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='boltpdf_icon.ico',
)

coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=['Qt6WebEngine*', 'Qt6Core*', 'Qt6Gui*', 'Qt6Widget*',
                 'Qt6Network*', 'Qt6OpenGL*', 'Qt6Quick*', 'Qt6Qml*',
                 'Qt6WebChannel*', 'Qt6Positioning*', 'QtWebEngineProcess*',
                 'python3*', 'vcruntime*', 'msvcp*', 'ucrtbase*'],
    name='BoltPDF',
)
