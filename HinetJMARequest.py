#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Author: Dongdong Tian @ USTC
#
# Revision History:
#   2014-08-31  Dongdong Tian   Initial Coding
#   2014-12-03  Dongdong Tian   Update to Hinet V141201
#   2015-01-08  Dongdong Tian   Fix bugs caused by update on Dec. 1st, 2014
#

"""Request arrival time data or focal mechanism catalog from Hi-net.

Usage:
    HinetJMARequest.py (--measure | --mecha) <yyyymmdd> <span> [--os=OS]
    HinetJMARequest.py -h

Options:
    -h --help     Show this help.
    --measure     Request arrival time data.
    --mecha       Request focal mechanism catalog.
    --os=OS       Line break format, choose from DOS or UNIX. [default: DOS]

"""

import sys
from datetime import datetime

from docopt import docopt

from util import auth_login, read_config, JMA


def main():
    # parse arguments
    arguments = docopt(__doc__)
    if arguments['--measure']:
        data = "measure"
    elif arguments['--mecha']:
        data = "mecha"

    # check date validity
    rtm = arguments['<yyyymmdd>']
    try:
        datetime.strptime(rtm, '%Y%m%d')
    except ValueError:
        sys.exit("%s: Incorrect date or date format." % rtm)

    # check span
    span = arguments['<span>']
    if not (span.isdigit() and int(span) in range(1, 8)):
        sys.exit("<span> should be integer between 1 and 7.")

    # prepare data to post
    params = {
        "data": data,
        "rtm": rtm,
        "span": span,
        "os": arguments['--os'][0:1],
    }

    # specify user name and password
    config = read_config('Hinet.cfg')
    username = config['Account']['User']
    password = config['Account']['Password']
    s = auth_login(username, password)

    d = s.post(JMA, params=params, stream=True)
    fname = "{}_{}_{}.txt".format(data, rtm, span)
    with open(fname, "wb") as fd:
        for chunk in d.iter_content(chunk_size=1024):
            if chunk:  # filter out keep-alive new chunks
                fd.write(chunk)
                fd.flush()


if __name__ == '__main__':
    main()
