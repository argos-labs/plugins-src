REM DEL /Q/S pyinst\Release
REM XCOPY windnd\windnd\bin\Release\windnd.exe . /O /X /E /H /K
copy /Y windnd\windnd\bin\Release\windnd.exe .
sign\sign-all.bat
