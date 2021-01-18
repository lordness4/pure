import os
import subprocess




def createBins(reads1, reads2, contig_file, logdir, outdir, metabat_m, metabat_s):
    # workflow from: https://www.hadriengourle.com/tutorials/meta_assembly/
    logfile=os.path.join(logdir, "binning.log")
    index_file=os.path.join(outdir, "sample")
    bamfile=os.path.join(outdir, "sample.bam")
    sorted_bamfile=os.path.join(outdir, "sample.sorted.bam")

    with open(logfile, "w") as logfile:
        # first index
        command="bowtie2-build {contig_file} {index_file}".format(
            contig_file=contig_file,
            index_file=index_file)
        subprocess.call(command, shell=True, stdout=logfile, stderr=logfile)


        # map reads to contigs
        command="bowtie2 -x {index_file} -1 {reads1} -2 {reads2}\
         | samtools view -bS -o {bamfile}".format(
             index_file=index_file,
             reads1=reads1,
             reads2=reads2,
             bamfile=bamfile)
        subprocess.call(command, shell=True, stdout=logfile, stderr=logfile)

        # sort bam file and index bam file
        command="samtools sort {bamfile} -o {sorted_bamfile}".format(
            bamfile=bamfile,
            sorted_bamfile=sorted_bamfile)
        subprocess.call(command, shell=True, stdout=logfile, stderr=logfile)

        # index sorted file
        command="samtools index {sorted_bamfile}".format(
            sorted_bamfile=sorted_bamfile)
        subprocess.call(command, shell=True, stdout=logfile, stderr=logfile)

        # run metabat (switches cwd but switches also back to where we were)
        cwd = os.getcwd()
        os.chdir(outdir)
        command="runMetaBat.sh -m {metabat_m} -s {metabat_s} {contig_file} {sorted_bamfile}".format(
            metabat_m=metabat_m,
            metabat_s=metabat_s,
            contig_file=contig_file,
            sorted_bamfile=sorted_bamfile
        )
        subprocess.call(command, shell=True, stdout=logfile, stderr=logfile)
        os.chdir(cwd)
