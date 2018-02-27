#!/usr/bin/env python
###############################################################################
# Copyright (c) 2017 Koren Lev (Cisco Systems), Yaron Yogev (Cisco Systems)   #
# and others                                                                  #
#                                                                             #
# All rights reserved. This program and the accompanying materials            #
# are made available under the terms of the Apache License, Version 2.0       #
# which accompanies this distribution, and is available at                    #
# http://www.apache.org/licenses/LICENSE-2.0                                  #
###############################################################################

import argparse
import re
import sys
import subprocess

from binary_converter import binary2str


if len(sys.argv) < 2:
    raise ValueError('destination address must be specified')


def thresholds_string(string):
    matches = re.match('\d+%/\d+([.]\d+)?/\d+([.]\d+)?', string)
    if not matches:
        msg = "%r is not a valid thresholds string" % string
        raise argparse.ArgumentTypeError(msg)
    return string


def get_args():
    # try to read scan plan from command line parameters
    parser = argparse.ArgumentParser()

    parser.add_argument("-W", "--warning", nargs="?",
                        type=thresholds_string,
                        default='1%/300/600',
                        help="warning thresholds: packet-loss "
                             "(%)/avg-rtt (ms)/max-rtt (ms)"
                             "(example: 1%/300ms/600ms)")
    parser.add_argument("-C", "--critical", nargs="?",
                        type=thresholds_string,
                        default='10%/1000/2000',
                        help="critical thresholds: packet-loss "
                             "(%)/avg-rtt (ms)/max-rtt (ms)"
                             "(example: 1%/300ms/600ms)")
    parser.add_argument("-f", "--source", nargs="?", type=str, default='',
                        help="source address")
    parser.add_argument("-t", "--target", nargs="?", type=str, default='',
                        help="target address")
    parser.add_argument("-c", "--count", nargs="?", type=int, default=5,
                        help="how many packets will be sent")
    parser.add_argument("-i", "--interval", nargs="?", type=float, default=0.5,
                        help="seconds between sending each packet")
    parser.add_argument("-p", "--pattern", nargs="?", type=str,
                        default='OS-DNA', help="pattern to pad packet with")
    parser.add_argument("-w", "--wait", nargs="?", type=int, default=5,
                        help="seconds to wait for completion of all responses")
    parser.add_argument("-s", "--packetsize", nargs="?", type=int, default=256,
                        help="size of packet vseconds to wait for completion "
                             "of all responses")
    return parser.parse_args()

args = get_args()

if not args.target:
    raise ValueError('target address must be specified')

rc = 0

try:
    cmd = "ping -c {} -i {} -p {} -w {} -s {} {}{} {}".format(
        args.count, args.interval,
        args.pattern, args.wait,
        args.packetsize,
        '-I ' if args.source else '',
        args.source, args.target)
    out = subprocess.check_output([cmd],
                                  stderr=subprocess.STDOUT,
                                  shell=True)
    out = binary2str(out)
except subprocess.CalledProcessError as e:
    print("Error doing ping: {}\n".format(binary2str(e.output)))

# find packet loss data
packet_loss_match = re.search('(\d+)[%] packet loss', out, re.M)
if not packet_loss_match:
    out += '\npacket loss data not found'
    rc = 2

# find rtt avg/max data
rtt_results = None
if rc < 2:
    regexp = 'rtt min/avg/max/mdev = [0-9.]+/([0-9.]+)/([0-9.]+)/[0-9.]+ ms'
    rtt_results = re.search(regexp, out, re.M)
    if not rtt_results:
        out += '\nrtt results not found'
        rc = 2
if rc < 2:
    packet_loss = int(packet_loss_match.group(1))
    avg_rtt = float(rtt_results.group(1))
    max_rtt = float(rtt_results.group(2))
    thresholds_regexp = r'(\d+)%/(\d+[.0-9]*)/(\d+[.0-9]*)'
    warn_threshold_match = re.match(thresholds_regexp, args.warning)
    critical_threshold_match = re.match(thresholds_regexp, args.critical)
    packet_loss_warn = int(warn_threshold_match.group(1))
    packet_loss_critical = int(critical_threshold_match.group(1))
    avg_rtt_warn = float(warn_threshold_match.group(2))
    avg_rtt_critical = float(critical_threshold_match.group(2))
    max_rtt_warn = float(warn_threshold_match.group(3))
    max_rtt_critical = float(critical_threshold_match.group(3))
    if packet_loss > packet_loss_critical or avg_rtt >= avg_rtt_critical or \
            max_rtt >= max_rtt_critical:
        rc = 2
    elif packet_loss > packet_loss_warn or avg_rtt >= avg_rtt_warn or \
            max_rtt >= max_rtt_warn:
        rc = 1

print(out)
exit(rc)
