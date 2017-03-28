# -*- coding: utf-8 -*-
"""Client related header information."""

from datetime import datetime
from collections import namedtuple

Network = namedtuple('Network', "name, channels, starttime, url")
""" An object containing information of a network.

.. py:attribute:: name

   Network name.

.. py:attribute:: channels

   Number of channels the network has.

.. py:attribute:: starttime

   Start time (in JST time) when waveform data is avaiable.

.. py:attribute:: url

   Network homepage.

``NETWORK`` is a dict of :class:`~HinetPy.header.Network`, containing
information of all networks available from Hi-net website.

>>> from HinetPy.header import NETWORK
>>> for code in NETWORK.keys():
...     print(code, NETWORK[code].name)
"""

NETWORK = {}

NETWORK['0101'] = Network(name='NIED Hi-net',
                          channels=2336,
                          starttime=datetime(2004, 4, 1, 0, 0),
                          url="http://www.hinet.bosai.go.jp/")
NETWORK['0103'] = Network(name='NIED F-net (broadband)',
                          channels=438,
                          starttime=datetime(2004, 4, 1, 0, 0),
                          url="http://www.fnet.bosai.go.jp/")
NETWORK['0103A'] = Network(name='NIED F-net (strong motion)',
                           channels=438,
                           starttime=datetime(2004, 4, 1, 0, 0),
                           url="http://www.fnet.bosai.go.jp/")

NETWORK['0201'] = Network(name='Hokkaido University',
                          channels=183,
                          starttime=datetime(2004, 4, 1, 0, 0),
                          url="http://www.sci.hokudai.ac.jp/isv/english/")
NETWORK['0202'] = Network(name='Tohoku University',
                          channels=157,
                          starttime=datetime(2004, 4, 1, 0, 0),
                          url="http://www.aob.geophys.tohoku.ac.jp/aob-e/")
NETWORK['0203'] = Network(name='Tokyo University',
                          channels=301,
                          starttime=datetime(2004, 4, 1, 0, 0),
                          url="http://www.eri.u-tokyo.ac.jp/eng/")
NETWORK['0204'] = Network(name='Kyoto University',
                          channels=196,
                          starttime=datetime(2004, 4, 1, 0, 0),
                          url="http://www.dpri.kyoto-u.ac.jp/en/")
NETWORK['0205'] = Network(name='Kyushu University',
                          channels=73,
                          starttime=datetime(2004, 4, 1, 0, 0),
                          url="http://www.sevo.kyushu-u.ac.jp/index-e.html")
NETWORK['0206'] = Network(name='Hirosaki University',
                          channels=13,
                          starttime=datetime(2004, 4, 1, 0, 0),
                          url="http://hrsryu.geo.hirosaki-u.ac.jp/")
NETWORK['0207'] = Network(name='Nagoya University',
                          channels=75,
                          starttime=datetime(2004, 4, 1, 0, 0),
                          url="http://www.seis.nagoya-u.ac.jp/index_e/")
NETWORK['0208'] = Network(name='Kochi University',
                          channels=28,
                          starttime=datetime(2004, 4, 1, 0, 0),
                          url="http://www-en.kochi-u.ac.jp/")
NETWORK['0209'] = Network(name='Kagoshima University',
                          channels=45,
                          starttime=datetime(2004, 4, 1, 0, 0),
                          url="http://leopard.sci.kagoshima-u.ac.jp/noev/English/home.htm")

NETWORK['0301'] = Network(name='JMA Seismometer Network',
                          channels=869,
                          starttime=datetime(2004, 4, 1, 0, 0),
                          url="http://www.jma.go.jp/jma/indexe.html")

NETWORK['0401'] = Network(name='JAMSTEC Realtime Data '
                               'from the Deep Sea Floor Observatory',
                          channels=73,
                          starttime=datetime(2004, 4, 1, 0, 0),
                          url="http://www.jamstec.go.jp/e/index.html")
NETWORK['0402'] = Network(name='NIED DONET1 (broadband)',
                          channels=132,
                          starttime=datetime(2014, 10, 1, 0, 0),
                          url="http://www.hinet.bosai.go.jp/?LANG=en")
NETWORK['0402N'] = Network(name='JAMSTEC NIED DONET1 (broadband)',
                           channels=132,
                           starttime=datetime(2014, 10, 1, 0, 0),
                           url="http://www.hinet.bosai.go.jp/?LANG=en")
NETWORK['0402A'] = Network(name='NIED DONET1 (strong motion)',
                           channels=132,
                           starttime=datetime(2014, 10, 1, 0, 0),
                           url="http://www.hinet.bosai.go.jp/?LANG=en")
NETWORK['0402AN'] = Network(name='JAMSTEC NIED DONET1 (broadband)',
                            channels=132,
                            starttime=datetime(2014, 10, 1, 0, 0),
                            url="http://www.hinet.bosai.go.jp/?LANG=en")

NETWORK['0501'] = Network(name='AIST',
                          channels=81,
                          starttime=datetime(2004, 4, 1, 0, 0),
                          url="http://www.aist.go.jp/index_en.html")

NETWORK['0601'] = Network(name='GSI',
                          channels=6,
                          starttime=datetime(2004, 4, 1, 0, 0),
                          url="http://www.gsi.go.jp/ENGLISH/index.html")

NETWORK['0701'] = Network(name='Tokyo Metropolitan Government',
                          channels=54,
                          starttime=datetime(2004, 4, 1, 0, 0),
                          url="http://www.metro.tokyo.jp/ENGLISH/index.htm")
NETWORK['0702'] = Network(name='Hot Spring Research Institute '
                               'of Kanagawa Prefecture',
                          channels=42,
                          starttime=datetime(2004, 4, 1, 0, 0),
                          url="http://www.onken.odawara.kanagawa.jp/")
NETWORK['0703'] = Network(name='Aomori Prefectural Government',
                          channels=15,
                          starttime=datetime(2004, 4, 1, 0, 0),
                          url="http://www.pref.aomori.lg.jp/foreigners/")
NETWORK['0705'] = Network(name='Shizuoka Prefectural Government',
                          channels=3,
                          starttime=datetime(2004, 6, 15, 0, 0),
                          url="http://www.pref.shizuoka.jp/a_foreign/english/")

NETWORK['0801'] = Network(name='ADEP',
                          channels=606,
                          starttime=datetime(2015, 1, 1, 0, 0),
                          url="http://www.adep.or.jp/")

NETWORK['010501'] = Network(name='NIED V-net (Tokachidake)',
                            channels=33,
                            starttime=datetime(2010, 4, 1, 0, 0),
                            url="http://www.vnet.bosai.go.jp/")
NETWORK['010502'] = Network(name='NIED V-net (Tarumaesan)',
                            channels=33,
                            starttime=datetime(2010, 4, 1, 0, 0),
                            url="http://www.vnet.bosai.go.jp/")
NETWORK['010503'] = Network(name='NIED V-net (Usuzan)',
                            channels=33,
                            starttime=datetime(2010, 4, 1, 0, 0),
                            url="http://www.vnet.bosai.go.jp/")
NETWORK['010504'] = Network(name='NIED V-net (Hokkaido-Komagatake)',
                            channels=33,
                            starttime=datetime(2010, 4, 1, 0, 0),
                            url="http://www.vnet.bosai.go.jp/")
NETWORK['010505'] = Network(name='NIED V-net (Iwatesan)',
                            channels=33,
                            starttime=datetime(2010, 4, 1, 0, 0),
                            url="http://www.vnet.bosai.go.jp/")
NETWORK['010506'] = Network(name='NIED V-net (Nasudake)',
                            channels=9,
                            starttime=datetime(2010, 4, 1, 0, 0),
                            url="http://www.vnet.bosai.go.jp/")
NETWORK['010507'] = Network(name='NIED V-net (Asamayama)',
                            channels=33,
                            starttime=datetime(2010, 4, 1, 0, 0),
                            url="http://www.vnet.bosai.go.jp/")
NETWORK['010508'] = Network(name='NIED V-net (Kusatsu-Shiranesan)',
                            channels=33,
                            starttime=datetime(2010, 4, 1, 0, 0),
                            url="http://www.vnet.bosai.go.jp/")
NETWORK['010509'] = Network(name='NIED V-net (Fujisan)',
                            channels=57,
                            starttime=datetime(2010, 4, 1, 0, 0),
                            url="http://www.vnet.bosai.go.jp/")
NETWORK['010510'] = Network(name='NIED V-net (Miyakejima)',
                            channels=40,
                            starttime=datetime(2010, 4, 1, 0, 0),
                            url="http://www.vnet.bosai.go.jp/")
NETWORK['010511'] = Network(name='NIED V-net (Izu-Oshima)',
                            channels=39,
                            starttime=datetime(2010, 4, 1, 0, 0),
                            url="http://www.vnet.bosai.go.jp/")
NETWORK['010512'] = Network(name='NIED V-net (Asosan)',
                            channels=44,
                            starttime=datetime(2010, 4, 1, 0, 0),
                            url="http://www.vnet.bosai.go.jp/")
NETWORK['010513'] = Network(name='NIED V-net (Unzendake)',
                            channels=33,
                            starttime=datetime(2010, 4, 1, 0, 0),
                            url="http://www.vnet.bosai.go.jp/")
NETWORK['010514'] = Network(name='NIED V-net (Kirishimayama)',
                            channels=22,
                            starttime=datetime(2010, 4, 1, 0, 0),
                            url="http://www.vnet.bosai.go.jp/")

JMA_VNET = 'JMA Volcanic Seismometer Network '

NETWORK['030201'] = Network(name=JMA_VNET + '(Atosanupuri)',
                            channels=7,
                            starttime=datetime(2010, 12, 1, 0, 0),
                            url="http://www.jma.go.jp/jma/indexe.html")
NETWORK['030202'] = Network(name=JMA_VNET + '(Meakandake)',
                            channels=16,
                            starttime=datetime(2010, 12, 1, 0, 0),
                            url="http://www.jma.go.jp/jma/indexe.html")
NETWORK['030203'] = Network(name=JMA_VNET + '(Taisetsuzan)',
                            channels=4,
                            starttime=datetime(2010, 12, 1, 0, 0),
                            url="http://www.jma.go.jp/jma/indexe.html")
NETWORK['030204'] = Network(name=JMA_VNET + '(Tokachidake)',
                            channels=23,
                            starttime=datetime(2010, 12, 1, 0, 0),
                            url="http://www.jma.go.jp/jma/indexe.html")
NETWORK['030205'] = Network(name=JMA_VNET + '(Tarumaesan)',
                            channels=18,
                            starttime=datetime(2010, 12, 1, 0, 0),
                            url="http://www.jma.go.jp/jma/indexe.html")
NETWORK['030206'] = Network(name=JMA_VNET + '(Kuttara)',
                            channels=4,
                            starttime=datetime(2010, 12, 1, 0, 0),
                            url="http://www.jma.go.jp/jma/indexe.html")
NETWORK['030207'] = Network(name=JMA_VNET + '(Usuzan)',
                            channels=15,
                            starttime=datetime(2010, 12, 1, 0, 0),
                            url="http://www.jma.go.jp/jma/indexe.html")
NETWORK['030208'] = Network(name=JMA_VNET + '(Hokkaido-Komagatake)',
                            channels=20,
                            starttime=datetime(2010, 12, 1, 0, 0),
                            url="http://www.jma.go.jp/jma/indexe.html")
NETWORK['030209'] = Network(name=JMA_VNET + '(Esan)',
                            channels=7,
                            starttime=datetime(2010, 12, 1, 0, 0),
                            url="http://www.jma.go.jp/jma/indexe.html")
NETWORK['030210'] = Network(name=JMA_VNET + '(Iwakisan)',
                            channels=4,
                            starttime=datetime(2010, 12, 1, 0, 0),
                            url="http://www.jma.go.jp/jma/indexe.html")
NETWORK['030211'] = Network(name=JMA_VNET + '(Akita-Yakeyama)',
                            channels=4,
                            starttime=datetime(2010, 12, 1, 0, 0),
                            url="http://www.jma.go.jp/jma/indexe.html")
NETWORK['030212'] = Network(name=JMA_VNET + '(Iwatesan)',
                            channels=10,
                            starttime=datetime(2010, 12, 1, 0, 0),
                            url="http://www.jma.go.jp/jma/indexe.html")
NETWORK['030213'] = Network(name=JMA_VNET + '(Akita-Komagatake)',
                            channels=7,
                            starttime=datetime(2010, 12, 1, 0, 0),
                            url="http://www.jma.go.jp/jma/indexe.html")
NETWORK['030214'] = Network(name=JMA_VNET + '(Chokaisan)',
                            channels=4,
                            starttime=datetime(2010, 12, 1, 0, 0),
                            url="http://www.jma.go.jp/jma/indexe.html")
NETWORK['030215'] = Network(name=JMA_VNET + '(Kurikomayama)',
                            channels=4,
                            starttime=datetime(2010, 12, 1, 0, 0),
                            url="http://www.jma.go.jp/jma/indexe.html")
NETWORK['030216'] = Network(name=JMA_VNET + '(Zaozan)',
                            channels=4,
                            starttime=datetime(2010, 12, 1, 0, 0),
                            url="http://www.jma.go.jp/jma/indexe.html")
NETWORK['030217'] = Network(name=JMA_VNET + '(Azumayama)',
                            channels=17,
                            starttime=datetime(2010, 12, 1, 0, 0),
                            url="http://www.jma.go.jp/jma/indexe.html")
NETWORK['030218'] = Network(name=JMA_VNET + '(Adatarayama)',
                            channels=8,
                            starttime=datetime(2010, 12, 1, 0, 0),
                            url="http://www.jma.go.jp/jma/indexe.html")
NETWORK['030219'] = Network(name=JMA_VNET + '(Bandaisan)',
                            channels=11,
                            starttime=datetime(2010, 12, 1, 0, 0),
                            url="http://www.jma.go.jp/jma/indexe.html")
NETWORK['030220'] = Network(name=JMA_VNET + '(Nasudake)',
                            channels=8,
                            starttime=datetime(2010, 12, 1, 0, 0),
                            url="http://www.jma.go.jp/jma/indexe.html")
NETWORK['030221'] = Network(name=JMA_VNET + '(Nikko-Shiranesan)',
                            channels=4,
                            starttime=datetime(2010, 12, 1, 0, 0),
                            url="http://www.jma.go.jp/jma/indexe.html")
NETWORK['030222'] = Network(name=JMA_VNET + '(Kusatsu-Shiranesan)',
                            channels=8,
                            starttime=datetime(2010, 12, 1, 0, 0),
                            url="http://www.jma.go.jp/jma/indexe.html")
NETWORK['030223'] = Network(name=JMA_VNET + '(Asamayama)',
                            channels=24,
                            starttime=datetime(2010, 12, 1, 0, 0),
                            url="http://www.jma.go.jp/jma/indexe.html")
NETWORK['030224'] = Network(name=JMA_VNET + '(Niigata-Yakeyama)',
                            channels=4,
                            starttime=datetime(2010, 12, 1, 0, 0),
                            url="http://www.jma.go.jp/jma/indexe.html")
NETWORK['030225'] = Network(name=JMA_VNET + '(Yakedake)',
                            channels=4,
                            starttime=datetime(2010, 12, 1, 0, 0),
                            url="http://www.jma.go.jp/jma/indexe.html")
NETWORK['030226'] = Network(name=JMA_VNET + '(Norikuradake)',
                            channels=4,
                            starttime=datetime(2010, 12, 1, 0, 0),
                            url="http://www.jma.go.jp/jma/indexe.html")
NETWORK['030227'] = Network(name=JMA_VNET + '(Ontakesan)',
                            channels=8,
                            starttime=datetime(2010, 12, 1, 0, 0),
                            url="http://www.jma.go.jp/jma/indexe.html")
NETWORK['030228'] = Network(name=JMA_VNET + '(Hakusan)',
                            channels=4,
                            starttime=datetime(2010, 12, 1, 0, 0),
                            url="http://www.jma.go.jp/jma/indexe.html")
NETWORK['030229'] = Network(name=JMA_VNET + '(Fujisan)',
                            channels=18,
                            starttime=datetime(2010, 12, 1, 0, 0),
                            url="http://www.jma.go.jp/jma/indexe.html")
NETWORK['030230'] = Network(name=JMA_VNET + '(Hakoneyama)',
                            channels=4,
                            starttime=datetime(2010, 12, 1, 0, 0),
                            url="http://www.jma.go.jp/jma/indexe.html")
NETWORK['030231'] = Network(name=JMA_VNET + '(Izu-Tobu Volcanoes)',
                            channels=11,
                            starttime=datetime(2010, 12, 1, 0, 0),
                            url="http://www.jma.go.jp/jma/indexe.html")
NETWORK['030232'] = Network(name=JMA_VNET + '(Izu-Oshima)',
                            channels=16,
                            starttime=datetime(2010, 12, 1, 0, 0),
                            url="http://www.jma.go.jp/jma/indexe.html")
NETWORK['030233'] = Network(name=JMA_VNET + '(Niijima)',
                            channels=4,
                            starttime=datetime(2010, 12, 1, 0, 0),
                            url="http://www.jma.go.jp/jma/indexe.html")
NETWORK['030234'] = Network(name=JMA_VNET + '(Kozushima)',
                            channels=4,
                            starttime=datetime(2010, 12, 1, 0, 0),
                            url="http://www.jma.go.jp/jma/indexe.html")
NETWORK['030235'] = Network(name=JMA_VNET + '(Miyakejima)',
                            channels=14,
                            starttime=datetime(2010, 12, 1, 0, 0),
                            url="http://www.jma.go.jp/jma/indexe.html")
NETWORK['030236'] = Network(name=JMA_VNET + '(Hachijojima)',
                            channels=4,
                            starttime=datetime(2010, 12, 1, 0, 0),
                            url="http://www.jma.go.jp/jma/indexe.html")
NETWORK['030237'] = Network(name=JMA_VNET + '(Aogashima)',
                            channels=4,
                            starttime=datetime(2010, 12, 1, 0, 0),
                            url="http://www.jma.go.jp/jma/indexe.html")
NETWORK['030238'] = Network(name=JMA_VNET + '(Tsurumidake and Garandake)',
                            channels=7,
                            starttime=datetime(2010, 12, 1, 0, 0),
                            url="http://www.jma.go.jp/jma/indexe.html")
NETWORK['030239'] = Network(name=JMA_VNET + '(Kujusan)',
                            channels=4,
                            starttime=datetime(2010, 12, 1, 0, 0),
                            url="http://www.jma.go.jp/jma/indexe.html")
NETWORK['030240'] = Network(name=JMA_VNET + '(Asosan)',
                            channels=18,
                            starttime=datetime(2010, 12, 1, 0, 0),
                            url="http://www.jma.go.jp/jma/indexe.html")
NETWORK['030241'] = Network(name=JMA_VNET + '(Unzendake)',
                            channels=10,
                            starttime=datetime(2010, 12, 1, 0, 0),
                            url="http://www.jma.go.jp/jma/indexe.html")
NETWORK['030242'] = Network(name=JMA_VNET + '(Kirishimayama)',
                            channels=19,
                            starttime=datetime(2010, 12, 1, 0, 0),
                            url="http://www.jma.go.jp/jma/indexe.html")
NETWORK['030243'] = Network(name=JMA_VNET + '(Sakurajima)',
                            channels=25,
                            starttime=datetime(2010, 12, 1, 0, 0),
                            url="http://www.jma.go.jp/jma/indexe.html")
NETWORK['030244'] = Network(name=JMA_VNET + '(Satsuma-Iojima)',
                            channels=7,
                            starttime=datetime(2010, 12, 1, 0, 0),
                            url="http://www.jma.go.jp/jma/indexe.html")
NETWORK['030245'] = Network(name=JMA_VNET + '(Kuchinoerabujima)',
                            channels=13,
                            starttime=datetime(2010, 12, 1, 0, 0),
                            url="http://www.jma.go.jp/jma/indexe.html")
NETWORK['030246'] = Network(name=JMA_VNET + '(Suwanosejima)',
                            channels=6,
                            starttime=datetime(2010, 12, 1, 0, 0),
                            url="http://www.jma.go.jp/jma/indexe.html")
NETWORK['030247'] = Network(name=JMA_VNET + '(Hakkodasan)',
                            channels=9,
                            starttime=datetime(2010, 12, 1, 0, 0),
                            url="http://www.jma.go.jp/jma/indexe.html")
