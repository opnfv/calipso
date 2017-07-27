########################################################################################
# Copyright (c) 2017 Koren Lev (Cisco Systems), Yaron Yogev (Cisco Systems) and others #
#                                                                                      #
# All rights reserved. This program and the accompanying materials                     #
# are made available under the terms of the Apache License, Version 2.0                #
# which accompanies this distribution, and is available at                             #
# http://www.apache.org/licenses/LICENSE-2.0                                           #
########################################################################################
#!/usr/bin/env bash

SECONDS=0
OS_TARGET_PATH=".."
OS_TARGET_NAME=osdna-meteor-frontend-$(date +%Y-%m-%d-%s).tar.gz
OS_NAME=${PWD##*/}

meteor build $OS_TARGET_PATH/ --architecture=os.linux.x86_64
mv $OS_TARGET_PATH/$OS_NAME.tar.gz $OS_TARGET_PATH/$OS_TARGET_NAME

duration=$SECONDS
echo "$(($duration / 60)) minutes and $(($duration % 60)) seconds elapsed."
