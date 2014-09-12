#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  Author:  Dongdong Tian @ USTC
#
#  Revision History:
#    2014-09-05 Dongdong Tian   Initial Coding
#
'''Convert Hi-net Channel Table file to SAC PZ files

Usage:
    ch2pz.py CHFILE [-C <comps>] [-D <outdir>] [-S <suffix>]

Options:
    -C <comps>      Channel Components to convert. Choose from U,N,E,X,Y.
                    [default: UNE]
    -D <outdir>     Output directory of SAC PZ files. Use the directory of
                    Channel Table file as default.
    -S <suffix>     Suffix for SAC PZ files. [default: SAC_PZ]
'''

import os
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


def write_pz(pzfile, real, imaginary, constant, outdir='.'):

    if not os.path.exists(outdir):
        os.makedirs(outdir)

    pzfile = os.path.join(outdir, pzfile)

    with open(pzfile, "w") as pz:
        pz.write("ZEROS 3\n")
        pz.write("POLES 2\n")
        pz.write("%9.6f %9.6f\n" % (real, imaginary))
        pz.write("%9.6f %9.6f\n" % (real, -imaginary))
        pz.write("CONSTANT %e\n" % (constant))


def ch2pz(chfile, comps, outdir, suffix):

    with open(chfile, "r") as f:
        for line in f:
            if line[0] == '#':
                continue

            items = line.split()
            station, comp = items[3], items[4]

            if comp not in comps:
                continue

            gain, damping = float(items[7]), float(items[10])
            freq = 2.0 * math.pi / float(items[9])
            pre_amp, lsb_value = float(items[11]), float(items[12])

            A0 = 2*damping
            factor = math.pow(10, pre_amp/20.0)
            constant = gain * factor / lsb_value * A0

            real, imaginary = find_poles(damping, freq)

            pzfile = "%s.%s" % (station, comp)
            if suffix:
                pzfile += '.' + suffix

            write_pz(pzfile, real, imaginary, constant, outdir)


if __name__ == "__main__":
    arguments = docopt(__doc__)
    print(arguments)

    chfile = arguments['CHFILE']
    comps = arguments['-C']
    suffix = arguments['-S']

    if arguments['-D']:
        outdir = arguments['-D']
    else:
        outdir = os.path.dirname(chfile)
        if outdir == '':
            outdir = '.'

    ch2pz(chfile, comps, outdir, suffix)
