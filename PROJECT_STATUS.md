# Project status

## Primary sequence processing

Validated and complete:

- [x] raw FASTQ inventory
- [x] duplicate raw-file audit
- [x] run-specific manifests
- [x] primer/orientation validation
- [x] read-length QC
- [x] direct Cutadapt + VSEARCH filtering
- [x] pooled exact dereplication
- [x] direct 99% OTU clustering
- [x] abundance-aware chimera screening
- [x] final read-to-OTU mapping
- [x] GTDB R226 classification
- [x] SILVA classification

## Validated final primary dataset

- 188 libraries
- 26,300 direct non-chimeric 99% OTUs
- 12,355,927 mapped reads
- GTDB and SILVA taxonomy available for every OTU ID in the count table

## Comparison branch

Complete:

- QIIME 2 DADA2 CCS by sequencing run
- merged DADA2 ASVs
- DADA2-derived 99% OTUs
- DADA2 retention diagnostic

The DADA2 table is retained as a stringent sensitivity dataset.

## Current downstream stage

In progress:

- master dual-taxonomy annotation
- organelle-filtered count table
- metadata harmonization
- resequencing QC
- taxonomic profiles
- alpha/beta diversity
- geochemical/environmental associations
- GTDB-rank comparison with MAGs
