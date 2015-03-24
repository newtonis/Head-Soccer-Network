# -*- mode: python -*-

block_cipher = None


a = Analysis(['../head_soccer_06_3/server_run.py'],
             pathex=['/home/newtonis/head_soccer_network/head_soccer_executables'],
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
          name='head_soccer_06_3Server',
          debug=False,
          strip=None,
          upx=True,
          console=True )
