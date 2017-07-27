###############################################################################
# Copyright (c) 2017 Koren Lev (Cisco Systems), Yaron Yogev (Cisco Systems)   #
# and others                                                                  #
#                                                                             #
# All rights reserved. This program and the accompanying materials            #
# are made available under the terms of the Apache License, Version 2.0       #
# which accompanies this distribution, and is available at                    #
# http://www.apache.org/licenses/LICENSE-2.0                                  #
###############################################################################
class MockCursor:

    def __init__(self, result):
        self.result = result
        self.current = 0

    def __next__(self):
        if self.current < len(self.result):
            next = self.result[self.current]
            self.current += 1
            return next
        else:
            raise StopIteration

    def __iter__(self):
        return self
