import os
import subprocess

def runVirSorter(virome_dir, vs_db_dir, infile, logdir):
    """
    Runs VirSorter2.0 on the infile, using the VirSorter2 database provided in
    vs_db_dir while logging to logdir/virsorter.log. Output is placed in
    virome_dir/virsorter/ .
    """

    logfile = os.path.join(logdir, "virsorter.log")
    wd = os.path.join(virome_dir, "virsorter")
    command = "virsorter run -w {working_dir} -d {vs_db_dir} -i {infile}".format(
        working_dir=virome_dir,
        vs_db_dir=vs_db_dir,
        infile=infile)
    #rm-tmpdir
    with open(logfile, "w") as logfile:
        subprocess.call(command, shell=True, stdout=logfile, stderr=logfile)

def runMarvel(output_dir, marvel_bin, marvel_threads, logdir):
    logfile = os.path.join(logdir, "marvel.log")
    bins_dir = os.path.join()

    command = "python3 {marvel_bin} -i {bins_dir} -t {marvel_threads}".format(
        marvel_bin=marvel_bin,
        bins_dir=bins_dir,
        marvel_threads=marvel_threads
    )
    with open(logfile, "w") as logfile:
        subprocess.call(command, shell=True, stdout=logfile, stderr=logfile)

    pass

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
