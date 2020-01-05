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
  source <(grep INSTALL_PHANTOMJS $APP_SOURCE_DIR/launchpad.conf)
  source <(grep PHANTOM_VERSION $APP_SOURCE_DIR/launchpad.conf)
fi

if [ "$INSTALL_PHANTOMJS" = true ]; then
  printf "\n[-] Installing Phantom.js...\n\n"

  PHANTOM_JS="phantomjs-$PHANTOM_VERSION-linux-x86_64"

  apt-get update
  apt-get install -y wget chrpath libssl-dev libxft-dev

  cd /tmp
  wget https://github.com/Medium/phantomjs/releases/download/v$PHANTOM_VERSION/$PHANTOM_JS.tar.bz2
  tar xvjf $PHANTOM_JS.tar.bz2
  mv $PHANTOM_JS /usr/local/share
  ln -sf /usr/local/share/$PHANTOM_JS/bin/phantomjs /usr/local/share/phantomjs
  ln -sf /usr/local/share/$PHANTOM_JS/bin/phantomjs /usr/local/bin/phantomjs
  ln -sf /usr/local/share/$PHANTOM_JS/bin/phantomjs /usr/bin/phantomjs

  apt-get -y purge wget
fi
