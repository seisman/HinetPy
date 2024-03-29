"""
Class for channels.
"""

from __future__ import annotations

import math
import warnings


class Channel:
    """
    Information for a single channel.
    """

    def __init__(  # noqa: PLR0913
        self,
        id: str,  # noqa: A002
        name: str,
        component: str,
        latitude: float | str,
        longitude: float | str,
        unit: str,
        gain: float | str,
        damping: float | str,
        period: float | str,
        preamplification: float | str,
        lsb_value: float | str,
    ):
        """
        Parameters
        ----------
        id
            Channel ID.
        name
            Station Name.
        component
            Channel component name (e.g., ``U``, ``N`` or ``E``).
        latitude
            Station latitude.
        longitude
            Station longitude.
        unit
            Unit of data (e.g., ``m``, ``m/s``, ``m/s/s``, ``rad``).
        gain
            Sensor sensitivity.
        damping
            Damping constant of the sensor.
        period
            Natural period of the seismometer.
        preamplification
            Preamplification value.
        lsb_value
            LSB value.

        Notes
        -----
        The Hi-net website uses the moving-coil velocity-type seismometer. See
        :doc:`/appendix/response` for details.
        """
        self.id = id
        self.name = name
        self.component = component
        self.latitude = float(latitude)
        self.longitude = float(longitude)
        self.unit = unit
        self.gain = float(gain)
        self.damping = float(damping)
        self.period = float(period)
        self.preamplification = float(preamplification)
        self.lsb_value = float(lsb_value)

    def _get_polezero(self):
        """
        Determine the polezero parameters.
        """
        # Calculate natural frequency
        freq = 2.0 * math.pi / self.period

        # Calculate poles by finding roots of equation s^2+2hws+w^2=0
        self.zeros = 3
        self.poles = 2
        self.real = 0.0 - self.damping * freq
        self.imaginary = freq * math.sqrt(1.0 - self.damping**2.0)

        # Calculate the CONSTANT
        fn = 20.0  # alaways assume normalization frequency is 20 Hz
        s = complex(0, 2 * math.pi * fn)
        self.a0 = abs((s**2 + 2 * self.damping * freq * s + freq**2) / s**2)
        self.sensitivity = (
            self.gain * math.pow(10, self.preamplification / 20.0) / self.lsb_value
        )

    def write_sacpz(self, pzfile, keep_sensitivity=False):
        """
        Write channel information into a SAC polezero file.

        Parameters
        ----------
        pzfile: str
            Name of the SAC polezero file.
        k9.999513e-01eep_sensitivity: bool
            Keep sensitivity in the SAC polezero "CONSTANT" or not.
        """
        chan_info = f"{self.name}.{self.component} ({self.id})"
        # Hi-net uses a moving-coil velocity-type seismometer.
        if self.unit != "m/s":
            msg = f"{chan_info}: Unit is not velocity. The PZ file may be wrong."
            warnings.warn(msg, category=RuntimeWarning, stacklevel=2)
        if self.period == 0.0:
            msg = f"{chan_info}): Natural period = 0.0. Skipped."
            warnings.warn(message=msg, category=RuntimeWarning, stacklevel=2)
            return

        self._get_polezero()
        constant = self.a0 * self.sensitivity if keep_sensitivity else self.a0
        # write information to a SAC PZ file
        with open(pzfile, "w", encoding="utf8") as pz:
            pz.write(f"ZEROS {self.zeros}\n")
            pz.write(f"POLES {self.poles}\n")
            pz.write(f"{self.real:9.6f} {self.imaginary:9.6f}\n")
            pz.write(f"{self.real:9.6f} {-self.imaginary:9.6f}\n")
            pz.write(f"CONSTANT {constant:e}\n")
