from Bio import SeqIO
from Bio.Seq import Seq

contigs_file = "../data/contigs.fasta"
contigs_filtered_file = "../data/contigs_filtered.fasta"
cutoff_len = 1000


def filterByLength(contigs_file, contigs_filtered_file, cutoff_len):
    contigs_filtered = []
    for record in SeqIO.parse(contigs_file, "fasta"):
        if len(record.seq) >= cutoff_len:
            contigs_filtered.append(record)
    SeqIO.write(contigs_filtered, contigs_filtered_file, "fasta")

filterByLength(contigs_file, contigs_filtered_file, cutoff_len)
