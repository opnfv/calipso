###############################################################################
# Copyright (c) 2017-2019 Koren Lev (Cisco Systems),                          #
# Yaron Yogev (Cisco Systems), Ilia Abashin (Cisco Systems) and others        #
#                                                                             #
# All rights reserved. This program and the accompanying materials            #
# are made available under the terms of the Apache License, Version 2.0       #
# which accompanies this distribution, and is available at                    #
# http://www.apache.org/licenses/LICENSE-2.0                                  #
###############################################################################

# This is an aggregator script to initiate multiple calipso functional tests #
# can be used for functional testing as well as for other testing sent from the UI or API #

import datetime
import os

# will start by calling/running connection_test.py on bash shell
# future plan is to use multiple calls for multiple tests
print(datetime.datetime.utcnow(), ": running connection_test")
os.system("cd /home/scan/calipso & python3 -m scan.connection_test.connection_test -m $MONGO_CONFIG")

