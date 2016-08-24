#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Author: Dongdong Tian @ USTC
#
# Revision History:
#   2014-12-05  Dongdong Tian   Initial Coding
#   2014-12-27  Dongdong Tian   Fix bugs caused by update on Dec. 1st, 2014
#   2015-02-25  Dongdong Tian   Add data download service for ADEP (code=0801).
#   2015-06-27  Dongdong Tian   Move URLs to configure file
#   2015-07-25  Dongdong Tian   Hi-net website updated, nothing changes
#

import re
import sys
import shutil
import logging
import configparser

import clint
import docopt
import requests

from util import auth_login, read_config, get_station_number, CONT


def cmd_exists(cmd):
    ''' check if a cmd exists '''

    cmd_path = shutil.which(cmd)
    if cmd_path:
        logging.info("%s in your PATH: %s", cmd, cmd_path)
    else:
        logging.error("%s not in your PATH or not executable.", cmd)


def check_version(s):
    ''' check version of Hinet website '''

    r = s.get(CONT)
    version = re.search(r'cont\.js\?(?P<VER>\d{6})', r.text).group('VER')

    if version == '160422':
        logging.info("Hi-net website version = %s.", version)
    else:
        logging.warning("Hi-net website seems to have been updated."
                        "These scripts may not work as expected.")

def check_maxspan(code, maxspan, hinet, fnet):
    ''' check if maxspan in allowed range '''

    if code == '0301':
        allowed_max_span = 13
    elif code == '0204':
        allowed_max_span = 59
    elif code == '0203':
        allowed_max_span = 39
    elif code == '0101':  # Hi-net
        allowed_max_span = min(int(12000/hinet/3), 60)
    elif code in ['0103', '0103A']:  # F-net
        allowed_max_span = min(int(12000/fnet/6), 60)
    elif code == '0801':
        allowed_max_span = 15
    else:
        allowed_max_span = 60

    if 1 <= maxspan <= allowed_max_span:
        logging.info("MaxSpan is in allowed range: [1, %d]", allowed_max_span)
    else:
        logging.error("MaxSpan is NOT in allowed range: [1, %d]",
                      allowed_max_span)


def main():
    ''' main function '''

    if sys.version_info < (3, 3):
        raise RuntimeError("Python 3.3 or newer is required")

    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s %(levelname)-7s %(message)s',
                        datefmt='%H:%M:%S')
    logging.getLogger("requests").setLevel(logging.WARNING)

    logging.info("Reading Hi-net configure file...")
    config = read_config('Hinet.cfg')

    username = config['Account']['User']
    password = config['Account']['Password']
    s = auth_login(username, password)
    check_version(s)

    hinet = get_station_number(s, "Hi-net")
    fnet = get_station_number(s, "F-net")
    code = config['Cont']['Net']
    maxspan = config.getint('Cont', 'MaxSpan')
    check_maxspan(code, maxspan, hinet, fnet)

    cmd_exists("catwin32")
    cmd_exists("win2sac_32")

if __name__ == '__main__':
    main()
