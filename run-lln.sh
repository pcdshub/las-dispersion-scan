#!/usr/bin/env bash

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
cd "$SCRIPT_DIR" || exit 1

export QMINI_PREFIX=LAS:LLN:QMINI:01
export QMINI_NAME=las_lln_spec_01

export MOTOR_PREFIX=LAS:ELL:LLN:TST
export MOTOR_NAME=las_lln_ell_01

# If not available through the record itself, set this:
export MOTOR_UNITS=mm

./run.sh gui --script las_dispersion_scan.loaders.qmini_and_elliptec
