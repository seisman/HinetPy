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
#   2014-11-01  Dongdong Tian   Support volcanos data from NIED Hi-net website.
#                               Add option for channel table filename.
#                               Modify the default filename for cnt and ch.
#

"""Request continuous waveform data from NIED Hi-net.

Usage:
    HinetContRequest.py <year> <month> <day> <hour> <min> <span> [options]
    HinetContRequest.py -h

Options:
    -h, --help              Show this help.
    -c CODE --code=CODE     Select code for organization and network.
    -d DIR --directory=DIR  Output directory. Default: current directory.
    -o FILE --output=FILE   Output filename.
                            Default: CODE_YYYYMMDDHHMM_SPAN.cnt
    -t FILE --ctable=FILE   Channel table filename. Default: CODE_YYYYMMDD.ch

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
    '0301' : 'JMA:JMA Seismometer Network',
    '0401' : 'JAMSTEC: Realtime Data from the Deep Sea Floor Observatory',
    '0402' : 'JAMSTEC:JAMSTEC DONET1 (broadband)',
    '0402A': 'JAMSTEC:JAMSTEC DONET1 (strong motion)';
    '0501' : 'OTHER:AIST',
    '0601' : 'OTHER:GSI',
    '0701' : 'LOCAL:Tokyo Metropolitan Government',
    '0702' : 'LOCAL:Hot Spring Research Institute of Kanagawa Prefecture',
    '0703' : 'LOCAL:Aomori Prefectural Government',
    '0705' : 'LOCAL:Shizuoka Prefectural Government',

Codes for NIED V-net (0105):
    '010503' : '0105:Usuzan';
    '010505' : '0105:Iwatesan';
    '010507' : '0105:Asamayama';
    '010509' : '0105:Fujisan';
    '010510' : '0105:Miyakejima';
    '010511' : '0105:Izu-Oshima';
    '010512' : '0105:Asosan';
    '010514' : '0105:Kirishimayama';

Codes for JMA Volcanic Seismometer Network (0302):
    '030201' : '0302:Atosanupuri';
    '030202' : '0302:Meakandake';
    '030203' : '0302:Taisetsuzan';
    '030204' : '0302:Tokachidake';
    '030205' : '0302:Tarumaesan';
    '030206' : '0302:Kuttara';
    '030207' : '0302:Usuzan';
    '030208' : '0302:Hokkaido-Komagatake';
    '030209' : '0302:Esan';
    '030210' : '0302:Iwakisan';
    '030247' : '0302:Hakkodasan';
    '030211' : '0302:Akita-Yakeyama';
    '030212' : '0302:Iwatesan';
    '030213' : '0302:Akita-Komagatake';
    '030214' : '0302:Chokaisan';
    '030215' : '0302:Kurikomayama';
    '030216' : '0302:Zaozan';
    '030217' : '0302:Azumayama';
    '030218' : '0302:Adatarayama';
    '030219' : '0302:Bandaisan';
    '030220' : '0302:Nasudake';
    '030221' : '0302:Nikko-Shiranesan';
    '030222' : '0302:Kusatsu-Shiranesan';
    '030223' : '0302:Asamayama';
    '030224' : '0302:Niigata-Yakeyama';
    '030225' : '0302:Yakedake';
    '030226' : '0302:Norikuradake';
    '030227' : '0302:Ontakesan';
    '030228' : '0302:Hakusan';
    '030229' : '0302:Fujisan';
    '030230' : '0302:Hakoneyama';
    '030231' : '0302:Izu-Tobu Volcanoes';
    '030232' : '0302:Izu-Oshima';
    '030233' : '0302:Niijima';
    '030234' : '0302:Kozushima';
    '030235' : '0302:Miyakejima';
    '030236' : '0302:Hachijojima';
    '030237' : '0302:Aogashima';
    '030238' : '0302:Tsurumidake and Garandake';
    '030239' : '0302:Kujusan';
    '030240' : '0302:Asosan';
    '030241' : '0302:Unzendake';
    '030242' : '0302:Kirishimayama';
    '030243' : '0302:Sakurajima';
    '030244' : '0302:Satsuma-Iojima';
    '030245' : '0302:Kuchinoerabujima';
    '030246' : '0302:Suwanosejima';
"""

import os
import re
import sys
import time
import math
import glob
import zipfile
import subprocess
import configparser
import multiprocessing
from datetime import date, datetime, timedelta

import requests
from docopt import docopt
from clint.textui import progress

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
             '0401', '0402', '0402A',
             '0501',
             '0601',
             '0701', '0702', '0703', '0705',
             '010503', '010505', '010507', '010509',
             '010510', '010511', '010512', '010514',
             '030201', '030202', '030203', '030204', '030205',
             '030206', '030207', '030208', '030209', '030210',
             '030211', '030212', '030213', '030214', '030215',
             '030216', '030217', '030218', '030219', '030220',
             '030221', '030222', '030223', '030224', '030225',
             '030226', '030227', '030228', '030229', '030230',
             '030231', '030232', '030233', '030234', '030235',
             '030236', '030237', '030238', '030239', '030240',
             '030241', '030242', '030243', '030244', '030245',
             '030246', '030247',
             ]


def status_check(status_code):
    ''' check request status '''

    if status_code == 200:
        pass
    elif status_code == 401:
        print("Unauthorized. Check your username and password!")
        sys.exit()
    else:
        print("status code: {}".format(status_code))
        sys.exit()


def date_check(code, event):
    ''' check if waveform data are available '''

    # start date of avaiable data
    if code[0:4] == '0105':  # NIED V-net
        start = date(2010, 4, 1)
    elif code[0:4] == '0302':  # JMA Volcanic Seismometer Network
        start = date(2010, 12, 1)
    elif code[0:4] == '0705':  # Shizuoka Prefectural Government
        start = date(2004, 6, 15)
    elif code[0:4] == '0402':  # JAMSTEC DONET1
        start = date(2014, 10, 1)
    else:
        start = date(2004, 4, 1)

    today = date.today()        # end date of avaiable data
    if event.date() < start or event.date() > today:
        print("Not within Hi-net service period.")
        sys.exit()


def code_parser(code):
    ''' parser network code '''

    if code not in code_list:
        print("{}: Error code for organization and network.".format(code))
        sys.exit()

    if len(code) == 6:  # volcanos
        org, net = code[0:2], code[2:4]
        volc = code
    else:
        org, net = code[0:2], code[2:]
        volc = None

    return org, net, volc


def cont_request(org, net, volc, event, span):
    ''' request continuous data with limited time span '''

    payload = {
        'org1':  org,
        'org2':  net,
        'volc':  volc,
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


    try:
        r = requests.post(request, params=payload, auth=(user, passwd))
        status_check(r.status_code)
    except requests.exceptions.ConnectionError:
        print("Name or service not known")
        sys.exit(0)

    status_html = requests.get(status, auth=(user, passwd)).text
    id = re.search(r'<td class="bgcolist2">(?P<ID>\d{10})</td>',
                   status_html).group('ID')

    # check data status
    p = re.compile(r'<tr class="bglist(?P<OPT>\d)">'
                   + r'<td class="bgcolist2">'
                   + id
                   + r'</td>')

    while True:
        status_html = requests.get(status, auth=(user, passwd)).text
        opt = p.search(status_html).group('OPT')
        if opt == '1':  # still preparing data
            time.sleep(2)
        elif opt == '2':  # data available
            break
        elif opt == '4':  # Error
            print("Error!")
            sys.exit()
        elif opt == '3':  # ?
            print("What's bglist3?")
            sys.exit()

    return id


def cont_download_requests(id):
    ''' Download continuous waveform data of specified id '''

    try:
        d = requests.get(download, params={"id": id},
                     auth=(user, passwd), stream=True)
        status_check(d.status_code)
    except requests.exceptions.ConnectionError:
        print("Name or service not known")
        sys.exit(0)

    # file size
    total_length = int(d.headers.get('Content-Length'))
    # file name
    # disposition = d.headers['Content-Disposition'].strip()
    # fname = disposition.split('filename=')[1].strip('\'"')
    fname = "{}.zip".format(id)   # now use id as filename

    with open(fname, "wb") as fd:
        for chunk in progress.bar(d.iter_content(chunk_size=1024),
                                  label=fname,
                                  expected_size=(total_length/1024) + 1):
            if chunk:  # filter out keep-alive new chunks
                fd.write(chunk)
                fd.flush()

    if os.path.getsize(fname) != total_length:
        print("File {} is not complete!".format(fname))


def cont_download_wget(id):

    subprocess.call(["wget", '-c', '--user=' + user, '--password=' + passwd,
                     download + "?id=" + id, "-O", id + ".zip"])


def unzip(zips):
    """unzip zip filelist"""

    for file in zips:
        zipFile = zipfile.ZipFile(file, "r")
        for name in zipFile.namelist():
            zipFile.extract(name)


def win32_cat(cnts, cnt_total):
    """merge WIN32 files to one total WIN32 file"""

    subprocess.call([catwin32, '-s', '-o', cnt_total] + cnts,
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL)


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
    method = config['Tools']['downloader']

    arguments = docopt(__doc__)
    # Code for org & net
    code = config['Cont']['Net']
    if arguments['--code']:
        code = arguments['--code']
    org, net, volc = code_parser(code)

    year = int(arguments['<year>'])
    month = int(arguments['<month>'])
    day = int(arguments['<day>'])
    hour = int(arguments['<hour>'])
    minute = int(arguments['<min>'])
    timespan = int(arguments['<span>'])

    event = datetime(year, month, day, hour, minute)
    date_check(code, event)

    print("{} ~{}".format(event.strftime("%Y-%m-%d %H:%M"), timespan))

    count = math.ceil(timespan/maxspan)
    span = [timespan//count for i in range(0, count)]
    for i in range(0, timespan % count):
        span[i] += 1

    ids = []
    start = event
    for i in range(0, count):
        ids.append(cont_request(org, net, volc, start, span[i]))
        start += timedelta(minutes=span[i])
        time.sleep(2)
    zips = [x+'.zip' for x in ids]

    procs = min(len(ids), multiprocessing.cpu_count())
    if method == 'requests':
        multiprocessing.Pool(processes=procs).map(cont_download_requests, ids)
    elif method == 'wget':
        multiprocessing.Pool(processes=procs).map(cont_download_wget, ids)

    # unzip zip files
    unzip(zips)
    unlink_lists(zips)

    # get cnt and ch filename
    if not volc:
        cnts = sorted(glob.glob("????????????{}??.cnt".format(code[0:4])))
        ch_prefix = "{}_{}".format(code[0:2], code[2:4])
    else:
        cnts = sorted(glob.glob("????????????{}.cnt".format(code[0:4])))
        ch_prefix = "{}_{}_{}".format(code[0:2], code[2:4], code[4:6])

    cnt_total = "{}_{}_{}.cnt".format(code, event.strftime("%Y%m%d%H%M"), timespan)
    if arguments['--output']:
        cnt_total = arguments['--output']

    cheuc = "{}_{}.euc.ch".format(ch_prefix, event.strftime("%Y%m%d"))
    chfile = "{}_{}.ch".format(code, event.strftime("%Y%m%d"))
    if arguments['--ctable']:
        chfile = arguments['--ctable']

    if arguments['--directory']:
        dir = arguments['--directory']
        if not os.path.exists(dir):
            os.makedirs(dir)
        cnt_total = os.path.join(dir, cnt_total)
        chfile = os.path.join(dir, chfile)

    win32_cat(cnts, cnt_total)
    unlink_lists(cnts)
    os.rename(cheuc, chfile)

    unlink_lists(glob.glob("*.*.ch"))
    if os.path.exists("readme.txt"):
        os.unlink("readme.txt")
