# -*- mode: python ; coding: utf-8 -*-

block_cipher = None
import importlib
import pathlib
package_imports = [['qtmodern', ['resources/frameless.qss', 'resources/style.qss']]]

added_file = []
for package, files in package_imports:
    proot = pathlib.Path(importlib.import_module(package).__file__).parent
    added_file.extend((proot / f, package) for f in files)
block_cipher = None

added_file += [("C:\\Users\\hunte\\OneDrive\\Desktop\\Adelphi\\splashscreen.gif", '.' )]
added_file += [("C:\\Users\\hunte\\OneDrive\\Desktop\\Adelphi\\adellphi.png", '.' )]
a = Analysis(['adellphi.py'],
             pathex=['C:\\Users\\hunte\\OneDrive\\Desktop\\Adelphi'],
             binaries=[],
             datas=added_file,
             hiddenimports=['PyQt5'],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          [],
          name='adellphi',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=True )
