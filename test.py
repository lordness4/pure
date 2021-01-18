import subprocess
import os


###############################################################################
# # test dvf
# dvf_bin = "/home/domi/Documents/promotion/mvome_pipeline/bin/DeepVirFinder/dvf.py"
# infile = "/home/domi/Documents/promotion/mvome_pipeline/pure/test_pure/contigs.fasta"
# logfile = "test.log"
# dvf_models = "/home/domi/Documents/promotion/mvome_pipeline/bin/DeepVirFinder/models"
# dvf_cutoff_len = 1000
# dvf_output_dir = "dvf_out"
#
# activator_script = "/home/domi/Documents/promotion/mvome_pipeline/pure/activate_conda_env.sh"
# deactivator_script = "/home/domi/Documents/promotion/mvome_pipeline/pure/deactivate_conda_env.sh"
#
# # then run dvf itself
# command = \
# "bash {activator_script} &&\
#  python {dvf_bin} -i {infile} -o {dvf_output_dir} -l {dvf_cutoff_len} -m {dvf_models} &&\
#  bash {deactivator_script}".format(
#      activator_script=activator_script,
#      dvf_bin=dvf_bin,
#      infile=infile,
#      dvf_output_dir=dvf_output_dir,
#      dvf_cutoff_len=dvf_cutoff_len,
#      dvf_models=dvf_models,
#      deactivator_script=deactivator_script)
#
# with open(logfile, "w") as logfile:
#     subprocess.call(command, shell=True, stdout=logfile, stderr=logfile)



# ################################################################################
# # dedupe
# logfile = "dedupe.log"
# infile = "test_pure/contigs.fasta"
# outfile = "test_pure/contigs_deduplicated.fasta"
#
# command = "dedupe.sh in={infile} out={outfile}".format(infile = infile, outfile=outfile)
#
# with open(logfile, "w") as logfile:
#     subprocess.call(command, shell=True, stdout=logfile, stderr=logfile)



################################################################################
# # test marvel
# dvf_bin = "/home/domi/Documents/promotion/mvome_pipeline/bin/DeepVirFinder/dvf.py"
# infile = "/home/domi/Documents/promotion/mvome_pipeline/pure/test_pure/contigs.fasta"
# logfile = "test.log"
# dvf_models = "/home/domi/Documents/promotion/mvome_pipeline/bin/DeepVirFinder/models"
# dvf_cutoff_len = 1000
# dvf_output_dir = "dvf_out"
#
#
# command = "python {dvf_bin} -i {infile} -o {dvf_output_dir} -l {dvf_cutoff_len} -m {dvf_models}".format(
#     dvf_bin=dvf_bin, infile=infile, dvf_output_dir=dvf_output_dir, dvf_cutoff_len=dvf_cutoff_len, dvf_models=dvf_models)
#
#
# with open(logfile, "w") as logfile:
#     subprocess.call(command, shell=True, stdout=logfile, stderr=logfile)


################################################################################
# bowtie2
# workflow from: https://www.hadriengourle.com/tutorials/meta_assembly/

# contigs_file="test_pure/contigs.fasta"
# index_file="test_pure/sample"
# reads1="test_pure/reads1.fastq.gz"
# reads2="test_pure/reads2.fastq.gz"
# bamfile="test_pure/sample.bam"
# sorted_bamfile="test_pure/sample.sorted.bam"
# logfile="log/binning.log"
# metabat_outdir="test_pure/binning/"
# metabat_m = 1500
# metabat_s = 10000
#
#
# with open(logfile, "w") as logfile:
#     # first index
#     command="bowtie2-build {contigs_file} {index_file}".format(
#         contigs_file=contigs_file,
#         index_file=index_file)
#     # subprocess.call(command, shell=True, stdout=logfile, stderr=logfile)
#
#
#     # map reads to contigs
#     command="bowtie2 -x {index_file} -1 {reads1} -2 {reads2}\
#      | samtools view -bS -o {bamfile}".format(
#          index_file=index_file,
#          reads1=reads1,
#          reads2=reads2,
#          bamfile=bamfile)
#     # subprocess.call(command, shell=True, stdout=logfile, stderr=logfile)
#
#     # sort bam file and index bam file
#     command="samtools sort {bamfile} -o {sorted_bamfile}".format(
#         bamfile=bamfile,
#         sorted_bamfile=sorted_bamfile)
#     # subprocess.call(command, shell=True, stdout=logfile, stderr=logfile)
#
#     # index sorted file
#     command="samtools index {sorted_bamfile}".format(
#         sorted_bamfile=sorted_bamfile)
#     # subprocess.call(command, shell=True, stdout=logfile, stderr=logfile)
#
#     # run metabat
#     contigs_file=os.path.abspath(contigs_file)
#     sorted_bamfile=os.path.abspath(sorted_bamfile)
#     os.chdir(metabat_outdir)
#     command="runMetaBat.sh -m {metabat_m} -s {metabat_s} {contigs_file} {sorted_bamfile}".format(
#         metabat_m=metabat_m,
#         metabat_s=metabat_s,
#         contigs_file=contigs_file,
#         sorted_bamfile=sorted_bamfile
#     )
#     subprocess.call(command, shell=True, stdout=logfile, stderr=logfile)


################################################################################
# test metaspades super simple
logfile="metaspades_simple.log"
with open(logfile, "w") as logfile:
    subprocess.call("metaspades.py --test", shell=True, stdout=logfile, stderr=logfile)
