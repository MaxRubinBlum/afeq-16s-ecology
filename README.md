# Afeq full-length 16S ecology

Reproducible processing and analysis workflow for PacBio Kinnex full-length 16S rRNA gene data from the Afeq sediment time series.

This repository documents the **methods, QC decisions, executable pipelines, and analysis code**. It intentionally does not contain raw FASTQ files, large QIIME 2 artifacts, or biological interpretation.

## Current primary workflow

The primary ecological feature table is generated with a direct 99% OTU workflow:

```text
PacBio Kinnex CCS FASTQ
        |
        v
Cutadapt: orient reads + trim full-length 16S primers
        |
        v
VSEARCH: maxEE and length filtering
        |
        v
pooled exact dereplication
        |
        v
VSEARCH abundance-sorted clustering at 99%
        |
        v
abundance-aware de novo chimera screening
        |
        v
map all filtered reads back to accepted centroids
        |
        v
sample x 99% OTU count table
        |
        +--> GTDB R226 full-length Naive Bayes taxonomy
        |
        +--> SILVA full-length Naive Bayes taxonomy
```

The earlier QIIME 2 DADA2 CCS workflow is retained as a stringent comparison branch.

## Validated dataset checkpoints

- sequencing run 2860: 62 libraries
- sequencing run 3408: 126 libraries
- total libraries: 188
- six copied run-2860 Jan EA4 FASTQs in the second directory were byte-identical duplicates and were excluded from run 3408 input
- raw reads: 25,395,564
- direct primer + quality/length-filtered reads: 20,117,175 (79.22%)
- final direct non-chimeric 99% OTUs: 26,300
- final direct OTU table: 12,355,927 mapped reads
- GTDB and SILVA outputs each match the 26,300 OTU identifiers one-to-one

See `docs/06_analysis_decisions_qc.md` for the reasoning behind the final workflow.

## Taxonomy policy

- **GTDB R226**: primary taxonomy because MAGs are classified with GTDB and downstream 16S-MAG comparisons require a common nomenclature.
- **SILVA**: secondary independent taxonomy, conventional 16S nomenclature, and organelle identification.
- Chloroplast and mitochondrial OTUs should be removed before prokaryotic ecological analyses.

## Repository layout

```text
config/       example paths and parameters
docs/         student-facing workflow and decision log
scripts/      executable pipeline and analysis scripts
metadata/     metadata templates / small curated metadata files only
results/      README and small non-interpretive QC summaries only
tests/        lightweight checks
```

## Large files

Do **not** commit FASTQ, QZA, QZV, BIOM, large FASTA, or full generated count tables. These remain on the analysis workstation.

## Software

Core tools used in the validated workflow:

- Cutadapt
- VSEARCH 2.27.1
- QIIME 2 Amplicon 2026.1
- q2-feature-classifier / scikit-learn
- RESCRIPt
- Python 3

Exact commands and parameters are recorded in `docs/` and `scripts/`.
