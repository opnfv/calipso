###############################################################################
# Copyright (c) 2017 Koren Lev (Cisco Systems), Yaron Yogev (Cisco Systems)   #
# and others                                                                  #
#                                                                             #
# All rights reserved. This program and the accompanying materials            #
# are made available under the terms of the Apache License, Version 2.0       #
# which accompanies this distribution, and is available at                    #
# http://www.apache.org/licenses/LICENSE-2.0                                  #
###############################################################################
from test.api.test_base import TestBase
from test.api.responders_test.test_data import base
from test.api.responders_test.test_data import clique_constraints
from unittest.mock import patch


class TestCliqueConstraints(TestBase):

    def test_get_clique_constraints_list_with_invalid_filter(self):
        self.validate_get_request(clique_constraints.URL,
                                  params={
                                      "invalid": "invalid"
                                  },
                                  expected_code=base.BAD_REQUEST_CODE)

    def test_get_clique_constraints_list_with_non_int_page(self):
        self.validate_get_request(clique_constraints.URL,
                                  params={
                                     "page": base.NON_INT_PAGE
                                  },
                                  expected_code=base.BAD_REQUEST_CODE)

    @patch(base.RESPONDER_BASE_READ)
    def test_get_clique_constraints_list_with_int_page(self, read):
        self.validate_get_request(clique_constraints.URL,
                                  params={
                                     "page": base.INT_PAGE
                                  },
                                  mocks={
                                     read: clique_constraints.CLIQUE_CONSTRAINTS
                                  },
                                  expected_code=base.SUCCESSFUL_CODE,
                                  expected_response=clique_constraints.
                                     CLIQUE_CONSTRAINTS_RESPONSE
                                  )

    def test_get_clique_constraints_list_with_non_int_pagesize(self):
        self.validate_get_request(clique_constraints.URL,
                                  params={
                                     "page_size": base.NON_INT_PAGESIZE
                                  },
                                  expected_code=base.BAD_REQUEST_CODE)

    @patch(base.RESPONDER_BASE_READ)
    def test_get_clique_constraints_list_with_int_pagesize(self, read):
        self.validate_get_request(clique_constraints.URL,
                                  params={
                                     "page_size": base.INT_PAGESIZE
                                  },
                                  mocks={
                                     read: clique_constraints.CLIQUE_CONSTRAINTS
                                  },
                                  expected_code=base.SUCCESSFUL_CODE,
                                  expected_response=clique_constraints.
                                     CLIQUE_CONSTRAINTS_RESPONSE
                                  )

    def test_get_clique_constraints_with_wrong_id(self):
        self.validate_get_request(clique_constraints.URL,
                                  params={
                                      'id': clique_constraints.WRONG_ID
                                  },
                                  expected_code=base.BAD_REQUEST_CODE)

    @patch(base.RESPONDER_BASE_READ)
    def test_get_clique_constraints_with_nonexistent_id(self, read):
        self.validate_get_request(clique_constraints.URL,
                                  params={
                                      "id": clique_constraints.NONEXISTENT_ID
                                  },
                                  mocks={
                                      read: []
                                  },
                                  expected_code=base.NOT_FOUND_CODE
                                  )

    @patch(base.RESPONDER_BASE_READ)
    def test_get_clique_constraints_with_id(self, read):
        self.validate_get_request(clique_constraints.URL,
                                  params={
                                     "id": clique_constraints.CORRECT_ID
                                  },
                                  mocks={
                                     read: clique_constraints.
                                           CLIQUE_CONSTRAINTS_WITH_SPECIFIC_ID
                                  },
                                  expected_code=base.SUCCESSFUL_CODE,
                                  expected_response=clique_constraints.
                                     CLIQUE_CONSTRAINTS_WITH_SPECIFIC_ID[0]
                                  )

    def test_get_clique_constraints_list_with_wrong_focal_point_type(self):
        self.validate_get_request(clique_constraints.URL,
                                  params={
                                      "focal_point_type":
                                          clique_constraints.WRONG_FOCAL_POINT_TYPE
                                  },
                                  expected_code=base.BAD_REQUEST_CODE)

    @patch(base.RESPONDER_BASE_READ)
    def test_get_clique_constraints_list_with_focal_point_type(self, read):
        self.validate_get_request(clique_constraints.URL,
                                  params={
                                      "focal_point_type":
                                          clique_constraints.CORRECT_FOCAL_POINT_TYPE
                                  },
                                  mocks={
                                      read: clique_constraints.
                                        CLIQUE_CONSTRAINTS_WITH_SPECIFIC_FOCAL_POINT_TYPE
                                  },
                                  expected_code=base.SUCCESSFUL_CODE,
                                  expected_response=clique_constraints.
                                      CLIQUE_CONSTRAINTS_WITH_SPECIFIC_FOCAL_POINT_TYPE_RESPONSE
                                  )

    @patch(base.RESPONDER_BASE_READ)
    def test_get_clique_constraints_list_with_constraints(self, read):
        self.validate_get_request(clique_constraints.URL,
                                  params={
                                      "constraint": clique_constraints.CONSTRAINT
                                  },
                                  mocks={
                                      read: clique_constraints.
                                        CLIQUE_CONSTRAINTS_WITH_SPECIFIC_CONSTRAINT
                                  },
                                  expected_code=base.SUCCESSFUL_CODE,
                                  expected_response=clique_constraints.
                                      CLIQUE_CONSTRAINTS_WITH_SPECIFIC_CONSTRAINT_RESPONSE
                                  )
