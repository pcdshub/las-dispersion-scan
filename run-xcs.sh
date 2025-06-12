#!/usr/bin/env bash

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
cd "$SCRIPT_DIR" || exit 1

export QMINI_PREFIX=LAS:XCS:QMINI:01
export QMINI_NAME=xcs_spec_01_qmini

export MOTOR_PREFIX=XCS:LAS:MMN:02
export MOTOR_NAME=xcs_las_mmn_02

# If not available through the record itself, set this:
export MOTOR_UNITS=mm

./run.sh gui --script las_dispersion_scan.loaders.qmini_and_newport
