#!/bin/bash
CONDA_BASE=$(conda info --base)
source ${CONDA_BASE}/etc/profile.d/conda.sh
conda deactivate
conda env list | grep "\*"
