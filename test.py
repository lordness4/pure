import os
import subprocess

with open("snakemake.log", "w") as log:
    command="snakemake -j 4 "
    subprocess.call(command,shell = True, stdout=log, stderr=log)

#&& conda activate dvf && python /home/domi/Documents/promotion/mvome_pipeline/bin/DeepVirFinder/dvf.py -i ../data/contigs_short.fasta -m /home/domi/Documents/promotion/mvome_pipeline/bin/DeepVirFinder/models/ -o here.txt
