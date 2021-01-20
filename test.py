import os

outdir = "/home/domi/Documents/promotion/mvome_pipeline/test_pure/out3"
bin_dir = os.path.join(outdir, "bins")

files = os.listdir(bin_dir)
dir = [f for f in files if os.path.isdir(os.path.join(bin_dir, f))]


subfolders = [ f.path for f in os.scandir(bin_dir) if f.is_dir() ]
subfolders = subfolders[0]


#
# Traceback (most recent call last):
#   File "/home/domi/Documents/promotion/mvome_pipeline/bin/MARVEL/marvel_bins.py", line 314, in <module>
#     pickle_model = pickle.load(file)
# ModuleNotFoundError: No module named 'sklearn.ensemble.forest'
