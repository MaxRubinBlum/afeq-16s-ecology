# Comparison branch and Jan resequencing QC

## Why this chapter exists

Two separate QC questions arose during processing:

1. should DADA2 ASV inference be the main way to process these full-length PacBio reads?
2. should the repeated Jan run-3408 libraries be merged with their same-name run-2860 libraries?

The answer to both was: not automatically.

## DADA2 comparison branch

The QIIME 2 DADA2 CCS workflow is preserved as a stringent sensitivity branch.

Observed pattern:

- primer removal was approximately 98%;
- ordinary quality filtering retained roughly 65-74% of raw reads;
- the major read loss occurred during DADA2 inference, before chimera removal;
- the DADA2-derived 99% table retained only about 0.64 million reads.

By contrast, the direct Cutadapt + VSEARCH workflow retained:

~~~text
20,117,175 reads after primer/quality/length filtering
12,355,927 reads in the final non-chimeric 99% OTU table
~~~

Therefore the direct 99% workflow is primary and DADA2 is a sensitivity comparison.

## Jan run-3408 libraries

Eleven Jan biological names were sequenced again in run 3408 and carry the suffix -r3408.

Use:

~~~bash
python3 scripts/08_compare_jan_resequencing.py   --table "$FILTERED_OTU_TABLE"   --annotation "$MASTER_TAXONOMY"   --out "$ECOLOGY_OUT/qc/jan_resequencing.tsv"
~~~

The script normalizes each library to relative abundance before calculating Bray-Curtis similarity, so library-size differences do not dominate the comparison.

## Decision

Do not merge the -r3408 libraries by name alone. Preserve them separately until the biological/technical provenance is resolved and the intended statistical treatment is documented.
