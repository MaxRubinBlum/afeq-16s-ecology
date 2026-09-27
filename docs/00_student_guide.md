# Student guide

This repository records the complete validated processing logic for the Afeq PacBio Kinnex full-length 16S dataset.

## Read this first

The project contains two sequence-processing branches:

1. **Direct 99% OTU workflow — primary ecological dataset**
2. **QIIME 2 DADA2 CCS workflow — stringent comparison dataset**

Do not substitute one for the other without documenting the change.

## Why two branches exist

The raw PacBio data were high quality and primer matching was excellent. In the QIIME 2 DADA2 CCS branch, approximately 98% of reads had primers removed successfully and roughly 65–74% of raw reads passed the ordinary quality filter. However, most reads were then lost during DADA2 sequence inference, before chimera removal.

Because the intended ecological unit for this project is a 99% full-length 16S OTU, the primary workflow was changed to cluster the quality-filtered reads directly rather than require each sequence to survive ASV inference first.

The DADA2 output remains useful as a stringent sensitivity dataset.

## Primary workflow

Read the documents in this order:

1. `01_project_and_data.md`
2. `02_input_qc_and_manifests.md`
3. `03_qiime_dada2_comparison.md`
4. `04_direct_otu99_pipeline.md`
5. `05_taxonomy.md`
6. `06_analysis_decisions_qc.md`
7. `07_downstream_analysis.md`
8. `08_run_recipe.md`

## Rules

- Never commit raw FASTQs or large generated artifacts.
- Never rename biological samples manually after table construction.
- Keep run-3408 Jan resequencing libraries with the `-r3408` suffix unless a documented decision is made to combine them.
- GTDB is the primary taxonomy.
- SILVA is an independent taxonomy and the source used to flag chloroplast and mitochondrial OTUs.
- Keep methodological QC separate from biological interpretation.
