import os
import subprocess

f = "lala.log"

with open(f, "w") as log:
    subprocess.call("conda env list", shell=True, stdout=log, stderr=log)

#
# Traceback (most recent call last):
#   File "/home/domi/Documents/promotion/mvome_pipeline/bin/MARVEL/marvel_bins.py", line 314, in <module>
#     pickle_model = pickle.load(file)
# ModuleNotFoundError: No module named 'sklearn.ensemble.forest'
