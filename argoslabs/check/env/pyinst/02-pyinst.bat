REM PYTHON installer for PPM

REM    --add-data README.md;README.md ^
REM    --add-data LICENSE.txt;LICENSE.txt ^
REM    --add-data requirements.txt;requirements.txt ^
REM    --add-data setup.yaml;setup.yaml ^

DEL /Q/S exe
DEL /Q/S build
DEL /Q/S dist

REM sign.bat

COPY __main__.py alabs-ppm-main.py

REM     --onefile ^
REM    __main__.py
rem    --uac-admin ^

pyinstaller ^
    --add-data pyinst;. ^
    --add-data setup.yaml;. ^
    alabs-ppm-main.py

if %ERRORLEVEL% == 0 goto :next2
    echo "Errors encountered during pyinstaller.  Exited with status: %errorlevel%"
    goto :endofscript
:next2

mkdir exe
REM move __pycache__ exe
REM move build exe
REM move dist exe
MOVE dist\alabs-ppm-main exe

sign\SignTool.exe sign ^
    /f sign\20190703-774162_CHAIN_argos-labs_com.pfx ^
    -p han!@35ssl ^
    /v -tr "http://sha256timestamp.ws.symantec.com/sha256/timestamp" ^
    exe\alabs-ppm-main\alabs-ppm-main.exe

REM for test
REM COPY exe\dist\alabs-ppm.exe C:\work\ppm\ppm.exe

DEL /Q/S build
DEL /Q/S dist

:endofscript
echo "Script complete"
