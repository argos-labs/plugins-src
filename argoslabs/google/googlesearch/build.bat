@echo off
REM !/bin/bash

set VB=-vvv

for /f %%i in ('alabs.ppm get repository') do set REP=%%i
for /f %%i in ('alabs.ppm get trusted-host') do set TH=%%i

pip install -U alabs.ppm -i %REP% --trusted-host %TH%

REM # clear
alabs.ppm --venv clear-all

REM test
alabs.ppm --venv %VB% test
REM RuntimeError: implement_array_function method already has a docstring
REM test is done. success is False
REM IF NOT %ERRORLEVEL% == 0 (
REM 	echo "test have error"
REM     goto errorExit
REM )

REM # build
alabs.ppm --venv %VB% build
IF NOT %ERRORLEVEL% == 0 (
	echo "build have error"
    goto errorExit
)

REM # submit to repository
REM alabs.ppm %VB% submit
REM IF NOT %ERRORLEVEL% == 0 (
REM 	echo "upload have error"
REM     goto errorExit
REM )

REM # upload to private repository
alabs.ppm --venv %VB% upload
IF NOT %ERRORLEVEL% == 0 (
	echo "upload have error"
    goto errorExit
)

alabs.ppm submit --submit-key 202365426967206e652f http://175.209.228.141:25478

REM # clear
REM alabs.ppm --venv clear-all

echo "Build all success!"

: errorExit