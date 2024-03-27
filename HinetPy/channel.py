import logging
import math

# Setup the logger
FORMAT = "[%(asctime)s] %(levelname)s: %(message)s"
logging.basicConfig(level=logging.INFO, format=FORMAT, datefmt="%Y-%m-%d %H:%M:%S")
logger = logging.getLogger(__name__)


class Channel:
    """
    Class for channel information.
    """

    def __init__(  # noqa: PLR0913
        self,
        id=None,  # noqa: A002
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
    ):
        """
        Initialize a channel.

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
            Preamplification value.
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
            Name of the SAC polezero file.
        keep_sensitivity: bool
            Keep sensitivity in the SAC polezero "CONSTANT" or not.
        """
        chan_info = f"{self.name}.{self.component} ({self.id})"
        # Hi-net uses a moving-coil velocity-type seismometer.
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
        imaginary = freq * math.sqrt(1.0 - self.damping**2.0)

        # calculate the CONSTANT
        fn = 20.0  # alaways assume normalization frequency is 20 Hz
        s = complex(0, 2 * math.pi * fn)
        a0 = abs((s**2 + 2 * self.damping * freq * s + freq**2) / s**2)
        if keep_sensitivity:
            factor = math.pow(10, self.preamplification / 20.0)
            constant = a0 * self.gain * factor / self.lsb_value
        else:
            constant = a0

        # write information to a SAC PZ file
        with open(pzfile, "w", encoding="utf8") as pz:
            pz.write("ZEROS 3\n")
            pz.write("POLES 2\n")
            pz.write(f"{real:9.6f} {imaginary:9.6f}\n")
            pz.write(f"{real:9.6f} {-imaginary:9.6f}\n")
            pz.write(f"CONSTANT {constant:e}\n")
