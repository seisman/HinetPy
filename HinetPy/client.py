# -*- coding: utf-8 -*-

import os
import re
import sys
import time
import math
import logging
import zipfile
from datetime import datetime, timedelta

import requests

from HinetPy.win32 import merge
from HinetPy import __version__, __title__, __repo__
from HinetPy import header

# Setup the logger
FORMAT = "[%(asctime)s] %(levelname)s: %(message)s"
logging.basicConfig(level=logging.INFO, format=FORMAT, datefmt='%Y-%m-%d %H:%M:%S')
logger = logging.getLogger(__name__)


class Client(object):
    # Hi-net related URLs
    _HINET = 'http://www.hinet.bosai.go.jp'
    _AUTH = 'https://hinetwww11.bosai.go.jp/auth'
    _JMA = _AUTH + '/JMA/dlDialogue.php'
    _CONT = _AUTH + '/download/cont'
    _STATUS = _CONT + '/cont_status.php'
    _SELECT = _CONT + '/select_confirm.php'
    _STATION = _CONT + '/select_info.php'
    _REQUEST = _CONT + '/cont_request.php'
    _DOWNLOAD = _CONT + '/cont_download.php'
    _STATION_INFO = _HINET + '/st_info/detail/dlDialogue.php?f=CSV'
    _WIN32TOOLS = _AUTH + '/manual/dlDialogue.php?r=win32tools'

    # ETAG for v160422
    _ETAG = "16cd-537f317987000"

    def __init__(self, user=None, password=None, timeout=120, retries=3,
                 sleep_time_in_seconds=5, max_sleep_count=30):
        """Hi-net web service client.

        Parameters
        ----------
        user: str
            Username of Hi-net account.
        password: str
            Password of Hi-net account.
        timeout: int or float
            How long to wait for the server to send data before giving up.
        retries: int
            How many times to retry if request fails.
        sleep_time_in_seconds: int or float
            See notes below.
        max_sleep_count: int
            See notes below.

        Examples
        --------

        >>> from HinetPy import Client               # doctest: +SKIP
        >>> client = Client("username", "password")  # doctest: +SKIP

        Notes
        -----

        Hi-net server ususally spend 10 seconds to 1 minute on data preparation
        after receiving a data request. During the data preparation, users are
        **NOT** allowed to request another data. So users have to wait until
        the data is ready.

        HinetPy checks data status every ``sleep_time_in_seconds`` seconds
        until the data is ready. If HinetPy checks the data status for more
        than ``max_sleep_count`` times, it possibly indicates something wrong
        happend with this data. Then, HinetPy will retry to request this data
        ``retries`` times. Ususally, you don't need to modify these settings
        unless you know what you're doing.
        """
        self.timeout = timeout
        self.retries = retries
        self.sleep_time_in_seconds = sleep_time_in_seconds
        self.max_sleep_count = max_sleep_count
        if user and password:
            self.login(user, password)

    def login(self, user, password):
        """Login in Hi-net server.

        Parameters
        ----------
        user: str
            Username of Hi-net account.
        password: str
            Password of Hi-net account.

        Examples
        --------

        >>> from HinetPy import Client            # doctest: +SKIP
        >>> client = Client()                     # doctest: +SKIP
        >>> client.login("username", "password")  # doctest: +SKIP
        """
        self.user = user
        self.password = password
        self.session = requests.Session()
        auth = {
            'auth_un': self.user,
            'auth_pw': self.password,
        }
        self.session.get(self._AUTH, timeout=self.timeout)  # get cookie
        r = self.session.post(self._AUTH, data=auth, timeout=self.timeout)

        # Hi-net server return 200 even when unauthorized,
        # thus I have to check the webpage content
        inout = re.search(r'auth_log(?P<LOG>.*)\.png', r.text).group('LOG')
        if inout == 'out':
            msg = "Unauthorized. Check your username and password!"
            raise requests.ConnectionError(msg)

        logger.debug("Logging into Hi-net server.")

    def doctor(self):
        """ Doctor does some checks.

        >>> client.doctor()  # doctest: +SKIP
        [2017-01-01 00:00:00] INFO: You're using the latest release (v0.3.2).
        [2017-01-01 00:00:00] INFO: Hi-net web service is NOT updated.
        [2017-01-01 21:52:09] INFO: catwin32: /home/user/bin/catwin32.
        [2017-01-01 21:52:09] INFO: win2sac_32: /home/user/bin/win2sac_32.

        **Checklist**

        - if HinetPy has a new release (see :meth:`~HinetPy.client.Client.check_module_release`)
        - if Hi-net web service is updated (see :meth:`~HinetPy.client.Client.check_service_update`)
        - if catwin32 and win2sac_32 from win32tools in PATH (see :meth:`~HinetPy.client.Client.check_cmd_exists`)
        """
        self.check_module_release()
        self.check_service_update()
        self.check_cmd_exists()

    def _request_waveform(self, org, net, volc, starttime, span):
        '''
        Request waveform.

        Parameters
        ----------
        org: str
            Orgnization code.
        net: str
            Network code.
        volc: str
            Volcano code if avaiable.
        starttime: :py:class:`datetime.datetime`
            Starttime of data request.
        span: int
            Time span in minutes.

        Returns
        -------
        id: str
            ID of requested data. None if request fails.
        '''

        payload = {
            'org1':  org,
            'org2':  net,
            'volc':  volc,
            'year':  starttime.strftime("%Y"),
            'month': starttime.strftime("%m"),
            'day':   starttime.strftime("%d"),
            'hour':  starttime.strftime("%H"),
            'min':   starttime.strftime("%M"),
            'span':  str(span),
            'arc':   'ZIP',
            'size':  '93680',  # the actual size doesn't matter
            'LANG':  'en',
        }

        # retry if request fails else return id
        for _ in range(self.retries):
            try:
                # the timestamp determine the unique id
                payload['rn'] = str(int(datetime.now().timestamp()))
                r = self.session.post(self._REQUEST, params=payload,
                                      timeout=self.timeout)
                # assume the first one on status page is the one
                id = re.search(r'<td class="bgcolist2">(?P<ID>\d{10})</td>',
                               r.text).group('ID')
                p = re.compile(r'<tr class="bglist(?P<OPT>\d)">' +
                               r'<td class="bgcolist2">' + id + r'</td>')
                # wait until data is ready
                for _i in range(self.max_sleep_count):
                    status = self.session.post(self._STATUS, timeout=self.timeout)
                    opt = p.search(status.text).group('OPT')
                    if opt == '1':  # still preparing data
                        time.sleep(self.sleep_time_in_seconds)
                    elif opt == '2':  # data is available
                        return id
                    elif opt == '3':  # ?
                        msg = "If you see this, please report an issue on GitHub!"
                        logger.error(msg)
                        break
                    elif opt == '4':  # something wrong, retry
                        logger.error("Error in data status.")
                        break
                else:   # wait too long time
                    return None
            except Exception:
                continue
        else:
            msg = "Data request fails after {} retries".format(self.retries)
            logger.error(msg)
            msg = "Possible causes:\n" \
                    "1. max_span too large, call get_allowed_span" \
                    " and choose a proper value.\n" \
                    "2. runing two requests simultaneously."
            print(msg)
            return None

    def _download_waveform(self, id):
        '''
        Download waveform.

        Parameters
        ----------
        id: str
            Data id to be downloaded.

        Returns
        -------
        filesize: str
            Size of data file. 0 if download fails.
        '''

        for _ in range(self.retries):
            try:
                r = self.session.post(self._DOWNLOAD, data={'id': id},
                                      stream=True, timeout=self.timeout)

                total_length = int(r.headers['Content-Length'])
                fname = "{}.zip".format(id)

                with open(fname, "wb") as fd:
                    for chunk in r.iter_content(chunk_size=1024):
                        if chunk:  # filter out keep-alive new chunks
                            fd.write(chunk)
                if os.path.getsize(fname) != total_length:
                    msg = "File {} is not complete!".format(fname)
                    logger.error(msg)
                return total_length
            except Exception:
                continue
        else:
            msg = "Data download fails after {} retries".format(self.retries)
            logger.error(msg)
            return 0

    def _parse_code(self, code):
        """Parse network code.

        >>> client._parse_code('0101')
        ('01', '01', None)
        >>> client._parse_code('0103A')
        ('01', '03A', None)
        >>> client._parse_code('010501')
        ('01', '05', '010501')
        """
        if code not in header.network.keys():
            msg = "{}: Incorrect network code.".format(code)
            raise ValueError(msg)
        elif code.startswith('0105') or code.startswith('0302'):
            org, net, volc = code[0:2], code[2:4], code
        else:
            org, net, volc = code[0:2], code[2:], None

        return org, net, volc

    def get_waveform(self, code, starttime, span,
                     max_span=5, data=None, ctable=None, outdir=None):
        '''
        Get waveform from Hi-net server.

        Parameters
        ----------
        code: str
            Network code. See :meth:`~HinetPy.client.Client.help` for details.
        starttime: :py:class:`datetime.datetime`
            Starttime of data request.
        span: int
            Time span in minutes.
        max_span: int
            Maximum time span for sub-requests.
        data: str
            Filename of downloaded win32 data.
            Default format: CODE_YYYYmmddHHMM_SPAN.cnt
        ctable: str
            Filename of downloaded channel table file.
            Default format: CODE_YYYYmmdd.ch
        outdir: str
            Save win32 and channel table data to specified directory.
            Default is current directory.

        Returns
        -------
        data: str
            Filename of downloaded win32 data.
        ctable: str
            Filename of downloaded win32 data.

        Examples
        --------

        Request 10 minutes data since 2010-01-01T00:00 (GMT+0900) from Hi-net.

        >>> from datetime import datetime
        >>> starttime = datetime(2010, 1, 1, 0, 0)
        >>> client.get_waveform('0101', starttime, 10)
        ('0101_201001010000_10.cnt', '0101_20100101.ch')

        Request full-day data of 2010-01-01T00:00 (GMT+0900) of F-net:

        >>> client.get_waveform('0103', starttime, 1440, max_span=25)  # doctest: +SKIP
        ('0103_201001010000_1440.cnt', '0103_20100101.ch')

        Notes
        -----
        **TimeZone**

        All times in HinetPy are in JST (GMT+0900).

        **max_span**

        Hi-net set two limitations of each data request:

        1. Record_Length <= 60 min
        2. Number_of_channels * Record_Length <= 12000 min

        For example, Hi-net network has about 24000 channels. Acoording to
        limitation 2, the record length should be no more than 5 minutes
        in each data request. HinetPy "break" the limitation by splitting
        a long data request into several short sub-requsts.

        **Workflow**

        1. do several checks
        2. split a long request into several short sub-requests
        3. loop over all sub-requests and return data id to download
        4. download all data based on data id
        5. extract all downloaded zip files and merge into one win32 format data
        6. cleanup
        '''
        org, net, volc = self._parse_code(code)

        # 1. check starttime and endtime
        # TODO: correct starttime and endtime if not in allowed range
        time0 = header.network[code].starttime
        # time1 = UTCTime + JST(GMT+0900) - 2 hour delay
        time1 = datetime.utcnow() + timedelta(hours=9) + timedelta(hours=-2)
        endtime = starttime + timedelta(minutes=span)
        if not time0 <= starttime <= time1 or not time0 <= endtime <= time1:
            raise ValueError("Not within network service period.")

        # 2. check span:
        #    max limits is determined by the max number of data points
        #    allowed in code s4win2sacm.c
        if not isinstance(span, int):
            raise TypeError("span must be integer")
        if not 1 <= span <= (2**31 - 1)/6000:
            raise ValueError("Span is NOT in the allowed range [1, 357913]")

        # 3. check max_span
        #    Don't call self.get_allowed_span to avoid too much time cost
        if not 1 <= max_span <= 60:
            msg = "max_span not in allowed range." + \
                  "call Client.get_allowed_span() for help."
            raise ValueError(msg)

        # 4. prepare requests
        spans = split_integer(span, max_span)
        count = len(spans)
        if len(spans) > 120:
            msg = "Time span {:d} greater than allowed value".format(span)
            raise ValueError(msg)
        starttimes = [starttime]
        for i in range(1, count):
            dt = starttimes[i-1] + timedelta(minutes=spans[i-1])
            starttimes.append(dt)

        # 5. requests
        logger.info("%s ~%s", starttime.strftime("%Y-%m-%d %H:%M"), span)
        ids = []
        for i in range(count):
            logger.info("[%s/%d] => %s ~%d",
                        str(i+1).zfill(len(str(count))),
                        count,
                        starttimes[i].strftime("%Y-%m-%d %H:%M"),
                        spans[i])
            id = self._request_waveform(org, net, volc, starttimes[i], spans[i])
            ids.append(id)
        if len(ids) == 0:
            logger.error("Error in data requesting, exiting now.")
            return

        # 6. download
        for id in ids:  # check if all id is not None
            if not id:
                logger.error("Fail to request some data. Skipping downloading.")
                return None, None
        for id in ids:
            self._download_waveform(id)
        # multiprocessing.Pool(processes=3).map(self._download_waveform, ids)

        # post processes
        # 1. unzip files
        cnts, ch_euc = unzip([x + '.zip' for x in ids])

        # 2. merge all cnt files
        # TODO: sort cnts?
        if not data:
            data = "{}_{}_{:d}.cnt".format(code,
                                           starttime.strftime("%Y%m%d%H%M"),
                                           span)
        dirname = None
        if os.path.dirname(data):
            dirname = os.path.dirname(data)
        elif outdir:
            dirname = outdir
            data = os.path.join(dirname, data)
        if dirname and not os.path.exists(dirname):
            os.mkdir(dirname)
        merge(cnts, data)

        # 3. rename channeltable file
        if not ctable:
            ctable = "{}_{}.ch".format(code, starttime.strftime("%Y%m%d"))

        dirname = None
        if os.path.dirname(ctable):
            dirname = os.path.dirname(ctable)
        elif outdir:
            dirname = outdir
            ctable = os.path.join(dirname, ctable)
        if dirname and not os.path.exists(dirname):
            os.mkdir(dirname)
        os.rename(ch_euc, ctable)

        # 4. cleanup
        for cnt in cnts:
            os.unlink(cnt)

        return data, ctable

    def _get_catalog(self, datatype, startdate, span, filename=None, os="DOS"):
        """Request JMA catalog."""

        if int(span) not in range(1, 8):
            raise ValueError("span is not digit or not in [1, 7].")

        params = {
            'data': datatype,
            'rtm': startdate.strftime("%Y%m%d"),
            'span': span,
            'os': os[0],
        }
        d = self.session.post(self._JMA, params=params, stream=True)
        if not filename:
            filename = "{}_{}_{}.txt".format(datatype, startdate.strftime("%Y%m%d"), span)
        with open(filename, "wb") as fd:
            for chunk in d.iter_content(chunk_size=1024):
                if chunk:  # filter out keep-alive new chunks
                    fd.write(chunk)
        return filename

    def get_arrivaltime(self, startdate, span, filename=None, os="DOS"):
        """Get JMA arrival time data from Hi-net.

        Parameters
        ----------
        startdate: :py:class:`datetime.date`
            Start date to request.
        span: int
            Data length in days.
        os: str
            File format. "DOS" or "UNIX".
        filename: str
            Filename to save.

        Returns
        -------
        filename: str
            Filename saved.

        Examples
        --------

        >>> from datetime import date
        >>> startdate = date(2010, 1, 1)
        >>> client.get_arrivaltime(startdate, 5)
        'measure_20100101_5.txt'
        >>> client.get_arrivaltime(startdate, 5, filename="arrivaltime.txt")
        'arrivaltime.txt'
        """
        return self._get_catalog("measure", startdate, span, filename, os)

    def get_focalmechanism(self, startdate, span, filename=None, os="DOS"):
        """Get JMA focal mechanism data from Hi-net.

        Parameters
        ----------
        startdate: :py:class:`datetime.date`
            Start date to request.
        span: int
            Data length in days.
        os: str
            File format. "DOS" or "UNIX".
        filename: str
            Filename to save.

        Returns
        -------
        filename: str
            Filename saved.

        Examples
        --------
        >>> from datetime import date
        >>> startdate = date(2010, 1, 1)
        >>> client.get_focalmechanism(startdate, 5)
        'focal_20100101_5.txt'
        >>> client.get_focalmechanism(startdate, 5, filename="focalmechanism.txt")
        'focalmechanism.txt'
        """
        return self._get_catalog("focal", startdate, span, filename, os)

    def get_station_list(self, code=None):
        """Get a station list of Hi-net and F-net.

        >>> client.get_station_list()  # doctest: +ELLIPSIS
        network station longtitude latitude
        0101 N.WNNH 141.8850 45.4883
        0101 N.SFNH 142.1185 45.3346
        ...
        """
        # no need to login
        r = requests.get(self._STATION_INFO)
        lines = r.iter_lines()
        next(lines)  # skip csv header
        print("network station longtitude latitude")
        for line in lines:
            items = line.decode('shift_jis').split(",")
            network = "{}{}".format(items[0].strip("'"), items[1].strip("'"))
            station = items[2]
            latitude, longtitude = items[7], items[8]
            if not code or network == code:
                print(network, station, longtitude, latitude)

    def get_allowed_span(self, code):
        """Get allowed max span for each network.

        Hi-net set a limitation of data file size:

        #. Number_of_channels * record_length(min.) <= 12000 min
        #. record_length <= 60min

        >>> client.get_allowed_span('0201')
        60

        Parameters
        ----------
        code: str
            Network code.

        Returns
        -------
        max_span: int
            Maximum allowed span in mimutes.
        """
        channels = header.network[code].channels
        if code in ('0101', '0103', '0103A'):
            stations = self.get_selected_stations(code)
            if stations != 0:
                channels = stations * 3
        return min(int(12000/channels), 60)

    def get_selected_stations(self, code):
        """Query numbers of Hi-net/F-net stations selected for requesting data.

        Parameters
        ----------
        code: str
            Network code.

        Returns
        -------
        no_of_stations: int
            Number of selected stations.
        """

        if code == '0101':
            pattern = r'<td class="td1">(?P<CHN>N\..{3}H)<\/td>'
        elif code in ('0103', '0103A'):
            pattern = r'<td class="td1">(?P<CHN>N\..{3}F)<\/td>'
        else:
            raise ValueError("Can only query stations of Hi-net/F-net")

        r = self.session.get(self._STATION, timeout=self.timeout)
        counts = len(re.findall(pattern, r.text))
        return counts

    def select_stations(self, code, stations=None):
        """Select Hi-net/F-net stations

        Parameters
        ----------
        code: str
            Network code.
        stations: str or list
            Stations to select.

        Examples
        --------
        Select only two stations:

        >>> client.select_stations('0101', ['N.AAKH', 'N.ABNH'])
        >>> client.get_selected_stations('0101')
        2

        Select all Hi-net stations:

        >>> client.select_stations('0101')
        >>> client.get_selected_stations('0101')
        0

        """

        if stations:
            stcds = ':'.join(stations)
        else:
            stcds = None

        payload = {
            'net': code,
            'stcds': stcds,
            'mode': '1',
        }
        self.session.post(self._SELECT, data=payload, timeout=self.timeout)

    def check_service_update(self):
        """Check if Hi-net service is updated.

        >>> client.check_service_update()  # doctest: +SKIP
        [2017-01-01 00:00:00] INFO: Hi-net web service is NOT updated.
        """
        r = self.session.get(self._CONT + '/js/cont.js')

        if r.headers['ETag'].strip('"') == self._ETAG:
            logger.info("Hi-net web service is NOT updated.")
            return False
        else:
            logger.warning("Hi-net web service is updated."
                           "This module may FAIL!")
            return True

    def check_module_release(self):
        """Check whether this module has a new release.

        >>> client.check_module_release()  # doctest: +SKIP
        [2017-01-01 00:00:00] INFO: You're using the latest release (v0.3.2).
        """
        import json
        from distutils.version import StrictVersion

        url = 'https://api.github.com/repos/seisman/HinetPy/releases/latest'
        r = requests.get(url)
        latest_release = json.loads(r.text)['tag_name']

        if StrictVersion(latest_release) > StrictVersion(__version__):
            msg = '{} v{} is released. See {} for details.'.format(__title__, latest_release, __repo__)
            logger.warning(msg)
            return True
        else:
            logger.info("You're using the latest release (v%s)." % __version__)
            return False

    def check_cmd_exists(self):
        """Check if ``catwin32`` and ``win2sac_32`` from win32tools in PATH.

        >>> client.check_cmd_exists()  # doctest: +SKIP
        [2017-01-01 00:00:00] INFO: catwin32: /home/user/bin/catwin32.
        [2017-01-01 00:00:00] INFO: win2sac_32: /home/user/bin/win2sac_32.

        The client will report errors if ``catwin32`` and/or ``win2sac_32``
        are NOT in PATH. In this case, please download win32tools from Hi-net_
        and make sure both binary files are in your PATH.

        .. _Hi-net: http://www.hinet.bosai.go.jp/
        """
        import shutil

        catwin32 = shutil.which('catwin32')
        if catwin32:
            logger.info("catwin32: %s.", catwin32)
        else:
            logger.error("catwin32 not found in PATH.")

        win2sac_32 = shutil.which('win2sac_32')
        if win2sac_32:
            logger.info("win2sac_32: %s.", win2sac_32)
        else:
            logger.error("win2sac_32 not found in PATH.")

        return True if catwin32 and win2sac_32 else False

    def help(self, code=None):
        """List information of networks.

        >>> client.help()  # doctest: +ELLIPSIS
        0101   : NIED Hi-net
        0103   : NIED F-net (broadband)
        0103A  : NIED F-net (strong motion)
        010501 : NIED V-net (Tokachidake)
        ...
        0703   : Aomori Prefectural Government
        0705   : Shizuoka Prefectural Government
        0801   : ADEP
        >>> client.help('0101')
        == Information of Network 0101 ==
        Name: NIED Hi-net
        Starttime: 20040401
        No. of channels: 2336

        Parameters
        ----------

        code: None or str
            Network code.
        """
        if code:
            net = header.network[code]
            string = "== Information of Network {} ==\n".format(code)
            string += "Name: {}\n".format(net.name)
            string += "Starttime: {}\n".format(net.starttime.strftime("%Y%m%d"))
            string += "No. of channels: {}".format(net.channels)
            print(string)
        else:
            for code in sorted(header.network.keys()):
                print("{:7s}: {}".format(code, header.network[code].name))

    def _get_win32tools(self):
        """Download win32 tools"""
        d = self.session.get(self._WIN32TOOLS, stream=True)
        with open("win32tools.tar.gz", "wb") as fd:
            for chunk in d.iter_content(chunk_size=1024):
                if chunk:  # filter out keep-alive new chunks
                    fd.write(chunk)
        return "win32tools.tar.gz"

    def __str__(self):
        string = "<== Hi-net web service client ==>\n"
        string += "{:22s}: {}\n".format("url", self._HINET)
        for key in ("user", "password", "timeout", "retries", "debug",
                    "max_sleep_count", "sleep_time_in_seconds"):
            try:
                value = getattr(self, key)
                if key == "password":
                    value = "*" * len(value)
                string += "{:22s}: {}\n".format(key, value)
            except Exception:
                continue
        return string


def unzip(zips):
    """Unzip .cnt and .euc.ch from zipfiles."""

    win32_filelist = []
    channel_table = ''
    for file in zips:
        with zipfile.ZipFile(file, 'r') as zipFile:
            for filename in zipFile.namelist():
                if filename.endswith(".cnt"):
                    zipFile.extract(filename)
                    win32_filelist.append(filename)
                elif not channel_table and filename.endswith(".euc.ch"):
                    zipFile.extract(filename)
                    channel_table = filename

        os.unlink(file)

    return win32_filelist, channel_table


def split_integer(m, n):
    '''
    Split an integer into evenly sized chunks

    >>> split_integer(12, 3)
    [3, 3, 3, 3]
    >>> split_integer(15, 4)
    [4, 4, 4, 3]
    '''
    count = math.ceil(m / n)
    chunks = [m//count for i in range(count)]
    for i in range(m % count):
        chunks[i] += 1
    return chunks

if __name__ == '__main__':
    import doctest
    client = Client("username", "password")
    doctest.testmod()
