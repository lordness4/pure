import os
import subprocess
import shutil

def runVirSorter(virome_dir, vs_db_dir, infile, logdir, conda_sh):
    """
    Runs VirSorter2.0 on the infile, using the VirSorter2 database provided in
    vs_db_dir while logging to logdir/virsorter.log. Output is placed in
    virome_dir/virsorter/ .
    """

    logfile = os.path.join(logdir, "virsorter.log")
    wd = os.path.join(virome_dir, "virsorter")
    command = \
    "bash -c '. {conda_sh} && \
    conda activate vs2 && \
    virsorter run -w {working_dir} -d {vs_db_dir} -i {infile} && \
    conda deactivate'".format(
        working_dir=wd,
        vs_db_dir=vs_db_dir,
        infile=infile,
        conda_sh=conda_sh)
    #rm-tmpdir
    with open(logfile, "w") as logfile:
        subprocess.call(command, shell=True, stdout=logfile, stderr=logfile)

def runMarvel(output_dir, marvel_bin, marvel_threads, logdir, conda_sh):
    """
    Runs MARVEL (with a certain number of threads) on the bins created in the
    binning process, which can be found at
    output_dir/bins/contigs.fasta. Logs are written to logs/marvel.log .
    Switches cwd to the path where the marvel bin is placed and back to where the cwd
    was.
    """

    logfile = os.path.join(logdir, "marvel.log")
    # this line gives me the name of the unknown folder in bins/
    bins_dir = [f.path for f in os.scandir(os.path.join(output_dir, "bins")) if f.is_dir()]
    bins_dir = bins_dir[0]

    virome_dir = os.path.join(output_dir, "virome")
    marvel_outdir = os.path.join(virome_dir, "marvel")
    marvel_dir = os.path.dirname(marvel_bin)

    # switch cwd to marvel, run marvel on the bins, switch back
    cwd = os.getcwd()
    os.chdir(os.path.abspath(marvel_dir))

    command = \
    "bash -c '. {conda_sh} && \
    conda activate marvel && \
    python3 {marvel_bin} -i {bins_dir} -t {marvel_threads} &&\
    conda deactivate'".format(
        conda_sh=conda_sh,
        marvel_bin=marvel_bin,
        bins_dir=bins_dir,
        marvel_threads=marvel_threads)

    with open(logfile, "w") as logfile:
        subprocess.call(command, shell=True, stdout=logfile, stderr=logfile)
    os.chdir(os.path.abspath(cwd))

    # move files from bins/blabla/results back to virome/marvel
    marvel_results_dir = os.path.join(bins_dir, "results/phage_bins")
    marvel_output_dir = os.path.join(output_dir, "virome/marvel/phage_bins")

    shutil.copytree(marvel_results_dir, marvel_output_dir)



def runDeepVirFinder(virome_dir, infile, logdir, dvf_bin, dvf_models, conda_sh):
    """
    Switches conda env to dvf, then runs dvf on the infile. Logs to log/deepvirfinder.logs .
    """
    logfile = os.path.join(logdir, "deepvirfinder.log")
    dvf_output_dir = os.path.join(virome_dir, "deepvirfinder")

    # then run dvf itself
    command = \
    "bash -c '. {conda_sh} && \
    conda activate dvf && \
    python {dvf_bin} -i {infile} -o {dvf_output_dir} -m {dvf_models} && \
    conda deactivate'".format(
         dvf_bin=dvf_bin,
         infile=infile,
         dvf_output_dir=dvf_output_dir,
         dvf_models=dvf_models,
         conda_sh=conda_sh)

    print(command)

    with open(logfile, "w") as logfile:
        subprocess.call(command, shell=True, stdout=logfile, stderr=logfile)
