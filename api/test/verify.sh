#!/bin/bash
###############################################################################
# Copyright (c) 2017-2018 Koren Lev (Cisco Systems),                          #
# Yaron Yogev (Cisco Systems), Ilia Abashin (Cisco Systems) and others        #
#                                                                             #
# All rights reserved. This program and the accompanying materials            #
# are made available under the terms of the Apache License, Version 2.0       #
# which accompanies this distribution, and is available at                    #
# http://www.apache.org/licenses/LICENSE-2.0                                  #
###############################################################################
set -o errexit
set -o nounset
set -o pipefail
PYTHONPATH=$PWD python3 -m unittest discover -s api/test/api
PYTHONPATH=$PWD python3 -m unittest discover -s listen/test/event_based_scan/
PYTHONPATH=$PWD python3 -m unittest discover -s scan/test/fetch/
PYTHONPATH=$PWD python3 -m unittest discover -s scan/test/scan
