###############################################################################
# Copyright (c) 2017-2019 Koren Lev (Cisco Systems),                          #
# Yaron Yogev (Cisco Systems), Ilia Abashin (Cisco Systems) and others        #
#                                                                             #
# All rights reserved. This program and the accompanying materials            #
# are made available under the terms of the Apache License, Version 2.0       #
# which accompanies this distribution, and is available at                    #
# http://www.apache.org/licenses/LICENSE-2.0                                  #
###############################################################################


def require_open(method):
    def wrapped(self, *args, **kwargs):
        if self.closed:
            raise ValueError("Cursor is closed")
        return method(self, *args, **kwargs)
    return wrapped


class MockCursor:

    def __init__(self, result):
        self.result = result
        self.current = 0
        self.closed = False

    @require_open
    def __next__(self):
        if self.current < len(self.result):
            nxt = self.result[self.current]
            self.current += 1
            return nxt
        else:
            raise StopIteration

    @require_open
    def __iter__(self):
        return self

    @require_open
    def fetchall(self):
        return self.result

    def close(self):
        self.closed = True
