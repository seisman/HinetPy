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
#   2014-12-03  Dongdong Tian   Hi-net website updated on Dec. 1st, 2014.
#                               Skip SSL verification.
#                               Use post method for SSL authentication.
#   2014-12-05  Dongdong Tian   Add -m option to specify maxspan.
#   2014-12-27  Dongdong Tian   Fix bugs caused by update on Dec. 1st, 2014
#   2015-01-08  Dongdong Tian   Naming cnt file with start time not end time.
#   2015-02-25  Dongdong Tian   Add data download service for ADEP (code=0801).
#   2015-06-27  Dongdong Tian   Move URLs to configure file
#

"""Request continuous waveform data from NIED Hi-net.

Usage:
    HinetContRequest.py <year> <month> <day> <hour> <min> <span> [options]
    HinetContRequest.py -h

Options:
    -h, --help              Show this help.
    -c CODE --code=CODE     Select code for organization and network.
    -m SPAN --maxspan=SPAN  Max time span for sub-requests
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
    '0801' : 'OTHER:ADEP',

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
import logging
import zipfile
import subprocess
import configparser
import multiprocessing
from datetime import date, datetime, timedelta

import requests
from docopt import docopt
from clint.textui import progress

# external tools from Hi-net
catwin32 = "catwin32"


# all legal codes
CODE_LIST = ['0101', '0103', '0103A',
             '0201', '0202', '0203', '0204', '0205',
             '0206', '0207', '0208', '0209',
             '0301',
             '0401', '0402', '0402A',
             '0501',
             '0601',
             '0701', '0702', '0703', '0705',
             '0801',
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


def check_date(code, event):
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
    elif code[0:4] == '0801':  # ADEP
        start = date(2015, 1, 1)
    else:
        start = date(2004, 4, 1)

    if not start <= event.date() <= date.today():
        logging.error("Not within service period.")
        sys.exit()


def parse_code(code):
    ''' parser network code '''

    if code not in CODE_LIST:
        logging.error("{}: Error code for org and net.".format(code))
        sys.exit()
    elif len(code) == 6:  # volcanos
        org, net = code[0:2], code[2:4]
        volc = code
    else:
        org, net = code[0:2], code[2:]
        volc = None

    return org, net, volc


def parse_event(args):
    ''' extract datetime information from arguments'''

    year = int(args['<year>'])
    month = int(args['<month>'])
    day = int(args['<day>'])
    hour = int(args['<hour>'])
    minute = int(args['<min>'])

    return datetime(year, month, day, hour, minute)


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
        'arc':   'ZIP',      # zip format is preferred
        'size':  '93680',    # estimated size of the data, it is not important
        'LANG':  'en',       # english version of web
        'rn': str(int((datetime.now() - datetime(1970, 1, 1)).total_seconds()))
    }

    try:
        r = s.post(REQUEST, params=payload)
    except requests.exceptions.ConnectionError:
        logging.error("Name or service not known")
        sys.exit()

    # assume the first one is the right one
    id = re.search(r'<td class="bgcolist2">(?P<ID>\d{10})</td>',
                   r.text).group('ID')

    p = re.compile(r'<tr class="bglist(?P<OPT>\d)">' +
                   r'<td class="bgcolist2">' + id + r'</td>')

    while True:  # check data status
        try:
            status_html = s.post(STATUS).text
        except requests.exceptions.ConnectionError:
            logging.error("Error in fetch status")
            sys.exit()

        opt = p.search(status_html).group('OPT')
        if opt == '1':  # still preparing data
            time.sleep(2)
        elif opt == '2':  # data available
            return id
        elif opt == '4':  # Error
            logging.error("Error in data status.")
            sys.exit()
        elif opt == '3':  # ?
            logging.error("What's bglist3?")
            sys.exit()


def cont_download(id):
    ''' Download continuous waveform data of specified id '''

    try:
        dn = requests.Session()
        dn.post(AUTH, verify=False)
        dn.post(AUTH, data=auth)
        d = dn.post(DOWNLOAD, params={"id": id}, stream=True)
    except requests.exceptions.ConnectionError:
        logging.error("Name or service not known")
        sys.exit()

    # file size
    total_length = int(d.headers.get('Content-Length'))
    # file name
    fname = "{}.zip".format(id)   # now use id as filename

    with open(fname, "wb") as fd:
        for chunk in progress.bar(d.iter_content(chunk_size=1024),
                                  label=fname,
                                  expected_size=(total_length/1024) + 1):
            if chunk:  # filter out keep-alive new chunks
                fd.write(chunk)
                fd.flush()

    if os.path.getsize(fname) != total_length:
        logging.error("File {} is not complete!".format(fname))
        sys.exit()


def unzip(zips):
    """unzip zip filelist"""

    for file in zips:
        with zipfile.ZipFile(file, 'r') as zipFile:
            zipFile.extractall()


def cat_win32(cnts, cnt_total):
    """merge WIN32 files to one total WIN32 file"""

    subprocess.call([catwin32, '-o', cnt_total] + cnts,
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL)


def unlink_lists(files):
    for f in files:
        os.unlink(f)


def evenly_timespan(timespan, maxspan):
    count = math.ceil(timespan/maxspan)
    span = [timespan//count for i in range(0, count)]
    for i in range(0, timespan % count):
        span[i] += 1

    return span


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s %(levelname)-7s %(message)s',
                        datefmt='%H:%M:%S')
    logging.getLogger("requests").setLevel(logging.WARNING)
    requests.packages.urllib3.disable_warnings()

    config = configparser.ConfigParser()
    if not config.read("Hinet.cfg"):
        logging.error("Configure file `Hinet.cfg' not found.")
        sys.exit()
    arguments = docopt(__doc__)

    # basic urls
    AUTH = config['URL']['AUTH']
    CONT = config['URL']['CONT']
    STATUS = config['URL']['STATUS']
    REQUEST = config['URL']['REQUEST']
    DOWNLOAD = config['URL']['DOWNLOAD']

    # global variables
    auth = {
        'auth_un': config['Account']['User'],
        'auth_pw': config['Account']['Password'],
        }
    s = requests.Session()
    s.post(AUTH, verify=False)  # get cookies
    s.post(AUTH, data=auth)  # login

    # Code for org & net
    code = config['Cont']['Net']
    if arguments['--code']:
        code = arguments['--code']
    org, net, volc = parse_code(code)

    # parser arguments
    event = parse_event(arguments)
    check_date(code, event)

    # timespan
    timespan = int(arguments['<span>'])
    if not 1 <= timespan <= (2**31-1)/100:
        logging.error("timespan is not in the range[1,(2^32-1)/100]")
        sys.exit()

    maxspan = int(config['Cont']['MaxSpan'])
    if arguments['--maxspan']:
        maxspan = int(arguments['--maxspan'])
    if not 1 <= maxspan <= 60:
        logging.error("maxspan is not in the range[1,60]")
        sys.exit()

    span = evenly_timespan(timespan, maxspan)
    count = len(span)
    if count > 140:
        logging.error("Too long time duration for one request.")
        sys.exit()

    logging.info("%s ~%s", event.strftime("%Y-%m-%d %H:%M"), timespan)

    # set cnt_total
    cnt_total = "{}_{}_{}.cnt".format(code,
                                      event.strftime("%Y%m%d%H%M"),
                                      timespan)

    ids = []
    count_len = len(str(count))
    for i in range(0, count):
        logging.info("[%s/%s] => %s ~%s",
                     str(i+1).zfill(count_len),
                     str(count).zfill(count_len),
                     event.strftime("%Y-%m-%d %H:%M"),
                     span[i]
                     )
        ids.append(cont_request(org, net, volc, event, span[i]))
        event += timedelta(minutes=span[i])

    procs = min(len(ids), multiprocessing.cpu_count())
    multiprocessing.Pool(processes=procs).map(cont_download, ids)

    # unzip zip files
    zips = [x+'.zip' for x in ids]
    unzip(zips)
    unlink_lists(zips)

    outdir = os.getcwd()  # use current directory as default
    if arguments['--directory']:
        outdir = arguments['--directory']
        if not os.path.exists(outdir):
            os.makedirs(outdir)

    if arguments['--output']:
        cnt_total = arguments['--output']
    cnt_total = os.path.join(outdir, cnt_total)

    if not volc:
        cnts = sorted(glob.glob("????????????{}??.cnt".format(code[0:4])))
    else:
        cnts = sorted(glob.glob("????????????{}.cnt".format(code[0:4])))
    cat_win32(cnts, cnt_total)

    # set channel table file
    if not volc:
        ch_prefix = "{}_{}".format(code[0:2], code[2:4])
    else:
        ch_prefix = "{}_{}_{}".format(code[0:2], code[2:4], code[4:6])
    cheuc = "{}_{}.euc.ch".format(ch_prefix, event.strftime("%Y%m%d"))

    chfile = "{}_{}.ch".format(code, event.strftime("%Y%m%d"))
    if arguments['--ctable']:
        chfile = arguments['--ctable']
    chfile = os.path.join(outdir, chfile)

    eucs = glob.glob("*.euc.ch")
    eucs.remove(cheuc)
    os.rename(cheuc, chfile)

    unlink_lists(cnts)
    unlink_lists(eucs)
    unlink_lists(glob.glob("*.sjis.ch"))
    if os.path.exists("readme.txt"):
        os.unlink("readme.txt")
