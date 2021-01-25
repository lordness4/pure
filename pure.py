import os
import argparse
import sys
import json
import shutil
from Bio import SeqIO
from pure.pure_structure import createStructure
from pure.pure_metaspades import runMetaspades
from pure.pure_virome import runMarvel, runVirSorter, runDeepVirFinder
from pure.pure_plasmidome import runPlasFlow
from pure.pure_dedup import deduplicateContigs
from pure.pure_binning import createBins
from pure.pure_cleaner import cleanAssemblyDir, cleanBinningDir, cleanViromeDir, cleanPlasmidomeDir

################################################################################ WORKS
# config
config_file = "config.txt"

with open(config_file, "r") as f:
    data = f.read()

f.close()
config = json.loads(data)


################################################################################ WORKS
# handle arguments
parser = argparse.ArgumentParser()

parser.add_argument("--reads1", "-r1",
                    help="<filename> file with forward paired-end reads", required=True)

parser.add_argument("--reads2", "-r2",
                    help="<filename> file with reverse paired-end reads", required=True)

parser.add_argument("--output_dir", "-o",
                    help="<output_dir> directory to store all the resulting files", required=True)

parser.add_argument("--contigs_file", "-c",
                    help="optional <filename> multifasta file containing all contigs assembled form r1 and r2 (skips assembly)")

parser.add_argument("--cleanup", "-cu",
                    help="optional <TRUE/FALSE> flag. Default=FALSE. If TRUE, all intermediate files will be deleted, in order to save space.")

args = parser.parse_args()

# print help if not enough arguments
if len(sys.argv)<7:
    parser.print_help(sys.stderr)
    exit()


################################################################################ WORKS
# check arguments given
reads1 = args.reads1
reads2 = args.reads2

if not (os.path.exists(reads1) or os.path.exists(reads2)):
    print("cannot find reads file: ")
    print("either {} or {} not found. ".format(reads1, reads2))
    print("exiting...")
    #exit()

output_dir = args.output_dir
output_dir = os.path.abspath(output_dir)

if os.path.exists(output_dir):
    print("output directory already exists: ")
    print("{}".format(output_dir))
    print("exiting...")
    #exit()

# contig file given by the user
contig_file = args.contigs_file
# should we clean up afterwards?
cleanup = args.cleanup


################################################################################ WORKS
# create Structure
# createStructure(output_dir)

# log directory
logdir = os.path.join(output_dir, "log")


################################################################################ HAS TROUBLE WITH RAM
# run metaspades
assembly_dir = os.path.join(output_dir, "assembly")
# this only runs when we have no contigs file, else we copy over the contigs_file
if not contig_file:
    runMetaspades(assembly_dir, reads1, reads2, logdir)
else:
    shutil.copy(contig_file, os.path.join(output_dir, "assembly/contigs.fasta"),
                follow_symlinks=True)

contig_file = os.path.join(output_dir, "assembly/contigs.fasta")


################################################################################ WORKS
# deduplicate using bbmap
# deduplicateContigs(contig_file=contig_file, assembly_dir=assembly_dir, logdir=logdir)
contigs_deduplicated = os.path.join(output_dir, "assembly/contigs_deduplicated.fasta")

# map reads against deduplicated contigs in order to create bins
binning_dir = os.path.join(output_dir, "bins")
# createBins(reads1=reads1, reads2=reads2, contig_file=contigs_deduplicated, logdir=logdir,
#            outdir=binning_dir,
#            metabat_m=config["metabat_m"],
#            metabat_s=config["metabat_s"])


################################################################################ WORKS
# filter contigs file by length.
# NOTE: I should think about the figures in the end: do the incorporate the shorter sequences?


def filterByLength(contigs_input, contigs_output, cutoff_len):
    contigs_filtered = []
    for record in SeqIO.parse(contigs_input, "fasta"):
        if len(record.seq) >= cutoff_len:
            contigs_filtered.append(record)

    SeqIO.write(contigs_filtered, contigs_output, "fasta")


# from here on out: all programs only work on the filtered contigs
contigs_final = os.path.join(assembly_dir, "contigs_final.fasta")
# filterByLength(contigs_deduplicated, contigs_final, config["cutoff_len"])


################################################################################ WORKS
virome_dir = os.path.join(output_dir, "virome")

# run virsorter
# runVirSorter(virome_dir=virome_dir,
#              vs_db_dir=config["virsorter_db_path"],
#              infile=contigs_final,
#              logdir=logdir)

# run marvel
# runMarvel(output_dir=output_dir,
#           marvel_bin=config["marvel_bin"],
#           marvel_threads=config["marvel_threads"],
#           logdir=logdir)

# run deepvirfinder
# runDeepVirFinder(virome_dir=virome_dir,
#                  infile=contigs_final,
#                  logdir=logdir,
#                  dvf_bin=config["dvf_bin"],
#                  dvf_models=config["dvf_models"],
#                  conda_sh=config["conda_sh"])


################################################################################ WORKS
# plasmidome part
plasmidome_dir = os.path.join(output_dir, "plasmidome")
runPlasFlow(logdir=logdir,
            plasmidome_dir=plasmidome_dir,
            infile=contigs_final,
            plasflow_threshold=config["plasflow_threshold"],
            conda_sh=config["conda_sh"])


################################################################################
# gather report part


################################################################################
# clean up
if cleanup:
    pass
