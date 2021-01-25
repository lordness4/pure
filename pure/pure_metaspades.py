import os
import subprocess

def runMetaspades(metaspades_output_dir, reads1, reads2, logdir, max_threads):
    """
    Uses metapsades2 to assemble the reads 1 and 2 into the file "contigs.fasta"
    placed at output_dir/assembly/ .
    """
    logfile = os.path.join(logdir, "metaspades.log")
    command = "metaspades.py -1 {reads1} -2 {reads2} -o {out} -t {max_threads}".format(
        reads1=reads1,
        reads2=reads2,
        out=metaspades_output_dir,
        max_threads=max_threads)

    with open(logfile, "w") as logfile:
        subprocess.call(command, shell=True, stdout=logfile, stderr=logfile)
