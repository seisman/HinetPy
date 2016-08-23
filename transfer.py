#!/usr/bin/env python
# -*- coding: utf8 -*-
import os
import sys
import glob
import subprocess

os.putenv("SAC_DISPLAY_COPYRIGHT", "0")

if len(sys.argv) != 2:
    sys.exit("Usage: python %s dirname\n" % sys.argv[0])

dir = sys.argv[1]

os.chdir(dir)

p = subprocess.Popen(['sac'], stdin=subprocess.PIPE)

s = ""
for sacfile in glob.glob("*.SAC"):
    net, sta, loc, chn = sacfile.split('.')[0:4]
    pz = glob.glob("SAC_PZs_%s_%s_%s_%s_*_*" % (net, sta, chn, loc))
    # 暂不考虑多个PZ文件的情况
    if len(pz) != 1:
        sys.exit("PZ file error for %s" % sacfile)

    s += "r %s \n" % sacfile
    s += "rmean; rtr; taper \n"
    s += "trans from pol s %s to none freq 0.01 0.02 5 10\n" % pz[0]
    s += "mul 1.0e9 \n"
    s += "w over \n"

s += "q \n"
p.communicate(s.encode())

os.chdir("..")
