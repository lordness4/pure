#!/bin/bash
conda env list | grep "\*"
CONDA_BASE=$(conda info --base)
source ${CONDA_BASE}/etc/profile.d/conda.sh
conda deactivate
conda env list | grep "\*"
