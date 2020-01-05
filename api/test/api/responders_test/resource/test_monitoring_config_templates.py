###############################################################################
# Copyright (c) 2017-2019 Koren Lev (Cisco Systems),                          #
# Yaron Yogev (Cisco Systems), Ilia Abashin (Cisco Systems) and others        #
#                                                                             #
# All rights reserved. This program and the accompanying materials            #
# are made available under the terms of the Apache License, Version 2.0       #
# which accompanies this distribution, and is available at                    #
# http://www.apache.org/licenses/LICENSE-2.0                                  #
###############################################################################
from unittest.mock import patch

from api.test.api.responders_test.test_data import base
from api.test.api.responders_test.test_data import monitoring_config_templates
from api.test.api.test_base import TestBase


class TestMonitoringConfigTemplates(TestBase):

    def test_get_templates_list_with_unknown_filter(self):
        self.validate_get_request(monitoring_config_templates.URL,
                                  params={
                                      "unknown": "unknown"
                                  },
                                  expected_code=base.BAD_REQUEST_CODE)

    def test_get_templates_list_with_non_int_order(self):
        self.validate_get_request(monitoring_config_templates.URL,
                                  params={
                                      "order": monitoring_config_templates.NON_INT_ORDER
                                  },
                                  expected_code=base.BAD_REQUEST_CODE)

    @patch(base.RESPONDER_BASE_READ)
    def test_get_templates_list_with_order(self, read):
        self.validate_get_request(monitoring_config_templates.URL,
                                  params={
                                      "order": monitoring_config_templates.INT_ORDER
                                  },
                                  mocks={
                                      read: monitoring_config_templates.
                                         TEMPLATES_WITH_SPECIFIC_ORDER
                                  },
                                  expected_code=base.SUCCESSFUL_CODE,
                                  expected_response=monitoring_config_templates.
                                      TEMPLATES_WITH_SPECIFIC_ORDER_RESPONSE
                                  )

    def test_get_templates_list_with_wrong_side(self):
        self.validate_get_request(monitoring_config_templates.URL,
                                  params={
                                      "side": monitoring_config_templates.WRONG_SIDE
                                  },
                                  expected_code=base.BAD_REQUEST_CODE)

    @patch(base.RESPONDER_BASE_READ)
    def test_get_templates_list_with_side(self, read):
        self.validate_get_request(monitoring_config_templates.URL,
                                  params={
                                      "side": monitoring_config_templates.CORRECT_SIDE
                                  },
                                  mocks={
                                      read: monitoring_config_templates.
                                         TEMPLATES_WITH_SPECIFIC_SIDE
                                  },
                                  expected_code=base.SUCCESSFUL_CODE,
                                  expected_response=monitoring_config_templates.
                                      TEMPLATES_WITH_SPECIFIC_SIDE_RESPONSE
                                  )

    @patch(base.RESPONDER_BASE_READ)
    def test_get_templates_list_with_type(self, read):
        self.validate_get_request(monitoring_config_templates.URL,
                                  params={
                                      "type": monitoring_config_templates.TYPE
                                  },
                                  mocks={
                                      read: monitoring_config_templates.
                                         TEMPLATES_WITH_SPECIFIC_TYPE
                                  },
                                  expected_code=base.SUCCESSFUL_CODE,
                                  expected_response=monitoring_config_templates.
                                      TEMPLATES_WITH_SPECIFIC_TYPE_RESPONSE
                                  )

    def test_get_templates_list_with_non_int_page(self):
        self.validate_get_request(monitoring_config_templates.URL,
                                  params={
                                      "page": base.NON_INT_PAGE
                                  },
                                  expected_code=base.BAD_REQUEST_CODE)

    @patch(base.RESPONDER_BASE_READ)
    def test_get_templates_list_with_int_page(self, read):
        self.validate_get_request(monitoring_config_templates.URL,
                                  params={
                                      "page": base.INT_PAGE
                                  },
                                  mocks={
                                      read: monitoring_config_templates.TEMPLATES
                                  },
                                  expected_code=base.SUCCESSFUL_CODE,
                                  expected_response=monitoring_config_templates.
                                      TEMPLATES_RESPONSE
                                  )

    def test_get_templates_list_with_non_int_pagesize(self):
        self.validate_get_request(monitoring_config_templates.URL,
                                  params={
                                      "page_size": base.NON_INT_PAGESIZE
                                  },
                                  expected_code=base.BAD_REQUEST_CODE)

    @patch(base.RESPONDER_BASE_READ)
    def test_get_templates_list_with_int_pagesize(self, read):
        self.validate_get_request(monitoring_config_templates.URL,
                                  params={
                                      "page_size": base.INT_PAGESIZE
                                  },
                                  mocks={
                                      read: monitoring_config_templates.TEMPLATES
                                  },
                                  expected_code=base.SUCCESSFUL_CODE,
                                  expected_response=monitoring_config_templates.
                                      TEMPLATES_RESPONSE
                                  )

    def test_get_template_with_wrong_id(self):
        self.validate_get_request(monitoring_config_templates.URL,
                                  params={
                                      "id": monitoring_config_templates.WRONG_ID
                                  },
                                  expected_code=base.BAD_REQUEST_CODE)

    @patch(base.RESPONDER_BASE_READ)
    def test_get_template_with_unknown_id(self, read):
        self.validate_get_request(monitoring_config_templates.URL,
                                  params={
                                      "id": monitoring_config_templates.UNKNOWN_ID
                                  },
                                  mocks={
                                      read: []
                                  },
                                  expected_code=base.NOT_FOUND_CODE)

    @patch(base.RESPONDER_BASE_READ)
    def test_get_template_with_id(self, read):
        self.validate_get_request(monitoring_config_templates.URL,
                                  params={
                                      "id": monitoring_config_templates.CORRECT_ID
                                  },
                                  mocks={
                                      read: monitoring_config_templates.TEMPLATES_WITH_SPECIFIC_ID
                                  },
                                  expected_code=base.SUCCESSFUL_CODE,
                                  expected_response=monitoring_config_templates.
                                      TEMPLATES_WITH_SPECIFIC_ID[0]
                                  )
