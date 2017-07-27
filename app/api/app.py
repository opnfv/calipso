###############################################################################
# Copyright (c) 2017 Koren Lev (Cisco Systems), Yaron Yogev (Cisco Systems)   #
# and others                                                                  #
#                                                                             #
# All rights reserved. This program and the accompanying materials            #
# are made available under the terms of the Apache License, Version 2.0       #
# which accompanies this distribution, and is available at                    #
# http://www.apache.org/licenses/LICENSE-2.0                                  #
###############################################################################
import importlib

import falcon

from api.auth.token import Token
from api.backends.ldap_access import LDAPAccess
from api.exceptions.exceptions import CalipsoApiException
from api.middleware.authentication import AuthenticationMiddleware
from utils.inventory_mgr import InventoryMgr
from utils.logging.full_logger import FullLogger
from utils.mongo_access import MongoAccess


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
        "/auth/tokens": "auth.tokens.Tokens"
    }

    responders_path = "api.responders"

    def __init__(self, mongo_config="", ldap_config="",
                 log_level="", inventory="", token_lifetime=86400):
        MongoAccess.set_config_file(mongo_config)
        self.inv = InventoryMgr()
        self.inv.set_collections(inventory)
        self.log = FullLogger()
        self.log.set_loglevel(log_level)
        self.ldap_access = LDAPAccess(ldap_config)
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
            module = self.responders_path + "." + \
                     class_path[:class_path.rindex(".")]
            class_name = class_path.split('.')[-1]
            module = importlib.import_module(module)
            class_ = getattr(module, class_name)
            resource = class_()
            app.add_route(url, resource)
