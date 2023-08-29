#!/bin/bash

VB=-vvv
#VB=

# for linux alabs.ppm bin
export PATH=$PATH:/home/toor/.local/bin

REP=$(alabs.ppm get repository)
TH=$(alabs.ppm get trusted-host)

# install alabs.ppm
pip3 install -U alabs.ppm -i $REP --trusted-host $TH

# clear
alabs.ppm --venv clear-all

# test
alabs.ppm --venv $VB test
if [ $? -ne 0 ];then
	RC=$?
	echo "test failed!"
	exit $RC
fi

# build
alabs.ppm --venv $VB build
if [ $? -ne 0 ];then
	RC=$?
	echo "build failed!"
	exit $RC
fi

# submit to repository
alabs.ppm $VB submit
if [ $? -ne 0 ];then
	RC=$?
	echo "upload failed!"
	exit $RC
fi

# upload to private repository
alabs.ppm --venv $VB upload
if [ $? -ne 0 ];then
	RC=$?
	echo "upload failed!"
	exit $RC
fi

# clear
alabs.ppm --venv clear-all
