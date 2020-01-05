###############################################################################
# Copyright (c) 2017-2019 Koren Lev (Cisco Systems),                          #
# Yaron Yogev (Cisco Systems), Ilia Abashin (Cisco Systems) and others        #
#                                                                             #
# All rights reserved. This program and the accompanying materials            #
# are made available under the terms of the Apache License, Version 2.0       #
# which accompanies this distribution, and is available at                    #
# http://www.apache.org/licenses/LICENSE-2.0                                  #
###############################################################################
import abc


class AuthBackend(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def authenticate_user(self, username, password):
        pass


class AutoAuthBackend(AuthBackend):
    def authenticate_user(self, username, password):
        return True


ApiAuth = AutoAuthBackend()  # type: AuthBackend
