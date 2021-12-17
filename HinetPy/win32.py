"""
Process seismic waveform data in win32 format.
"""
import glob
import logging
import math
import os
import subprocess
import tempfile
from fnmatch import fnmatch
from multiprocessing import Pool
from subprocess import DEVNULL, PIPE, Popen

# Setup the logger
FORMAT = "[%(asctime)s] %(levelname)s: %(message)s"
logging.basicConfig(level=logging.INFO, format=FORMAT, datefmt="%Y-%m-%d %H:%M:%S")
logger = logging.getLogger(__name__)


class Channel:
    """
    Class for channel which contain information for channels.
    """

    # pylint: disable=too-many-instance-attributes,invalid-name,redefined-builtin
    # pylint: disable=too-few-public-methods
    def __init__(
        self,
        id=None,
        name=None,
        component=None,
        latitude=None,
        longitude=None,
        unit=None,
        gain=None,
        damping=None,
        period=None,
        preamplification=None,
        lsb_value=None,
    ):  # pylint: disable=too-many-arguments
        """Initialize a channel.

        Parameters
        ----------
        id: str
            Channel ID.
        name: str
            Station Name.
        component: str
            Channel component name (e.g., ``U``, ``N`` or ``E``).
        latitude: float
            Station latitude.
        longitude: float
            Station longitude.
        unit: str
            Unit of data (e.g., ``m``, ``m/s``, ``m/s/s``, ``rad``).
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

        Notes
        -----
        The Hi-net website uses the moving-coil velocity-type seismometer.
        See :doc:`/appendix/response` for details.
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

    def write_sacpz(self, pzfile, keep_sensitivity=False):
        """
        Write channel information into a SAC polezero file.

        Parameters
        ----------
        pzfile: str
            Name of the SAC PoleZero file.
        keep_sensitivity: bool
            Keep sensitivity in the "constant" or not.
        """
        chan_info = f"{self.name}.{self.component} ({self.id})"
        # Hi-net uses a moving coil velocity type seismometer.
        if self.unit != "m/s":
            logger.warning(
                "%s: Unit is not velocity. The PZ file may be wrong.", chan_info
            )

        try:
            freq = 2.0 * math.pi / self.period
        except ZeroDivisionError:
            logger.warning("%s: Natural period = 0. Skipped.", chan_info)
            return

        # calculate poles by finding roots of equation s^2+2hws+w^2=0
        real = 0.0 - self.damping * freq
        imaginary = freq * math.sqrt(1.0 - self.damping ** 2.0)

        # calculate constant
        fn = 20.0  # alaways assume normalization frequency is 20 Hz
        s = complex(0, 2 * math.pi * fn)
        A0 = abs((s ** 2 + 2 * self.damping * freq * s + freq ** 2) / s ** 2)
        if keep_sensitivity:
            factor = math.pow(10, self.preamplification / 20.0)
            constant = A0 * self.gain * factor / self.lsb_value
        else:
            constant = A0

        # write information to a SAC PZ file
        with open(pzfile, "w", encoding="utf8") as pz:
            pz.write("ZEROS 3\n")
            pz.write("POLES 2\n")
            pz.write(f"{real:9.6f} {imaginary:9.6f}\n")
            pz.write(f"{real:9.6f} {-imaginary:9.6f}\n")
            pz.write(f"CONSTANT {constant:e}\n")


def extract_sac(
    data,
    ctable,
    suffix="SAC",
    outdir=".",
    pmax=8640000,
    filter_by_id=None,
    filter_by_name=None,
    filter_by_component=None,
    with_sacpz=False,
    processes=None,
):
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
        Maximum number of data points for a single channel. Defaults to 8640000.
        If the win32 data have data points more than 8640000 (i.e., longer than
        one day for a 100 Hz sampling rate), you MUST increase ``pmax``.
    filter_by_id: list or str
        Filter channels by ID. It can be a list of IDs or a wildcard.
    filter_by_name: list or str
        Filter channels by name. It can be a list of names or a wildcard.
    filter_by_component: list or str
        Filter channels by component. It can be a list of component names or
        a wildcard.
    with_sacpz: bool
        Aslo extract SAC PZ files. The default suffix is ``.SAC_PZ``.
    processes: None or int
        Number of processes to speed up data extraction parallelly.
        ``None`` means using all CPUs.


    .. deprecated:: 0.7.0

        Parameter ``with_pz`` is deprecated. Use ``with_sacpz`` instead.

    Note
    ----
    ``win2sac`` removes sensitivity from waveform data, then multiply by 1.0e9.
    Thus the extracted SAC files are velocity in nm/s, or acceleration in nm/s/s.

    Examples
    --------
    >>> extract_sac("0101_201001010000_5.cnt", "0101_20100101.ch")

    Extract all channel with specified SAC suffix and output directory:

    >>> extract_sac(
    ...     "0101_201001010000_5.cnt",
    ...     "0101_20100101.ch",
    ...     suffix="",
    ...     outdir="20100101000",
    ... )

    Extract only specified channels:

    >>> extract_sac(
    ...     "0101_201001010000_5.cnt",
    ...     "0101_20100101.ch",
    ...     filter_by_name="N.NA*",
    ...     filter_by_component="[NE]",
    ... )
    """
    if not (data and ctable):
        logger.error("data or ctable is `None'. Data requests may fail. Skipped.")
        return

    channels = read_ctable(ctable)
    logger.info("%s channels found in %s.", len(channels), ctable)
    if filter_by_id or filter_by_name or filter_by_component:
        channels = _filter_channels(
            channels, filter_by_id, filter_by_name, filter_by_component
        )
    logger.info("%s channels to be extracted.", len(channels))

    if not os.path.exists(outdir):
        os.makedirs(outdir, exist_ok=True)

    with Pool(processes=processes) as pool:
        with tempfile.NamedTemporaryFile() as ftmp:
            _write_winprm(ctable, ftmp.name)
            sacfiles = pool.starmap(
                _extract_channel,
                [(data, ch, suffix, outdir, ftmp.name, pmax) for ch in channels],
            )
            logger.info(
                "%s SAC data successfully extracted.",
                len(sacfiles) - sacfiles.count(None),
            )

        if with_sacpz:
            # "SAC_PZ" here is hardcoded.
            pzfiles = pool.starmap(
                _extract_sacpz, [(ch, "SAC_PZ", outdir) for ch in channels]
            )
            logger.info(
                "%s SAC PZ files successfully extracted.",
                len(pzfiles) - pzfiles.count(None),
            )


def extract_sacpz(
    ctable,
    suffix="SAC_PZ",
    outdir=".",
    keep_sensitivity=False,
    filter_by_chid=None,
    filter_by_name=None,
    filter_by_component=None,
    processes=None,
):
    """Extract instrumental response in SAC PZ format from channel table.

    .. warning::

       Only works for instrumental responses of Hi-net network.

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
    keep_sensitivity: bool
        The ``win2sac_32`` program automatically removes sensitivity from waveform
        data during the win32-to-SAC format conversion.
        So the generated polezero file should omit the sensitivity.
    filter_by_id: list or str
        Filter channels by ID. It can be a list of IDs or a wildcard.
    filter_by_name: list or str
        Filter channels by name. It can be a list of names or a wildcard.
    filter_by_component: list or str
        Filter channels by component. It can be a list of component names or
        a wildcard.
    processes: None or int
        Number of processes to speed up data extraction parallelly.
        ``None`` means using all CPUs.

    Examples
    --------
    >>> extract_sacpz("0101_20100101.ch")

    Extract all channel with specified suffix and output directory:

    >>> extract_sacpz("0101_20100101.ch", suffix="", outdir="20100101000")

    Extract only specified channels:

    >>> extract_sacpz(
    ...     "0101_20100101.ch", filter_by_name="N.NA*", filter_by_component="[NE]"
    ... )
    """
    if not ctable:
        logger.error("ctable is `None'. Data requests may fail. Skipped.")
        return

    channels = read_ctable(ctable)
    if filter_by_chid or filter_by_name or filter_by_component:
        channels = _filter_channels(
            channels, filter_by_chid, filter_by_name, filter_by_component
        )
    if not os.path.exists(outdir):
        os.makedirs(outdir, exist_ok=True)

    with Pool(processes=processes) as pool:
        args = [(ch, suffix, outdir, keep_sensitivity) for ch in channels]
        pzfiles = pool.starmap(_extract_sacpz, args)
        logger.info(
            "%s SAC PZ files successfully extracted.",
            len(pzfiles) - pzfiles.count(None),
        )


def extract_pz(**kwargs):
    """
    Extract instrumental response in SAC PZ format from channel table.

    .. deprecated:: 0.7.0

        :meth:`~HinetPy.win32.extract_pz` is deprecated.
        Use :meth:`~HinetPy.win32.extract_sacpz` instead.
    """
    logger.warning("Function extract_pz() is deprecated. Use extract_sacpz() instead.")
    return extract_sacpz(**kwargs)


def read_ctable(ctable):
    """
    Read channel table file.

    Parameters
    ----------
    ctable: str
        Channle table file.

    Returns
    -------
    list:
        List of :class:`~HinetPy.win32.Channel`.
    """
    channels = []
    with open(ctable, "r", encoding="utf8") as fct:
        for line in fct:
            # skip blank lines and comment lines
            if not line.strip() or line.strip().startswith("#"):
                continue
            items = line.split()
            try:
                channel = Channel(
                    id=items[0],
                    name=items[3],
                    component=items[4],
                    latitude=float(items[13]),
                    longitude=float(items[14]),
                    unit=items[8],
                    gain=float(items[7]),
                    damping=float(items[10]),
                    period=float(items[9]),
                    preamplification=float(items[11]),
                    lsb_value=float(items[12]),
                )
                channels.append(channel)
            except ValueError as err:
                logger.warning(
                    "Error in parsing channel information for %s.%s (%s). Skipped.",
                    items[3],
                    items[4],
                    items[0],
                )
                logger.warning("Original error message: %s", err)
    return channels


def _filter_channels(
    channels, filter_by_id=None, filter_by_name=None, filter_by_component=None
):
    """Filter channels by id, name and/or component.

    Parameters
    ----------
    channels: :class:`~HinetPy.win32.Channel`
        Channels to be filtered.
    filter_by_id: list or str
        Filter channels by ID. It can be a list of IDs or a wildcard.
    filter_by_name: list or str
        Filter channels by name. It can be a list of names or a wildcard.
    filter_by_component: list or str
        Filter channels by component. It can be a list of component names or
        a wildcard.
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
        channels = _filter(channels, "id", filter_by_id)
    if filter_by_name:
        channels = _filter(channels, "name", filter_by_name)
    if filter_by_component:
        channels = _filter(channels, "component", filter_by_component)

    return channels


def _write_winprm(ctable, prmfile="win.prm"):
    """
    Write a four-line parameter file.
    """
    with open(prmfile, "w", encoding="utf8") as fprm:
        msg = "\n".join([".", ctable, ".", "."])
        fprm.write(msg)


def _extract_channel(
    winfile, channel, suffix="SAC", outdir=".", prmfile="win.prm", pmax=8640000
):
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

    Returns
    -------
    str:
        The extracted SAC file name.
    """

    cmd = [
        "win2sac_32",
        winfile,
        channel.id,
        suffix,
        outdir,
        "-e",
        "-p" + prmfile,
        "-m" + str(pmax),
    ]
    with Popen(cmd, stdout=DEVNULL, stderr=PIPE) as proc:
        # check stderr output
        for line in proc.stderr.read().decode().split("\n"):
            if "The number of points is maximum over" in line:
                msg = "The number of data points is over maximum. Try to increase pmax."
                raise ValueError(msg)
            if f"Data for channel {channel.id} not existed" in line:
                # return None if no data avaiable
                logger.warning(
                    "Data for %s.%s (%s) not exists. Skipped.",
                    channel.name,
                    channel.component,
                    channel.id,
                )
                return None

    filename = f"{channel.name}.{channel.component}.{suffix}"
    if outdir != ".":
        filename = os.path.join(outdir, filename)

    if os.path.exists(filename):  # some channels have no data
        if suffix == "":  # remove extra dot if suffix is empty
            os.rename(filename, filename[:-1])
            return filename[:-1]
        return filename
    return None


def _extract_sacpz(channel, suffix="SAC_PZ", outdir=".", keep_sensitivity=False):
    """Extract one SAC PZ file from a channel table file.

    Parameters
    ----------
    channel: str
        Channel to be extracted.
    suffix: str
        Suffix of the SAC PZ file.
    outdir: str
        Output directory.
    keep_sensitivity: bool
        Keep sensitivity in the "constant" or not.

    Returns
    -------
    str:
        The extracted SAC PZ file name.
    """
    pzfile = f"{channel.name}.{channel.component}"
    if suffix:
        pzfile += "." + suffix
    pzfile = os.path.join(outdir, pzfile)
    channel.write_sacpz(pzfile, keep_sensitivity=keep_sensitivity)
    return pzfile


def merge(data, total_data, force_sort=False):
    """Merge several win32 files to one win32 file.

    Parameters
    ----------
    data: list or str
        Win32 files to be merged. It can be a list of file names or a wildcard.
    total_data: str
        Filename of ouput win32 file.
    force_sort: bool
        Sort all win32 files by date.

    Examples
    --------
    If win32 files are named by starttime (e.g. ``201304040203.cnt``), sorting
    win32 files in list by name/time is prefered:

    >>> data = sorted(glob.glob("20130404*.cnt"))
    >>> merge(data, "outdir/final.cnt")

    If win32 files are named randomly, you should set ``force_sort`` to
    ``True`` to force ``catwin32`` to sort all data by time.
    However, it's time consuming. Do NOT use it unless necessary:

    >>> data = ["001.cnt", "002.cnt", "003.cnt"]
    >>> merge(data, "final.cnt", force_sort=True)

    You can also use wildcard to specify the win32 files to be merged.

    >>> merge("20130404*.cnt", "final.cnt")
    """
    if isinstance(data, str):  # wildcard support
        data = sorted(glob.glob(data))
        if not data:
            raise FileNotFoundError("Files to be merged not found.\n")

    if os.path.dirname(total_data):
        os.makedirs(os.path.dirname(total_data), exist_ok=True)

    cmd = ["catwin32", "-o", total_data] + data
    if force_sort:  # add -s option to force sort
        cmd.append("-s")

    subprocess.call(cmd, stdout=DEVNULL, stderr=DEVNULL)
