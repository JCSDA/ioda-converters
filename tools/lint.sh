#!/bin/sh

set -ex

SRC_DIR=${1:-"./"}
PYCODESTYLE_CFG_PATH=${2:-"./"}

cd $SRC_DIR

pycodestyle --config="$PYCODESTYLE_CFG_PATH/.pycodestyle" .

# These require some more work, and may not be worth the effort.
#python bin/run-pyflakes.py
#python bin/run-mccabe.py
#pylint modulename