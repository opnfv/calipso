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

from base.utils.cli_dist_translator import CliDistTranslator


class TestCliDistTranslator(unittest.TestCase):

    MERCURY_DIST = 'Mercury'
    MERCURY_VER = '10239'

    SOURCE_TEXT = 'some text'
    IP_LINK_TEXT = 'ip link show'
    IP_LINK_TRANSLATED_MERCURY = \
        'docker exec --user root ovs_vswitch_10239 ip link show'

    def test_unknown_dist(self):
        translator = CliDistTranslator('UNKNOWN')
        result = translator.translate(self.SOURCE_TEXT)
        self.assertEqual(result, self.SOURCE_TEXT,
                         'unknown dist should not cause translation')

    def test_mercury_dist(self):
        translator = CliDistTranslator(self.MERCURY_DIST, self.MERCURY_VER)
        result = translator.translate(self.SOURCE_TEXT)
        self.assertEqual(result, self.SOURCE_TEXT,
                         'known dist should not translate unrelated texts')
        result = translator.translate(self.IP_LINK_TEXT)
        self.assertEqual(result, self.IP_LINK_TRANSLATED_MERCURY,
                         'incorrect translation of command for mercury dist')
