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
try:
    import configparser
except ImportError:
    raise RuntimeError("Python 2.X is NOT supported.")

import clint
import docopt
import requests


def auth_check(auth):
    ''' check authentication '''

    logging.info("Username: %s", auth['auth_un'])
    logging.info("Password: %s", auth['auth_pw'])

    try:
        s = requests.Session()
        s.post(AUTH, verify=False)  # get cookies
        r = s.post(AUTH, data=auth, timeout=20)  # login
    except requests.exceptions.ConnectTimeout:
        logging.error("ConnectTimeout in 20 seconds.")
        sys.exit()
    except requests.exceptions.ConnectionError:
        logging.error("Name or service not known")
        sys.exit()

    inout = re.search(r'auth_log(?P<LOG>.*)\.png', r.text).group('LOG')

    if inout == 'out':
        logging.error("Maybe unauthorized. Check your username and password!")
        sys.exit()


def cmd_exists(cmd):
    ''' check if a cmd exists '''

    if shutil.which(cmd):
        logging.info("%s in your PATH.", cmd)
    else:
        logging.error("%s not in your PATH or not executable.", cmd)
        sys.exit()


def check_version(auth):

    try:
        s = requests.Session()
        s.post(AUTH, verify=False)
        s.post(AUTH, data=auth)
        r = s.post(CONT, timeout=20)
    except requests.exceptions.ConnectTimeout:
        logging.error("ConnectTimeout in 20 seconds.")
        sys.exit()
    except requests.exceptions.ConnectionError:
        logging.error("Name or service not known")
        sys.exit()

    version = re.search(r'cont\.js\?(?P<VER>\d{6})', r.text).group('VER')

    if version == '150708':
        logging.info("Hi-net website version = %s.", version)
    else:
        logging.warning("Hi-net website seems to have been updated. "
                        "These scripts may be working or not working")


def check_station_number():

    try:
        s = requests.Session()
        s.post(AUTH, verify=False)
        s.post(AUTH, data=auth)
        r = s.post(STATION, timeout=20)
    except requests.exceptions.ConnectTimeout:
        logging.error("ConnectTimeout in 20 seconds.")
        sys.exit()
    except requests.exceptions.ConnectionError:
        logging.error("Name or service not known")
        sys.exit()

    # Hi-net station numbers
    hinet = re.compile(r'<td class="td1">(?P<CHN>N\..{3}H)<\/td>')
    hinet_count = len(hinet.findall(r.text))
    if hinet_count == 0:
        hinet_count = 777
    logging.info("Selected Stations of Hi-net: %d", hinet_count)

    # F-net station numbers
    fnet = re.compile(r'<td class="td1">(?P<CHN>N\..{3}F)<\/td>')
    fnet_count = len(fnet.findall(r.text))
    if fnet_count == 0:
        fnet_count = 73
    logging.info("Selected Stations of F-net: %d", fnet_count)

    return hinet_count, fnet_count


def check_maxspan(code, maxspan, hinet, fnet):

    if code == '0301':
        allowed_max_span = 13
    elif code == '0204':
        allowed_max_span = 59
    elif code == '0203':
        allowed_max_span = 39
    elif code == '0101':  # hinet
        allowed_max_span = min(int(12000/hinet/3), 60)
    elif code in ['0103', '0103A']:
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


if __name__ == '__main__':
    if sys.version_info < (3, 3):
        raise RuntimeError("Python 3.4 or 3.3 is required")

    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s %(levelname)-7s %(message)s',
                        datefmt='%H:%M:%S')
    logging.getLogger("requests").setLevel(logging.WARNING)
    requests.packages.urllib3.disable_warnings()

    config = configparser.ConfigParser()
    logging.info("Reading Hi-net configure file...")
    if not config.read("Hinet.cfg"):
        logging.error("Configure file `Hinet.cfg' not found.")
        sys.exit()

    AUTH = config['URL']['AUTH']
    CONT = config['URL']['CONT']
    STATION = config['URL']['STATION']

    auth = {
        'auth_un': config['Account']['User'],
        'auth_pw': config['Account']['Password'],
        }
    auth_check(auth)

    check_version(auth)

    cmd_exists("catwin32")
    cmd_exists("win2sac_32")

    hinet, fnet = check_station_number()

    code = config['Cont']['Net']
    maxspan = int(config['Cont']['MaxSpan'])
    check_maxspan(code, maxspan, hinet, fnet)
