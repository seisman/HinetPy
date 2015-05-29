#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Author: Dongdong Tian @ USTC
#
# Revision History:
#   2015-05-29  Dongdong Tian   Initial Coding
#

"""Select Hi-net/F-net stations to request waveform data from NIED

Usage:
    StationSelector.py -c CODE [-l LIST]
    StationSelector.py -h

Options:
    -h, --help              Show this help.
    -c CODE, --code=CODE    Network code. Hi-net: 0101, F-net: 0103.
    -l LIST, --list=LIST    Station list file.

Notes:
    1. All stations will be selected if -l options is NOT used.
    2. List file contains station list, one station per line,
       lines start with '#' will be ignored.
    3. This script does NOT check whether a station belongs to a network.
"""

import logging
import configparser

from docopt import docopt
import requests

AUTH = "https://hinetwww11.bosai.go.jp/auth/"
SELECT = AUTH + "/download/cont/select_confirm.php"

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s %(levelname)-7s %(message)s',
                        datefmt='%H:%M:%S')
    logging.getLogger("requests").setLevel(logging.WARNING)
    requests.packages.urllib3.disable_warnings()

    arguments = docopt(__doc__)
    config = configparser.ConfigParser()
    if not config.read("Hinet.cfg"):
        logging.error("Configure file `Hinet.cfg' not found.")
        sys.exit()

    auth = {
        'auth_un': config['Account']['User'],
        'auth_pw': config['Account']['Password'],
    }

    s = requests.Session()
    s.verify = False
    s.post(AUTH)    # get cookies
    s.post(AUTH, data=auth)  # login

    code = None
    if arguments['--code'] not in ["0101", "0103"]:
        logging.error("Network code must be 0101 or 0103.")
    else:
        code = arguments['--code']

    sta = None
    count = 0
    if arguments['--list']:
        with open(arguments['--list']) as f:
            lines = [line.strip() for line in f if not line.startswith("#")]
        count = len(lines)
        if lines:
            sta = ':'.join(lines)

    payload = {
        'net': code,
        'stcds': sta,
        'mode': '1',
    }

    r = s.post(SELECT, data=payload)

    if code == "0101":
        net = "Hi-net"
    else:
        net = "F-net"

    if count == 0:
        count = "All"

    logging.info("%s stations selected for %s.", count, net)
