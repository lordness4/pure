import os
import subprocess

def runPlasFlow(logdir, plasmidome_dir, infile, plasflow_threshold):
    logfile = os.path.join(logdir, "plasflow.log")
    plasflow_dir = os.path.join(plasmidome_dir, "plasflow")
    output = os.path.join(plasflow_dir, "plasflow_out.tsv")

    command = "PlasFlow.py --input {infile} --output {output} --threshold {threshold}".format(
        infile=infile,
        output=output,
        threshold=plasflow_threshold)

    with open(logfile, "w") as logfile:
        subprocess.call(command, shell=True, stdout=logfile, stderr=logfile)
