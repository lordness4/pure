import os
import subprocess
import shutil

def runVirSorter(virome_dir, vs_db_dir, infile, logdir):
    """
    Runs VirSorter2.0 on the infile, using the VirSorter2 database provided in
    vs_db_dir while logging to logdir/virsorter.log. Output is placed in
    virome_dir/virsorter/ .
    """

    logfile = os.path.join(logdir, "virsorter.log")
    wd = os.path.join(virome_dir, "virsorter")
    command = "virsorter run -w {working_dir} -d {vs_db_dir} -i {infile}".format(
        working_dir=wd,
        vs_db_dir=vs_db_dir,
        infile=infile)
    #rm-tmpdir
    with open(logfile, "w") as logfile:
        subprocess.call(command, shell=True, stdout=logfile, stderr=logfile)

def runMarvel(output_dir, marvel_bin, marvel_threads, logdir):
    """
    Runs MARVEL (with a certain number of threads) on the bins created in the
    binning process, which can be found at
    output_dir/bins/contigs.fasta. Logs are written to logs/marvel.log .
    Switches cwd to the path where the marvel bin is placed and back to where the cwd
    was.
    """

    logfile = os.path.join(logdir, "marvel.log")
    # this line gives me the name of the unknown folder in bins/
    bins_dir = [ f.path for f in os.scandir(os.path.join(output_dir, "bins")) if f.is_dir() ]
    bins_dir = bins_dir[0]

    virome_dir = os.path.join(output_dir, "virome")
    marvel_outdir = os.path.join(virome_dir, "marvel")
    marvel_dir = os.path.dirname(marvel_bin)

    # switch cwd to marvel, run marvel on the bins, switch back
    cwd = os.getcwd()
    os.chdir(marvel_dir)
    command = "python3 {marvel_bin} -i {bins_dir} -t {marvel_threads}".format(
        marvel_bin=marvel_bin,
        bins_dir=bins_dir,
        marvel_threads=marvel_threads
    )
    with open(logfile, "w") as logfile:
        subprocess.call(command, shell=True, stdout=logfile, stderr=logfile)
    os.chdir(cwd)

    # move files from bins/blabla/results back to virome/marvel




def runDeepVirFinder(virome_dir, infile, logdir, dvf_bin, dvf_models, dvf_cutoff_len, activator_script, deactivator_script):
    logfile = os.path.join(logdir, "deepvirfinder.log")
    dvf_output_dir = os.path.join(virome_dir, "deepvirfinder")

    # then run dvf itself
    command = \
    "bash {activator_script} &&\
     python {dvf_bin} -i {infile} -o {dvf_output_dir} -l {dvf_cutoff_len} -m {dvf_models} &&\
     bash {deactivator_script}".format(
         activator_script=activator_script,
         dvf_bin=dvf_bin,
         infile=infile,
         dvf_output_dir=dvf_output_dir,
         dvf_cutoff_len=dvf_cutoff_len,
         dvf_models=dvf_models,
         deactivator_script=deactivator_script)

    with open(logfile, "w") as logfile:
        subprocess.call(command, shell=True, stdout=logfile, stderr=logfile)
