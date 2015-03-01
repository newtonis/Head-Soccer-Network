# -*- mode: python -*-

block_cipher = None


a = Analysis(['C:\\users\\dylan\\dropbox\\Proyectos2015\\HeadSoccer\\head_soccer_05\\server_run.py'],
             pathex=['C:\\Users\\Dylan\\Dropbox\\Proyectos2015\\HeadSoccer\\head_soccer_05\\pyinstaller-develop\\HeadSoccerServer'],
             hiddenimports=[],
             hookspath=None,
             runtime_hooks=None,
             excludes=None,
             cipher=block_cipher)
pyz = PYZ(a.pure,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name='HeadSoccerServer.exe',
          debug=False,
          strip=None,
          upx=True,
          console=True )
