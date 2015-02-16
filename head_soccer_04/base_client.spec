# -*- mode: python -*-

block_cipher = None


a = Analysis(['base_client.py'],
             pathex=['Z:\\home\\ariel\\final\\HeadSoccer'],
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
          name='base_client.exe',
          debug=False,
          strip=None,
          upx=True,
          console=True )
