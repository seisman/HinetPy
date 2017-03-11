# -*- coding: utf-8 -*-
import os
import math
import subprocess
from fnmatch import fnmatch


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
            Natural period of the seismometer.abs
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


def extract_sac(data, ctable, suffix="SAC", outdir=".",
                filter_by_id=None,
                filter_by_name=None,
                filter_by_component=None,
                with_pz=False):
    """Extract data as SAC format files.

    Parameters
    ----------
    data: str
        win32 file to be processed.
    ctable: str
        Channel table file.
    suffix: str
        SAC suffix.
    outdir: str
        Output directory.
    filter_by_id: list of str or wildcard
        Filter channels by ID.
    filter_by_name: list of str or wildcard
        Filter channels by name.
    filter_by_component: list of str or wildcard
        Filter channels by component.
    with_pz: bool
        Extract PZ files at the same time. PZ file has default suffix ``.SAC_PZ``.

    Examples
    --------
    >>> extract_sac("0101_201001010000_5.cnt", "0101_20100101.ch")  # doctest: +SKIP

    Extract all channel with specified SAC suffix and output directory:

    >>> extract_sac("0101_201001010000_5.cnt", "0101_20100101.ch",
    ...             suffix="", outdir="20100101000")  # doctest: +SKIP

    Extract only specified channels:

    >>> extract_sac("0101_201001010000_5.cnt", "0101_20100101.ch",
    ...             filter_by_name="N.NA*", filter_by_channel='[NE]')  # doctest: +SKIP
    """

    channels = _get_channels(ctable)
    if filter_by_id or filter_by_name or filter_by_component:
        channels = _filter_channels(channels,
                                    filter_by_id,
                                    filter_by_name,
                                    filter_by_component)

    if not os.path.exists(outdir):
        os.mkdir(outdir)

    _write_winprm(ctable)
    for channel in channels:
        _extract_channel(data, channel, suffix, outdir)
        if with_pz:
            _extract_sacpz(channel, outdir=outdir)
    os.unlink("win.prm")


def extract_pz(ctable, suffix='SAC_PZ', outdir='.',
               filter_by_chid=None, filter_by_name=None, filter_by_component=None):
    """Extract instrumental response in SAC PZ format from channel table.

    Parameters
    ----------
    ctable: str
        Channel table file.
    suffix: str
        SAC suffix.
    outdir: str
        Output directory.
    filter_by_id: list of str or wildcard
        Filter channels by ID.
    filter_by_name: list of str or wildcard
        Filter channels by name.
    filter_by_component: list of str or wildcard
        Filter channels by component.

    Examples
    --------
    >>> extract_pz("0101_20100101.ch")  # doctest: +SKIP

    Extract all channel with specified suffix and output directory:

    >>> extract_pz("0101_20100101.ch", suffix="", outdir="20100101000")  # doctest: +SKIP

    Extract only specified channels:

    >>> extract_pz("0101_20100101.ch",
    ...            filter_by_name="N.NA*", filter_by_channel='[NE]')  # doctest: +SKIP
    """
    channels = _get_channels(ctable)
    if filter_by_chid or filter_by_name or filter_by_component:
        channels = _filter_channels(channels,
                                    filter_by_name,
                                    filter_by_chid,
                                    filter_by_component)
    if not os.path.exists(outdir):
        os.mkdir(outdir)

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
    """Filter channels by id, name, and/or component.

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
            raise ValueError("Incorrect key: only id|name|component are supported.")
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


def _extract_channel(winfile, channel,
                     suffix="SAC", outdir=".", prmfile="win.prm", pmax=2000000):
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
    # win2sac_32 always need a suffix
    sacsuffix = "SAC" if suffix == '' else suffix
    subprocess.call(['win2sac_32',
                     winfile,
                     channel.id,
                     sacsuffix,
                     outdir,
                     '-e',
                     '-p'+prmfile,
                     '-m'+str(pmax)],
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL)
    if suffix == '':  # remove extra suffix
        filename = "{}.{}.SAC".format(channel.name, channel.component)
        filename = os.path.join(outdir, filename)
        os.rename(filename, filename[:-4])


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

    if channel.unit != 'm/s':  # only works for velocity
        print("Warning: {}.{} isn't velocity in m/s".format(channel.name, channel.component))

    try:
        freq = 2.0 * math.pi / channel.period
    except ZeroDivisionError:
        print("Warning: {}.{} Natural period = 0!".format(channel.name, channel.component))

    A0 = 2 * channel.damping
    factor = math.pow(10, channel.preamplification/20.0)
    constant = channel.gain * factor / channel.lsb_value * A0

    real, imaginary = _find_poles(channel.damping, freq)

    pzfile = "{}.{}".format(channel.name, channel.component)
    if suffix:
        pzfile += '.' + suffix
    pzfile = os.path.join(outdir, pzfile)
    _write_pz(pzfile, real, imaginary, constant)

    return pzfile


def merge(datas, final_data, force_sort=False):
    """Merge several win32 files to one win32 file.

    >>> merge(['001.cnt', '002.cnt', '003.cnt'], "final.cnt")  # doctest: +SKIP

    Parameters
    ----------
    datas: list of str
        Win32 files to be merged.
    final_data: str
        Name of the final win32 file.
    force_sort: bool
        Sort all win32 files by date.
    """
    cmd = ['catwin32', '-o', final_data]
    if force_sort:  # add -s option to force sort
        cmd.append('-s')

    subprocess.call(cmd + datas,
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL)


if __name__ == '__main__':
    import doctest
    doctest.testmod()
