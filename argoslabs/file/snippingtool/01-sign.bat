REM DEL /Q/S pyinst\Release
REM XCOPY Screenshot\Screenshot\bin\Debug\Screenshot.exe . /O /X /E /H /K
copy /Y Screenshot\Screenshot\bin\Debug\Screenshot.exe .
sign\sign-all.bat
