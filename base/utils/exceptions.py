###############################################################################
# Copyright (c) 2017-2019 Koren Lev (Cisco Systems),                          #
# Yaron Yogev (Cisco Systems), Ilia Abashin (Cisco Systems) and others        #
#                                                                             #
# All rights reserved. This program and the accompanying materials            #
# are made available under the terms of the Apache License, Version 2.0       #
# which accompanies this distribution, and is available at                    #
# http://www.apache.org/licenses/LICENSE-2.0                                  #
###############################################################################


class OpenStackAPIError(Exception):
    pass


class ScanArgumentsError(ValueError):
    pass


class ResourceGoneError(ValueError):
    pass


class HostAddressError(ValueError):
    def __init__(self, message=None):
        super().__init__(message if message else "Wrong host and/or port")


class CredentialsError(ValueError):
    def __init__(self, message=None):
        super().__init__(message if message else "Wrong credentials")


class SshKeyError(ValueError):
    def __init__(self, message=None):
        super().__init__(message if message else "Wrong SSH key")
