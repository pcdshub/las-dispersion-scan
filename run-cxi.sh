#!/usr/bin/env bash

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
cd "$SCRIPT_DIR" || exit 1

export QMINI_PREFIX=CXI:LAS:SPL:SP1
export QMINI_NAME=cxi_spec_01_qmini

export MOTOR_PREFIX=CXI:LAS:MMN:09
export MOTOR_NAME=cxi_las_mmn_09

# If not available through the record itself, set this:
export MOTOR_UNITS=mm

./run.sh gui --script las_dispersion_scan.loaders.qmini_and_newport
