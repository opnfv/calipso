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

printf "\n[-] Performing post install cleanup...\n\n"

# Clean out docs
rm -rf /usr/share/{doc,doc-base,man,locale,zoneinfo}

# Clean out package management dirs
rm -rf /var/lib/{cache,log}

# clean additional files created outside the source tree
rm -rf /root/{.cache,.config,.local}
rm -rf /tmp/*

# remove os dependencies
apt-get -y autoremove
rm -rf /var/lib/apt/lists/*
