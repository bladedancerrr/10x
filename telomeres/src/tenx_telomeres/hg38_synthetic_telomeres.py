#!/usr/bin/env python

import math
import gzip
from typing import List
from pathlib import Path
from collections import defaultdict, deque
from itertools import islice, tee
from Bio import SeqIO
from Bio.Seq import MutableSeq, Seq
from Bio.SeqRecord import SeqRecord
from Bio.Alphabet import generic_dna

import logging

# Set log level
loglevel = logging.INFO
logging.basicConfig(level=loglevel)
log = logging.getLogger(__name__)


## Global
# Telomeric hexamer
KMER_K = 6

# Human telomeric hexamers
PATTERN1 = 'ccctaa'
PATTERN2 = 'ttaggg'


def find_N_boundaries(seq: str):
    ''' Returns all N-boundaries in a sequence via tuple: (first, second)
    '''
    pos = first = second = 0

    # first N stretch
    for base in seq:
        if 'N' in base:
            pos = pos + 1
        else:
            first = pos
            break

    base = None
    pos = 0

    # last N stretch
    for base in reversed(seq):
        if 'N' in base:
            pos = pos + 1
        else:
            second = len(seq) - pos - 1
            break

    return (first, second)


# Elongate forward and backward N's, respecting telomeric patterns
def elongate_forward_sequence(seq):
    # Determine N boundaries in the sequence
    boundary, boundary_r = find_N_boundaries(seq)

    # K-mer telomeric sequence right after the N boundary
    kmer_seq = seq[boundary:boundary + KMER_K]

    # How many chunks to elongate and remainder
    chunks = len(seq[0:boundary]) % KMER_K
    chunks_r = len(seq[0:boundary]) / KMER_K

    # Capture remainder of the pattern to fit in sequence
    kmer_seq_r = kmer_seq[math.floor(chunks_r):]
    tmp_seq = kmer_seq_r
    
    # Build forward sequence
    for _ in range(0, chunks - 2): # XXX 2?
        tmp_seq = tmp_seq + kmer_seq

    # Attach inner pattern
    tmp_seq = tmp_seq + seq[boundary:boundary_r] + seq[boundary_r:]

    return tmp_seq

def elongate_reverse_sequence(seq):
    # Determine N boundaries in the sequence
    boundary, boundary_r = find_N_boundaries(seq)

    # K-mer telomeric sequence right before the N boundary
    kmer_seq = seq[boundary_r - KMER_K:boundary_r]

    # How many chunks to elongate and remainder
    chunks = len(seq[boundary_r:]) % KMER_K
    chunks_r = len(seq[boundary_r:]) / KMER_K

    # Start with the N boundary
    tst_seq = seq[0:boundary]

    # Attach inner pattern
    tst_seq = tst_seq + seq[boundary:boundary_r]

    # Build reverse sequence
    for _ in range(0, chunks):
        tst_seq = tst_seq + kmer_seq

    # Capture remainder of the pattern to fit in sequence
    kmer_seq_r = kmer_seq[0:math.floor(chunks_r)]
    tst_seq = tst_seq + kmer_seq_r

    return tst_seq


def determine_hexamer(seq: str):
    ''' 
    Builds a table containing hexamers and all its possible rotations.
    
    Useful to determine boundary conditions between N-regions and telomeric
    repeats on the reference genome(s).

    Also takes the sequence seq and tries to find which hexamer pattern it has
    '''
    hexamer_table = defaultdict(list)
    rotated = []

    # Seed table with first non-rotated "canonical" hexamer
    hexamer_table[PATTERN1] = PATTERN1
    hexamer_table[PATTERN2] = PATTERN2

    for pat in [PATTERN1, PATTERN2]:
        dq = deque(pat)
        for rot in range(1, len(pat)):
            dq.rotate(rot)
            rotated.append(''.join(dq))

        hexamer_table[pat] = rotated

        for k, v in hexamer_table.items():
            for kmer in v:
                if str(str.upper(kmer)) in str(str.upper(seq)):
                    return str.upper(k)
    
    return None


#def main(genome_build='../../data/processed/hg38_synthetic/new_hg38.fa.gz'):
def main(genome_build='../../data/external/chr11.fa.gz'):
    with gzip.open(genome_build, "rt") as hg38_fa:
        record_dict = SeqIO.to_dict(SeqIO.parse(hg38_fa, "fasta"))
        for _, chrom_attrs in record_dict.items():
            sequence = chrom_attrs.seq
            seq_id = chrom_attrs.id

            if "_" not in seq_id:
                if "chr11" in seq_id:
                    boundaries = find_N_boundaries(sequence)
                    print("{}\t{}:\t\t{}\t...\t{}\t...\t{}".format(seq_id.split(':')[0], boundaries, sequence[boundaries[0]:boundaries[0] + KMER_K + 30], sequence[boundaries[1] - KMER_K - 30:boundaries[1]], len(sequence)))

            #detected_hexamer = determine_hexamer(sequence)

            #final_seq = elongate_forward_sequence(sequence)
            #final_seq = elongate_reverse_sequence(final_seq)

#        with open("hg38_elongated_telomeres.fasta", "w") as output_handle:
#            SeqIO.write(new_hg38, output_handle, "fasta")

if __name__ == "__main__":
    main()