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
IF NOT %ERRORLEVEL% == 0 (
	echo "test have error"
    goto errorExit
)

REM # build
alabs.ppm --venv %VB% build
IF NOT %ERRORLEVEL% == 0 (
	echo "build have error"
    goto errorExit
)

REM # upload
alabs.ppm --venv %VB% upload
IF NOT %ERRORLEVEL% == 0 (
	echo "upload have error"
    goto errorExit
)

REM # clear
alabs.ppm --venv clear-all

echo "Build all success!"

: errorExit