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

## Downstream analysis status

Completed first-pass analyses:

- master GTDB + SILVA annotation
- chloroplast / mitochondria / Eukaryota / GTDB-unassigned filtering
- metadata harmonization
- Jan resequencing QC
- GTDB family/genus profiles
- repeated-rarefaction alpha diversity
- Bray-Curtis / PCoA
- site and month community-structure tests
- site-stratified depth and geochemical associations
- 16S–mcrA community-distance coupling
- depth/site/month-adjusted 16S taxon–mcrA lineage coupling

In progress:

- selection of publication-level taxa/associations
- visualization of depth and geochemical gradients
- integrated 16S–mcrA figures
- GTDB-rank comparison with MAGs
