# -*- coding: utf-8 -*-

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

network['0401'] = Network(name='JAMSTEC Realtime Data from the Deep Sea Floor Observatory',
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
network['0702'] = Network(name='Hot Spring Research Institute of Kanagawa Prefecture',
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

network['030201'] = Network(name='JMA Volcanic Seismometer Network (Atosanupuri)',
                            channels=7,
                            starttime=datetime(2010, 12, 1, 0, 0))
network['030202'] = Network(name='JMA Volcanic Seismometer Network (Meakandake)',
                            channels=16,
                            starttime=datetime(2010, 12, 1, 0, 0))
network['030203'] = Network(name='JMA Volcanic Seismometer Network (Taisetsuzan)',
                            channels=4,
                            starttime=datetime(2010, 12, 1, 0, 0))
network['030204'] = Network(name='JMA Volcanic Seismometer Network (Tokachidake)',
                            channels=23,
                            starttime=datetime(2010, 12, 1, 0, 0))
network['030205'] = Network(name='JMA Volcanic Seismometer Network (Tarumaesan)',
                            channels=18,
                            starttime=datetime(2010, 12, 1, 0, 0))
network['030206'] = Network(name='JMA Volcanic Seismometer Network (Kuttara)',
                            channels=4,
                            starttime=datetime(2010, 12, 1, 0, 0))
network['030207'] = Network(name='JMA Volcanic Seismometer Network (Usuzan)',
                            channels=15,
                            starttime=datetime(2010, 12, 1, 0, 0))
network['030208'] = Network(name='JMA Volcanic Seismometer Network (Hokkaido-Komagatake)',
                            channels=20,
                            starttime=datetime(2010, 12, 1, 0, 0))
network['030209'] = Network(name='JMA Volcanic Seismometer Network (Esan)',
                            channels=7,
                            starttime=datetime(2010, 12, 1, 0, 0))
network['030210'] = Network(name='JMA Volcanic Seismometer Network (Iwakisan)',
                            channels=4,
                            starttime=datetime(2010, 12, 1, 0, 0))
network['030211'] = Network(name='JMA Volcanic Seismometer Network (Akita-Yakeyama)',
                            channels=4,
                            starttime=datetime(2010, 12, 1, 0, 0))
network['030212'] = Network(name='JMA Volcanic Seismometer Network (Iwatesan)',
                            channels=10,
                            starttime=datetime(2010, 12, 1, 0, 0))
network['030213'] = Network(name='JMA Volcanic Seismometer Network (Akita-Komagatake)',
                            channels=7,
                            starttime=datetime(2010, 12, 1, 0, 0))
network['030214'] = Network(name='JMA Volcanic Seismometer Network (Chokaisan)',
                            channels=4,
                            starttime=datetime(2010, 12, 1, 0, 0))
network['030215'] = Network(name='JMA Volcanic Seismometer Network (Kurikomayama)',
                            channels=4,
                            starttime=datetime(2010, 12, 1, 0, 0))
network['030216'] = Network(name='JMA Volcanic Seismometer Network (Zaozan)',
                            channels=4,
                            starttime=datetime(2010, 12, 1, 0, 0))
network['030217'] = Network(name='JMA Volcanic Seismometer Network (Azumayama)',
                            channels=17,
                            starttime=datetime(2010, 12, 1, 0, 0))
network['030218'] = Network(name='JMA Volcanic Seismometer Network (Adatarayama)',
                            channels=8,
                            starttime=datetime(2010, 12, 1, 0, 0))
network['030219'] = Network(name='JMA Volcanic Seismometer Network (Bandaisan)',
                            channels=11,
                            starttime=datetime(2010, 12, 1, 0, 0))
network['030220'] = Network(name='JMA Volcanic Seismometer Network (Nasudake)',
                            channels=8,
                            starttime=datetime(2010, 12, 1, 0, 0))
network['030221'] = Network(name='JMA Volcanic Seismometer Network (Nikko-Shiranesan)',
                            channels=4,
                            starttime=datetime(2010, 12, 1, 0, 0))
network['030222'] = Network(name='JMA Volcanic Seismometer Network (Kusatsu-Shiranesan)',
                            channels=8,
                            starttime=datetime(2010, 12, 1, 0, 0))
network['030223'] = Network(name='JMA Volcanic Seismometer Network (Asamayama)',
                            channels=24,
                            starttime=datetime(2010, 12, 1, 0, 0))
network['030224'] = Network(name='JMA Volcanic Seismometer Network (Niigata-Yakeyama)',
                            channels=4,
                            starttime=datetime(2010, 12, 1, 0, 0))
network['030225'] = Network(name='JMA Volcanic Seismometer Network (Yakedake)',
                            channels=4,
                            starttime=datetime(2010, 12, 1, 0, 0))
network['030226'] = Network(name='JMA Volcanic Seismometer Network (Norikuradake)',
                            channels=4,
                            starttime=datetime(2010, 12, 1, 0, 0))
network['030227'] = Network(name='JMA Volcanic Seismometer Network (Ontakesan)',
                            channels=8,
                            starttime=datetime(2010, 12, 1, 0, 0))
network['030228'] = Network(name='JMA Volcanic Seismometer Network (Hakusan)',
                            channels=4,
                            starttime=datetime(2010, 12, 1, 0, 0))
network['030229'] = Network(name='JMA Volcanic Seismometer Network (Fujisan)',
                            channels=18,
                            starttime=datetime(2010, 12, 1, 0, 0))
network['030230'] = Network(name='JMA Volcanic Seismometer Network (Hakoneyama)',
                            channels=4,
                            starttime=datetime(2010, 12, 1, 0, 0))
network['030231'] = Network(name='JMA Volcanic Seismometer Network (Izu-Tobu Volcanoes)',
                            channels=11,
                            starttime=datetime(2010, 12, 1, 0, 0))
network['030232'] = Network(name='JMA Volcanic Seismometer Network (Izu-Oshima)',
                            channels=16,
                            starttime=datetime(2010, 12, 1, 0, 0))
network['030233'] = Network(name='JMA Volcanic Seismometer Network (Niijima)',
                            channels=4,
                            starttime=datetime(2010, 12, 1, 0, 0))
network['030234'] = Network(name='JMA Volcanic Seismometer Network (Kozushima)',
                            channels=4,
                            starttime=datetime(2010, 12, 1, 0, 0))
network['030235'] = Network(name='JMA Volcanic Seismometer Network (Miyakejima)',
                            channels=14,
                            starttime=datetime(2010, 12, 1, 0, 0))
network['030236'] = Network(name='JMA Volcanic Seismometer Network (Hachijojima)',
                            channels=4,
                            starttime=datetime(2010, 12, 1, 0, 0))
network['030237'] = Network(name='JMA Volcanic Seismometer Network (Aogashima)',
                            channels=4,
                            starttime=datetime(2010, 12, 1, 0, 0))
network['030238'] = Network(name='JMA Volcanic Seismometer Network (Tsurumidake and Garandake)',
                            channels=7,
                            starttime=datetime(2010, 12, 1, 0, 0))
network['030239'] = Network(name='JMA Volcanic Seismometer Network (Kujusan)',
                            channels=4,
                            starttime=datetime(2010, 12, 1, 0, 0))
network['030240'] = Network(name='JMA Volcanic Seismometer Network (Asosan)',
                            channels=18,
                            starttime=datetime(2010, 12, 1, 0, 0))
network['030241'] = Network(name='JMA Volcanic Seismometer Network (Unzendake)',
                            channels=10,
                            starttime=datetime(2010, 12, 1, 0, 0))
network['030242'] = Network(name='JMA Volcanic Seismometer Network (Kirishimayama)',
                            channels=19,
                            starttime=datetime(2010, 12, 1, 0, 0))
network['030243'] = Network(name='JMA Volcanic Seismometer Network (Sakurajima)',
                            channels=25,
                            starttime=datetime(2010, 12, 1, 0, 0))
network['030244'] = Network(name='JMA Volcanic Seismometer Network (Satsuma-Iojima)',
                            channels=7,
                            starttime=datetime(2010, 12, 1, 0, 0))
network['030245'] = Network(name='JMA Volcanic Seismometer Network (Kuchinoerabujima)',
                            channels=13,
                            starttime=datetime(2010, 12, 1, 0, 0))
network['030246'] = Network(name='JMA Volcanic Seismometer Network (Suwanosejima)',
                            channels=6,
                            starttime=datetime(2010, 12, 1, 0, 0))
network['030247'] = Network(name='JMA Volcanic Seismometer Network (Hakkodasan)',
                            channels=9,
                            starttime=datetime(2010, 12, 1, 0, 0))
