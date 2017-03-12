# -*- coding: utf-8 -*-
"""Network information."""

from datetime import datetime
from collections import namedtuple

Network = namedtuple('Network', "name, channels, starttime")
"""
.. py:attribute:: name

   Name of network.

.. py:attribute:: channels

   No of channels in each network.

.. py:attribute:: starttime

   Start time when data is avaiable.

>>> network = {}
>>> network['0101'] = Network(name='NIED Hi-net',
                              channels=2336,
                              starttime=datetime(2004, 4, 1, 0, 0))
"""

network = {}

network['0101'] = Network(name='NIED Hi-net',
                          channels=2336,
                          starttime=datetime(2004, 4, 1, 0, 0))
network['0103'] = Network(name='NIED F-net (broadband)',
                          channels=438,
                          starttime=datetime(2004, 4, 1, 0, 0))
network['0103A'] = Network(name='NIED F-net (strong motion)',
                           channels=438,
                           starttime=datetime(2004, 4, 1, 0, 0))

network['0201'] = Network(name='Hokkaido University',
                          channels=183,
                          starttime=datetime(2004, 4, 1, 0, 0))
network['0202'] = Network(name='Tohoku University',
                          channels=157,
                          starttime=datetime(2004, 4, 1, 0, 0))
network['0203'] = Network(name='Tokyo University',
                          channels=301,
                          starttime=datetime(2004, 4, 1, 0, 0))
network['0204'] = Network(name='Kyoto University',
                          channels=196,
                          starttime=datetime(2004, 4, 1, 0, 0))
network['0205'] = Network(name='Kyushu University',
                          channels=73,
                          starttime=datetime(2004, 4, 1, 0, 0))
network['0206'] = Network(name='Hirosaki University',
                          channels=13,
                          starttime=datetime(2004, 4, 1, 0, 0))
network['0207'] = Network(name='Nagoya University',
                          channels=75,
                          starttime=datetime(2004, 4, 1, 0, 0))
network['0208'] = Network(name='Kochi University',
                          channels=28,
                          starttime=datetime(2004, 4, 1, 0, 0))
network['0209'] = Network(name='Kagoshima University',
                          channels=45,
                          starttime=datetime(2004, 4, 1, 0, 0))

network['0301'] = Network(name='JMA Seismometer Network',
                          channels=869,
                          starttime=datetime(2004, 4, 1, 0, 0))

network['0401'] = Network(name='JAMSTEC Realtime Data '
                               'from the Deep Sea Floor Observatory',
                          channels=73,
                          starttime=datetime(2004, 4, 1, 0, 0))
network['0402'] = Network(name='NIED DONET1 (broadband)',
                          channels=132,
                          starttime=datetime(2014, 10, 1, 0, 0))
network['0402A'] = Network(name='NIED DONET1 (strong motion)',
                           channels=132,
                           starttime=datetime(2014, 10, 1, 0, 0))
network['0402N'] = Network(name='JAMSTEC NIED DONET1 (broadband)',
                           channels=132,
                           starttime=datetime(2014, 10, 1, 0, 0))
network['0402AN'] = Network(name='JAMSTEC NIED DONET1 (broadband)',
                            channels=132,
                            starttime=datetime(2014, 10, 1, 0, 0))

network['0501'] = Network(name='AIST',
                          channels=81,
                          starttime=datetime(2004, 4, 1, 0, 0))

network['0601'] = Network(name='GSI',
                          channels=6,
                          starttime=datetime(2004, 4, 1, 0, 0))

network['0701'] = Network(name='Tokyo Metropolitan Government',
                          channels=54,
                          starttime=datetime(2004, 4, 1, 0, 0))
network['0702'] = Network(name='Hot Spring Research Institute '
                               'of Kanagawa Prefecture',
                          channels=42,
                          starttime=datetime(2004, 4, 1, 0, 0))
network['0703'] = Network(name='Aomori Prefectural Government',
                          channels=15,
                          starttime=datetime(2004, 4, 1, 0, 0))
network['0705'] = Network(name='Shizuoka Prefectural Government',
                          channels=3,
                          starttime=datetime(2004, 6, 15, 0, 0))

network['0801'] = Network(name='ADEP',
                          channels=606,
                          starttime=datetime(2015, 1, 1, 0, 0))

network['010501'] = Network(name='NIED V-net (Tokachidake)',
                            channels=33,
                            starttime=datetime(2010, 4, 1, 0, 0))
network['010502'] = Network(name='NIED V-net (Tarumaesan)',
                            channels=33,
                            starttime=datetime(2010, 4, 1, 0, 0))
network['010503'] = Network(name='NIED V-net (Usuzan)',
                            channels=33,
                            starttime=datetime(2010, 4, 1, 0, 0))
network['010504'] = Network(name='NIED V-net (Hokkaido-Komagatake)',
                            channels=33,
                            starttime=datetime(2010, 4, 1, 0, 0))
network['010505'] = Network(name='NIED V-net (Iwatesan)',
                            channels=33,
                            starttime=datetime(2010, 4, 1, 0, 0))
network['010506'] = Network(name='NIED V-net (Nasudake)',
                            channels=9,
                            starttime=datetime(2010, 4, 1, 0, 0))
network['010507'] = Network(name='NIED V-net (Asamayama)',
                            channels=33,
                            starttime=datetime(2010, 4, 1, 0, 0))
network['010508'] = Network(name='NIED V-net (Kusatsu-Shiranesan)',
                            channels=33,
                            starttime=datetime(2010, 4, 1, 0, 0))
network['010509'] = Network(name='NIED V-net (Fujisan)',
                            channels=57,
                            starttime=datetime(2010, 4, 1, 0, 0))
network['010510'] = Network(name='NIED V-net (Miyakejima)',
                            channels=40,
                            starttime=datetime(2010, 4, 1, 0, 0))
network['010511'] = Network(name='NIED V-net (Izu-Oshima)',
                            channels=39,
                            starttime=datetime(2010, 4, 1, 0, 0))
network['010512'] = Network(name='NIED V-net (Asosan)',
                            channels=44,
                            starttime=datetime(2010, 4, 1, 0, 0))
network['010513'] = Network(name='NIED V-net (Unzendake)',
                            channels=33,
                            starttime=datetime(2010, 4, 1, 0, 0))
network['010514'] = Network(name='NIED V-net (Kirishimayama)',
                            channels=22,
                            starttime=datetime(2010, 4, 1, 0, 0))

JMA_VNET = 'JMA Volcanic Seismometer Network '

network['030201'] = Network(name=JMA_VNET + '(Atosanupuri)',
                            channels=7,
                            starttime=datetime(2010, 12, 1, 0, 0))
network['030202'] = Network(name=JMA_VNET + '(Meakandake)',
                            channels=16,
                            starttime=datetime(2010, 12, 1, 0, 0))
network['030203'] = Network(name=JMA_VNET + '(Taisetsuzan)',
                            channels=4,
                            starttime=datetime(2010, 12, 1, 0, 0))
network['030204'] = Network(name=JMA_VNET + '(Tokachidake)',
                            channels=23,
                            starttime=datetime(2010, 12, 1, 0, 0))
network['030205'] = Network(name=JMA_VNET + '(Tarumaesan)',
                            channels=18,
                            starttime=datetime(2010, 12, 1, 0, 0))
network['030206'] = Network(name=JMA_VNET + '(Kuttara)',
                            channels=4,
                            starttime=datetime(2010, 12, 1, 0, 0))
network['030207'] = Network(name=JMA_VNET + '(Usuzan)',
                            channels=15,
                            starttime=datetime(2010, 12, 1, 0, 0))
network['030208'] = Network(name=JMA_VNET + '(Hokkaido-Komagatake)',
                            channels=20,
                            starttime=datetime(2010, 12, 1, 0, 0))
network['030209'] = Network(name=JMA_VNET + '(Esan)',
                            channels=7,
                            starttime=datetime(2010, 12, 1, 0, 0))
network['030210'] = Network(name=JMA_VNET + '(Iwakisan)',
                            channels=4,
                            starttime=datetime(2010, 12, 1, 0, 0))
network['030211'] = Network(name=JMA_VNET + '(Akita-Yakeyama)',
                            channels=4,
                            starttime=datetime(2010, 12, 1, 0, 0))
network['030212'] = Network(name=JMA_VNET + '(Iwatesan)',
                            channels=10,
                            starttime=datetime(2010, 12, 1, 0, 0))
network['030213'] = Network(name=JMA_VNET + '(Akita-Komagatake)',
                            channels=7,
                            starttime=datetime(2010, 12, 1, 0, 0))
network['030214'] = Network(name=JMA_VNET + '(Chokaisan)',
                            channels=4,
                            starttime=datetime(2010, 12, 1, 0, 0))
network['030215'] = Network(name=JMA_VNET + '(Kurikomayama)',
                            channels=4,
                            starttime=datetime(2010, 12, 1, 0, 0))
network['030216'] = Network(name=JMA_VNET + '(Zaozan)',
                            channels=4,
                            starttime=datetime(2010, 12, 1, 0, 0))
network['030217'] = Network(name=JMA_VNET + '(Azumayama)',
                            channels=17,
                            starttime=datetime(2010, 12, 1, 0, 0))
network['030218'] = Network(name=JMA_VNET + '(Adatarayama)',
                            channels=8,
                            starttime=datetime(2010, 12, 1, 0, 0))
network['030219'] = Network(name=JMA_VNET + '(Bandaisan)',
                            channels=11,
                            starttime=datetime(2010, 12, 1, 0, 0))
network['030220'] = Network(name=JMA_VNET + '(Nasudake)',
                            channels=8,
                            starttime=datetime(2010, 12, 1, 0, 0))
network['030221'] = Network(name=JMA_VNET + '(Nikko-Shiranesan)',
                            channels=4,
                            starttime=datetime(2010, 12, 1, 0, 0))
network['030222'] = Network(name=JMA_VNET + '(Kusatsu-Shiranesan)',
                            channels=8,
                            starttime=datetime(2010, 12, 1, 0, 0))
network['030223'] = Network(name=JMA_VNET + '(Asamayama)',
                            channels=24,
                            starttime=datetime(2010, 12, 1, 0, 0))
network['030224'] = Network(name=JMA_VNET + '(Niigata-Yakeyama)',
                            channels=4,
                            starttime=datetime(2010, 12, 1, 0, 0))
network['030225'] = Network(name=JMA_VNET + '(Yakedake)',
                            channels=4,
                            starttime=datetime(2010, 12, 1, 0, 0))
network['030226'] = Network(name=JMA_VNET + '(Norikuradake)',
                            channels=4,
                            starttime=datetime(2010, 12, 1, 0, 0))
network['030227'] = Network(name=JMA_VNET + '(Ontakesan)',
                            channels=8,
                            starttime=datetime(2010, 12, 1, 0, 0))
network['030228'] = Network(name=JMA_VNET + '(Hakusan)',
                            channels=4,
                            starttime=datetime(2010, 12, 1, 0, 0))
network['030229'] = Network(name=JMA_VNET + '(Fujisan)',
                            channels=18,
                            starttime=datetime(2010, 12, 1, 0, 0))
network['030230'] = Network(name=JMA_VNET + '(Hakoneyama)',
                            channels=4,
                            starttime=datetime(2010, 12, 1, 0, 0))
network['030231'] = Network(name=JMA_VNET + '(Izu-Tobu Volcanoes)',
                            channels=11,
                            starttime=datetime(2010, 12, 1, 0, 0))
network['030232'] = Network(name=JMA_VNET + '(Izu-Oshima)',
                            channels=16,
                            starttime=datetime(2010, 12, 1, 0, 0))
network['030233'] = Network(name=JMA_VNET + '(Niijima)',
                            channels=4,
                            starttime=datetime(2010, 12, 1, 0, 0))
network['030234'] = Network(name=JMA_VNET + '(Kozushima)',
                            channels=4,
                            starttime=datetime(2010, 12, 1, 0, 0))
network['030235'] = Network(name=JMA_VNET + '(Miyakejima)',
                            channels=14,
                            starttime=datetime(2010, 12, 1, 0, 0))
network['030236'] = Network(name=JMA_VNET + '(Hachijojima)',
                            channels=4,
                            starttime=datetime(2010, 12, 1, 0, 0))
network['030237'] = Network(name=JMA_VNET + '(Aogashima)',
                            channels=4,
                            starttime=datetime(2010, 12, 1, 0, 0))
network['030238'] = Network(name=JMA_VNET + '(Tsurumidake and Garandake)',
                            channels=7,
                            starttime=datetime(2010, 12, 1, 0, 0))
network['030239'] = Network(name=JMA_VNET + '(Kujusan)',
                            channels=4,
                            starttime=datetime(2010, 12, 1, 0, 0))
network['030240'] = Network(name=JMA_VNET + '(Asosan)',
                            channels=18,
                            starttime=datetime(2010, 12, 1, 0, 0))
network['030241'] = Network(name=JMA_VNET + '(Unzendake)',
                            channels=10,
                            starttime=datetime(2010, 12, 1, 0, 0))
network['030242'] = Network(name=JMA_VNET + '(Kirishimayama)',
                            channels=19,
                            starttime=datetime(2010, 12, 1, 0, 0))
network['030243'] = Network(name=JMA_VNET + '(Sakurajima)',
                            channels=25,
                            starttime=datetime(2010, 12, 1, 0, 0))
network['030244'] = Network(name=JMA_VNET + '(Satsuma-Iojima)',
                            channels=7,
                            starttime=datetime(2010, 12, 1, 0, 0))
network['030245'] = Network(name=JMA_VNET + '(Kuchinoerabujima)',
                            channels=13,
                            starttime=datetime(2010, 12, 1, 0, 0))
network['030246'] = Network(name=JMA_VNET + '(Suwanosejima)',
                            channels=6,
                            starttime=datetime(2010, 12, 1, 0, 0))
network['030247'] = Network(name=JMA_VNET + '(Hakkodasan)',
                            channels=9,
                            starttime=datetime(2010, 12, 1, 0, 0))
