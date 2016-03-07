#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Author: Dongdong Tian @ USTC
#
# Revision History:
#   2014-09-03  Dongdong Tian   Initial Coding
#   2014-10-05  Dongdong Tian   Fix bugs:
#                               - handle datas with more than 2000000 points
#                               - delimite components code with commas
#   2014-11-01  Dongdong Tian   Modify to fit new version of request script
#   2015-03-21  Dongdong Tian   Fix a bug when dirname contains underscore
#   2015-05-18  Dongdong Tian   Keep endian of SAC data same as current machine
#   2015-06-05  Dongdong Tian   Fix a bug with code 0103A and 0402A

"""Extract SAC data files from NIED Hi-net WIN32 files

Usage:
    rdhinet.py DIRNAME [-C <comps>] [-D <outdir>] [-S <suffix>] [-P <procs>]
    rdhinet.py -h

Options:
    -h          Show this help.
    -C <comps>  Components to extract, delimited using commas.
                Avaiable components are U, N, E, X, Y et. al.
                Default to extract all components.
    -D <outdir> Output directory for SAC files.
    -S <suffix> Suffix of output SAC files. Default: no suffix.
    -P <procs>  Parallel using multiple processes.
                Set number of CPUs to <procs> if <procs> equals 0. [default: 0]
"""

import os
import glob
import subprocess
import multiprocessing

from docopt import docopt

# external tools from Hi-net
win2sac = "win2sac_32"


def win_prm(chfile, prmfile="win.prm"):
    """four line parameters file"""

    with open(prmfile, "w") as f:
        f.write(".\n")
        f.write(chfile + "\n")
        f.write(".\n")
        f.write(".\n")


def get_chno(chfile, comps):
    """ read channel no list from channel table"""

    chno = []
    with open(chfile, "r") as f:
        for line in f:
            if line[0] == '#':
                continue

            items = line.split()
            no, comp = items[0], items[4]
            if comps is None or comp in comps:
                chno.append(no)

    print("Total %d channels" % len(chno))
    return chno


def _extract_channel(tup):
    """extract only one channel for one time"""

    winfile, chno, outdir, prmfile, pmax = tup
    #   print(winfile, chno, outdir, prmfile, pmax)
    subprocess.call([win2sac,
                     winfile,
                     chno,
                     "SAC",
                     outdir,
                     '-e',
                     '-p'+prmfile,
                     '-m'+str(pmax)
                     ],
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL)


def win32_sac(winfile, ch_no, outdir=".", prmfile="win.prm", pmax=2000000):

    tuple_list = []
    for ch in chno:
        t = winfile, ch, outdir, prmfile, pmax
        tuple_list.append(t)

    procs = int(arguments['-P'])

    if procs == 1:
        for t in tuple_list:
            _extract_channel(t)
    else:
        if procs == 0:
            procs = multiprocessing.cpu_count()
        else:
            procs = min(multiprocessing.cpu_count(), procs)

        pool = multiprocessing.Pool(processes=procs)
        pool.map(_extract_channel, tuple_list)


def rename_sac(dirname, outdir, sacfile=None):
    for file in glob.glob(os.path.join(dirname, "*.SAC")):
        dir, base = os.path.split(file)
        filename = os.path.splitext(base)[0]
        if sacfile:
            filename += "." + sacfile
        dest = os.path.join(outdir, filename)
        os.rename(file, dest)


if __name__ == "__main__":
    arguments = docopt(__doc__)
    dirname = arguments['DIRNAME']

    chfile = glob.glob(os.path.join(dirname, "*_????????.ch"))[0]
    cntfile = glob.glob(os.path.join(dirname, "*_????????????_*.cnt"))[0]
    basename = os.path.basename(cntfile)
    span = int(os.path.splitext(basename)[0].split("_")[2])

    # generate win32 paramerter file
    prmfile = os.path.join(dirname, "win.prm")
    win_prm(chfile, prmfile=prmfile)

    # get channel NO. lists for channel table
    comps = None
    if arguments['-C']:
        comps = arguments['-C'].split(",")
    chno = get_chno(chfile, comps)

    # maximum number of points
    pmax = span * 60 * 100  # assume data sample rate = 0.01
    # extrac sac files to dirname
    win32_sac(cntfile, chno, outdir=dirname, prmfile=prmfile, pmax=pmax)
    os.unlink(prmfile)

    # rename SAC files and move to outdir
    outdir = dirname
    if arguments['-D']:
        outdir = arguments['-D']
        if not os.path.exists(outdir):
            os.makedirs(outdir)

    rename_sac(dirname, outdir, arguments['-S'])
