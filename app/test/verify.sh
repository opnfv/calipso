#!/bin/bash
###############################################################################
# Copyright (c) 2017 Koren Lev (Cisco Systems), Yaron Yogev (Cisco Systems)   #
# and others                                                                  #
#                                                                             #
# All rights reserved. This program and the accompanying materials            #
# are made available under the terms of the Apache License, Version 2.0       #
# which accompanies this distribution, and is available at                    #
# http://www.apache.org/licenses/LICENSE-2.0                                  #
###############################################################################

ret=0
PYTHONPATH=$PWD/app python3 -m unittest discover -s app/test/api
if [ $? -eq 1 ]; then ret=1; fi
PYTHONPATH=$PWD/app python3 -m unittest discover -s app/test/event_based_scan
if [ $? -eq 1 ]; then ret=1; fi
PYTHONPATH=$PWD/app python3 -m unittest discover -s app/test/fetch
if [ $? -eq 1 ]; then ret=1; fi
PYTHONPATH=$PWD/app python3 -m unittest discover -s app/test/scan
if [ $? -eq 1 ]; then ret=1; fi
PYTHONPATH=$PWD/app python3 -m unittest discover -s app/test/utils
if [ $? -eq 1 ]; then ret=1; fi
if [ $ret ]; then false; fi
