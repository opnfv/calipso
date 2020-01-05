#!/usr/bin/env bash
###############################################################################
# Copyright (c) 2017-2018 Koren Lev (Cisco Systems),                          #
# Yaron Yogev (Cisco Systems), Ilia Abashin (Cisco Systems) and others        #
#                                                                             #
# All rights reserved. This program and the accompanying materials            #
# are made available under the terms of the Apache License, Version 2.0       #
# which accompanies this distribution, and is available at                    #
# http://www.apache.org/licenses/LICENSE-2.0                                  #
###############################################################################

OS_TARGET_PATH=".."

# Compress current source to a tar object. 
# -exclude: Excluding specific folders and files
# -z: use gzip
# -c: create new archive
# -v: verbose log file processed
# -f: use archive file as target to build the tar to.
tar \
  --exclude='./.meteor/local' \
  --exclude='./node_modules' \
  --exclude='./.git' \
  -zcvf $OS_TARGET_PATH/calipso-source-$(date +%Y-%m-%d-%s).tar.gz .
