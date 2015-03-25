..\pyinstaller\pyinstaller.py ..\%1\main.py --onefile -n%1
..\pyinstaller\pyinstaller.py ..\%1\server_run.py --onefile -n%1Server
mkdir %1
move dist\%1.exe %1\%1.exe
move dist\%1Server.exe %1\%1Server.exe
xcopy ..\%1\databases %1\databases /e /i /y
xcopy ..\%1\fonts %1\fonts /e /i /y
xcopy ..\%1\images %1\images /e /i /y
xcopy ..\%1\server_db %1\server_db /e /i /y
rmdir dist /S /Q
rmdir build /S /Q
del %1.spec
del %1Server.spec