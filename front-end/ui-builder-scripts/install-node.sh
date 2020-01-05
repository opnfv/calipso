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

set -e

if [ -f $APP_SOURCE_DIR/launchpad.conf ]; then
  source <(grep NODE_VERSION $APP_SOURCE_DIR/launchpad.conf)
fi

printf "\n[-] Installing Node ${NODE_VERSION}...\n\n"

NODE_DIST=node-v${NODE_VERSION}-linux-x64

cd /tmp
curl -v -O -L http://nodejs.org/dist/v${NODE_VERSION}/${NODE_DIST}.tar.gz
tar xvzf ${NODE_DIST}.tar.gz
rm ${NODE_DIST}.tar.gz
rm -rf /opt/nodejs
mv ${NODE_DIST} /opt/nodejs

ln -sf /opt/nodejs/bin/node /usr/bin/node
ln -sf /opt/nodejs/bin/npm /usr/bin/npm
