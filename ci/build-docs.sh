#!/bin/bash
#
# Build HTML pages

# To return a failure if any commands inside fail
set -e

cd docs
# build Chinese version first
sphinx-intl build
make -e SPHINXOPTS="-D language='zh_CN'" html
# backup Chinese version
mv _build/html _build/html_zh_CN

# build English version
make html

# move Chinese version back
mv _build/html_zh_CN _build/html/zh_CN

set +e
