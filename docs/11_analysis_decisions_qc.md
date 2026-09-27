# Analysis decisions and current QC

This file records decisions that materially affect the final 16S dataset. A student should read it before changing thresholds.

## 1. PacBio Kinnex input

The libraries are single-FASTQ full-length 16S CCS/Kinnex data, not paired-end Illumina reads.

## 2. Raw sequencing runs

- run 2860: 62 libraries;
- run 3408: 126 genuine libraries;
- total: 188 libraries.

Six copied run-2860 files present in the second raw-data directory were byte-identical duplicates and were excluded.

## 3. Full-length primer pair

Forward:

~~~text
AGRGTTYGATYMTGGCTCAG
~~~

Reverse primer:

~~~text
RGYTACCTTGTTACGACTT
~~~

Cutadapt uses the forward-oriented reverse-terminal sequence:

~~~text
AAGTCGTAACAAGGTARCY
~~~

with --revcomp to orient reads.

## 4. Length and quality filtering

Working length range:

~~~text
1000-1800 bp
~~~

VSEARCH filtering uses maximum expected errors of 2 and fastq_qmax 93.

The direct workflow retained 20,117,175 of 25,395,564 raw reads after primer/quality/length filtering: 79.22%.

## 5. Why the direct 99% workflow is primary

DADA2 primer removal and ordinary filtering worked well, but most reads were lost during DADA2 inference. The DADA2-derived 99% table retained only about 0.64 million reads.

The direct workflow instead clusters quality-filtered full-length reads at 99% identity and maps all filtered reads back to accepted non-chimeric centroids.

Final direct dataset:

~~~text
26,300 non-chimeric 99% OTUs
12,355,927 mapped reads
~~~

DADA2 is retained as a stringent sensitivity branch.

## 6. Exact singleton handling

Global exact dereplication uses a minimum unique size of 2 for centroid founding. Exact sequences observed once cannot found a cluster centroid, but the original singleton reads remain in the pooled filtered reads and can map back to an accepted 99% OTU during final mapping.

## 7. Chimera handling

De novo UCHIME is run on abundance-annotated 99% centroids for computational efficiency. This is a pragmatic workflow decision and should be retained in the methods record.

## 8. Taxonomy

- GTDB R226 = primary ecological taxonomy;
- SILVA = independent classification and organelle/non-target detection.

All 26,300 OTU IDs match one-to-one between the OTU table and both taxonomy outputs.

## 9. Bacterial-dominated interpretation

The 27F-like forward primer underrepresents Archaea. Low archaeal read abundance in this dataset must not be interpreted as low archaeal abundance in sediment.

For the current integrated ecology:

- 16S describes the bacterial-dominated community;
- mcrA describes the targeted methane-cycling archaeal community.

## 10. Ecology filtering

Remove chloroplast, mitochondrial, SILVA-Eukaryota, and GTDB-unassigned-domain OTUs before bacterial community analysis.

Validated working table:

~~~text
26,054 OTUs
12,209,120 reads
~~~

## 11. Jan resequencing libraries

Eleven Jan identities reappear in run 3408 and retain the suffix -r3408. They are not merged automatically because their 99% OTU profiles do not behave as simple interchangeable technical duplicates.

## 12. Current ecological design

Use EA1-EA4 samples with validated metadata for depth/geochemistry inference. Keep site-stratified depth/environment analyses as the default because pooled gradients can confound site identity with environmental response.

Use repeated rarefaction to 5,000 reads, 50 iterations, for publication-style Shannon comparisons.

Use 999 permutations and a fixed random seed for permutation-based tests unless a documented rerun changes these values.
