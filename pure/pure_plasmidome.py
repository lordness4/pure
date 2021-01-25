import os
import subprocess

def runPlasFlow(logdir, plasmidome_dir, infile, plasflow_threshold, conda_sh):
    logfile = os.path.join(logdir, "plasflow.log")
    plasflow_dir = os.path.join(plasmidome_dir, "plasflow")
    output = os.path.join(plasflow_dir, "plasflow_out.tsv")

    command = \
    "bash -c '. {conda_sh} && \
    conda activate plasflow && \
    PlasFlow.py --input {infile} --output {output} --threshold {threshold} && \
    conda deactivate'".format(
        infile=infile,
        output=output,
        threshold=plasflow_threshold,
        conda_sh=conda_sh)

    with open(logfile, "w") as logfile:
        subprocess.call(command, shell=True, stdout=logfile, stderr=logfile)
