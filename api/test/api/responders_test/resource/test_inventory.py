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
from api.test.api.responders_test.test_data import inventory
from api.test.api.test_base import TestBase


class TestInventory(TestBase):

    def test_get_objects_list_without_env_name(self):
        self.validate_get_request(inventory.URL,
                                  expected_code=base.BAD_REQUEST_CODE)

    def test_get_objects_list_with_invalid_filter(self):
        self.validate_get_request(inventory.URL,
                                  params={
                                      "invalid": "invalid"
                                  },
                                  expected_code=base.BAD_REQUEST_CODE)

    def test_get_objects_list_with_non_boolean_subtree(self):
        self.validate_get_request(inventory.URL,
                                  params={
                                     'env_name': base.ENV_NAME,
                                     'sub_tree': base.NON_BOOL
                                  },
                                  expected_code=base.BAD_REQUEST_CODE)

    @patch(base.RESPONDER_BASE_READ)
    def test_get_objects_list_with_boolean_subtree(self, read):
        self.validate_get_request(inventory.URL,
                                  params={
                                     'env_name': base.ENV_NAME,
                                     'sub_tree': base.BOOL
                                  },
                                  mocks={
                                      read: inventory.OBJECTS_LIST
                                  },
                                  expected_code=base.SUCCESSFUL_CODE,
                                  expected_response=inventory.OBJECT_IDS_RESPONSE
                                  )

    def test_get_objects_list_with_non_int_page(self):
        self.validate_get_request(inventory.URL,
                                  params={
                                     'env_name': base.ENV_NAME,
                                     'page': base.NON_INT_PAGE
                                  },
                                  expected_code=base.BAD_REQUEST_CODE)

    @patch(base.RESPONDER_BASE_READ)
    def test_get_objects_list_with_int_page(self, read):
        self.validate_get_request(inventory.URL,
                                  params={
                                     'env_name': base.ENV_NAME,
                                     'page': base.INT_PAGE
                                  },
                                  mocks={
                                     read: inventory.OBJECTS_LIST
                                  },
                                  expected_code=base.SUCCESSFUL_CODE,
                                  expected_response=inventory.OBJECT_IDS_RESPONSE
                                  )

    def test_get_objects_list_with_non_int_pagesize(self):
        self.validate_get_request(inventory.URL,
                                  params={
                                     'env_name': base.ENV_NAME,
                                     'page_size': base.NON_INT_PAGESIZE
                                  },
                                  expected_code=base.BAD_REQUEST_CODE)

    @patch(base.RESPONDER_BASE_READ)
    def test_get_objects_list_with_int_pagesize(self, read):
        self.validate_get_request(inventory.URL,
                                  params={
                                     'env_name': base.ENV_NAME,
                                     'page_size': base.INT_PAGESIZE
                                  },
                                  mocks={
                                     read: inventory.OBJECTS_LIST
                                  },
                                  expected_code=base.SUCCESSFUL_CODE,
                                  expected_response=inventory.OBJECT_IDS_RESPONSE
                                  )

    @patch(base.RESPONDER_BASE_READ)
    @patch(base.RESPONDER_BASE_CHECK_ENVIRONMENT_NAME)
    def test_get_nonexistent_objects_list_with_env_name(self, check_env_name, read):
        self.validate_get_request(inventory.URL,
                                  params={
                                     'env_name': base.ENV_NAME,
                                  },
                                  mocks={
                                     read: [],
                                     check_env_name: True
                                  },
                                  expected_code=base.NOT_FOUND_CODE,
                                  )

    @patch(base.RESPONDER_BASE_READ)
    @patch(base.RESPONDER_BASE_CHECK_ENVIRONMENT_NAME)
    def test_get_objects_list_with_unkown_env_name(self, check_env_name, read):
        self.validate_get_request(inventory.URL,
                                  params={
                                      'env_name': base.ENV_NAME,
                                  },
                                  mocks={
                                      read: [],
                                      check_env_name: False
                                  },
                                  expected_code=base.BAD_REQUEST_CODE)

    @patch(base.RESPONDER_BASE_READ)
    def test_get_object_with_env_name_and_id(self, read):
        self.validate_get_request(inventory.URL,
                                  params={
                                     'env_name': base.ENV_NAME,
                                     'id': inventory.ID
                                  },
                                  mocks={
                                     read: inventory.OBJECTS
                                  },
                                  expected_code=base.SUCCESSFUL_CODE,
                                  expected_response=inventory.OBJECTS[0]
                                  )

    @patch(base.RESPONDER_BASE_READ)
    @patch(base.RESPONDER_BASE_CHECK_ENVIRONMENT_NAME)
    def test_get_nonexistent_object_with_env_name_and_id(self, check_env_name, read):
        self.validate_get_request(inventory.URL,
                                  params={
                                     'env_name': base.ENV_NAME,
                                     'id': inventory.NONEXISTENT_ID
                                  },
                                  mocks={
                                     read: [],
                                     check_env_name: True
                                  },
                                  expected_code=base.NOT_FOUND_CODE)

    @patch(base.RESPONDER_BASE_READ)
    @patch(base.RESPONDER_BASE_CHECK_ENVIRONMENT_NAME)
    def test_get_object_with_unkown_env_name_and_id(self, check_env_name, read):
        self.validate_get_request(inventory.URL,
                                  params={
                                      'env_name': base.UNKNOWN_ENV,
                                      'id': inventory.ID
                                  },
                                  mocks={
                                      read: [],
                                      check_env_name: False
                                  },
                                  expected_code=base.BAD_REQUEST_CODE)
