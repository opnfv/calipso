###############################################################################
# Copyright (c) 2017-2019 Koren Lev (Cisco Systems),                          #
# Yaron Yogev (Cisco Systems), Ilia Abashin (Cisco Systems) and others        #
#                                                                             #
# All rights reserved. This program and the accompanying materials            #
# are made available under the terms of the Apache License, Version 2.0       #
# which accompanies this distribution, and is available at                    #
# http://www.apache.org/licenses/LICENSE-2.0                                  #
###############################################################################
from api.ldap_api.responder import Responder
from api.ldap_api.server import user_access


class UserIdTypeHandler(Responder):

    def __init__(self):
        super().__init__()
        self.user_id = None

    def validate_user_id(self) -> bool:
        self.get_request_param('user_id')
        if not self.user_id:
            self.error = 'user_id is missing'
            return False
        # validate that this is a real user
        user_data = user_access.get_user_data(self.user_id)
        if not user_data:
            self.error = 'User does not exist'
            return False
        # TBD: add validation that current user is either this user or admin
        return True
