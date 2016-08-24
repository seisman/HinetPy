#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Author:  Dongdong Tian @ USTC
#
# Revision History:
#   2014-09-05  Dongdong Tian  Initial Coding
#   2015-01-17  Dongdong Tian  Only works for velocity input
#   2015-07-25  Dongdong Tian  Not work for F-net.
#   2016-07-27  Dongdong Tian  Extract multiple channel table files in one directory
#
'''Convert NIED Hi-net Channel Table file to SAC PZ files

Usage:
    ch2pz.py DIRNAME [-C <comps>] [-D <outdir>] [-S <suffix>]
    ch2pz.py -h

Options:
    -C <comps>    Channel Components to convert. Choose from U,N,E,X,Y et. al.
                  Default to convert all components.
    -D <outdir>   Output directory of SAC PZ files. Use the directory of
                  Channel Table file as default.
    -S <suffix>   Suffix for SAC PZ files. [default: SAC_PZ]
'''

import os
import sys
import glob
import math

from docopt import docopt


def find_poles(damping, freq):
    ''' find roots of equation s^2+2hws+w^2=0

        h is damping constant
        w is angular frequency
    '''
    real = -damping*freq
    imaginary = freq * math.sqrt(1 - damping*damping)

    return real, imaginary


def write_pz(pzfile, real, imaginary, constant):
    ''' write SAC PZ file '''

    with open(pzfile, "w") as pz:
        pz.write("ZEROS 3\n")
        pz.write("POLES 2\n")
        pz.write("%9.6f %9.6f\n" % (real, imaginary))
        pz.write("%9.6f %9.6f\n" % (real, -imaginary))
        pz.write("CONSTANT %e\n" % (constant))


def ch2pz(chfile, comps, outdir, suffix):

    with open(chfile, "r") as f:
        for line in f:
            if line.startswith('#'):
                continue

            items = line.split()
            station, comp, unit = items[3], items[4], items[8]

            if not (comps is None or comp in comps):
                continue

            if unit != 'm/s':  # only works for velocity
                print("Warning: %s.%s isn't velocity in m/s" % (station, comp))
                continue

            gain, damping = float(items[7]), float(items[10])
            try:
                freq = 2.0 * math.pi / float(items[9])
            except ZeroDivisionError:
                print("Warning: %s.%s Natural period = 0!" % (station, comp))
                continue
            pre_amp, lsb_value = float(items[11]), float(items[12])

            A0 = 2*damping
            factor = math.pow(10, pre_amp/20.0)
            constant = gain * factor / lsb_value * A0

            real, imaginary = find_poles(damping, freq)

            pzfile = "%s.%s" % (station, comp)
            if suffix:
                pzfile += '.' + suffix
            pzfile = os.path.join(outdir, pzfile)

            write_pz(pzfile, real, imaginary, constant)


def main():
    arguments = docopt(__doc__)
    dirname = arguments['DIRNAME']
    comps = arguments['-C'].split(',') if arguments['-C'] else None
    suffix = arguments['-S']

    outdir = arguments['-D'] if arguments['-D'] else dirname
    if not os.path.exists(outdir):
        os.makedirs(outdir)

    for chfile in glob.glob(os.path.join(dirname, "*_????????.ch")):
        code = os.path.basename(chfile).split("_")[0]
        if code in ['0103', '0103A']:
            print("This script does not work for F-net!")
            print("Please use https://github.com/seisman/FnetScript!")
            print("Exit Now!")
            sys.exit()
        ch2pz(chfile, comps, outdir, suffix)


if __name__ == "__main__":
    main()
