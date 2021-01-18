import os
import subprocess

def runMetaspades(metaspades_output_dir, reads1, reads2, logdir):
    # not enough ram!
    logfile = os.path.join(logdir, "metaspades.log")
    with open(logfile, "w") as logfile:
        subprocess.call("metaspades.py -1 {reads1} -2 {reads2} -o {out} -t 2".format(
            reads1=reads1,
            reads2=reads2,
            out=metaspades_output_dir),
                         shell=True, stdout=logfile, stderr=logfile)
