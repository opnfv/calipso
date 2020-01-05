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
from api.test.api.responders_test.test_data import cliques
from api.test.api.test_base import TestBase


class TestCliques(TestBase):

    def test_get_cliques_list_without_env_name(self):
        self.validate_get_request(cliques.URL,
                                  params={},
                                  expected_code=base.BAD_REQUEST_CODE)

    def test_get_cliques_list_with_invalid_filter(self):
        self.validate_get_request(cliques.URL,
                                  params={
                                      "env_name": base.ENV_NAME,
                                      "invalid": "invalid"
                                  },
                                  expected_code=base.BAD_REQUEST_CODE)

    def test_get_cliques_list_with_non_int_page(self):
        self.validate_get_request(cliques.URL,
                                  params={
                                     "env_name": base.ENV_NAME,
                                     "page": base.NON_INT_PAGE
                                  },
                                  expected_code=base.BAD_REQUEST_CODE)

    @patch(base.RESPONDER_BASE_READ)
    def test_get_cliques_list_with_int_page(self, read):
        self.validate_get_request(cliques.URL,
                                  params={
                                     "env_name": base.ENV_NAME,
                                     "page": base.INT_PAGE
                                  },
                                  mocks={
                                     read: cliques.CLIQUES
                                  },
                                  expected_code=base.SUCCESSFUL_CODE,
                                  expected_response=cliques.CLIQUES_RESPONSE)

    def test_get_cliques_list_with_non_int_pagesize(self):
        self.validate_get_request(cliques.URL,
                                  params={
                                     "env_name": base.ENV_NAME,
                                     "page_size": base.NON_INT_PAGESIZE
                                  },
                                  expected_code=base.BAD_REQUEST_CODE)

    @patch(base.RESPONDER_BASE_READ)
    def test_get_cliques_list_with_int_pagesize(self, read):
        self.validate_get_request(cliques.URL,
                                  params={
                                     "env_name": base.ENV_NAME,
                                     "page_size": base.INT_PAGESIZE
                                  },
                                  mocks={
                                     read: cliques.CLIQUES
                                  },
                                  expected_code=base.SUCCESSFUL_CODE,
                                  expected_response=cliques.CLIQUES_RESPONSE)

    def test_get_clique_with_wrong_clique_id(self):
        self.validate_get_request(cliques.URL,
                                  params={
                                      'env_name': base.ENV_NAME,
                                      'id': cliques.WRONG_CLIQUE_ID
                                  },
                                  expected_code=base.BAD_REQUEST_CODE)

    @patch(base.RESPONDER_BASE_READ)
    def test_get_clique_with_clique_id(self, read):
        self.validate_get_request(cliques.URL,
                                  params={
                                     "env_name": base.ENV_NAME,
                                     "id": cliques.CORRECT_CLIQUE_ID
                                  },
                                  mocks={
                                     read: cliques.CLIQUES_WITH_SPECIFIC_ID
                                  },
                                  expected_code=base.SUCCESSFUL_CODE,
                                  expected_response=cliques.CLIQUES_WITH_SPECIFIC_ID[0]
                                  )

    def test_get_cliques_list_with_wrong_focal_point(self):
        self.validate_get_request(cliques.URL,
                                  params={
                                     "env_name": base.ENV_NAME,
                                     "focal_point": cliques.WRONG_FOCAL_POINT
                                  },
                                  expected_code=base.BAD_REQUEST_CODE)

    @patch(base.RESPONDER_BASE_READ)
    def test_get_cliques_list_with_focal_point(self, read):
        self.validate_get_request(cliques.URL,
                                  params={
                                     "env_name": base.ENV_NAME,
                                     "focal_point": cliques.CORRECT_FOCAL_POINT
                                  },
                                  mocks={
                                     read: cliques.CLIQUES_WITH_SPECIFIC_FOCAL_POINT
                                  },
                                  expected_code=base.SUCCESSFUL_CODE,
                                  expected_response=cliques.
                                     CLIQUES_WITH_SPECIFIC_FOCAL_POINT_RESPONSE
                                  )

    def test_get_cliques_list_with_wrong_focal_point_type(self):
        self.validate_get_request(cliques.URL,
                                  params={
                                     "env_name": base.ENV_NAME,
                                     "focal_point_type": cliques.WRONG_FOCAL_POINT_TYPE
                                  },
                                  expected_code=base.BAD_REQUEST_CODE)

    @patch(base.RESPONDER_BASE_READ)
    def test_get_cliques_list_with_focal_point_type(self, read):
        self.validate_get_request(cliques.URL,
                                  params={
                                     "env_name": base.ENV_NAME,
                                     "focal_point_type": cliques.CORRECT_FOCAL_POINT_TYPE
                                  },
                                  mocks={
                                     read: cliques.CLIQUES_WITH_SPECIFIC_FOCAL_POINT_TYPE
                                  },
                                  expected_code=base.SUCCESSFUL_CODE,
                                  expected_response=cliques.
                                     CLIQUES_WITH_SPECIFIC_FOCAL_POINT_TYPE_RESPONSE
                                  )

    def test_get_cliques_list_with_wrong_link_type(self):
        self.validate_get_request(cliques.URL,
                                  params={
                                      "env_name": base.ENV_NAME,
                                      "link_type": base.WRONG_LINK_TYPE
                                  },
                                  expected_code=base.BAD_REQUEST_CODE)

    @patch(base.RESPONDER_BASE_READ)
    def test_get_cliques_list_with_link_type(self, read):
        self.validate_get_request(cliques.URL,
                                  params={
                                      "env_name": base.ENV_NAME,
                                      "link_type": cliques.CORRECT_LINK_TYPE
                                  },
                                  mocks={
                                      read: cliques.CLIQUES_WITH_SPECIFIC_LINK_TYPE
                                  },
                                  expected_code=base.SUCCESSFUL_CODE,
                                  expected_response=cliques.
                                     CLIQUES_WITH_SPECIFIC_LINK_TYPE_RESPONSE
                                  )

    def test_get_cliques_list_with_wrong_link_id(self):
        self.validate_get_request(cliques.URL,
                                  {
                                     "env_name": base.ENV_NAME,
                                     "link_id": cliques.WRONG_LINK_ID
                                  },
                                  expected_code=base.BAD_REQUEST_CODE)

    @patch(base.RESPONDER_BASE_READ)
    def test_get_clique_ids_with_correct_link_id(self, read):
        self.validate_get_request(cliques.URL,
                                  params={
                                     "env_name": base.ENV_NAME,
                                     "link_id": cliques.CORRECT_LINK_ID
                                  },
                                  mocks={
                                     read: cliques.CLIQUES_WITH_SPECIFIC_LINK_ID
                                  },
                                  expected_code=base.SUCCESSFUL_CODE,
                                  expected_response=cliques.
                                     CLIQUES_WITH_SPECIFIC_LINK_ID_RESPONSE
                                  )

    @patch(base.RESPONDER_BASE_CHECK_ENVIRONMENT_NAME)
    @patch(base.RESPONDER_BASE_READ)
    def test_get_cliques_list_with_env_name_and_nonexistent_link_id(self, read, check_env_name):
        self.validate_get_request(cliques.URL,
                                  params={
                                     "env_name": base.ENV_NAME,
                                     "link_id": cliques.NONEXISTENT_LINK_ID
                                  },
                                  mocks={
                                     read: [],
                                     check_env_name: True
                                  },
                                  expected_code=base.NOT_FOUND_CODE)

    @patch(base.RESPONDER_BASE_CHECK_ENVIRONMENT_NAME)
    @patch(base.RESPONDER_BASE_READ)
    def test_get_cliques_list_with_unknown_env_name(self, read, check_env_name):
        self.validate_get_request(cliques.URL,
                                  params={
                                      "env_name": base.UNKNOWN_ENV
                                  },
                                  mocks={
                                      read: [],
                                      check_env_name: False
                                  },
                                  expected_code=base.BAD_REQUEST_CODE)

    @patch(base.RESPONDER_BASE_CHECK_ENVIRONMENT_NAME)
    @patch(base.RESPONDER_BASE_READ)
    def test_get_clique_with_env_name_and_nonexistent_clique_id(self, read, check_env_name):
        self.validate_get_request(cliques.URL,
                                  params={
                                      "env_name": base.ENV_NAME,
                                      "id": cliques.NONEXISTENT_CLIQUE_ID
                                  },
                                  mocks={
                                      read: [],
                                      check_env_name: True
                                  },
                                  expected_code=base.NOT_FOUND_CODE)

    @patch(base.RESPONDER_BASE_CHECK_ENVIRONMENT_NAME)
    @patch(base.RESPONDER_BASE_READ)
    def test_get_clique_with_unknown_env_name_and_clique_id(self, read, check_env_name):
        self.validate_get_request(cliques.URL,
                                  params={
                                      "env_name": base.UNKNOWN_ENV,
                                      "id": cliques.NONEXISTENT_CLIQUE_ID
                                  },
                                  mocks={
                                      read: [],
                                      check_env_name: False
                                  },
                                  expected_code=base.BAD_REQUEST_CODE)
