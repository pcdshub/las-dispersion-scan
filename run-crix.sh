#!/usr/bin/env bash

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
cd "$SCRIPT_DIR" || exit 1

export QMINI_PREFIX=LM2K2:COM_DP2_TF1_SP1
export QMINI_NAME=lm2k2:com_dp2_tf1_sp1

export MOTOR_PREFIX=LM2K2:COM:ELL:2
export UPSTREAM_PORT=0
export UPSTREAM_CHANNEL=1
export DOWNSTREAM_PORT=0
export DOWNSTREAM_CHANNEL=2
export MOTOR_NAME=lmk2k2_com_ell

# If not available through the record itself, set this:
export MOTOR_UNITS=mm

./run.sh gui --script las_dispersion_scan.loaders.qmini_and_opcpa_compressor
