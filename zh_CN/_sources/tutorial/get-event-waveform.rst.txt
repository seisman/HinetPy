Get Event Waveform
==================

Since v0.6.0, HinetPy supports requesting event waveform data via
:meth:`~HinetPy.client.Client.get_event_waveform`.

Following is a simple example code to request waveforms of events
in a specified time range, magnitude and depth.

>>> from HinetPy import Client
>>> client = Client("username", "password")
>>> client.get_event_waveform('201001010000', '201001020000',
                              minmagnitude=4.0, maxmagnitude=7.0,
                              mindepth=0, maxdepth=70)

You can also limit events to a specified region by three ways:

- specify region code
- specify a box region
- specify a circular region

See :meth:`~HinetPy.client.Client.get_event_waveform` for more available options.
