"""
Regression tests for issue #152: stale/missing results reported silently.

Uses a fake Popen so no win2sac_32 binary, account, or network is needed.
"""

import logging
import os

from HinetPy import win32
from HinetPy.channel import Channel


def _make_channel():
    return Channel(
        id="3e81",
        name="N.NGUH",
        component="U",
        latitude=35.0,
        longitude=140.0,
        unit="m/s",
        gain=1000.0,
        damping=0.7,
        period=1.0,
        preamplification=20.0,
        lsb_value=0.001,
    )


class _FakeStderr:
    def __init__(self, text):
        self._text = text

    def read(self):
        return self._text.encode()


class _FakeProc:
    """Mimics Popen as used in _extract_channel_sac (context manager)."""

    def __init__(self, text):
        self.stderr = _FakeStderr(text)

    def __enter__(self):
        return self

    def __exit__(self, *args):
        return False


def _fake_popen_no_data(*args, **kwargs):
    return _FakeProc("Data for channel 3e81 not existed\n")


def test_no_data_warns_about_stale_file(tmp_path, monkeypatch, caplog):
    channel = _make_channel()
    stale = tmp_path / "N.NGUH.U.SAC"
    stale.write_text("DATO VIEJO", encoding="utf8")
    monkeypatch.setattr(win32, "Popen", _fake_popen_no_data)
    with caplog.at_level(logging.WARNING, logger="HinetPy.win32"):
        result = win32._extract_channel_sac("dummy.cnt", channel, outdir=str(tmp_path))
    assert result is None
    assert any("may be stale" in r.message for r in caplog.records)


def test_no_data_without_stale_file_warns_once(tmp_path, monkeypatch, caplog):
    channel = _make_channel()
    monkeypatch.setattr(win32, "Popen", _fake_popen_no_data)
    with caplog.at_level(logging.WARNING, logger="HinetPy.win32"):
        result = win32._extract_channel_sac("dummy.cnt", channel, outdir=str(tmp_path))
    assert result is None
    assert not any("may be stale" in r.message for r in caplog.records)
    assert any("not exists" in r.message for r in caplog.records)
    assert not os.path.exists(str(tmp_path / "N.NGUH.U.SAC"))
