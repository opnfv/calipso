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

echo "Testing if MONGO_URL was set by calipso installer..."
if [ -n "$MONGO_URL" ]; then
    echo "MONGO_URL was set by calipso installer and the value is: "$MONGO_URL", going to use this value..."
else 
    echo "MONGO_URL was not set by calipso installer, trying to build it from environment variables..."
    export MONGO_URL="mongodb://$CALIPSO_MONGO_SERVICE_USER:$CALIPSO_MONGO_SERVICE_PWD@$CALIPSO_MONGO_SERVICE_HOST:$CALIPSO_MONGO_SERVICE_PORT/$CALIPSO_MONGO_SERVICE_AUTH_DB"
    echo MONGO_URL built as: "$MONGO_URL"
fi

# try to start local MongoDB if no external MONGO_URL was built
if [[ "${MONGO_URL}" == *"127.0.0.1"* ]]; then
  if hash mongod 2>/dev/null; then
    printf "\n[-] External MONGO_URL not found. Starting local MongoDB...\n\n"
    exec gosu mongodb mongod --storageEngine=wiredTiger > /dev/null 2>&1 &
  else
    echo "ERROR: Mongo not installed inside the container."
    echo "Rebuild with INSTALL_MONGO=true in your launchpad.conf or supply a MONGO_URL environment variable."
    exit 1
  fi
fi


# Set a delay to wait to start the Node process
if [[ $STARTUP_DELAY ]]; then
  echo "Delaying startup for $STARTUP_DELAY seconds..."
  sleep $STARTUP_DELAY
fi

if [ "${1:0:1}" = '-' ]; then
	set -- node "$@"
fi

# allow the container to be started with `--user`
if [ "$1" = "node" -a "$(id -u)" = "0" ]; then
	exec gosu node "$BASH_SOURCE" "$@"
fi

# Start app
echo "=> Starting app on port $PORT..."
exec "$@"
