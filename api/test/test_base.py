###############################################################################
# Copyright (c) 2017-2019 Koren Lev (Cisco Systems),                          #
# Yaron Yogev (Cisco Systems), Ilia Abashin (Cisco Systems) and others        #
#                                                                             #
# All rights reserved. This program and the accompanying materials            #
# are made available under the terms of the Apache License, Version 2.0       #
# which accompanies this distribution, and is available at                    #
# http://www.apache.org/licenses/LICENSE-2.0                                  #
###############################################################################
import unittest


class TestBase(unittest.TestCase):
    @staticmethod
    def get_dict_subset(expected, actual):
        def _get_subset(_expected, _actual, key):
            expected_value = _expected[key]
            actual_value = _actual.get(key)

            if not isinstance(actual_value, expected_value.__class__):
                return None
            if isinstance(expected_value, dict):
                return {_key: _get_subset(expected_value, actual_value, _key)
                        for _key in actual_value.keys()
                        if _key in expected_value}
            if isinstance(expected_value, list):
                # Deep list inspection is too complicated for this purpose
                return [elem for elem in actual_value if elem in expected_value]
            return actual_value

        return {key: _get_subset(expected, actual, key)
                for key in actual.keys()
                if key in expected}

    def assertDictContains(self, expected, actual):
        self.assertDictEqual(expected, self.get_dict_subset(expected, actual))

    def assertListsContain(self, expected, actual, order_field='id'):
        if not expected:
            raise ValueError("Expected list is empty")

        actual = [self.get_dict_subset(expected[0], elem)
                  for elem in
                  actual]

        if order_field:
            expected = sorted(expected, key=lambda elem: elem[order_field])
            actual = sorted(actual, key=lambda elem: elem[order_field])

        self.assertListEqual(expected, actual)
