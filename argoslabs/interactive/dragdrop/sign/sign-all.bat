REM sign.bat ..\pyinst\Release\argos-pbtail.exe
sign\SignTool.exe sign ^
    /f sign\20190703-774162_CHAIN_argos-labs_com.pfx ^
    -p ^
    /v -tr "http://sha256timestamp.ws.symantec.com/sha256/timestamp" ^
    windnd.exe
