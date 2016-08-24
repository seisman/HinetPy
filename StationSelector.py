#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Author: Dongdong Tian @ USTC
#
# Revision History:
#   2015-05-29  Dongdong Tian   Initial Coding
#   2015-06-27  Dongdong Tian   Move URLs to configure file
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
    1. All stations will be selected if -l options is omitted.
    2. List file contains station list, one station per line,
       lines start with '#' will be ignored.
    3. Format of station name is 'X.XXXX' not 'X.XXXX.X'.
    4. This script does NOT check whether a station belongs to a network.
"""

import sys
import logging

from docopt import docopt

from util import auth_login, read_config, get_station_number, SELECT


def main():
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s %(levelname)-7s %(message)s',
                        datefmt='%H:%M:%S')
    logging.getLogger("requests").setLevel(logging.WARNING)

    # parse arguments
    arguments = docopt(__doc__)
    code = arguments['--code']
    if code not in ["0101", "0103"]:
        logging.error("Network code must be 0101 or 0103.")
        sys.exit()
    else:
        net = "Hi-net" if code == "0101" else "F-net"

    stations = None   # default to select all stations
    listfile = arguments['--list']
    if listfile:
        with open(listfile) as f:
            lines = [line.strip() for line in f if not line.startswith("#")]
        stations = ':'.join(lines)
        logging.info("Number of stations in %s: %d", listfile, len(lines))

    payload = {
        'net': code,
        'stcds': stations,
        'mode': '1',
    }

    # select stations
    config = read_config('Hinet.cfg')
    username = config['Account']['User']
    password = config['Account']['Password']
    s = auth_login(username, password)
    s.post(SELECT, data=payload)

    # check station numbers
    get_station_number(s, net)


if __name__ == "__main__":
    main()
