# Primary full-length 99% OTU processing

This is the primary sequence-processing branch for the Afeq 16S project.

The final ecological units are 99% full-length OTUs produced directly from primer-trimmed, quality-filtered PacBio CCS reads.

## 1. Why this is the primary branch

The raw reads are high-quality full-length CCS reads. A QIIME 2 DADA2 CCS workflow was tested, but most reads were lost during sequence inference even though primer recognition and ordinary quality filtering worked well.

Because the project intentionally uses 99% full-length OTUs for ecological analysis, the main workflow clusters the high-quality reads directly rather than requiring them to survive ASV inference first.

The DADA2 workflow is retained as a documented sensitivity branch.

## 2. Generate manifests

Script:

~~~text
scripts/01_make_manifests.py
~~~

The manifest generator:

- selects 62 run-2860 libraries;
- selects 126 genuine run-3408 libraries;
- ignores copied 2860 FASTQs in the second directory;
- creates canonical biological sample IDs;
- appends -r3408 to repeated Jan run-3408 libraries;
- writes Unix line endings.

## 3. Orient and trim primers

Script:

~~~text
scripts/02_trim_filter.sh
~~~

Cutadapt uses a linked full-length amplicon pattern:

~~~text
AGRGTTYGATYMTGGCTCAG ... AAGTCGTAACAAGGTARCY
~~~

The --revcomp option handles CCS reads arriving in either orientation.

Only reads containing the expected linked primer structure are retained.

## 4. Quality and length filtering

VSEARCH settings:

~~~text
fastq_qmax   93
fastq_maxee  2
min length   1000 bp
max length   1800 bp
~~~

The explicit qmax value is required because PacBio CCS qualities can exceed the VSEARCH default of 41.

Validated result:

~~~text
raw reads       25,395,564
filtered reads  20,117,175
retention       79.22%
~~~

## 5. Pool and exact-dereplicate

Script:

~~~text
scripts/03_build_otu99.sh
~~~

All filtered sample FASTAs are pooled.

Exact full-length dereplication uses a minimum unique size of 2. An exact sequence observed only once cannot found an OTU centroid, but the original read remains in the pooled filtered reads and can map to an accepted OTU at the final mapping step.

## 6. Cluster at 99%

VSEARCH clusters exact non-singleton sequences at:

~~~text
identity = 0.99
strand   = plus
~~~

Reads are already oriented by Cutadapt, so only the plus strand is required.

## 7. Add abundance and screen chimeras

All filtered reads are first mapped back to the raw 99% centroids.

Total OTU abundance is then written onto centroid headers and VSEARCH UCHIME-denovo is applied to the abundance-annotated 99% centroids.

This is a computationally practical abundance-aware chimera screen.

## 8. Final mapping

All filtered reads are mapped to the accepted non-chimeric centroids at 99% identity.

Validated result:

~~~text
non-chimeric 99% OTUs  26,300
mapped reads             12,355,927
~~~

These are the primary sequence units used for taxonomy and ecological analysis.

## 9. Checkpoint before taxonomy

Confirm:

- 188 samples are present;
- final OTU count is 26,300 for the validated run;
- the final OTU table contains 12,355,927 mapped reads;
- centroid headers are unique;
- no sample column is empty;
- run-3408 Jan samples remain distinguishable with the -r3408 suffix.

Do not proceed if these checkpoints unexpectedly change.
