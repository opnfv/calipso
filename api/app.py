###############################################################################
# Copyright (c) 2017-2019 Koren Lev (Cisco Systems),                          #
# Yaron Yogev (Cisco Systems), Ilia Abashin (Cisco Systems) and others        #
#                                                                             #
# All rights reserved. This program and the accompanying materials            #
# are made available under the terms of the Apache License, Version 2.0       #
# which accompanies this distribution, and is available at                    #
# http://www.apache.org/licenses/LICENSE-2.0                                  #
###############################################################################
import importlib

import falcon

from api.auth.token import Token
from api.backends import auth_backend
from api.backends.credentials_backend import CredentialsBackend
from api.backends.ldap_backend import LDAPBackend
from api.exceptions.exceptions import CalipsoApiException
from api.middleware.authentication import AuthenticationMiddleware
from base.utils.inventory_mgr import InventoryMgr
from base.utils.logging.full_logger import FullLogger
from base.utils.mongo_access import MongoAccess


class App:

    ROUTE_DECLARATIONS = {
        "/inventory": "resource.inventory.Inventory",
        "/links": "resource.links.Links",
        "/messages": "resource.messages.Messages",
        "/cliques": "resource.cliques.Cliques",
        "/clique_types": "resource.clique_types.CliqueTypes",
        "/clique_constraints": "resource.clique_constraints.CliqueConstraints",
        "/scans": "resource.scans.Scans",
        "/scheduled_scans": "resource.scheduled_scans.ScheduledScans",
        "/constants": "resource.constants.Constants",
        "/monitoring_config_templates":
            "resource.monitoring_config_templates.MonitoringConfigTemplates",
        "/aggregates": "resource.aggregates.Aggregates",
        "/environment_configs":
            "resource.environment_configs.EnvironmentConfigs",
        "/connection_tests": "resource.connection_tests.ConnectionTests",
        "/auth/tokens": "auth.tokens.Tokens"
    }

    responders_path = "api.responders"

    def __init__(self, mongo_config="", ldap_enabled=True, ldap_config="", auth_config="",
                 log_level="", inventory="", token_lifetime=86400):
        MongoAccess.set_config_file(mongo_config)
        self.inv = InventoryMgr()
        self.inv.set_collections(inventory)
        self.log = FullLogger()
        self.log.set_loglevel(log_level)
        self.setup_auth_backend(ldap_enabled=ldap_enabled, ldap_config=ldap_config, auth_config=auth_config)
        Token.set_token_lifetime(token_lifetime)
        self.middleware = AuthenticationMiddleware()
        self.app = falcon.API(middleware=[self.middleware])
        self.app.add_error_handler(CalipsoApiException)
        self.set_routes(self.app)

    def get_app(self):
        return self.app

    def set_routes(self, app):
        for url in self.ROUTE_DECLARATIONS.keys():
            class_path = self.ROUTE_DECLARATIONS.get(url)
            module = self.responders_path + "." + class_path[:class_path.rindex(".")]
            class_name = class_path.split('.')[-1]
            module = importlib.import_module(module)
            class_ = getattr(module, class_name)
            resource = class_()
            app.add_route(url, resource)

    def setup_auth_backend(self, ldap_enabled, ldap_config, auth_config=""):
        if ldap_enabled:
            try:
                auth_backend.ApiAuth = LDAPBackend(ldap_config)
                return
            except ValueError as e:
                self.log.error("Failed to setup LDAP access. Exception: {}".format(e))
                raise ValueError("LDAP authentication required.")
        elif auth_config:
            try:
                auth_backend.ApiAuth = CredentialsBackend(auth_config)
                return
            except ValueError as e:
                self.log.error("Failed to setup credentials access. Exception: {}".format(e))
                raise ValueError("Credentials authentication required.")
        else:
            self.log.info("Skipping LDAP authentication")

        # TODO: try mongo auth
        self.log.warning("Falling back to no authentication")
