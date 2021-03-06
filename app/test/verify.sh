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
#set -o errexit
#set -o nounset
#set -o pipefail

#sudo yum install -y https://centos7.iuscommunity.org/ius-release.rpm
#sudo yum -y install python35
#sudo pip install virtualenv
#virtualenv -p $(which python3.5) $WORKSPACE/venv       
#. $WORKSPACE/venv/bin/activate

PYTHONPATH=$PWD/app python3 -m unittest discover -s app/test/api
PYTHONPATH=$PWD/app python3 -m unittest discover -s app/test/event_based_scan
PYTHONPATH=$PWD/app python3 -m unittest discover -s app/test/fetch
PYTHONPATH=$PWD/app python3 -m unittest discover -s app/test/scan
PYTHONPATH=$PWD/app python3 -m unittest discover -s app/test/utils
