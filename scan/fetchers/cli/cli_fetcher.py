###############################################################################
# Copyright (c) 2017-2019 Koren Lev (Cisco Systems),                          #
# Yaron Yogev (Cisco Systems), Ilia Abashin (Cisco Systems) and others        #
#                                                                             #
# All rights reserved. This program and the accompanying materials            #
# are made available under the terms of the Apache License, Version 2.0       #
# which accompanies this distribution, and is available at                    #
# http://www.apache.org/licenses/LICENSE-2.0                                  #
###############################################################################
from base.fetcher import Fetcher
from base.utils.cli_access import CliAccess
from base.utils.exceptions import CredentialsError, HostAddressError
from base.utils.ssh_connection import SshError


class CliFetcher(Fetcher, CliAccess):

    def run_fetch_lines(self, cmd, ssh_to_host="", enable_cache=True,
                        use_sudo=True) -> list:
        try:
            lines = super().run_fetch_lines(cmd,
                                            ssh_to_host=ssh_to_host,
                                            enable_cache=enable_cache,
                                            use_sudo=use_sudo)
        except (SshError, CredentialsError, HostAddressError) as e:
            msg = 'error running command {} (host:{}): {}'\
                .format(cmd, ssh_to_host, str(e))
            self.log.error(msg)
            raise SshError(msg)
        return lines

    def run(self, cmd, ssh_to_host="", enable_cache=True, on_gateway=False,
            ssh=None, use_sudo=True) -> str:
        try:
            output = super().run(cmd, ssh_to_host,
                                 enable_cache=enable_cache,
                                 on_gateway=on_gateway,
                                 ssh=ssh,
                                 use_sudo=use_sudo)
        except (SshError, CredentialsError, HostAddressError) as e:
            msg = 'error running command {} (host:{}): {}' \
                .format(cmd, ssh_to_host, str(e))
            self.log.error(msg)
            raise SshError(msg)
        return output
