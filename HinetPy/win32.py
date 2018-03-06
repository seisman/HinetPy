# -*- coding: utf-8 -*-
import os
import math
import glob
import logging
import tempfile
import subprocess
from subprocess import Popen, DEVNULL, PIPE
from multiprocessing import Pool, cpu_count
from fnmatch import fnmatch

# Setup the logger
FORMAT = "[%(asctime)s] %(levelname)s: %(message)s"
logging.basicConfig(level=logging.INFO,
                    format=FORMAT,
                    datefmt='%Y-%m-%d %H:%M:%S')
logger = logging.getLogger(__name__)


class Channel(object):
    def __init__(self, id=None, name=None, component=None,
                 latitude=None, longitude=None, unit=None,
                 gain=None, damping=None, period=None, preamplification=None,
                 lsb_value=None):
        """ Class for channel.

        Parameters
        ----------
        id: str
            Channel ID.
        name: str
            Station Name.
        component: str
            Channel component name (``U|N|E``).
        latitude: float
            Station latitude.
        longitude: float
            Station longitude.
        unit: str
            Unit of data (``m``, ``m/s``, ``m/s/s``, ``rad``).
        gain: float
            Sensor sensitivity.
        damping: float
            Damping constant of the sensor.
        period: float
            Natural period of the seismometer.
        preamplification:
            Preamplification.
        lsb_value:
            LSB value.
        """
        self.id = id
        self.name = name
        self.component = component
        self.latitude = latitude
        self.longitude = longitude
        self.unit = unit
        self.gain = gain
        self.damping = damping
        self.period = period
        self.preamplification = preamplification
        self.lsb_value = lsb_value


def extract_sac(data, ctable, suffix="SAC", outdir=".", pmax=8640000,
                filter_by_id=None,
                filter_by_name=None,
                filter_by_component=None,
                with_pz=False, processes=0):
    """Extract data as SAC format files.

    Parameters
    ----------
    data: str
        win32 file to be processed.
    ctable: str
        Channel table file.
    suffix: str
        Suffix of output SAC files. Defaults to ``SAC``.
    outdir: str
        Output directory. Defaults to current directory.
    pmax: int
        Maximum number of data points. Defaults to 8640000. If the input data
        is longer than one day, you have to to increase ``pmax``.
    filter_by_id: list of str or wildcard
        Filter channels by ID.
    filter_by_name: list of str or wildcard
        Filter channels by name.
    filter_by_component: list of str or wildcard
        Filter channels by component.
    with_pz: bool
        Extract PZ files at the same time.
        PZ file has default suffix ``.SAC_PZ``.
    processes: int
        Number of parallel processes to speed up data extraction.
        Use all processes by default.

    Examples
    --------
    >>> extract_sac("0101_201001010000_5.cnt", "0101_20100101.ch")

    Extract all channel with specified SAC suffix and output directory:

    >>> extract_sac("0101_201001010000_5.cnt", "0101_20100101.ch",
    ...             suffix="", outdir="20100101000")

    Extract only specified channels:

    >>> extract_sac("0101_201001010000_5.cnt", "0101_20100101.ch",
    ...             filter_by_name="N.NA*", filter_by_component='[NE]')
    """
    if not (data and ctable):
        logger.info("No data and ctable found. Skipped.")
        return

    channels = _get_channels(ctable)
    logger.info("%d channels found in %s.", len(channels), ctable)
    if filter_by_id or filter_by_name or filter_by_component:
        channels = _filter_channels(channels,
                                    filter_by_id,
                                    filter_by_name,
                                    filter_by_component)
    logger.info("%d channels to be extracted.", len(channels))

    if not os.path.exists(outdir):
        os.makedirs(outdir, exist_ok=True)

    pool = Pool(processes=_get_processes(processes))
    with tempfile.NamedTemporaryFile() as ft:
        _write_winprm(ctable, ft.name)
        args = [(data, ch, suffix, outdir, ft.name, pmax) for ch in channels]
        sacfiles = pool.starmap(_extract_channel, args)
        logger.info("%d SAC data successfully extracted.",
                    len(sacfiles) - sacfiles.count(None))

    if with_pz:
        # "SAC_PZ" here is hardcoded.
        args = [(ch, "SAC_PZ", outdir) for ch in channels]
        pzfiles = pool.starmap(_extract_sacpz, args)
        logger.info("%d SAC PZ files successfully extracted.",
                    len(pzfiles) - pzfiles.count(None))


def _get_processes(procs):
    """Choose the best processes."""
    cpus = cpu_count()
    if cpus == 1:
        return cpus
    else:
        if not 0 < procs < cpus:
            return cpus - 1
        else:
            return procs


def extract_pz(ctable, suffix='SAC_PZ', outdir='.',
               filter_by_chid=None,
               filter_by_name=None,
               filter_by_component=None):
    """Extract instrumental response in SAC PZ format from channel table.

    .. warning::

       Only works for Hi-net network.

       RESP files of F-net network can be downloaded from
       `F-net website <http://www.fnet.bosai.go.jp/st_info/response.php?LANG=en>`_.

    Parameters
    ----------
    ctable: str
        Channel table file.
    suffix: str
        Suffix of SAC PZ files. Defaults to ``SAC_PZ``.
    outdir: str
        Output directory. Defaults to current directory.
    filter_by_id: list of str or wildcard
        Filter channels by ID.
    filter_by_name: list of str or wildcard
        Filter channels by name.
    filter_by_component: list of str or wildcard
        Filter channels by component.

    Examples
    --------
    >>> extract_pz("0101_20100101.ch")

    Extract all channel with specified suffix and output directory:

    >>> extract_pz("0101_20100101.ch", suffix="", outdir="20100101000")

    Extract only specified channels:

    >>> extract_pz("0101_20100101.ch",
    ...            filter_by_name="N.NA*", filter_by_component='[NE]')
    """
    if not ctable:
        logger.error("No ctable found. Skipped.")
        return

    channels = _get_channels(ctable)
    if filter_by_chid or filter_by_name or filter_by_component:
        channels = _filter_channels(channels,
                                    filter_by_name,
                                    filter_by_chid,
                                    filter_by_component)
    if not os.path.exists(outdir):
        os.makedirs(outdir, exist_ok=True)

    for channel in channels:
        _extract_sacpz(channel, suffix=suffix, outdir=outdir)


def _get_channels(ctable):
    """Get channel information from channel table file.

    Parameters
    ----------
    ctable: str
        Channle table file.
    """
    channels = []
    with open(ctable, "r") as f:
        for line in f:
            if line.strip().startswith("#"):  # skip comment line
                continue
            items = line.split()
            channels.append(Channel(id=items[0],
                                    name=items[3],
                                    component=items[4],
                                    latitude=float(items[13]),
                                    longitude=float(items[14]),
                                    unit=items[8],
                                    gain=float(items[7]),
                                    damping=float(items[10]),
                                    period=float(items[9]),
                                    preamplification=float(items[11]),
                                    lsb_value=float(items[12])))
    return channels


def _filter_channels(channels,
                     filter_by_id=None,
                     filter_by_name=None,
                     filter_by_component=None):
    """Filter channels by id, name and/or component.

    Parameters
    ----------
    channels: :class:`~HinetPy.win32.Channel`
        Channels to be filtered.
    filter_by_id: list of str or wildcard
        Filter channels by ID.
    filter_by_name: list of str or wildcard
        Filter channels by name.
    filter_by_component: list of str or wildcard
        Filter channels by component.
    """

    def _filter(channels, key, filters):
        filtered_channels = []
        if isinstance(filters, list):  # filter by list
            for channel in channels:
                if getattr(channel, key) in filters:
                    filtered_channels.append(channel)
        elif isinstance(filters, str):  # filter by wildcard
            for channel in channels:
                if fnmatch(getattr(channel, key), filters):
                    filtered_channels.append(channel)
        else:
            raise ValueError("Only list and wildcard filter are supported.")
        return filtered_channels

    if filter_by_id:
        channels = _filter(channels, 'id', filter_by_id)
    if filter_by_name:
        channels = _filter(channels, 'name', filter_by_name)
    if filter_by_component:
        channels = _filter(channels, 'component', filter_by_component)

    return channels


def _write_winprm(ctable, prmfile="win.prm"):
    """
    Four line parameters file
    """

    with open(prmfile, "w") as f:
        msg = ".\n" + ctable + "\n" + ".\n.\n"
        f.write(msg)


def _extract_channel(winfile, channel, suffix="SAC", outdir=".",
                     prmfile="win.prm", pmax=8640000):
    """Extract one channel data from win32 file.

    Parameters
    ----------
    winfile: str
        win32 file to be processed.
    channel: str
        Channel to be extracted.
    suffix: str
        SAC file suffix.
    outdir: str
        Output directory.
    prmfile: str
        Win32 parameter file.
    pmax: int
        Maximum number of data points.
    """

    cmd = ['win2sac_32', winfile, channel.id, suffix, outdir,
           '-e', '-p'+prmfile, '-m'+str(pmax)]
    p = Popen(cmd, stdout=DEVNULL, stderr=PIPE)

    # check stderr output
    for line in p.stderr.read().decode().split("\n"):
        if 'The number of points is maximum over' in line:
            msg = "The number of data points is over maximum. " \
                  "Try to increase pmax."
            raise ValueError(msg)
        elif 'Data for channel {} not existed'.format(channel.id) in line:
            # return None if no data avaiable
            logger.warning("Data for %s.%s (%s) not exists. Skipped.",
                           channel.name, channel.component, channel.id)
            return None

    filename = "{}.{}.{}".format(channel.name, channel.component, suffix)
    if outdir != '.':
        filename = os.path.join(outdir, filename)

    if os.path.exists(filename):  # some channels have no data
        if suffix == '':  # remove extra dot if suffix is empty
            os.rename(filename, filename[:-1])
            return filename[:-1]
        else:
            return filename


def _find_poles(damping, freq):
    """Find roots of equation s^2+2hws+w^2=0

    Parameters
    ----------
    damping: float
        Damping constant.
    freq: float
        Angular frequency.
    """

    real = -damping*freq
    imaginary = freq * math.sqrt(1 - damping*damping)

    return real, imaginary


def _write_pz(pzfile, real, imaginary, constant):
    """Write SAC PZ file.

    Parameters
    ----------
    pzfile: str
        SAC PoleZero filename.
    real: float
        Real part of poles.
    imaginary: float
        Imaginary part of poles
    constant: float
        Constant in SAC PZ.
    """
    with open(pzfile, "w") as pz:
        pz.write("ZEROS 3\n")
        pz.write("POLES 2\n")
        pz.write("{:9.6f} {:9.6f}\n".format(real, imaginary))
        pz.write("{:9.6f} {:9.6f}\n".format(real, -imaginary))
        pz.write("CONSTANT {:e}\n".format(constant))


def _extract_sacpz(channel, suffix='SAC_PZ', outdir='.'):
    # Hi-net use moving coil velocity type seismometer.
    if channel.unit != 'm/s':
        logger.warning("%s.%s (%s): Unit is not velocity.",
                       channel.name, channel.component, channel.id)

    # calculate poles
    try:
        freq = 2.0 * math.pi / channel.period
    except ZeroDivisionError:
        logger.warning("%s.%s (%s): Natural period = 0. Skipped.",
                       channel.name, channel.component, channel.id)
        return None
    real, imaginary = _find_poles(channel.damping, freq)

    # calculate sensitivity and constant
    A0 = 2 * channel.damping
    factor = math.pow(10, channel.preamplification/20.0)
    sensitivity = channel.gain * factor / channel.lsb_value
    constant = A0 * sensitivity

    pzfile = "{}.{}".format(channel.name, channel.component)
    if suffix:
        pzfile += '.' + suffix
    pzfile = os.path.join(outdir, pzfile)
    _write_pz(pzfile, real, imaginary, constant)

    return pzfile


def merge(datas, total_data, force_sort=False):
    """Merge several win32 files to one win32 file.

    Parameters
    ----------
    datas: list of str or wildcard
        Win32 files to be merged.
    total_data: str
        Filename of ouput win32 file.
    force_sort: bool
        Sort all win32 files by date.

    Examples
    --------
    If win32 files are named by starttime (e.g. ``201304040203.cnt``), sorting
    win32 files in list by name/time is prefered:

    >>> datas = sorted(glob.glob("20130404*.cnt"))
    >>> merge(datas, "outdir/final.cnt")

    If win32 files are named randomly, you should set ``force_sort`` to
    ``True`` to force ``catwin32`` to sort all data by time.
    However, it's time consuming. Do NOT use it unless necessary:

    >>> datas = ["001.cnt", "002.cnt", "003.cnt"]
    >>> merge(datas, "final.cnt", force_sort=True)

    You can also use wildcard to specify the win32 files to be merged.

    >>> merge("20130404*.cnt", "final.cnt")
    """
    if isinstance(datas, str):  # wildcard support
        datas = sorted(glob.glob(datas))
        if not datas:
            raise FileNotFoundError("Files to be merged not found.\n")

    if os.path.dirname(total_data):
        os.makedirs(os.path.dirname(total_data), exist_ok=True)

    cmd = ['catwin32', '-o', total_data] + datas
    if force_sort:  # add -s option to force sort
        cmd.append('-s')

    subprocess.call(cmd, stdout=DEVNULL, stderr=DEVNULL)
