import os
import subprocess

with open("here.txt", "w") as log:
    command=". ~/bin/anaconda3/etc/profile.d/conda.sh && conda activate dvf"
    subprocess.call(command,shell = True, stdout=log, stderr=log)

#&& conda activate dvf && python /home/domi/Documents/promotion/mvome_pipeline/bin/DeepVirFinder/dvf.py -i ../data/contigs_short.fasta -m /home/domi/Documents/promotion/mvome_pipeline/bin/DeepVirFinder/models/ -o here.txt
