import os
import argparse
import sys
import json
import shutil
import pprint
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


################################################################################
# handle arguments
parser = argparse.ArgumentParser()

# reads metagenome
parser.add_argument("--metagenome_reads1", "-mr1",
                    help="<filename> file with forward paired-end reads, from which --metagenome_contigs_file was assembled")
parser.add_argument("--metagenome_reads2", "-mr2",
                    help="<filename> file with reverse paired-end reads, from which --metagenome_contigs_file was assembled")
# reads virome
parser.add_argument("--virome_reads1", "-vr1",
                    help="<filename> file with forward paired-end reads, from which --virome_contigs_file was assembled")
parser.add_argument("--virome_reads2", "-vr2",
                    help="<filename> file with reverse paired-end reads, from which --virome_contigs_file was assembled")
# contig file metagnome
parser.add_argument("--metagenome_contigs_file", "-mc",
                    help="optional <filename> multifasta file containing all contigs assembled form mr1 and mr2 (skips assembly)")
# contig file virome
parser.add_argument("--virome_contigs_file", "-vc",
                    help="optional <filename> multifasta file containing all contigs assembled form vr1 and vr2 (skips assembly)")

# output dir
parser.add_argument("--output_dir", "-o",
                    help="<output_dir> directory to store all the resulting files", required=True)
# cleanup flag
parser.add_argument("--cleanup", "-cu",
                    help="optional <TRUE/FALSE> flag. Default=FALSE. If TRUE, all intermediate files will be deleted, in order to save space.")

args = parser.parse_args()


################################################################################
# parse inputs
metagenome_reads1 = args.metagenome_reads1
metagenome_reads2 = args.metagenome_reads2

virome_reads1 = args.virome_reads1
virome_reads2 = args.virome_reads2

metagenome_contigs_file = args.metagenome_contigs_file
virome_contigs_file = args.virome_contigs_file

output_dir = args.output_dir

clean_up = args.cleanup


################################################################################
# run settings
settings = {
    "run virsorter": True,
    "run deepvirfinder": True,
    "run marvel": True,
    "run plasflow": True,
    "deduplicate metagenome": True,
    "deduplicate virome": True,
    "map back to metagenome": True,
}



################################################################################
# check arguments given
reads1 = args.reads1
reads2 = args.reads2

if not (os.path.exists(reads1) or os.path.exists(reads2)):
    print("cannot find reads file: ")
    print("either {} or {} not found. ".format(reads1, reads2))
    print("will not run marvel, since we cannt create bins without reads!")
    reads_are_given = False
else:
    reads_are_given = True

output_dir = args.output_dir
output_dir = os.path.abspath(output_dir)

if os.path.exists(output_dir):
    print("output directory already exists: ")
    print("{}".format(output_dir))
    print("exiting...")
    exit()

# contig file given by the user
contig_file = args.contigs_file

# should we clean up afterwards?
cleanup = args.cleanup


# if nothing is given (should be caught by sys.argv < 7)
if reads_are_given or contig_file:
    pass
else:
    print("either contig file or reads must be provided!")
    print("exiting...")
    exit()

################################################################################
# create Structure
createStructure(output_dir)

# log directory
logdir = os.path.join(output_dir, "log")


################################################################################
# run metaspades
assembly_dir = os.path.join(output_dir, "assembly")
# this only runs when we have no contigs file, else we copy over the contigs_file
if not contig_file:
    runMetaspades(assembly_dir, reads1, reads2, logdir, config["max_threads"])
else:
    shutil.copy(contig_file, os.path.join(output_dir, "assembly/contigs.fasta"),
                follow_symlinks=True)

contig_file = os.path.join(output_dir, "assembly/contigs.fasta")


################################################################################
# deduplicate using bbmap
deduplicateContigs(contig_file=contig_file, assembly_dir=assembly_dir, logdir=logdir)
contigs_deduplicated = os.path.join(output_dir, "assembly/contigs_deduplicated.fasta")


################################################################################
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
filterByLength(contigs_deduplicated, contigs_final, config["cutoff_len"])


################################################################################
# map reads against deduplicated contigs in order to create bins
bin_dir = os.path.join(output_dir, "bins")
createBins(reads1, reads2, contig_file=contigs_final, logdir=logdir,\
           bin_dir=bin_dir, metabat_m=config["metabat_m"], metabat_s=config["metabat_s"])



################################################################################
virome_dir = os.path.join(output_dir, "virome")

# run virsorter
runVirSorter(virome_dir=virome_dir,
             vs_db_dir=config["virsorter_db_path"],
             infile=contigs_final,
             logdir=logdir,
             conda_sh=config["conda_sh"])

# run marvel
if reads_are_given:
    runMarvel(output_dir=output_dir,
              marvel_bin=config["marvel_bin"],
              marvel_threads=config["marvel_threads"],
              logdir=logdir,
              conda_sh=config["conda_sh"])

# run deepvirfinder
runDeepVirFinder(virome_dir=virome_dir,
                 infile=contigs_final,
                 logdir=logdir,
                 dvf_bin=config["dvf_bin"],
                 dvf_models=config["dvf_models"],
                 conda_sh=config["conda_sh"])


################################################################################
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
