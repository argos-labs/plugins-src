@ECHO OFF
REM testall.bat

REM SET EXE=python ..\rdb_op.py
SET EXE=..\..\..\..\exe\windows\rdb_op.exe

SET CONN=mysql:10.211.55.8:3306:myuser:myuser123!@#:mytest

REM 1) create-table
%EXE% -f 2010-create-table.sql %CONN%
set /p DUMMY=Do 2010-create-table.sql -- Hit ENTER to continue...
%EXE% -f 2020-static-insert.sql %CONN%
set /p DUMMY=Do 2020-static-insert.sql -- Hit ENTER to continue...
%EXE% -f 2030-template-insert.sql -i foo.csv -x 1 %CONN%
set /p DUMMY=Do 2030-template-insert.sql -- Hit ENTER to continue...
%EXE% -q -f 2040-select.sql %CONN%
set /p DUMMY=Do 2040-select.sql -- Hit ENTER to continue...
%EXE% -f 2050-drop-table.sql %CONN%
set /p DUMMY=Do 2050-drop-table.sql -- Hit ENTER to continue...

REM -f test\2010-create-table.sql mysql:10.211.55.8:3306:myuser:myuser123!@#:mytest
REM -f test\2020-static-insert.sql mysql:10.211.55.8:3306:myuser:myuser123!@#:mytest
REM -f test\2030-template-insert.sql -i test\foo.csv -x 1 mysql:10.211.55.8:3306:myuser:myuser123!@#:mytest
REM -q -f test\2040-select.sql mysql:10.211.55.8:3306:myuser:myuser123!@#:mytest
REM -f test\2050-drop-table.sql mysql:10.211.55.8:3306:myuser:myuser123!@#:mytest

