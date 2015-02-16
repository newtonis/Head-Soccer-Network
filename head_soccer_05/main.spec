# -*- mode: python -*-
a = Analysis(['main.py'],
             pathex=['/home/newtonis/Dropbox/Proyectos2015/HeadSoccer/head_soccer_05'],
             hiddenimports=[],
             hookspath=None,
             runtime_hooks=None)
pyz = PYZ(a.pure)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name='main',
          debug=False,
          strip=None,
          upx=True,
          console=True )
