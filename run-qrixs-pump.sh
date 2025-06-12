#!/usr/bin/env bash

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
cd "$SCRIPT_DIR" || exit 1

export QMINI_PREFIX=LM1K2:EJX_DP1_SP1
export QMINI_NAME=lm1k2:ejx_dp1_sp1

export MOTOR_PREFIX=LM1K2:COM:ELL:1
export UPSTREAM_PORT=0
export UPSTREAM_CHANNEL=1
export DOWNSTREAM_PORT=0
export DOWNSTREAM_CHANNEL=2
export MOTOR_NAME=lmk1k2_com_ell

# If not available through the record itself, set this:
export MOTOR_UNITS=mm

./run.sh gui --script las_dispersion_scan.loaders.qmini_and_opcpa_compressor
