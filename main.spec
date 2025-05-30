# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=[
        'keyboard', 
        'PIL._imaging',
        'pyautogui',
        'reportlab.pdfgen',
        'reportlab.lib',
        'requests',
        'webbrowser',
        'tkinter',
        'src.config.config',
        'src.core.screenshot',
        'src.core.pdf_generator',
        'src.core.automation',
        'src.core.update_checker',
        'src.gui.main_window'
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        # Excluir bibliotecas científicas desnecessárias
        'numpy',
        'scipy',
        'pandas',
        'matplotlib',
        'nibabel',
        'nipype',
        'networkx',
        'traits',
        'prov',
        'rdflib',
        'lxml',
        'configobj',
        'etelemetry',
        'pydot',
        'pyxnat',
        'starlette',
        'uvicorn',
        'aiofiles',
        'anyio',
        'h11',
        'sniffio',
        'acres',
        'ci-info',
        'frontend',
        'looseversion',
        'puremagic',
        'simplejson',
        'chardet',
        'configparser',
        'httplib2',
        'isodate',
        'itsdangerous'
    ],
    noarchive=False,
    optimize=2,
)

pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='PDF-Maker',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,  # Alterar para False para modo GUI
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
    strip=False,  # Desativado para evitar erros
    upx=True,
    upx_exclude=[],
    name='PDF-Maker'
)
