###############################################################################
# Copyright (c) 2017-2019 Koren Lev (Cisco Systems),                          #
# Yaron Yogev (Cisco Systems), Ilia Abashin (Cisco Systems) and others        #
#                                                                             #
# All rights reserved. This program and the accompanying materials            #
# are made available under the terms of the Apache License, Version 2.0       #
# which accompanies this distribution, and is available at                    #
# http://www.apache.org/licenses/LICENSE-2.0                                  #
###############################################################################
import re


class SpecialCharConverter:

    translated_re = re.compile(r'---[.][.][0-9]+[.][.]---')

    def encode_special_characters(self, s):
        SPECIAL_CHARS = [':', '/']
        for c in SPECIAL_CHARS:
            if c in s:
                s = s.replace(c, '---..' + str(ord(c)) + '..---')
        return s

    def decode_special_characters(self, s):
        replaced = []
        for m in re.finditer(self.translated_re, s):
            match = m.group(0)
            char_code = match[5:len(match)-5]
            if char_code not in replaced:
                replaced.append(char_code)
                s = s.replace(match, chr(int(char_code)))
        return s
