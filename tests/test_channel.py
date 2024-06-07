"""
Tests for channel.
"""

from HinetPy.channel import Channel


def test_channel():
    """
    Make sure channel calculation is correct.
    """
    chn = Channel(
        id="3e83",
        name="N.NNMH",
        component="U",
        latitude=37.2822,
        longitude=140.2144,
        unit="m/s",
        gain=183.20,
        damping=0.70,
        period=0.98,
        preamplification=0.0,
        lsb_value=1.023e-7,
    )
    chn._get_polezero()
    assert chn.zeros == 3
    assert chn.poles == 2
    assert chn.real == -4.487989505128276
    assert chn.imaginary == 4.578665119846432
    assert chn.a0 == 0.999951325192476
    assert chn.sensitivity == 1790811339.198436
