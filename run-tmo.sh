#!/usr/bin/env bash

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
cd "$SCRIPT_DIR" || exit 1

export QMINI_PREFIX=LM1K4:COM_DP2_TF1_SP1
export QMINI_NAME=lm1k4:com_dp2_tf1_sp1

export MOTOR_PREFIX=LM1K4:COM:ELL:2
export UPSTREAM_PORT=0
export UPSTREAM_CHANNEL=6
export DOWNSTREAM_PORT=0
export DOWNSTREAM_CHANNEL=7
export MOTOR_NAME=lmk1k4_com_ell

# If not available through the record itself, set this:
export MOTOR_UNITS=mm

./run.sh gui --script las_dispersion_scan.loaders.qmini_and_opcpa_compressor
