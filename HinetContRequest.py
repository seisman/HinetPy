#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Author: Dongdong Tian @ USTC
#
# Revision History:
#   2013-07-09  Dongdong Tian   Initial Coding using perl
#   2014-01-15  Dongdong Tian   Now support selection of Organization & Network
#   2014-06-16  Dongdong Tian   Reimplement using new request method.
#                               Simpler, Smarter and Faster!
#                               Now using Python.
#   2014-08-22  Dongdong Tian   Add option for selection of code
#   2014-08-30  Dongdong Tian   Add option for compressed format.
#                               Default value (ZIP) is highly recommended.
#   2014-10-27  Dongdong Tian   Support requests with long time span.
#                               Support downloading after requests.
#                               Unzip and merge files.
#                               Move options to configure file.
#                               Add progressbar.
#   2014-10-31  Dongdong Tian   Remove option for compressed format, use ZIP.
#                               Add option for selection of code.
#                               Add option for output directory and filename.
#                               Adjust time span distribution strategy.
#

"""Request continuous waveform data from NIED Hi-net.

Usage:
    HinetContRequest.py <year> <month> <day> <hour> <min> <span> [options]
    HinetContRequest.py -h

Options:
    -h, --help              Show this help.
    -c CODE --code=CODE     Select code for organization and network.
    -o FILE --output=FILE   Output filename. Default: YYYYMMDDHHMM_SPAN.cnt.
    -d DIR --directory=DIR  Output directory. Default: current directory.

Codes of org & net:
    '0101' : 'NIED:NIED Hi-net',
    '0103' : 'NIED:NIED F-net (broadband)',
    '0103A': 'NIED:NIED F-net (strong motion)',
    '0201' : 'UNIV:Hokkaido University',
    '0202' : 'UNIV:Tohoku University',
    '0203' : 'UNIV:Tokyo University',
    '0204' : 'UNIV:Kyoto University',
    '0205' : 'UNIV:Kyushu University',
    '0206' : 'UNIV:Hirosaki University',
    '0207' : 'UNIV:Nagoya University',
    '0208' : 'UNIV:Kochi University',
    '0209' : 'UNIV:Kagoshima University',
    '0301' : 'JMA:JMA',
    '0401' : 'OTHER:JAMSTEC',
    '0501' : 'OTHER:AIST',
    '0601' : 'OTHER:GSI',
    '0701' : 'LOCAL:Tokyo Metropolitan Government',
    '0702' : 'LOCAL:Hot Spring Research Institute of Kanagawa Prefecture',
    '0703' : 'LOCAL:Aomori Prefectural Government',
    '0705' : 'LOCAL:Shizuoka Prefectural Government',

"""

import os
import sys
import time
import math
import glob
import shlex
import zipfile
import subprocess
import configparser
import multiprocessing
from datetime import date, datetime, timedelta

from clint.textui import progress
import requests
from bs4 import BeautifulSoup
from docopt import docopt

# basic urls
base = "http://www.hinet.bosai.go.jp/REGS/download/cont/"
request = base + "cont_request.php"
status = base + "cont_status.php"
download = base + "cont_download.php"

# all legal codes
code_list = ['0101', '0103', '0103A',
             '0201', '0202', '0203', '0204', '0205',
             '0206', '0207', '0208', '0209',
             '0301',
             '0401',
             '0501',
             '0601',
             '0701', '0702', '0703', '0705',
             ]


def auth_check(status_code):
    ''' check authorization '''

    if status_code == 401:
        print("Unauthorized. Check your username and password!")
        sys.exit()


def date_check(event):
    ''' check if waveform data are available '''

    start = date(2004, 4, 1)    # start date of avaiable data
    today = date.today()        # end date of avaiable data

    if event.date() < start or event.date() > today:
        print("Not within Hi-net service period.")
        sys.exit()


def code_parser(code):
    ''' parser network code '''

    if code not in code_list:
        print("%s: Error code for organization and network." % (code))
        sys.exit()
    org, net = code[0:2], code[2:]

    return org, net


def cont_request(org, net, event, span):
    ''' request continuous data with limited time span '''

    payload = {
        'org1':  org,
        'org2':  net,
        'year':  event.strftime("%Y"),
        'month': event.strftime("%m"),
        'day':   event.strftime("%d"),
        'hour':  event.strftime("%H"),
        'min':   event.strftime("%M"),
        'span':  str(span),
        'arc':   'ZIP',
        'size':  '93680',    # estimated size of the data, it is not important
        'LANG':  'en',       # english version of web
        'rn': str(int((datetime.now() - datetime(1970, 1, 1)).total_seconds()))
    }
    r = requests.post(request, params=payload, auth=(user, passwd))
    auth_check(r.status_code)

    s = requests.get(status, auth=(user, passwd))
    soup = BeautifulSoup(s.content)
    id = str(soup.find("tr", class_="bglist1").contents[0].string)

    # check data status
    while True:
        s = requests.get(status, auth=(user, passwd))
        soup = BeautifulSoup(s.content)
        if str(soup.find("tr", class_="bglist1").contents[0].string) == id:
            time.sleep(2)  # still preparing data
        elif str(soup.find("tr", class_="bglist2").contents[0].string) == id:
            break          # data available
        elif str(soup.find("tr", class_="bglist3").contents[0].string) == id:
            print("What's bglist3?")
        elif str(soup.find("tr", class_="bglist4").contents[0].string) == id:
            print("Error!")

    return id


def cont_download(id):
    ''' Download continuous waveform data of specified id '''

    d = requests.get(download, params={"id": id},
                     auth=(user, passwd), stream=True)
    auth_check(d.status_code)

    # file size
    total_length = int(d.headers['Content-Length'].strip())
    # file name
    # disposition = d.headers['Content-Disposition'].strip()
    # fname = disposition.split('filename=')[1].strip('\'"')
    fname = "%s.zip" % id   # now use id as filename

    with open(fname, "wb") as fd:
        for chunk in progress.bar(d.iter_content(chunk_size=1024),
                                  label=fname,
                                  expected_size=(total_length/1024) + 1):
            if chunk:  # filter out keep-alive new chunks
                fd.write(chunk)
                fd.flush()

    if os.path.getsize(fname) != total_length:
        print("File %s is not complete!")


def unzip(zips):
    """unzip zip filelist"""

    for file in zips:
        zipFile = zipfile.ZipFile(file, "r")
        for name in zipFile.namelist():
            zipFile.extract(name)


def win32_cat(cnts, cnt_total):
    """merge WIN32 files to one total WIN32 file"""

    cmd = "%s %s -o %s" % (catwin32, ' '.join(cnts), cnt_total)
    args = shlex.split(cmd)
    subprocess.call(args, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


def unlink_lists(files):
    for f in files:
        os.unlink(f)


if __name__ == "__main__":
    # User name & passwd
    config = configparser.ConfigParser()
    config.read("Hinet.cfg")
    user = config['Account']['User']
    passwd = config['Account']['Password']
    maxspan = int(config['Cont']['MaxSpan'])
    catwin32 = config['Tools']['catwin32']

    arguments = docopt(__doc__)

    # Code for org & net
    code = config['Cont']['Net']
    if arguments['--code']:
        code = arguments['--code']
    org, net = code_parser(code)

    year = int(arguments['<year>'])
    month = int(arguments['<month>'])
    day = int(arguments['<day>'])
    hour = int(arguments['<hour>'])
    minute = int(arguments['<min>'])
    total_span = int(arguments['<span>'])

    event = datetime(year, month, day, hour, minute)
    date_check(event)

    print("%s ~%s" % (event.strftime("%Y-%m-%d %H:%M"), total_span))

    count = math.ceil(total_span/maxspan)
    span = [total_span//count for i in range(0, count)]
    for i in range(0, total_span % count):
        span[i] += 1

    ids = []
    for i in range(0, count):
        id = cont_request(org, net, event, span[i])
        ids.append(id)
        event += timedelta(minutes=span[i])
    zips = [x+'.zip' for x in ids]

    procs = min(len(ids), multiprocessing.cpu_count())
    multiprocessing.Pool(processes=procs).map(cont_download, ids)

    # unzip zip files
    unzip(zips)
    unlink_lists(zips)

    # merge win32 files
    cnts = glob.glob("??????????????????.cnt")
    cnt_total = "%s_%d.cnt" % (event.strftime("%Y%m%d%H%M"), total_span)
    if arguments['--output']:
        cnt_total = arguments['--output']

    if arguments['--directory']:
        dir = arguments['--directory']
        if not os.path.exists(dir):
            os.makedirs(dir)
        cnt_total = os.path.join(dir, cnt_total)

    win32_cat(cnts, cnt_total)
    unlink_lists(cnts)

    if arguments['--directory']:
        chfile = "%s_%s_%s.euc.ch" % (org, net, event.strftime("%Y%m%d"))
        os.rename(chfile, os.path.join(dir, chfile))
    os.unlink("%s_%s_%s.sjis.ch" % (org, net, event.strftime("%Y%m%d")))
    os.unlink("readme.txt")
