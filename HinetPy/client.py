# -*- coding: utf-8 -*-

import os
import re
import time
import math
import logging
import tempfile
import zipfile
from datetime import datetime, date, timedelta
from multiprocessing.pool import ThreadPool

import requests

from .win32 import merge
from .header import NETWORK
from .utils import point_inside_box, point_inside_circular, split_integer, \
        string2datetime

# Setup the logger
FORMAT = "[%(asctime)s] %(levelname)s: %(message)s"
logging.basicConfig(level=logging.INFO,
                    format=FORMAT,
                    datefmt='%Y-%m-%d %H:%M:%S')
logger = logging.getLogger(__name__)


class Client():
    # Hinet website
    _HINET = 'http://www.hinet.bosai.go.jp/'
    # Authorization page
    _AUTH = 'https://hinetwww11.bosai.go.jp/auth/'
    # Download win32tools
    _WIN32TOOLS = _AUTH + 'manual/dlDialogue.php?r=win32tools'

    # Catalog
    _JMA = _AUTH + 'JMA/dlDialogue.php'

    # Continuous wavefroms
    _CONT = _AUTH + 'download/cont/'
    _CONT_STATUS = _CONT + 'cont_status.php'
    _CONT_REQUEST = _CONT + 'cont_request.php'
    _CONT_DOWNLOAD = _CONT + 'cont_download.php'

    # Station information
    _STATION_INFO = _HINET + 'st_info/detail/dlDialogue.php?f=CSV'
    _CONT_SELECT = _CONT + 'select_confirm.php'
    _STATION = _CONT + 'select_info.php'
    _MESONET_STATION_INFO = _CONT + 'st_mesonet_json.php'
    _SNET_STATION_INFO = _CONT + 'st_snet_json.php'

    # Event waveforms
    _EVENT = _AUTH + 'download/event/'
    _EVENT_STATUS = _EVENT + 'event_status.php'
    _EVENT_REQUEST = _EVENT + 'event_request.php'
    _EVENT_DOWNLOAD = _EVENT + 'event_download.php'

    # ETAG for v160422
    _ETAG = "1b61-5774e12e97f00"

    def __init__(self, user=None, password=None, timeout=60, retries=3,
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

        Notes
        -----
        Hi-net server ususally spends 10 seconds to 1 minute on data
        preparation after receiving a data request. During the data
        preparation, users are **NOT** allowed to post another data request.
        So users have to wait until the data is ready.

        HinetPy checks data status every ``sleep_time_in_seconds`` seconds
        until the data is ready. If HinetPy checks the data status for more
        than ``max_sleep_count * sleep_time_in_seconds`` seconds,
        it possibly indicates something wrong happend with this data request.
        Then, HinetPy will retry to request this data ``retries`` times.
        Ususally, you don't need to modify these settings
        unless you know what you're doing.

        Examples
        --------

        >>> from HinetPy import Client
        >>> client = Client("username", "password")
        """
        self.timeout = timeout
        self.retries = retries
        self.sleep_time_in_seconds = sleep_time_in_seconds
        self.max_sleep_count = max_sleep_count
        if user and password:
            self.login(user, password)
        # variables for internal use
        self._code = None
        self._max_span = 0

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

        >>> from HinetPy import Client
        >>> client = Client()
        >>> client.login("username", "password")
        """
        self.user = user
        # Hinet automatically trims password with >12 characters
        if len(password) > 12:
            logger.warning("Password with more than 12 characters may FAIL!")
        self.password = password[0:12]
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

    def doctor(self):
        """ Doctor does some checks.

        >>> client.doctor()
        [2019-02-19 00:00:00] INFO: You're using the latest release (v0.6.0).
        [2019-02-19 00:00:00] INFO: Hi-net web service is NOT updated.
        [2019-02-19 00:00:00] INFO: catwin32: /home/user/bin/catwin32.
        [2019-02-19 00:00:00] INFO: win2sac_32: /home/user/bin/win2sac_32.

        **Checklist**

        - if HinetPy has a new release
          (see :meth:`~HinetPy.client.Client.check_package_release`)
        - if Hi-net web service is updated
          (see :meth:`~HinetPy.client.Client.check_service_update`)
        - if ``catwin32`` and ``win2sac_32`` from win32tools are in PATH
          (see :meth:`~HinetPy.client.Client.check_cmd_exists`)
        """
        self.check_package_release()
        self.check_service_update()
        self.check_cmd_exists()

    ###########################################################################
    #                                                                         #
    # Methods for requesting continuous waveforms.                            #
    #                                                                         #
    ###########################################################################
    def _request_cont_waveform(self, code, starttime, span):
        '''
        Request continuous waveform.

        Parameters
        ----------
        code: str
            Network code.
        starttime: :py:class:`datetime.datetime`
            Starttime of data request.
        span: int
            Time span in minutes.

        Returns
        -------
        id: str
            ID of requested data. None if request fails.
        '''
        org, net, volc = _parse_code(code)
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
                r = self.session.post(self._CONT_REQUEST, params=payload,
                                      timeout=self.timeout)
                # assume the first one on status page is the one
                id = re.search(r'<td class="bgcolist2">(?P<ID>\d{10})</td>',
                               r.text).group('ID')
                p = re.compile(r'<tr class="bglist(?P<OPT>\d)">' +
                               r'<td class="bgcolist2">' + id + r'</td>')
                # wait until data is ready
                for _i in range(self.max_sleep_count):
                    status = self.session.post(self._CONT_STATUS,
                                               timeout=self.timeout)
                    opt = p.search(status.text).group('OPT')
                    if opt == '1':  # still preparing data
                        time.sleep(self.sleep_time_in_seconds)
                    elif opt == '2':  # data is available
                        return id
                    elif opt == '3':  # ?
                        msg = "If you see this, " \
                              "please report an issue on GitHub!"
                        logger.error(msg)
                        break  # break to else clause
                    elif opt == '4':  # something wrong, retry
                        logger.error("Error in data status.")
                        break  # break to else clause
                else:   # wait too long time
                    return None
            except Exception:
                continue
        else:
            msg = "Data request fails after {} retries.".format(self.retries)
            logger.error(msg)
            return None

    def _download_cont_waveform(self, job):
        '''
        Download continuous waveform.

        Parameters
        ----------
        id: str
            Data id to be downloaded.

        Returns
        -------
        cnts: list of str
            Filename of one-minute win32 data.
        ctable: str
            Filename of channle table.
        '''
        # session cannot be shared between threads, so always initialize
        # a new client for downloading.
        # Maybe there is other trick way?
        dlclient = Client(self.user, self.password)
        for _ in range(self.retries):
            try:
                r = dlclient.session.post(self._CONT_DOWNLOAD, data={'id': job.id},
                                          stream=True, timeout=self.timeout)

                with tempfile.NamedTemporaryFile() as ft:
                    # save to temporary file
                    for chunk in r.iter_content(chunk_size=1024):
                        if chunk:  # filter out keep-alive new chunks
                            ft.write(chunk)
                    ft.flush()

                    # unzip temporary file
                    cnts = []
                    ctable = None
                    with zipfile.ZipFile(ft.name) as fz:
                        for filename in fz.namelist():
                            if filename.endswith(".cnt"):
                                cnts.append(filename)
                            elif filename.endswith(".euc.ch"):
                                ctable = filename
                        fz.extractall(members=cnts+[ctable])
                    return cnts, ctable
            except Exception:
                continue
        else:
            msg = "Data download fails after {} retries".format(self.retries)
            logger.error(msg)
            return None, None

    def get_continuous_waveform(self, code, starttime, span,
                                max_span=None, data=None, ctable=None,
                                outdir=None, threads=3, cleanup=True):
        '''
        Get continuous waveform from Hi-net server.

        Parameters
        ----------
        code: str
            Network code. See :meth:`~HinetPy.client.Client.info` for details.
        starttime: :py:class:`datetime.datetime` or str
            Starttime of data request.
        span: int
            Time span in minutes.
        max_span: int
            Maximum time span for sub-requests. Defaults to be determined
            automatically.
        data: str
            Filename of downloaded win32 data.
            Default format: CODE_YYYYmmddHHMM_SPAN.cnt
        ctable: str
            Filename of downloaded channel table file.
            Default format: CODE_YYYYmmdd.ch
        outdir: str
            Save win32 and channel table data to specified directory.
            Default is current directory.
        threads: int
            How many threads used to speedup data downloading.
        cleanup: bool
            Clean up one-minute cnt files after merging.

        Returns
        -------
        data: str
            Filename of downloaded win32 data.
        ctable: str
            Filename of downloaded channel table file.

        Notes
        -----
        **TimeZone**

        All times in HinetPy are in JST (GMT+0900).

        **max_span**

        Hi-net server sets three limitations of each data request:

        1. Record_Length <= 60 min
        2. Number_of_channels * Record_Length <= 12000 min
        3. Only the latest 150 requested data are kept

        For example, Hi-net network has about 24000 channels. Acoording to
        limitation 2, the record length should be no more than 5 minutes
        in each data request. HinetPy "break through" the limitation by
        splitting a long-duration data request into several short-duration
        sub-requsts.

        **Workflow**

        1. do several checks
        2. split a long-duration request into several short-duration sub-requests
        3. loop over all sub-requests and return data id to download
        4. download all data based on data id
        5. extract all zip files and merge into one win32 format data
        6. cleanup

        Examples
        --------
        Request 6 minutes data since 2010-01-01T05:35 (GMT+0900) from Hi-net.

        >>> client.get_continuous_waveform('0101', '201001010535', 6)
        ('0101_201001010535_6.cnt', '0101_20100101.ch')

        Several other string formats of ``starttime`` are also supported:

        >>> client.get_continuous_waveform('0101', '2010-01-01 05:35', 6)
        >>> client.get_continuous_waveform('0101', '2010-01-01T05:35', 6)

        ``starttime`` can be given as :py:class:`datetime.datetime`:

        >>> from datetime import datetime
        >>> starttime = datetime(2010, 1, 1, 5, 35)
        >>> client.get_continuous_waveform('0101', starttime, 6)
        ('0101_201001010535_6.cnt', '0101_20100101.ch')

        Request full-day data of 2010-01-01T00:00 (GMT+0900) of F-net:

        >>> client.get_continuous_waveform('0103', starttime, 1440, max_span=25)
        ('0103_201001010000_1440.cnt', '0103_20100101.ch')

        '''
        # 1. check span:
        #    max limits is determined by the max number of data points
        #    allowed in code s4win2sacm.c
        if not isinstance(span, int):
            raise TypeError("span must be integer.")
        if not 1 <= span <= (2**31 - 1)/6000:
            raise ValueError("Span is NOT in the allowed range [1, 357913]")

        # 2. check starttime and endtime
        if code not in NETWORK.keys():
            raise ValueError("{}: Incorrect network code.".format(code))

        time0 = NETWORK[code].starttime
        # time1 = UTCTime + JST(GMT+0900) - 2 hour delay
        time1 = datetime.utcnow() + timedelta(hours=9) + timedelta(hours=-2)
        if not isinstance(starttime, datetime):
            starttime = string2datetime(starttime)
        endtime = starttime + timedelta(minutes=span)
        if not time0 <= starttime < endtime <= time1:
            msg = "Data not available in the time period. " + \
                  "Call Client.info('{}') for help.".format(code)
            raise ValueError(msg)

        # 3. set max_span
        if self._code != code:  # update default max_span
            self._code = code
            self._max_span = self._get_allowed_span(code)
        if not (max_span and 1 <= max_span <= 60):
            max_span = self._max_span

        # 4. prepare jobs
        jobs = prepare_jobs(starttime, span, max_span)

        cnts = []
        ch_euc = set()
        logger.info("%s ~%s", starttime.strftime("%Y-%m-%d %H:%M"), span)
        # 5. request and download
        count = len(jobs)
        for j in range(0, count, 100):  # to break the limitation of 150
            # 5.1. request <=100 data
            for i in range(j, min(j+100, count)):
                logger.info("[%s/%d] => %s ~%d",
                            str(i+1).zfill(len(str(count))),
                            count,
                            jobs[i].starttime.strftime("%Y-%m-%d %H:%M"),
                            jobs[i].span)
                jobs[i].id = self._request_cont_waveform(code, jobs[i].starttime,
                                                         jobs[i].span)

            # 5.2. check ids
            if not [job.id for job in jobs]:
                logger.error("No data requested succesuflly. Skipped.")
                return None, None
            # check if all ids are not None
            if not all([job.id for job in jobs]):
                logger.error("Fail to request some data. Skipped.")
                return None, None

            # 5.3. parallel downloading
            with ThreadPool(min(threads, len(jobs))) as p:
                rvalue = p.map(self._download_cont_waveform, jobs)
            for value in rvalue:
                cnts.extend(value[0])
                ch_euc.add(value[1])

        # post processes
        # 1. always sort cnts by name/time to avoid use -s option of catwin32
        cnts = sorted(cnts)
        #    always use the first ctable
        ch_euc = list(sorted(ch_euc))[0]

        # 2. merge all cnt files
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
            os.makedirs(dirname, exist_ok=True)
        os.rename(ch_euc, ctable)

        # 4. cleanup
        if cleanup:
            for cnt in cnts:
                os.remove(cnt)

        return data, ctable

    def get_waveform(self, code, starttime, span,
                     max_span=None, data=None, ctable=None,
                     outdir=None, threads=3, cleanup=True):
        """
        .. versionchanged:: 0.6.0

            Deprecated.

            :meth:`~HinetPy.client.Client.get_waveform` has been renamed to
            :meth:`~HinetPy.client.Client.get_continuous_waveform`.
        """
        logger.warn("The get_waveform() function is deprecated. Please "
                    "use get_continuous_waveform().")
        return self.get_continuous_waveform(code, starttime, span,
                                            max_span=max_span, data=data,
                                            ctable=ctable, outdir=outdir,
                                            threads=threads, cleanup=cleanup)

    ###########################################################################
    #                                                                         #
    # Methods for requesting event waveforms.                                 #
    #                                                                         #
    ###########################################################################
    def _search_event_by_day(self, year, month, day, region="00",
                             magmin=3.0, magmax=9.9,
                             include_unknown_mag=True):
        '''
        Search events catalog of one day.

        Parameters
        ----------

        region : str
            Limit events in specified region. Allowed values are:

            - ``00``: Whole Japan
            - ``01``: Hokkaido Region
            - ``02``: Tohoku Region
            - ``03``: Kanto Region
            - ``04``: Chubu Region
            - ``05``: Kinki Region
            - ``06``: Chugoku/Shikoku Region
            - ``07``: Kyushu Region
            - ``08``: Others

        include_unknown_mag: bool
            Include/exclude undetermined magnitude events.
        '''
        payload = {
            'year': year,
            'month': "{:02d}".format(month),
            'day': "{:02d}".format(day),
            'region': region,
            'mags': magmin,
            'mage': magmax,
            'undet': 0 if include_unknown_mag else 1,
            'sort': 0,  # always sort by origin time in ascending order
            'arc': 'ZIP',  # meaningless arguement in this request
            'go': 1,
            'LANG': 'en'
        }
        r = self.session.post(self._EVENT, data=payload, timeout=self.timeout)
        events = []
        for result in re.findall("openRequest\((.+)\)", r.text):
            items = [item.strip("'") for item in result.split(',')]
            events.append(Event(items[0], *items[3:10]))
        return events

    def _request_event_waveform(self, event, format="ZIP"):
        '''
        Request event waveform.

        Parameters
        ----------

        event: HinetPy.client.Event
            Event to be requested.
        format: str
            Format of requested waveform package.
        '''
        payload = {
            'evid': event.evid,
            'origin_jst': event.origin,
            'hypo_latitude': event.latitude,
            'hypo_logitude': event.longitude,  # logitude is Hinet's typo
            'hypo_depth': event.depth,
            'mg': '' if event.magnitude == '#' else event.magnitude,
            'hypo_name': event.name,
            'hypo_name_eng': event.name_en,
            'arc': format,
            'encoding': 'D',
            'lang': 'en',
            'rn': str(int(datetime.now().timestamp())),
        }

        # retry if request fails else return id
        for _ in range(self.retries):
            try:
                r = self.session.post(self._EVENT_REQUEST, data=payload, timeout=self.timeout)
                # assume the first one on status page is the one
                id = re.search(r'<td class="bgevlist2">(?P<ID>\d{10})</td>',
                               r.text).group('ID')
                p = re.compile(r'<tr class="bglist(?P<OPT>\d)">' +
                               r'<td class="bgevlist2">' + id + r'</td>')
                # wait until data is ready
                for _i in range(self.max_sleep_count):
                    status = self.session.post(self._EVENT_STATUS,
                                               timeout=self.timeout)
                    opt = p.search(status.text).group('OPT')
                    if opt == '1':  # still preparing data
                        time.sleep(self.sleep_time_in_seconds)
                    elif opt == '2':  # data is available
                        return id
                    elif opt == '3':  # ?
                        msg = "If you see this, " \
                              "please report an issue on GitHub!"
                        logger.error(msg)
                        break  # break to else clause
                    elif opt == '4':  # something wrong, retry
                        logger.error("Error in data status.")
                        break  # break to else clause
                else:   # wait too long time
                    return None
            except Exception:
                continue
        else:
            msg = "Data request fails after {} retries.".format(self.retries)
            logger.error(msg)
            return None

    def _download_event_waveform(self, id):
        '''
        Download event waveform.

        Parameters
        ----------
        id: str
            Request ID.
        '''

        payload = {
            'id': id,
            'encode': 'D',
            'LANG': 'en'
        }

        dlclient = Client(self.user, self.password)
        for _ in range(self.retries):
            try:
                r = dlclient.session.get(self._EVENT_DOWNLOAD, params=payload,
                                         stream=True, timeout=self.timeout)
                fname = r.headers['Content-Disposition'].split('=')[1].strip('"')
                outdir = '_'.join(fname.split('_')[0:2])

                with tempfile.NamedTemporaryFile() as ft:
                    # save to temporary file
                    for chunk in r.iter_content(chunk_size=1024):
                        if chunk:  # filter out keep-alive new chunks
                            ft.write(chunk)
                    ft.flush()

                    # unzip temporary file
                    with zipfile.ZipFile(ft.name) as fz:
                        fz.extractall(path=outdir)
                    return outdir
            except Exception:
                continue
        else:
            msg = "Data download fails after {} retries".format(self.retries)
            logger.error(msg)
            return None

    def get_event_waveform(self, starttime, endtime,
                           region="00",
                           minmagnitude=3.0, maxmagnitude=9.9,
                           include_unknown_mag=True,
                           mindepth=None, maxdepth=None,
                           minlatitude=None, maxlatitude=None,
                           minlongitude=None, maxlongitude=None,
                           latitude=None, longitude=None,
                           minradius=None, maxradius=None):
        '''Get event waveform data.

        Parameters
        ----------
        starttime: :py:class:`datetime.datetime` or str
            Starttime of events.
        endtime: :py:class:`datetime.datetime` or str
            Endtime of events.
        region: str
            Limit events in specified region. Allowed values are:

            - ``00``: Whole Japan
            - ``01``: Hokkaido Region
            - ``02``: Tohoku Region
            - ``03``: Kanto Region
            - ``04``: Chubu Region
            - ``05``: Kinki Region
            - ``06``: Chugoku/Shikoku Region
            - ``07``: Kyushu Region
            - ``08``: Others
        minmagnitude: float
            Limit to events with a magnitude larger than speicified minimum.
        maxmagnitude: float
            Limit to events with a magnitude smaller than speicified maximum.
        include_unknown_mag: bool
            Include/exclude undetermined magnitude events.
        minlatitude: float
            Limit to events with a latitude larger than the specified minimum.
        maxlatitude: float
            Limit to events with a latitude smaller than the specified maximum.
        minlongitude: float
            Limit to events with a longitude larger than the specified minimum.
        maxlongitude: float
            Limit to events with a longitude smaller than the specified maximum.
        latitude: float
            Specify the latitude to be used for a radius search.
        longitude: float
            Specify the longitude to be used for a radius search.
        minradius: float
            Limit to events within the specified minimum number of degrees
            from the geographic point defined by the latitude and longitude
            parameters.
        maxradius: float
            Limit to events within the specified maximum number of degrees
            from the geographic point defined by the latitude and longitude
            parameters.
        '''
        starttime = string2datetime(starttime)
        endtime = string2datetime(endtime)

        # get event list
        events = []
        days = (endtime.date() - starttime.date()).days
        for i in range(0, days + 1):
            event_date = starttime.date() + timedelta(days=i)
            events.extend(self._search_event_by_day(event_date.year,
                                                    event_date.month,
                                                    event_date.day,
                                                    region=region,
                                                    magmin=minmagnitude,
                                                    magmax=maxmagnitude,
                                                    include_unknown_mag=True))

        # select events
        selected_events = []
        for event in events:
            # select events based on origin time
            if not starttime <= event.origin <= endtime:
                continue
            # select events based on magnitude
            if not minmagnitude <= event.magnitude <= maxmagnitude:
                continue
            # select events based on depth
            if mindepth and event.depth < mindepth:
                continue
            if maxdepth and event.depth > maxdepth:
                continue

            # select events in a box region
            if minlatitude or maxlatitude or minlongitude or maxlongitude:
                if not point_inside_box(event.latitude, event.longitude,
                                        latitude=latitude, longitude=longitude,
                                        minradius=minradius, maxradius=maxradius):
                    continue

            # select events in a circular region
            if (latitude and longitude) and (minradius or maxradius):
                if not point_inside_circular(event.latitude, event.longitude,
                                             latitude, longitude,
                                             minradius=minradius,
                                             maxradius=maxradius):
                    continue
            selected_events.append(event)

        logger.info("EVENT WAVEFORM DOWNLOADER:")
        logger.info("{:d} events to download.".format(len(selected_events)))
        for i in range(len(selected_events)):
            logger.info("{}".format(selected_events[i]))

        for event in selected_events:
            id = self._request_event_waveform(event)
            dirname = self._download_event_waveform(id)
            logger.info("{} {}".format(event, dirname))

    ###########################################################################
    #                                                                         #
    # Methods for get catalogs                                                #
    #                                                                         #
    ###########################################################################
    def _get_catalog(self, datatype, startdate, span, filename=None, os="DOS"):
        """Request JMA catalog."""

        if not (isinstance(startdate, datetime) or
                isinstance(startdate, date)):
            startdate = string2datetime(startdate)

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
            filename = "{}_{}_{}.txt".format(datatype,
                                             startdate.strftime("%Y%m%d"),
                                             span)
        with open(filename, "wb") as fd:
            for chunk in d.iter_content(chunk_size=1024):
                if chunk:  # filter out keep-alive new chunks
                    fd.write(chunk)
        return filename

    def get_arrivaltime(self, startdate, span, filename=None, os="DOS"):
        """Get JMA arrival time data from Hi-net.

        Parameters
        ----------
        startdate: str, :py:class:`datetime.date`, :py:class:`datetime.datetime`
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
        startdate: str, :py:class:`datetime.date`, :py:class:`datetime.datetime`
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
        >>> client.get_focalmechanism(startdate, 5, filename="focal.txt")
        'focal.txt'
        """
        return self._get_catalog("focal", startdate, span, filename, os)

    def get_station_list(self, code):
        """Get station list of a network.

        Supported networks:

        - Hi-net (0101)
        - F-net (0103, 0103A)
        - S-net (0120, 0120A)
        - MeSO-net (0131)

        >>> stations = client.get_station_list('0101')
        >>> for station in stations:
        ...     print(station)
        0101 N.WNNH 45.4883 141.885 -159.06
        0101 N.SFNH 45.3346 142.1185 -81.6
        ...
        """
        stations = []
        # remove trailing 'A' in network code
        code = code[:4]
        if code in ['0101', '0103', '0103A']:  # Hinet and Fnet
            lines = requests.get(self._STATION_INFO).iter_lines()
            next(lines)  # skip csv header

            for line in lines:
                items = line.decode('shift_jis').split(",")
                if items[0].strip("'") + items[1].strip("'") != code:
                    continue
                name = items[2]
                latitude, longitude, elevation = items[7], items[8], items[12]
                stations.append(Station(code, name, latitude, longitude, elevation))
        elif code in ['0120', '0120A', '0131']:  # S-net and MeSO-net
            import json
            if code in ['0120', '0120A']:
                json_text = self.session.get(self._SNET_STATION_INFO).text.lstrip('var snet_station = [').rstrip('];')
            else:
                json_text = self.session.get(self._MESONET_STATION_INFO).text.lstrip('var mesonet_station = [').rstrip('];')
            for station in json.loads(json_text)['features']:
                code = station['properties']['id']
                name = station['properties']['station_cd']
                latitude = station['properties']['latitude']
                longitude = station['properties']['longitude']
                elevation = station['properties']['sensor_height']
                stations.append(Station(code, name, latitude, longitude, elevation))
        else:
            raise ValueError("Only support Hi-net, F-net, S-net and MeSO-net.")
        return stations

    def _get_allowed_span(self, code):
        """Get allowed max span for each network.

        Hi-net server sets two limitations of data file size:

        #. Number_of_channels * record_length(min.) <= 12000 min
        #. record_length <= 60min

        >>> client._get_allowed_span('0201')
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
        channels = NETWORK[code].channels
        if code in ('0101', '0103', '0103A'):
            stations = self.get_selected_stations(code)
            if stations != 0:
                channels = stations * 3
        return min(int(12000/channels), 60)

    def get_selected_stations(self, code):
        """Query the number of stations selected for requesting data.

        Supported networks:

        - Hi-net (0101)
        - F-net (0103, 0103A)

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
        return len(re.findall(pattern, r.text))

    def select_stations(self, code, stations=None, minlatitude=None,
                        maxlatitude=None, minlongitude=None, maxlongitude=None,
                        latitude=None, longitude=None, minradius=None,
                        maxradius=None):
        """Select stations of a network.

        Supported networks:

        - Hi-net (0101)
        - F-net (0103, 0103A)
        - S-net (0120, 0120A)
        - MeSO-net (0131)

        Parameters
        ----------
        code: str
            Network code.
        stations: str or list
            Stations to select.
        minlatitude: float
            Limit to stations with a latitude larger than the specified minimum.
        maxlatitude: float
            Limit to stations with a latitude smaller than the specified maximum.
        minlongitude: float
            Limit to stations with a longitude larger than the specified minimum.
        maxlongitude: float
            Limit to stations with a longitude smaller than the specified maximum.
        latitude: float
            Specify the latitude to be used for a radius search.
        longitude: float
            Specify the longitude to be used for a radius search.
        minradius: float
            Limit to stations within the specified minimum number of degrees
            from the geographic point defined by the latitude and longitude
            parameters.
        maxradius: float
            Limit to stations within the specified maximum number of degrees
            from the geographic point defined by the latitude and longitude
            parameters.

        Examples
        --------
        Select only two stations of Hi-net:

        >>> client.select_stations('0101', ['N.AAKH', 'N.ABNH'])
        >>> client.get_selected_stations('0101')
        2

        Select stations in a box region:

        >>> client.select_stations('0101', minlatitude=40, maxlatitude=50,
        ...                        minlongitude=140, maxlongitude=150)

        Select stations in a circular region:

        >>> client.select_stations('0101', latitude=30, longitude139,
        ...                        minradius=0, maxradius=2)

        Select all Hi-net stations:

        >>> client.select_stations('0101')
        >>> client.get_selected_stations('0101')
        0

        """
        if stations is None:
            stations = []
        stations_selected = stations

        # get station list from Hi-net server
        stations_at_server = self.get_station_list(code)

        # select stations in a box region
        if minlatitude or maxlatitude or minlongitude or maxlongitude:
            for station in stations_at_server:
                if station.code != code:
                    continue
                if point_inside_box(station.latitude,
                                    station.longitude,
                                    minlatitude=minlatitude,
                                    maxlatitude=maxlatitude,
                                    minlongitude=minlongitude,
                                    maxlongitude=maxlongitude):
                    stations_selected.append(station.name)

        # select stations in a circular region
        if (latitude and longitude) and (minradius or maxradius):
            for station in stations_at_server:
                if station.code != code:
                    continue
                if point_inside_circular(station.latitude, station.longitude,
                                         latitude, longitude,
                                         minradius=minradius,
                                         maxradius=maxradius):
                    stations_selected.append(station.name)
        payload = {
            'net': code,
            'stcds': ':'.join(stations_selected) if stations_selected else None,
            'mode': '1',
        }
        self.session.post(self._CONT_SELECT, data=payload, timeout=self.timeout)

    def check_service_update(self):
        """Check if Hi-net service is updated.

        >>> client.check_service_update()
        [2017-01-01 00:00:00] INFO: Hi-net web service is NOT updated.
        """
        r = self.session.get(self._CONT + '/js/cont.js')

        if r.headers['ETag'].strip('"') == self._ETAG:
            logger.info("Hi-net web service is NOT updated.")
            return False
        else:
            logger.warning("Hi-net web service is updated."
                           " HinetPy may FAIL!")
            return True

    def check_package_release(self):
        """Check whether HinetPy has a new release.

        >>> client.check_package_release()
        [2019-02-19 00:00:00] INFO: You're using the latest release (v0.6.0).
        """
        from HinetPy import __version__, __title__
        from distutils.version import StrictVersion

        url = "https://pypi.python.org/pypi/{}/json".format(__title__)
        r = requests.get(url)
        if r.status_code != 200:
            logger.warning("Error in connecting PyPI. Skipped.")
            return False
        latest_release = r.json()['info']['version']

        if StrictVersion(latest_release) > StrictVersion(__version__):
            logger.warning("%s v%s is released. See %s for details.",
                           __title__, latest_release, url)
            return True
        else:
            logger.info("You're using the latest version (v%s).", __version__)
            return False

    def check_cmd_exists(self):
        """Check if ``catwin32`` and ``win2sac_32`` from win32tools in PATH.

        >>> client.check_cmd_exists()
        [2017-01-01 00:00:00] INFO: catwin32: /home/user/bin/catwin32.
        [2017-01-01 00:00:00] INFO: win2sac_32: /home/user/bin/win2sac_32.

        The client will report errors if ``catwin32`` and/or ``win2sac_32``
        are NOT in PATH. In this case, please download win32tools from
        `Hi-net <http://www.hinet.bosai.go.jp/>`_
        and make sure both binary files are in your PATH.
        """
        import shutil

        error = 0
        for cmd in ('catwin32', 'win2sac_32'):
            fullpath = shutil.which(cmd)
            if fullpath:
                logger.info("%s: %s.", cmd, fullpath)
            else:
                logger.error("%s: not found in PATH.", cmd)
                error += 1

        return False if error else True

    def info(self, code=None):
        """List information of networks.

        Parameters
        ----------
        code: None or str
            Network code.

        Examples
        --------

        >>> client.info()
        0101   : NIED Hi-net
        0103   : NIED F-net (broadband)
        0103A  : NIED F-net (strong motion)
        010501 : NIED V-net (Tokachidake)
        ...
        0703   : Aomori Prefectural Government
        0705   : Shizuoka Prefectural Government
        0801   : ADEP
        >>> client.info('0101')
        == Information of Network 0101 ==
        Name: NIED Hi-net
        Starttime: 20040401
        No. of channels: 2336
        """
        if code:
            net = NETWORK[code]
            info = "== Information of Network {} ==\n".format(code)
            info += "Name: {}\n".format(net.name)
            info += "Homepage: {}\n".format(net.url)
            info += "Starttime: {}\n".format(net.starttime.strftime("%Y%m%d"))
            info += "No. of channels: {}".format(net.channels)
            print(info)
        else:
            for code in sorted(NETWORK.keys()):
                print("{:7s}: {}".format(code, NETWORK[code].name))

    def _get_win32tools(self):
        """Download win32 tools."""
        d = self.session.get(self._WIN32TOOLS, stream=True)
        if d.status_code != 200:
            logger.error("Error in downloading win32tools.")
            return None

        filename = "win32tools.tar.gz"
        with open(filename, "wb") as fd:
            for chunk in d.iter_content(chunk_size=1024):
                if chunk:  # filter out keep-alive new chunks
                    fd.write(chunk)
        return filename

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


def prepare_jobs(starttime, span, max_span):
    spans = split_integer(span, max_span)
    jobs = [_Job(starttime=starttime, span=spans[0])]
    for i in range(1, len(spans)):
        dt = jobs[i-1].starttime + timedelta(minutes=spans[i-1])
        jobs.append(_Job(dt, spans[i]))
    return jobs


class _Job(object):
    '''Job class for internal use.'''
    def __init__(self, starttime, span, id=None):
        self.starttime = starttime
        self.span = span
        self.id = id


class Station(object):
    """
    Class for Stations.
    """
    def __init__(self, code, name, latitude, longitude, elevation):
        self.code = code
        self.name = name
        self.latitude = float(latitude)
        self.longitude = float(longitude)
        self.elevation = float(elevation)

    def __str__(self):
        string = "{} {} {} {} {}".format(self.code, self.name, self.latitude,
                                         self.longitude, self.elevation)
        return string


class Event(object):
    """
    Event class for requesting event waveforms.
    """
    def __init__(self, evid, origin, latitude, longitude, depth, magnitude,
                 name, name_en):
        self.evid = evid
        self.origin = datetime.strptime(origin, "%Y/%m/%d %H:%M:%S.%f")
        if latitude[-1] == 'N':
            self.latitude = float(latitude[:-1])
        else:
            self.latitude = -float(latitude[:-1])

        if longitude[-1] == 'E':
            self.longitude = float(longitude[:-1])
        else:
            self.longitude = -float(longitude[:-1])

        self.depth = float(depth.strip('km'))
        self.magnitude = float(magnitude)
        self.name = name
        self.name_en = name_en

    def __str__(self):
        string = "{} {} {} {} {}".format(self.origin, self.latitude, self.longitude,
                                         self.depth, self.magnitude)
        return string


def _parse_code(code):
    """Parse network code.

    >>> client._parse_code('0101')
    ('01', '01', None)
    >>> client._parse_code('0103A')
    ('01', '03A', None)
    >>> client._parse_code('010501')
    ('01', '05', '010501')
    """
    if code not in NETWORK.keys():
        msg = "{}: Incorrect network code.".format(code)
        raise ValueError(msg)
    elif code.startswith('0105') or code.startswith('0302'):
        org, net, volc = code[0:2], code[2:4], code
    else:
        org, net, volc = code[0:2], code[2:], None

    return org, net, volc
