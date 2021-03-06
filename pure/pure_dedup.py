import os
import subprocess

def deduplicateContigs(contig_file, assembly_dir, logdir):
    """
    Deduplicates the contig file provided using dedupe.sh from the BBMap toolset.
    Writes a logfile to logdir/dedupe.log .
    """
    logfile = os.path.join(logdir, "dedupe.log")
    infile = contig_file
    outfile = os.path.join(assembly_dir, "contigs_deduplicated.fasta")
    command = "dedupe.sh in={infile} out={outfile}".format(infile = infile, outfile=outfile)

    with open(logfile, "w") as logfile:
        subprocess.call(command, shell=True, stdout=logfile, stderr=logfile)
