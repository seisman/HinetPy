#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Author: Dongdong Tian @ USTC
#
# Revision History:
#   2014-08-31  Dongdong Tian   Initial Coding
#   2014-12-03  Dongdong Tian   Update to Hinet V141201
#   2015-01-08  Dongdong Tian   Fix bugs caused by update on Dec. 1st, 2014
#

"""Request arrival time data or focal mechanism catalog from Hi-net.

Usage:
    HinetJMARequest.py (--measure | --mecha) <yyyymmdd> <span> [--os=OS]
    HinetJMARequest.py -h

Options:
    -h --help     Show this help.
    --measure     Request arrival time data.
    --mecha       Request focal mechanism catalog.
    --os=OS       Line break format, choose from DOS or UNIX. [default: DOS]

"""
import sys
import configparser

import requests
from docopt import docopt

# specify user name and password
config = configparser.ConfigParser()
if not config.read("Hinet.cfg"):
    logging.error("Configure file `Hinet.cfg' not found.")
    sys.exit()
auth = {
    'auth_un': config['Account']['User'],
    'auth_pw': config['Account']['Password'],
    }

# base url for continuous waveform data
AUTH = "https://hinetwww11.bosai.go.jp/auth/"
BASE = AUTH + "JMA/"
URL = BASE + "dlDialogue.php"


if __name__ == '__main__':
    arguments = docopt(__doc__)
    requests.packages.urllib3.disable_warnings()

    if arguments['--measure']:
        data = "measure"
    elif arguments['--mecha']:
        data = "mecha"

    rtm = arguments['<yyyymmdd>']
    span = arguments['<span>']
    os = arguments['--os'][0:1]

    params = {
        "data": data,
        "rtm": rtm,
        "span": span,
        "os": os,
    }

    s = requests.Session()
    s.verify = False
    s.post(AUTH)  # get cookies
    s.post(AUTH, data=auth)  # login

    d = s.post(URL, params=params, stream=True)

    # file size
    size = int(d.headers['Content-Length'].strip())
    # file name
    fname = "{}_{}_{}.txt".format(data, rtm, span)

    with open(fname, "wb") as fd:
        for chunk in d.iter_content(chunk_size=1024):
            if chunk:  # filter out keep-alive new chunks
                fd.write(chunk)
                fd.flush()
