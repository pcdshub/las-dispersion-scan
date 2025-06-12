#!/usr/bin/env bash

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

#source /reg/g/pcds/engineering_tools/latest-released/scripts/dev_conda ""
source /reg/g/pcds/engineering_tools/latest-released/scripts/pcds_conda ""

cd "$SCRIPT_DIR" || exit 1

export PYTHONPATH=/cds/group/pcds/pyps/apps/dev/pythonpath:$PYTHONPATH
#export PYTHONPATH=/cds/home/t/tjohnson/trunk/hutch-python/forks/pcdsdevices:$PYTHONPATH

# unset __GLX_VENDOR_LIBRARY_NAME
python -m las_dispersion_scan "$@"
