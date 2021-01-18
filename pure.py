import os
import argparse
import sys
import json
from pure_structure import createStructure
from pure_metaspades import runMetaspades
from pure_virome import runMarvel, runVirSorter, runDeepVirFinder
from pure_dedup import deduplicateContigs
from pure_binning import createBins



################################################################################
# config
config_file = "config.txt"

with open(config_file, "r") as f:
    data = f.read()

f.close()
config = json.loads(data)

################################################################################
# handle arguments
parser = argparse.ArgumentParser()

parser.add_argument("--reads1", "-r1", help="<filename> file with forward paired-end reads")
parser.add_argument("--reads2", "-r2", help="<filename> file with reverse paired-end reads")
parser.add_argument("--output_dir", "-o", help="<output_dir> directory to store all the resulting files")

args = parser.parse_args()

# print help if not enough arguments
if len(sys.argv)<7:
    parser.print_help(sys.stderr)
    exit()

################################################################################
# check if input files are present and output_dir is viable
reads1 = args.reads1
reads2 = args.reads2

if not (os.path.exists(reads1) or os.path.exists(reads2)):
    print("cannot find reads file: ")
    print("either {} or {} not found. ".format(reads1, reads2))
    print("exiting...")
    exit()

output_dir = args.output_dir
output_dir = os.path.abspath(output_dir)

if os.path.exists(output_dir):
    print("output directory already exists: ")
    print("{}".format(output_dir))
    print("exiting...")
    #exit()

################################################################################ WORKS
# create Structure
# createStructure(output_dir)

# log directory
logdir = os.path.join(output_dir, "log")

################################################################################ HAS TROUBLE WITH RAM
# run metaspades
assembly_dir = os.path.join(output_dir, "assembly")
# # NOTE: I cant run this locally, not enough RAM
# runMetaspades(assembly_dir, reads1, reads2, logdir)

contig_file = os.path.join(output_dir, "assembly/contigs.fasta")

################################################################################ WORKS
# deduplicate using bbmap
# deduplicateContigs(contig_file=contig_file, assembly_dir=assembly_dir, logdir=logdir)

# map reads against deduplicated contigs in order to create bins
binning_dir = os.path.join(output_dir, "bins")
createBins(reads1=reads1, reads2=reads2, contig_file=contig_file, logdir=logdir,
           outdir=binning_dir,
           metabat_m=config["metabat_m"],
           metabat_s=config["metabat_s"])


################################################################################
virome_dir = os.path.join(output_dir, "virome")

# run virsorter
# runVirSorter(virome_dir=virome_dir,
             # vs_db_dir=config["virsorter_db_path"],
             # infile=contig_file,
             # logdir=logdir)

# run marvel
# runMarvel()

# run deepvirfinder
# runDeepVirFinder(virome_dir=virome_dir,
#                  infile=contig_file,
#                  logdir=logdir,
#                  dvf_bin=config["dvf_bin"],
#                  dvf_models=config["dvf_models"],
#                  dvf_cutoff_len=config["dvf_cutoff_len"],
#                  activator_script=config["activator_script"],
#                  deactivator_script=config["deactivator_script"])
