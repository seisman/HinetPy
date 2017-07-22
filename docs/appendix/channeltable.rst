Channel Table file
==================

Channel table file contains important information about channels.

Below is an example of one channel in channel table file::

    6033 1 0 N.AAKH U 6 27 175.60 m/s 1.00 0.70 0 1.023e-07 36.3726 137.9203 483 0 0 Azuminoakashina

- [1]: Hexadecimal channel number (2-byte)
- [2]: Recording flag
- [3]: Delay time on a circuit (ms)
- [4]: Station code
- [5]: Motion component code
- [6]: Reduction ratio of monitoring waveform (expressed as the integer exponent of a power of 2)
- [7]: Quantization bit rate in A/D conversion
- [8]: Sensor sensitivity (V/unit of input, where unit of input is provided in column [9])
- [9]: Unit of input. Use MKS system: "m" for displacement, "m/s" for velocity, and "m/s/s" for acceleration.
- [10]: Natural period of the seismometer (s)
- [11]: Damping constant of the sensor
- [12]: Amplification factor applied to sensor output prior to A/D conversion (dB)
- [13]: Quantization width in A/D conversion (V), a.k.a. LSB value
- [14]: Station latitude (degrees). A positive value indicates North latitude.
- [15]: Station longitude (degrees). A positive value indicates East longitude.
- [16]: Station height (m)
- [17]: Station correction for P-wave (s)
- [18]: Station correction for S-wave (s)
- [19]: Station name (Optional)
