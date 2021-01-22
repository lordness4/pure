#!/bin/bash

CONDA_BASE=$(conda info --base)
source ${CONDA_BASE}/etc/profile.d/conda.sh
conda activate $1
conda env list | grep "\*"
