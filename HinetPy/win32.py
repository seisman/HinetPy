"""
Process seismic waveform data in win32 format.
"""

import glob
import logging
import os
import subprocess
import tempfile
from fnmatch import fnmatch
from multiprocessing import Pool
from subprocess import DEVNULL, PIPE, Popen

from .channel import Channel

# Setup the logger
FORMAT = "[%(asctime)s] %(levelname)s: %(message)s"
logging.basicConfig(level=logging.INFO, format=FORMAT, datefmt="%Y-%m-%d %H:%M:%S")
logger = logging.getLogger(__name__)


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
    """
    Extract data as SAC format files.

    This function calls the ``win2sac_32`` command, available in the Hi-net win32tools
    package, to convert data files from win32 format to SAC fomrat. It can also extract
    the channel information as SAC polezero files.

    Note that the ``win2sac_32`` command always remove the instrument sensitivity from
    waveform data, and multiply the data by 1.0e9. Thus, the extracted SAC files are not
    in digital counts, but velocity in nm/s, or acceleration in nm/s/s. Due to the same
    reason, the extracted SAC polezero files does not keep the sensitivity in the
    "CONSTANT" of SAC polezero files.

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
        Maximum number of data points for one channel. Defaults to 8640000. If one
        channel has more than 8640000 data points (i.e., longer than one day for a
        100 Hz sampling rate), you MUST increase ``pmax``.
    filter_by_id: list or str
        Filter channels by ID. It can be a list of IDs or a wildcard.
    filter_by_name: list or str
        Filter channels by name. It can be a list of names or a wildcard.
    filter_by_component: list or str
        Filter channels by component. It can be a list of component names or a wildcard.
    with_sacpz: bool
        Aslo extract SAC PZ files. By default, the suffix is ``.SAC_PZ`` and the channel
        sensitivity is not kept in the "CONSTANT".
    processes: None or int
        Number of processes to speed up data extraction parallelly. ``None`` means using
        all CPUs.

    .. deprecated:: 0.7.0

        Parameter ``with_pz`` is deprecated. Use ``with_sacpz`` instead.

    Examples
    --------
    Extract all channels with default settings:

    >>> extract_sac("0101_201001010000_5.cnt", "0101_20100101.ch")

    Extract all channels with a specified suffix and output directory:

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
    if data is None or ctable is None:
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
                _extract_channel_sac,
                [(data, ch, suffix, outdir, ftmp.name, pmax) for ch in channels],
            )
            logger.info(
                "%s SAC data successfully extracted.",
                len(sacfiles) - sacfiles.count(None),
            )

        if with_sacpz:
            # "SAC_PZ" here is hardcoded.
            pzfiles = pool.starmap(
                _extract_channel_sacpz, [(ch, "SAC_PZ", outdir) for ch in channels]
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
    """
    Extract instrumental responses in SAC polezero format from a channel table.

    .. warning::

       The function only works for Hi-net instrumental responses.

       RESP files of the F-net network can be downloaded from
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
        The ``win2sac_32`` program automatically removes sensitivity from waveform data
        during the win32-to-SAC format conversion. So the generated polezero file should
        omit the sensitivity.
    filter_by_id: list or str
        Filter channels by ID. It can be a list of IDs or a wildcard.
    filter_by_name: list or str
        Filter channels by name. It can be a list of names or a wildcard.
    filter_by_component: list or str
        Filter channels by component. It can be a list of component names or a wildcard.
    processes: None or int
        Number of processes to speed up data extraction parallelly. ``None`` means using
        all CPUs.

    Examples
    --------
    Extract all channels with default settings:

    >>> extract_sacpz("0101_20100101.ch")

    Extract all channels with a specified suffix and output directory:

    >>> extract_sacpz("0101_20100101.ch", suffix="", outdir="20100101000")

    Extract only specified channels:

    >>> extract_sacpz(
    ...     "0101_20100101.ch", filter_by_name="N.NA*", filter_by_component="[NE]"
    ... )
    """
    if ctable is None:
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
        pzfiles = pool.starmap(_extract_channel_sacpz, args)
        logger.info(
            "%s SAC PZ files successfully extracted.",
            len(pzfiles) - pzfiles.count(None),
        )


def extract_pz(ctable, **kwargs):
    """
    Extract instrumental responses in SAC polezero format from a channel table.

    .. deprecated:: 0.7.0

        :meth:`~HinetPy.win32.extract_pz` is deprecated.
        Use :meth:`~HinetPy.win32.extract_sacpz` instead.
    """
    logger.warning("Function extract_pz() is deprecated. Use extract_sacpz() instead.")
    return extract_sacpz(ctable, **kwargs)


def read_ctable(ctable):
    """
    Read a channel table file.

    Parameters
    ----------
    ctable: str
        Channle table file.

    Returns
    -------
    list
        List of :class:`~HinetPy.win32.Channel`.
    """
    channels = []
    with open(ctable, encoding="utf8") as fct:
        for line in fct:
            # skip blank lines and comment lines
            if not line.strip() or line.strip().startswith("#"):
                continue
            items = line.split()
            try:
                channels.append(
                    Channel(
                        id=items[0],
                        name=items[3],
                        component=items[4],
                        latitude=items[13],
                        longitude=items[14],
                        unit=items[8],
                        gain=items[7],
                        damping=items[10],
                        period=items[9],
                        preamplification=items[11],
                        lsb_value=items[12],
                    )
                )
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
    """
    Filter channels by id, name and/or component.

    Parameters
    ----------
    channels: :class:`~HinetPy.win32.Channel`
        List of channels to be filtered.
    filter_by_id: list or str
        Filter channels by ID. It can be a list of IDs or a wildcard.
    filter_by_name: list or str
        Filter channels by name. It can be a list of names or a wildcard.
    filter_by_component: list or str
        Filter channels by component. It can be a list of component names or a wildcard.
    """

    def _filter(channels, key, filters):
        """
        Filter channels by filters, which can be either a list or a wildcard.
        """
        if isinstance(filters, list):  # filter by list
            return [chn for chn in channels if getattr(chn, key) in filters]
        if isinstance(filters, str):  # filter by wildcard
            return [chn for chn in channels if fnmatch(getattr(chn, key), filters)]
        raise ValueError("Only list and wildcard filter are supported.")

    for key, filter_by in (
        ("id", filter_by_id),
        ("name", filter_by_name),
        ("component", filter_by_component),
    ):
        if filter_by is not None:
            channels = _filter(channels, key, filter_by)
    return channels


def _write_winprm(ctable, prmfile="win.prm"):
    """
    Write a four-line parameter file.
    """
    with open(prmfile, "w", encoding="utf8") as fprm:
        fprm.write(f".\n{ctable}\n.\n.")


def _extract_channel_sac(
    winfile, channel, suffix="SAC", outdir=".", prmfile="win.prm", pmax=8640000
):
    """
    Extract one channel data from win32 file.

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
        win32 parameter file.
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
        f"-p{prmfile}",
        f"-m{pmax}",
    ]
    with Popen(cmd, stdout=DEVNULL, stderr=PIPE) as proc:
        # check stderr output
        for line in proc.stderr.read().decode().split("\n"):
            if "The number of points is maximum over" in line:
                raise ValueError(
                    "The number of data points is over maximum. Try to increase pmax."
                )
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


def _extract_channel_sacpz(
    channel, suffix="SAC_PZ", outdir=".", keep_sensitivity=False
):
    """
    Extract one SAC PZ file from a channel table file.

    Parameters
    ----------
    channel: str
        Channel to be extracted.
    suffix: str
        Suffix of the SAC PZ file.
    outdir: str
        Output directory.
    keep_sensitivity: bool
        Keep sensitivity in the "CONSTANT" or not.

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
    """
    Merge multiple win32 files into one large win32 file.

    The function calls the ``catwin32`` command, available in the Hi-net win32tools
    package, to merge multiple win32 files into one large win32 file.

    By default, the ``catwin32`` command simply concatenates all files in the order they
    are passed. So the files must be sorted by their start time before being passed. If
    your files are named by starttime like ``201304040203.cnt``, you can use
    ``data=sorted(glob.glob("20130404*.cnt"))`` to pass the sorted list of files.
    Otherwise, you have to use ``force_sort=True``, forcing ``catwin32`` to sort all
    files by starttime before merging. However, the sorting process is very time
    consuming. Do NOT set ``force_sort=True`` unless necessary.

    Parameters
    ----------
    data: list or str
        Win32 files to be merged. It can be a list of file names or a wildcard.
    total_data: str
        Filename of the ouput win32 file.
    force_sort: bool
        Sort all win32 files by starttime before merging.

    Examples
    --------
    For win32 files that are named by starttime (e.g. ``201304040203.cnt``), sorting
    win32 files using Python's built-in :func:`sorted` function is preferred:

    >>> data = sorted(glob.glob("20130404*.cnt"))
    >>> merge(data, "outdir/final.cnt")

    If win32 files are randomly named, you should use ``force_sort=True`` to force
    ``catwin32`` to sort all data by time before merging.

    >>> data = ["001.cnt", "002.cnt", "003.cnt"]
    >>> merge(data, "final.cnt", force_sort=True)

    You can also use wildcard to specify the win32 files to be merged. The function will
    sort the matched files for you automatically.

    >>> merge("20130404*.cnt", "final.cnt")
    """
    if isinstance(data, str):  # wildcard support
        data = sorted(glob.glob(data))
        if not data:
            raise FileNotFoundError("Files to be merged not found.\n")

    if os.path.dirname(total_data):
        os.makedirs(os.path.dirname(total_data), exist_ok=True)

    cmd = ["catwin32", "-o", total_data, *data]
    if force_sort:  # add -s option to force sort
        cmd.append("-s")

    subprocess.call(cmd, stdout=DEVNULL, stderr=DEVNULL)
