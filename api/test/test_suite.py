###############################################################################
# Copyright (c) 2017-2019 Koren Lev (Cisco Systems),                          #
# Yaron Yogev (Cisco Systems), Ilia Abashin (Cisco Systems) and others        #
#                                                                             #
# All rights reserved. This program and the accompanying materials            #
# are made available under the terms of the Apache License, Version 2.0       #
# which accompanies this distribution, and is available at                    #
# http://www.apache.org/licenses/LICENSE-2.0                                  #
###############################################################################
import argparse
import unittest


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--dir", dest="start_dir", nargs="?",
                        type=str, default=".",
                        help="Name of root directory for test cases discovery")

    return parser.parse_args()

if __name__ == "__main__":
    args = get_args()
    suite = unittest.TestLoader().discover(start_dir=args.start_dir)
    unittest.TextTestRunner(verbosity=2).run(suite)