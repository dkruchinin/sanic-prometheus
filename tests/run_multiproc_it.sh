#!/usr/bin/env sh

TMPD=`mktemp -d`
env prometheus_multiproc_dir=$TMPD python -m unittest tests/it_multiprocess.py
EC=$?
rm -rf $TMPD
exit $EC
