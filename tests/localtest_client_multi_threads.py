import os
from datetime import datetime

from HinetPy import Client

username = os.environ["HINET_USERNAME"]
password = os.environ["HINET_PASSWORD"]
client = Client(username, password)
starttime = datetime(2017, 1, 1, 0, 0)
client.get_continuous_waveform("0101", starttime, 20, threads=4)
