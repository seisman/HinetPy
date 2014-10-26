#!/usr/bin/env python
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
#

"""Request continuous waveform data from Hi-net.

Usage:
    HinetContRequest.py <year> <month> <day> <hour> <min> <span> [options]
    HinetContRequest.py -h

Options:
    -h --help    Show this help.
    --code=CODE  Select code for organization and network. [default: 0101]
    --arc=ARC    Compressed format: Z, GZIP, ZIP, LZH. [default: ZIP]

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

import sys
import time
import configparser
from datetime import date, datetime

import requests
from bs4 import BeautifulSoup
from docopt import docopt

base = "http://www.hinet.bosai.go.jp/REGS/download/cont/"
request = base + "cont_request.php"
status = base + 'cont_status.php'

# all legal codes
code_list = ['0101', '0103', '0103A',
             '0201', '0202', '0203', '0204', '0205',
             '0206', '0207', '0208', '0209',
             '0301',
             '0401',
             '0501',
             '0601',
             '0701', '0702', '0703', '0705'
             ]


def cont_request(org, net, event, span, arc):
    ''' one time request '''

    payload = {
        'org1':  org,
        'org2':  net,
        'year':  event.strftime("%Y"),
        'month': event.strftime("%m"),
        'day':   event.strftime("%d"),
        'hour':  event.strftime("%H"),
        'min':   event.strftime("%M"),
        'span':  str(span),
        'arc':   arc,
        'size':  '93680',    # estimated size of the data, it is not important
        'LANG':  'en',       # english version of web
        'rn': str(int((datetime.now() - datetime(1970, 1, 1)).total_seconds()))
    }
    r = requests.post(request, params=payload, auth=(user, passwd), timeout=5)
    if r.status_code == 401:
        print("Unauthorized.")
        sys.exit()

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
            break          # data avaiable
        elif str(soup.find("tr", class_="bglist3").contents[0].string) == id:
            print("What's bglist3?")
        elif str(soup.find("tr", class_="bglist4").contents[0].string) == id:
            print("Error!")


if __name__ == "__main__":

    # User name & passwd
    config = configparser.ConfigParser()
    config.read("Hinet.cfg")
    user = config['Account']['User']
    passwd = config['Account']['Password']

    start = date(2004, 4, 1)    # start date of avaiable data
    today = date.today()        # end date of avaiable data

    arguments = docopt(__doc__)

    # Code for org & net
    code = arguments['--code']
    if code not in code_list:
        print("%s: Error code for organization and network." % (code))
        sys.exit()
    org, net = code[0:2], code[2:]

    # compressed format
    arc = arguments['--arc']
    if arc not in ["Z", "GZIP", "ZIP", "LHZ"]:
        print("%s: Error in compressed format." % (arc))
        sys.exit()

    # start time and time span
    year = int(arguments['<year>'])
    month = int(arguments['<month>'])
    day = int(arguments['<day>'])
    hour = int(arguments['<hour>'])
    minute = int(arguments['<min>'])
    span = int(arguments['<span>'])

    # check validity of time
    event = datetime(year, month, day, hour, minute)
    if event.date() < start or event.date() > today:
        print("Not within Hi-net service period")
        sys.exit()

    print("%s ~%s" % (event.strftime("%Y-%m-%d %H:%M"), span))

    cont_request(org, net, event, span, arc)
