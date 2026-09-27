# Project status

## Repository organization

The 16S repository is now organized in the same teaching-oriented style as the Afeq mcrA repository:

- numbered documentation chapters from project setup through ecology;
- numbered processing/QC scripts;
- ecology steps 13-20;
- one ecology runner;
- configuration template;
- metadata template;
- small reproducible QC summary;
- troubleshooting and GitHub workflow guides;
- tests.

The intended user is a student learning both the biological reasoning and the mechanics of the analysis.

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
- GTDB phylum/family/genus profiles
- repeated-rarefaction alpha diversity
- Bray-Curtis / PCoA
- site and month community-structure tests
- site-stratified depth and geochemical associations
- 16S-mcrA community-distance coupling
- depth/site/month-adjusted 16S taxon-mcrA lineage coupling

Current interpretation:

- 16S is treated as a bacterial-dominated community marker because the 27F-like primer strongly underrepresents Archaea.
- mcrA provides the targeted methane-cycling archaeal layer.
- MAGs are still in progress and are not part of the current integrated interpretation.

In progress:

- publication-level visualization of depth and geochemical gradients
- integrated 16S-mcrA figures
- refinement of publication-level taxon/association selection
- MAG reconstruction/analysis
- later GTDB-rank integration with MAGs
