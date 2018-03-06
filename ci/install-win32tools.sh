#!/bin/bash

set -e

python -c "from HinetPy import Client; Client('${HINET_USERNAME}', '${HINET_PASSWORD}')._get_win32tools()"
tar -xf win32tools.tar.gz
cd win32tools
make -j
mkdir bin
mv catwin32.src/catwin32 win2sac.src/win2sac_32 bin/
cd ..
rm win32tools.tar.gz

set +e
