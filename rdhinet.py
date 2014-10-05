#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  Author: Dongdong Tian @ USTC
#
#  Revision History:
#    2014-09-03  Dongdong Tian  Initial Coding
#

"""Extract SAC data files from Hi-net WIN32 files

Usage:
    rdhinet.py DIRNAME [-C <comps>] [-D <outdir>] [-S <suffix>] [-P <procs>]
    rdhinet.py -h

Options:
    -h          Show this help.
    -C <comps>  Selection of components to extract.
                Avaiable components are U, N, E, X, Y. [default: UNE]
    -D <outdir> Output directory for SAC files.
    -S <suffix> Suffix of output SAC files.
    -P <procs>  Parallel using multiple processes. Set number of cpus to <procs>
                if <procs> equals 0.    [default: 0]

"""

import os
import glob
import shlex
import zipfile
import datetime
import subprocess
import multiprocessing

from docopt import docopt

# external tools from Hi-net
catwin32 = "catwin32"
win2sac = "win2sac_32"


def unzip(zips):
    """unzip zip filelist"""

    for file in zips:
        print("Unzip %s" % (file))
        zipFile = zipfile.ZipFile(file, "r")
        for name in zipFile.namelist():
            zipFile.extract(name)


def win32_cat(cnts, cnt_total):
    """merge WIN32 files to one total WIN32 file"""

    print("Total %d win32 files" % (len(cnts)))
    cmd = "%s %s -o %s" % (catwin32, ' '.join(cnts), cnt_total)
    args = shlex.split(cmd)
    subprocess.call(args, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


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
            if comp in comps:
                chno.append(no)

    print("Total %d channels" % len(chno))
    return chno


def _exctract_channel(tup):
    """extract only one channel for one time"""

    winfile, chno, outdir, prmfile, pmax = tup
    subprocess.call([win2sac, winfile, chno, "SAC", outdir, prmfile, '-m'+str(pmax)],
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
            _exctract_channel(t)
    else:
        if procs == 0:
            procs = multiprocessing.cpu_count()
        else:
            procs = min(multiprocessing.cpu_count(), procs)

        pool = multiprocessing.Pool(processes=procs)
        pool.map(_exctract_channel, tuple_list)


def rename_sac(outdir, sacfile=None):
    for file in glob.glob(outdir + '/*.SAC'):
        dest = os.path.splitext(file)[0]
        if sacfile:
            dest += "." + sacfile
        os.rename(file, dest)


def unlink_lists(files):
    for f in files:
        os.unlink(f)


if __name__ == "__main__":
    arguments = docopt(__doc__)

    # change directory
    os.chdir(arguments['DIRNAME'])
    print("Working in dir %s" % (arguments['DIRNAME']))

    # unzip zip files
    unzip(glob.glob("??_??_????????????_*_?????.zip"))

    # merge win32 files
    cnts = sorted(glob.glob("??????????????????.cnt"))
    cnt_total = "%s_%d.cnt" % (cnts[0][0:11], len(cnts))
    win32_cat(cnts, cnt_total)
    unlink_lists(cnts)

    chfile = glob.glob("??_??_????????.euc.ch")[0]
    # generate win32 paramerter file
    win_prm(chfile)

    # get channel NO. lists for channel table
    comps = set(arguments['-C'])
    chno = get_chno(chfile, comps)

    # extract sac files
    outdir = '.'
    if arguments['-D']:
        outdir = arguments['-D']
    if not os.path.exists(outdir):
        os.makedirs(outdir)

    # maximum number of points
    pmax = len(cnts) * 60 * 100

    win32_sac(cnt_total, chno, outdir=outdir, pmax=pmax)

    sacfile = arguments['-S']
    rename_sac(outdir, sacfile)
