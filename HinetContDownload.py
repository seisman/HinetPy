#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Author: Dongdong Tian @ USTC
#
# Revision History:
#   2013-07-09  Dongdong Tian   Initial codes
#   2014-06-17  Dongdong Tian   Now using python
#   2014-06-26  Dongdong Tian   Now support download files in parallel
#   2014-08-21  Dongdong Tian   Remove progress bar
#   2014-08-22  Dongdong Tian   Add option for specify maximum processed
#

"""Download coutinuous waveform datas from Hi-net.

Usage:
    HinetContDownload.py (--all | --new | --ids=IDFILE) [--procs=N]
    HinetContDownload.py -h

Options:
    -h --help     Show this help.
    --all         Fetch ID list of all avaiable datas from Hinet Status page.
    --new         Fecth ID list of undownloaded datas from Hinet Status page.
    --ids=IDFILE  Read ID list from file (ONE ID PER LINE).
    --procs=N     Maximum processes in parallel. [default: 10]

"""
import re
import sys
import configparser
import multiprocessing

import requests
from docopt import docopt
from bs4 import BeautifulSoup

# specify user name and password
config = configparser.ConfigParser()
config.read("Hinet.cfg")
user = config['Account']['User']
passwd = config['Account']['Password']

# base url for continuous waveform data
base = "http://www.hinet.bosai.go.jp/REGS/download/cont/"


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

    print("Downloading %s ..." % (fname))
    with open(fname, "wb") as fd:
        self = 0
        for chunk in d.iter_content(chunk_size=1024):
            if chunk:  # filter out keep-alive new chunks
                fd.write(chunk)
                fd.flush()
            self += len(chunk)


def cont_download(id):
    """Download continuous waveform data of specified id"""

    url = base + "cont_download.php"
    params = {"id": id}
    download(url, params)


def get_ids():
    """Get IDs from Hinet or IDs file"""

    ids = []

    #  new or all
    if arguments['--new'] or arguments['--all']:
        status = base + "cont_status.php"
        r = requests.get(status, auth=(user, passwd))
        if r.status_code == 401:
            print("Unauthorized.")
            sys.exit()
        soup = BeautifulSoup(r.content)

        if arguments['--new']:
            for data in soup.find_all("tr", class_="bglist2"):
                ids.append(str(data.contents[0].string))
        elif arguments['--all']:
            for data in soup.find_all("tr", class_="bglist2"):
                ids.append(str(data.contents[0].string))
            p = re.compile("openDownload")
            for data in soup.find_all("tr", class_="bglist1"):
                if p.search(str(data)):
                    ids.append(str(data.contents[0].string))

    # idfile
    if arguments['--ids']:
        with open(arguments['--ids'], "r") as fid:
            ids = fid.read().splitlines()

    return ids


if __name__ == '__main__':
    arguments = docopt(__doc__)
    ids = get_ids()

    print("Total %d files to download." % (len(ids)))
    if len(ids) == 0:
        sys.exit()

    max_proc = int(arguments['--procs'])
    proc_size = min(len(ids), multiprocessing.cpu_count(), max_proc)
    multiprocessing.Pool(processes=proc_size).map(cont_download, ids)
