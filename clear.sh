#!/bin/bash

rm -rf *.log *.egg-info
rm -rf dist build __pycache__
rm -f setup.*

find . -name "._*" -exec rm -f {} \;
