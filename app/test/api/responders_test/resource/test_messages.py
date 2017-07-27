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
from test.api.responders_test.test_data import messages
from unittest.mock import patch


class TestMessage(TestBase):

    def test_get_messages_list_without_env_name(self):
        self.validate_get_request(messages.URL,
                                  params={},
                                  expected_code=base.BAD_REQUEST_CODE)

    def test_get_messages_list_with_invalid_filter(self):
        self.validate_get_request(messages.URL,
                                  params={
                                      'invalid': 'invalid'
                                  },
                                  expected_code=base.BAD_REQUEST_CODE)

    def test_get_messages_list_with_wrong_format_start_time(self):
        self.validate_get_request(messages.URL,
                                  params={
                                     'env_name': base.ENV_NAME,
                                     'start_time': messages.WRONG_FORMAT_TIME
                                  },
                                  expected_code=base.BAD_REQUEST_CODE)

    @patch(base.RESPONDER_BASE_READ)
    def test_get_messages_list_with_correct_format_start_time(self, read):
        self.validate_get_request(messages.URL,
                                  params={
                                     'env_name': base.ENV_NAME,
                                     'start_time': messages.CORRECT_FORMAT_TIME
                                  },
                                  mocks={
                                     read: messages.MESSAGES_WITH_SPECIFIC_TIME
                                  },
                                  expected_code=base.SUCCESSFUL_CODE,
                                  expected_response=
                                     messages.MESSAGES_WITH_SPECIFIC_TIME_RESPONSE
                                  )

    def test_get_messages_list_with_wrong_format_end_time(self):
        self.validate_get_request(messages.URL,
                                  params={
                                     'env_name': base.ENV_NAME,
                                     'end_time': messages.WRONG_FORMAT_TIME
                                  },
                                  expected_code=base.BAD_REQUEST_CODE)

    @patch(base.RESPONDER_BASE_READ)
    def test_get_messages_list_with_correct_format_end_time(self, read):
        self.validate_get_request(messages.URL,
                                  params={
                                     'env_name': base.ENV_NAME,
                                     'end_time': messages.CORRECT_FORMAT_TIME
                                  },
                                  mocks={
                                     read: messages.MESSAGES_WITH_SPECIFIC_TIME
                                  },
                                  expected_code=base.SUCCESSFUL_CODE,
                                  expected_response=
                                     messages.MESSAGES_WITH_SPECIFIC_TIME_RESPONSE
                                  )

    def test_get_messages_list_with_wrong_level(self):
        self.validate_get_request(messages.URL,
                                  params={
                                     'env_name': base.ENV_NAME,
                                     'level': messages.WRONG_SEVERITY
                                  },
                                  expected_code=base.BAD_REQUEST_CODE)

    @patch(base.RESPONDER_BASE_READ)
    def test_get_messages_list_with_level(self, read):
        self.validate_get_request(messages.URL,
                                  params={
                                     'env_name': base.ENV_NAME,
                                     'level': messages.CORRECT_SEVERITY
                                  },
                                  mocks={
                                     read: messages.MESSAGES_WITH_SPECIFIC_SEVERITY
                                  },
                                  expected_code=base.SUCCESSFUL_CODE,
                                  expected_response=messages.
                                     MESSAGES_WITH_SPECIFIC_SEVERITY_RESPONSE
                                  )

    def test_get_messages_list_with_wrong_related_object_type(self):
        self.validate_get_request(messages.URL,
                                  params={
                                     'env_name': base.ENV_NAME,
                                     'related_object_type':
                                         messages.WRONG_RELATED_OBJECT_TYPE
                                  },
                                  expected_code=base.BAD_REQUEST_CODE)

    @patch(base.RESPONDER_BASE_READ)
    def test_get_messages_list_with_correct_related_object_type(self, read):
        self.validate_get_request(messages.URL,
                                  params={
                                     'env_name': base.ENV_NAME,
                                     'related_object_type':
                                         messages.CORRECT_RELATED_OBJECT_TYPE
                                  },
                                  mocks={
                                     read: messages.
                                        MESSAGES_WITH_SPECIFIC_RELATED_OBJECT_TYPE
                                  },
                                  expected_code=base.SUCCESSFUL_CODE,
                                  expected_response=messages.
                                        MESSAGES_WITH_SPECIFIC_RELATED_OBJECT_TYPE_RESPONSE
                                  )

    def test_get_messages_list_with_non_int_page(self):
        self.validate_get_request(messages.URL,
                                  params={
                                     'env_name': base.ENV_NAME,
                                     'page': base.NON_INT_PAGE
                                  },
                                  expected_code=base.BAD_REQUEST_CODE)

    @patch(base.RESPONDER_BASE_READ)
    def test_get_messages_list_with_int_page(self, read):
        self.validate_get_request(messages.URL,
                                  params={
                                     'env_name': base.ENV_NAME,
                                     'page': base.INT_PAGE
                                  },
                                  mocks={
                                     read: messages.MESSAGES
                                  },
                                  expected_code=base.SUCCESSFUL_CODE,
                                  expected_response=messages.MESSAGES_RESPONSE)

    def test_get_messages_list_with_non_int_page_size(self):
        self.validate_get_request(messages.URL,
                                  params={
                                     'env_name': base.ENV_NAME,
                                     'page_size': base.NON_INT_PAGESIZE
                                  },
                                  expected_code=base.BAD_REQUEST_CODE)

    @patch(base.RESPONDER_BASE_READ)
    def test_get_messages_list_with_int_pagesize(self, read):
        self.validate_get_request(messages.URL,
                                  params={
                                     'env_name': base.ENV_NAME,
                                     'page_size': base.INT_PAGESIZE
                                  },
                                  mocks={
                                     read: messages.MESSAGES
                                  },
                                  expected_code=base.SUCCESSFUL_CODE,
                                  expected_response=messages.MESSAGES_RESPONSE)

    @patch(base.RESPONDER_BASE_CHECK_ENVIRONMENT_NAME)
    @patch(base.RESPONDER_BASE_READ)
    def test_get_messages_list_with_env_name_and_nonexistent_related_object(self, read, check_env_name):
        self.validate_get_request(messages.URL,
                                  params={
                                      'env_name': base.ENV_NAME,
                                      'related_object':  messages.NONEXISTENT_RELATED_OBJECT
                                  },
                                  mocks={
                                      read: [],
                                      check_env_name: True
                                  },
                                  expected_code=base.NOT_FOUND_CODE)

    @patch(base.RESPONDER_BASE_CHECK_ENVIRONMENT_NAME)
    @patch(base.RESPONDER_BASE_READ)
    def test_get_messages_list_with_unknown_env_name(self, read, check_env_name):
        self.validate_get_request(messages.URL,
                                  params={
                                      'env_name': base.UNKNOWN_ENV,
                                      'related_object': messages.RELATED_OBJECT
                                  },
                                  mocks={
                                      read: [],
                                      check_env_name: False
                                  },
                                  expected_code=base.BAD_REQUEST_CODE)

    @patch(base.RESPONDER_BASE_CHECK_ENVIRONMENT_NAME)
    @patch(base.RESPONDER_BASE_READ)
    def test_get_message_with_env_name_and_nonexistent_id(self, read, check_env_name):
        self.validate_get_request(messages.URL,
                                  params={
                                      'env_name': base.ENV_NAME,
                                      'id': messages.NONEXISTENT_MESSAGE_ID
                                  },
                                  mocks={
                                      read: [],
                                      check_env_name: True
                                  },
                                  expected_code=base.NOT_FOUND_CODE)

    @patch(base.RESPONDER_BASE_CHECK_ENVIRONMENT_NAME)
    @patch(base.RESPONDER_BASE_READ)
    def test_get_message_with_unknown_env_name_and_id(self, read, check_env_name):
        self.validate_get_request(messages.URL,
                                  params={
                                      'env_name': base.UNKNOWN_ENV,
                                      'id': messages.MESSAGE_ID
                                  },
                                  mocks={
                                      read: [],
                                      check_env_name: False
                                  },
                                  expected_code=base.BAD_REQUEST_CODE)

    @patch(base.RESPONDER_BASE_CHECK_ENVIRONMENT_NAME)
    @patch(base.RESPONDER_BASE_READ)
    def test_get_message_with_env_name_and_id(self, read, check_env_name):
        self.validate_get_request(messages.URL,
                                  params={
                                      'env_name': base.ENV_NAME,
                                      'id': messages.MESSAGE_ID
                                  },
                                  mocks={
                                      read: messages.MESSAGES_WITH_SPECIFIC_ID,
                                      check_env_name: False
                                  },
                                  expected_code=base.SUCCESSFUL_CODE,
                                  expected_response=messages.MESSAGES_WITH_SPECIFIC_ID[0])
