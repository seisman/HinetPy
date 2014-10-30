#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Author: Dongdong Tian @ USTC
#
# Revision History:
#   2014-08-31  Dongdong Tian   Initial Coding
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
config.read("Hinet.cfg")
user = config['Account']['User']
passwd = config['Account']['Password']

# base url for continuous waveform data
base = "http://www.hinet.bosai.go.jp/REGS/JMA/"


def download(url, params):
    d = requests.get(url, params=params, auth=(user, passwd), stream=True)
    if d.status_code == 401:
        print("Unauthorized.")
        sys.exit()

    # file size
    size = int(d.headers['Content-Length'].strip())
    # file name
    disposition = d.headers['Content-Disposition'].strip()
    fname = disposition.split('filename=')[1].strip('\'"')

    with open(fname, "wb") as fd:
        self = 0
        for chunk in d.iter_content(chunk_size=1024):
            if chunk:  # filter out keep-alive new chunks
                fd.write(chunk)
                fd.flush()
            self += len(chunk)


if __name__ == '__main__':
    arguments = docopt(__doc__)

    if arguments['--measure']:
        data = "measure"
    elif arguments['--mecha']:
        data = "mecha"

    os = arguments['--os'][0:1]

    url = base + "dlDialogue.php"
    params = {
        "data": data,
        "rtm": arguments['<yyyymmdd>'],
        "span": arguments['<span>'],
        "os": arguments['--os'][:1],
    }
    download(url, params)
