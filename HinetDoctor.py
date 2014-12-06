#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Author: Dongdong Tian @ USTC
#
# Revision History:
#   2014-12-05  Dongdong Tian   Initial Coding
#
import os
import re
import sys
import shutil
import logging
import configparser

import requests

AUTH = "https://hinetwww11.bosai.go.jp/auth/"
CONT = AUTH + "download/cont/"


def auth_check(auth):
    ''' check authentication '''

    try:
        r = requests.post(AUTH, data=auth, verify=False,
                          allow_redirects=False, timeout=20)
    except requests.exceptions.ConnectTimeout:
        logging.error("ConnectTimeout in 20 seconds.")
        sys.exit()
    except requests.exceptions.ConnectionError:
        logging.error("Name or service not known")
        sys.exit()

    if r.status_code == requests.codes.ok:  # succeed
        logging.info("Username and Password is right.")
    elif r.status_code == requests.codes.found:  # redirect
        logging.error("Maybe unauthorized. Check your username and password!")
        sys.exit()
    else:
        logging.warning("Status code: {}".format(status_code))
        logging.warning("Report this status code to seisman.info@gmail.com")


def cmd_exists(cmd):
    ''' check if a cmd exists '''

    if shutil.which(cmd):
        logging.info("%s in your PATH.", cmd)
    else:
        logging.error("%s not in your PATH or not executable.", cmd)
        sys.exit()


def check_version(auth):

    try:
        r = requests.post(CONT, data=auth, verify=False,
                          allow_redirects=False, timeout=20)
    except requests.exceptions.ConnectTimeout:
        logging.error("ConnectTimeout in 20 seconds.")
        sys.exit()
    except requests.exceptions.ConnectionError:
        logging.error("Name or service not known")
        sys.exit()

    version = re.search(r'cont\.js\?(?P<VER>\d{6})', r.text).group('VER')

    if version != '141201':
        logging.warning("Hi-net website seems to have been updated. "
                        "These scripts may be working or not working")


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s %(levelname)-7s %(message)s',
                        datefmt='%H:%M:%S')
    logging.getLogger("requests").setLevel(logging.WARNING)
    requests.packages.urllib3.disable_warnings()
    config = configparser.ConfigParser()
    config.read('Hinet.cfg')

    auth = {
        'auth_un': config['Account']['User'],
        'auth_pw': config['Account']['Password'],
        }
    auth_check(auth)

    check_version(auth)

    catwin32 = os.path.expanduser(config['Tools']['catwin32'])
    cmd_exists(catwin32)
