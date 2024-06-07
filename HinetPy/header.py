"""
This module provides a dict of seismic networks that are available from the Hi-net
website.

The dict is named ``NETWORK``. The network code is the key of the dict, and the value is
a :class:`~HinetPy.header.Network` object, which contains the network name, number of
channels, start time when waveform data is available, and the homepage URL. The network
code is a string, e.g., "0101" for Hi-net. The number of channels, start time, and
homepage URL are obtained from the Hi-net website, but they may not be up-to-date so
don't rely on them too much.

To view the list of supported networks, use:

>>> from HinetPy import NETWORK
>>> for code in NETWORK.keys():
...     print(code, NETWORK[code].name)
0101 NIED Hi-net
0103 NIED F-net (broadband)
0103A NIED F-net (strong motion)
0106 NIED Temp. obs. in eastern Shikoku
0120 NIED S-net (velocity)...
"""

from __future__ import annotations

from datetime import datetime


class Network:
    def __init__(
        self, name: str, channels: int | None, starttime: str | datetime, url: str
    ):
        """
        A seismic network and its information.

        Parameters
        ----------
        name
            Network name.
        channels
            Number of channels the network has.
        starttime
            Start time (JST: UTC+0900) when waveform data is avaiable.
        url
            Homepage of the network.
        """
        self.name = name
        self.channels = channels
        self.starttime = starttime
        self.url = url


URL = {
    "Hinet": "http://www.hinet.bosai.go.jp",
    "Fnet": "http://www.fnet.bosai.go.jp",
    "Vnet": "http://www.vnet.bosai.go.jp",
    "JMA": "http://www.jma.go.jp/jma/indexe.html",
    "Snet": "https://www.seafloor.bosai.go.jp/",
}
JMA_VNET = "JMA Volcanic Seismometer Network "

# fmt: off
_networks = [
    ("0101", "NIED Hi-net", 2336, "20040401", URL["Hinet"]),
    ("0103", "NIED F-net (broadband)", 438, "20040401", URL["Fnet"]),
    ("0103A", "NIED F-net (strong motion)", 438, "20040401", URL["Fnet"]),
    ("010501", "NIED V-net (Tokachidake)", 33, "20100401", URL["Vnet"]),
    ("010502", "NIED V-net (Tarumaesan)", 33, "20100401", URL["Vnet"]),
    ("010503", "NIED V-net (Usuzan)", 33, "20100401", URL["Vnet"]),
    ("010504", "NIED V-net (Hokkaido-Komagatake)", 33, "20100401", URL["Vnet"]),
    ("010505", "NIED V-net (Iwatesan)", 33, "20100401", URL["Vnet"]),
    ("010506", "NIED V-net (Nasudake)", 42, "20100401", URL["Vnet"]),
    ("010507", "NIED V-net (Asamayama)", 33, "20100401", URL["Vnet"]),
    ("010508", "NIED V-net (Kusatsu-Shiranesan)", 33, "20100401", URL["Vnet"]),
    ("010509", "NIED V-net (Fujisan)", 57, "20100401", URL["Vnet"]),
    ("010510", "NIED V-net (Miyakejima)", 40, "20100401", URL["Vnet"]),
    ("010511", "NIED V-net (Izu-Oshima)", 39, "20100401", URL["Vnet"]),
    ("010512", "NIED V-net (Asosan)", 44, "20100401", URL["Vnet"]),
    ("010513", "NIED V-net (Unzendake)", 33, "20100401", URL["Vnet"]),
    ("010514", "NIED V-net (Kirishimayama)", 22, "20100401", URL["Vnet"]),
    ("0106", "NIED Temp. obs. in eastern Shikoku", 15, "20151013", "https://doi.org/10.17598/NIED.0027"),
    ("0120", "NIED S-net (velocity)", 450, "20160815", URL["Hinet"]),
    ("0120A", "NIED S-net (acceleration)", 450, "20160815", URL["Hinet"]),
    ("0120B", "NIED S-net (acceleration 2LG)", 450, "20160815", URL["Hinet"]),
    ("0120C", "NIED S-net (acceleration 2HG)", 450, "20160815", URL["Hinet"]),
    ("0131", "NIED MeSO-net", 900, "20170401", URL["Hinet"]),
    ("0201", "Hokkaido University", 205, "20040401", "http://www.sci.hokudai.ac.jp/isv/english/"),
    ("0202", "Tohoku University", 157, "20040401", "http://www.aob.geophys.tohoku.ac.jp/aob-e/"),
    ("0203", "Tokyo University", 316, "20040401", "http://www.eri.u-tokyo.ac.jp/eng/"),
    ("0204", "Kyoto University", 196, "20040401", "http://www.dpri.kyoto-u.ac.jp/en/"),
    ("0205", "Kyushu University", 73, "20040401", "http://www.sevo.kyushu-u.ac.jp/index-e.html"),
    ("0206", "Hirosaki University", 13, "20040401", "http://hrsryu.geo.hirosaki-u.ac.jp/"),
    ("0207", "Nagoya University", 75, "20040401", "http://www.seis.nagoya-u.ac.jp/index_e/"),
    ("0208", "Kochi University", 34, "20040401", "http://www-en.kochi-u.ac.jp/"),
    ("0209", "Kagoshima University", 48, "20040401", "http://leopard.sci.kagoshima-u.ac.jp/noev/English/home.htm"),
    ("0231", "MeSO-net (~2017.03)", 900, "20080516", ""),
    ("0301", "JMA Seismometer Network", 872, "20040401", URL["JMA"]),
    ("030201", JMA_VNET + "(Atosanupuri)", 18, "20101201", URL["JMA"]),
    ("030202", JMA_VNET + "(Meakandake)", 16, "20101201", URL["JMA"]),
    ("030203", JMA_VNET + "(Taisetsuzan)", 9, "20101201", URL["JMA"]),
    ("030204", JMA_VNET + "(Tokachidake)", 32, "20101201", URL["JMA"]),
    ("030205", JMA_VNET + "(Tarumaesan)", 27, "20101201", URL["JMA"]),
    ("030206", JMA_VNET + "(Kuttara)", 15, "20101201", URL["JMA"]),
    ("030207", JMA_VNET + "(Usuzan)", 24, "20101201", URL["JMA"]),
    ("030208", JMA_VNET + "(Hokkaido-Komagatake)", 30, "20101201", URL["JMA"]),
    ("030209", JMA_VNET + "(Esan)", 14, "20101201", URL["JMA"]),
    ("030210", JMA_VNET + "(Iwakisan)", 9, "20101201", URL["JMA"]),
    ("030211", JMA_VNET + "(Akita-Yakeyama)", 11, "20101201", URL["JMA"]),
    ("030212", JMA_VNET + "(Iwatesan)", 17, "20101201", URL["JMA"]),
    ("030213", JMA_VNET + "(Akita-Komagatake)", 14, "20101201", URL["JMA"]),
    ("030214", JMA_VNET + "(Chokaisan)", 6, "20101201", URL["JMA"]),
    ("030215", JMA_VNET + "(Kurikomayama)", 11, "20101201", URL["JMA"]),
    ("030216", JMA_VNET + "(Zaozan)", 15, "20101201", URL["JMA"]),
    ("030217", JMA_VNET + "(Azumayama)", 28, "20101201", URL["JMA"]),
    ("030218", JMA_VNET + "(Adatarayama)", 19, "20101201", URL["JMA"]),
    ("030219", JMA_VNET + "(Bandaisan)", 18, "20101201", URL["JMA"]),
    ("030220", JMA_VNET + "(Nasudake)", 15, "20101201", URL["JMA"]),
    ("030221", JMA_VNET + "(Nikko-Shiranesan)", 11, "20101201", URL["JMA"]),
    ("030222", JMA_VNET + "(Kusatsu-Shiranesan)", 21, "20101201", URL["JMA"]),
    ("030223", JMA_VNET + "(Asamayama)", 44, "20101201", URL["JMA"]),
    ("030224", JMA_VNET + "(Niigata-Yakeyama)", 14, "20101201", URL["JMA"]),
    ("030225", JMA_VNET + "(Yakedake)", 15, "20101201", URL["JMA"]),
    ("030226", JMA_VNET + "(Norikuradake)", 9, "20101201", URL["JMA"]),
    ("030227", JMA_VNET + "(Ontakesan)", 40, "20101201", URL["JMA"]),
    ("030228", JMA_VNET + "(Hakusan)", 10, "20101201", URL["JMA"]),
    ("030229", JMA_VNET + "(Fujisan)", 27, "20101201", URL["JMA"]),
    ("030230", JMA_VNET + "(Hakoneyama)", 11, "20101201", URL["JMA"]),
    ("030231", JMA_VNET + "(Izu-Tobu Volcanoes)", 18, "20101201", URL["JMA"]),
    ("030232", JMA_VNET + "(Izu-Oshima)", 22, "20101201", URL["JMA"]),
    ("030233", JMA_VNET + "(Niijima)", 9, "20101201", URL["JMA"]),
    ("030234", JMA_VNET + "(Kozushima)", 9, "20101201", URL["JMA"]),
    ("030235", JMA_VNET + "(Miyakejima)", 19, "20101201", URL["JMA"]),
    ("030236", JMA_VNET + "(Hachijojima)", 11, "20101201", URL["JMA"]),
    ("030237", JMA_VNET + "(Aogashima)", 9, "20101201", URL["JMA"]),
    ("030238", JMA_VNET + "(Tsurumidake and Garandake)", 16, "20101201", URL["JMA"]),
    ("030239", JMA_VNET + "(Kujusan)", 13, "20101201", URL["JMA"]),
    ("030240", JMA_VNET + "(Asosan)", 31, "20101201", URL["JMA"]),
    ("030241", JMA_VNET + "(Unzendake)", 28, "20101201", URL["JMA"]),
    ("030242", JMA_VNET + "(Kirishimayama)", 66, "20101201", URL["JMA"]),
    ("030243", JMA_VNET + "(Sakurajima)", 31, "20101201", URL["JMA"]),
    ("030244", JMA_VNET + "(Satsuma-Iojima)", 16, "20101201", URL["JMA"]),
    ("030245", JMA_VNET + "(Kuchinoerabujima)", 29, "20101201", URL["JMA"]),
    ("030246", JMA_VNET + "(Suwanosejima)", 12, "20101201", URL["JMA"]),
    ("030247", JMA_VNET + "(Hakkodasan)", 18, "20101201", URL["JMA"]),
    ("030248", JMA_VNET + "(Towada)", 9, "20101201", URL["JMA"]),
    ("030249", JMA_VNET + "(Midagahara)", 9, "20101201", URL["JMA"]),
    ("0401", "JAMSTEC Realtime Data from the Deep Sea Floor Observatory", 73, "20040401", "http://www.jamstec.go.jp/e/index.html"),
    ("0402", "NIED DONET1 (broadband)", 132, "20160401", URL["Snet"]),
    ("0402A", "NIED DONET1 (strong motion)", 132, "20160401", URL["Snet"]),
    ("0402N", "JAMSTEC NIED DONET1 (broadband)", 132, "20160401", URL["Snet"]),
    ("0402AN", "JAMSTEC NIED DONET1 (strong motion)", 132, "20160401", URL["Snet"]),
    ("0403", "NIED DONET2 (broadband)", 174, "20160401", URL["Snet"]),
    ("0403A", "NIED DONET2 (strong motion)", 174, "20160401", URL["Snet"]),
    ("0403N", "JAMSTEC NIED DONET2 (broadband)", 174, "20160401", URL["Snet"]),
    ("0403AN", "JAMSTEC NIED DONET2 (strong motion)", 174, "20160401", URL["Snet"]),
    ("0501", "AIST", 84, "20040401", "http://www.aist.go.jp/index_en.html"),
    ("0601", "GSI", 6, "20040401", "http://www.gsi.go.jp/ENGLISH/index.html"),
    ("0701", "Tokyo Metropolitan Government", 54, "20040401", "http://www.metro.tokyo.jp/ENGLISH/index.htm"),
    ("0702", "Hot Spring Research Institute of Kanagawa Prefecture", 42, "20040401", "http://www.onken.odawara.kanagawa.jp/"),
    ("0703", "Aomori Prefectural Government", 15, "20040401", "http://www.pref.aomori.lg.jp/foreigners/"),
    ("0705", "Shizuoka Prefectural Government", 3, "20040615", "http://www.pref.shizuoka.jp/a_foreign/english/"),
    ("0801", "ADEP", 780, "20150101", "http://www.adep.or.jp/"),
]
# fmt: on

NETWORK = {
    code: Network(name, channels, datetime.strptime(starttime, "%Y%m%d"), url)
    for code, name, channels, starttime, url in _networks
}
