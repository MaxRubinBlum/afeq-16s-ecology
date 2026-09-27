# Direct 99% OTU pipeline

This is the primary sequence-processing branch for ecological analyses.

## Rationale

The PacBio input reads were high quality. Primer removal was approximately 98%, and ordinary maxEE/length filtering retained a large fraction of the reads. The major loss in the DADA2 branch occurred during ASV inference.

Because this project uses 99% full-length 16S OTUs as the ecological unit, the direct pipeline clusters the quality-filtered reads rather than first requiring them to survive DADA2 inference.

## Step 1 — orient and trim primers

Cutadapt is run with a linked full-length amplicon definition:

```text
AGRGTTYGATYMTGGCTCAG ... AAGTCGTAACAAGGTARCY
```

`--revcomp` permits random CCS orientations and outputs consistently oriented reads.

Only reads containing the expected linked primer structure are retained.

## Step 2 — quality and length filtering

VSEARCH settings:

- `--fastq_qmax 93`
- `--fastq_maxee 2`
- `--fastq_minlen 1000`
- `--fastq_maxlen 1800`

Observed result:

- raw reads: 25,395,564
- filtered reads: 20,117,175
- retention: 79.22%

## Step 3 — pool and exact-dereplicate

All filtered sample FASTAs are combined.

Exact full-length dereplication is performed globally.

`--minuniquesize 2` prevents a one-read exact sequence from founding an OTU centroid. The original singleton reads are still retained in the pooled filtered-read file and can map back to an accepted OTU later.

## Step 4 — cluster at 99%

Exact non-singleton sequences are clustered with VSEARCH `--cluster_size --id 0.99`.

Clustering is abundance-sorted and produces representative centroid sequences.

## Step 5 — estimate OTU abundance before chimera screening

All quality-filtered reads are mapped back to raw 99% centroids.

The resulting sample-by-OTU table is summed across samples to calculate total abundance for each centroid.

## Step 6 — de novo chimera screening

Total abundance values are written onto centroid FASTA headers.

VSEARCH `--uchime_denovo` is then run on the 99% centroid set rather than on millions of individual reads.

## Step 7 — final mapping

All quality-filtered reads are mapped to the accepted non-chimeric 99% centroids at 99% identity.

Final validated outputs:

- 26,300 non-chimeric 99% OTUs
- 12,355,927 reads assigned to the final OTU table

The executable scripts are:

- `scripts/01_trim_filter.sh`
- `scripts/02_build_otu99.sh`
