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
#   2016-07-24  Dongdong Tian   Extract multiple cnt files in one directory

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
            if line.strip().startswith('#'):
                continue

            items = line.split()
            no, comp = items[0], items[4]
            if comps is None or comp in comps:
                chno.append(no)

    print("Total %d channels" % len(chno))
    return chno


def _extract_channel(tup):
    """extract only one channel for one time"""

    winfile, chno, suffix, outdir, prmfile, pmax = tup
    #   print(winfile, chno, outdir, prmfile, pmax)
    subprocess.call(['win2sac_32',
                     winfile,
                     chno,
                     suffix,
                     outdir,
                     '-e',
                     '-p'+prmfile,
                     '-m'+str(pmax)
                    ],
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL)


def win32_sac(winfile, chno, suffix,
              outdir=".", prmfile="win.prm", pmax=2000000, procs=1):
    ''' extract SAC files from winfile '''

    tuple_list = []
    for ch in chno:
        t = winfile, ch, suffix, outdir, prmfile, pmax
        tuple_list.append(t)

    if procs == 1:  # serial
        for t in tuple_list:
            _extract_channel(t)
    else:           # parallel
        pool = multiprocessing.Pool(processes=procs)
        pool.map(_extract_channel, tuple_list)

    os.unlink(prmfile)


def get_procs(procs):
    ''' determine number of processors used in extracting '''

    cpu_count = multiprocessing.cpu_count()
    procs = cpu_count if procs == 0 else min(cpu_count, procs)

    return procs


def remove_suffix(outdir):
    ''' remove suffix ".SAC" from SAC files '''

    for filename in glob.glob(os.path.join(outdir, "*.SAC")):
        os.rename(filename, filename[:-4])  # remove '.SAC'


def main():
    arguments = docopt(__doc__)
    dirname = arguments['DIRNAME']

    chfiles = glob.glob(os.path.join(dirname, "*_????????.ch"))
    cntfiles = glob.glob(os.path.join(dirname, "*_????????????_*.cnt"))
    prmfile = os.path.join(dirname, "win.prm")

    # loop over cnt files
    for cntfile, chfile in zip(cntfiles, chfiles):
        # chno: get channel NO. lists for channel table
        comps = arguments['-C'].split(",") if arguments['-C'] else None
        chno = get_chno(chfile, comps)

        # suffix: determine suffix of SAC files
        suffix = arguments['-S'] if arguments['-S'] else 'SAC'

        # outdir: determine output directory
        outdir = arguments['-D'] if arguments['-D'] else dirname
        if not os.path.exists(outdir):
            os.makedirs(outdir)

        # prmfile: generate win32 paramerter file
        win_prm(chfile, prmfile=prmfile)

        # pmax: determine number of points from filename
        basename = os.path.basename(cntfile)
        span = int(os.path.splitext(basename)[0].split("_")[2])
        pmax = span * 60 * 100  # assume data sample rate = 0.01

        # procs
        procs = get_procs(int(arguments['-P']))

        # extrac sac files to dirname
        win32_sac(cntfile, chno, suffix,
                  outdir=outdir,
                  prmfile=prmfile,
                  pmax=pmax,
                  procs=procs)

        if not arguments['-S']:
            remove_suffix(outdir)


if __name__ == "__main__":
    main()
