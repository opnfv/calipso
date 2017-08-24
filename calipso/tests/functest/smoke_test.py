#!/usr/bin/env python3
###############################################################################
# Copyright (c) 2017 Koren Lev (Cisco Systems), Yaron Yogev (Cisco Systems)   #
# and others                                                                  #
#                                                                             #
# All rights reserved. This program and the accompanying materials            #
# are made available under the terms of the Apache License, Version 2.0       #
# which accompanies this distribution, and is available at                    #
# http://www.apache.org/licenses/LICENSE-2.0                                  #
###############################################################################

# Check that Docker images are up and running

import argparse
from subprocess import check_output
import sys

from utils.binary_converter import BinaryConverter

IMAGES_TO_SEARCH = ["ui", "sensu", "scan", "api", "ldap", "listen", "mongo"]


class DockerImageCheck:
    STATUS_HEADER = "STATUS"
    PORTS_HEADER = "PORTS"
    HEADERS = [
        "CONTAINER ID",
        "IMAGE",
        "COMMAND",
        "CREATED",
        "STATUS",
        "PORTS",
        "NAMES"
    ]

    def __init__(self):
        args = self.get_args()
        self.docker_ps = ""
        if args.inputfile:
            try:
                with open(args.inputfile, 'r') as input_file:
                    dummy_input = input_file.read()
                    self.docker_ps = dummy_input.splitlines()
            except FileNotFoundError:
                raise FileNotFoundError("failed to open input file: {}"
                                        .format(args.inputfile))
                exit(1)
        else:
            cmd = "sudo docker ps"
            output = check_output(cmd, shell=True)
            converter = BinaryConverter()
            output = converter.binary2str(output)
            self.docker_ps = output.splitlines()
        headers_line = self.docker_ps[0]
        self.header_location = {}
        for h in self.HEADERS:
            self.header_location[h] = headers_line.index(h)

    @staticmethod
    def get_args():
        # try to read scan plan from command line parameters
        parser = argparse.ArgumentParser()
        parser.add_argument('-i', '--inputfile', nargs='?', type=str,
                            default='',
                            help="read input from the specifed file \n" +
                                 "(default: from stdin)")
        return parser.parse_args()

    def verify_image_is_up(self, image_name) -> bool:
        matches = [line for line in self.docker_ps if line.endswith(image_name)]
        if not matches:
            print("missing docker image: {}".format(image_name))
            return False
        line = matches[0]
        status = line[self.header_location[self.STATUS_HEADER]-1:]
        status = status.split()[0] if ' ' in status else status
        status = status.lower()
        if status == "up":
            return True
        print("image {} is not up".format(image_name))
        return False

if __name__ == '__main__':
    image_checker = DockerImageCheck()
    ret = True
    for image in ["calipso-{}".format(i) for i in IMAGES_TO_SEARCH]:
        if not image_checker.verify_image_is_up(image):
            ret = False
    if ret:
        print("All containers are running")
    sys.exit(0 if ret else 1)
