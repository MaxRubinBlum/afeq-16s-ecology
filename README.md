# Afeq full-length 16S ecology

Reproducible workflow for the Afeq wetland **full-length 16S rRNA gene** project.

This repository documents the analysis from PacBio Kinnex CCS FASTQ files to a final direct 99% OTU table, dual GTDB/SILVA taxonomy, bacterial-dominated ecological analyses, and integration with the mcrA dataset. It is written for a student who is comfortable with basic biology but may be new to command-line bioinformatics and ecological statistics.

> **Important:** raw FASTQ files, unpublished sample metadata, QIIME artifacts, classifiers/reference databases, large feature tables, and generated ecological results are intentionally not stored in GitHub. The repository contains the workflow, small QC summaries, templates, reproducible scripts, and explanations of the analytical decisions.

## What this workflow does

1. Inventory two PacBio sequencing runs and construct canonical sample IDs.
2. Exclude copied duplicate FASTQs from the second raw-data directory.
3. Orient full-length reads and trim the biological 16S primers with Cutadapt.
4. Filter PacBio reads by expected error and full-length size with VSEARCH.
5. Pool and exactly dereplicate filtered reads.
6. Cluster full-length sequences at 99% identity.
7. Perform abundance-aware de novo chimera screening.
8. Map all filtered reads back to the accepted 99% centroids.
9. Preserve a QIIME 2 DADA2 CCS branch as a stringent sensitivity comparison.
10. Classify final 99% OTUs with GTDB R226 and SILVA.
11. Build one master annotation and remove organelle/non-target features.
12. Harmonize and validate sample metadata.
13. Generate GTDB phylum/family/genus composition tables.
14. Calculate repeated-rarefaction richness and Shannon diversity.
15. Calculate Bray-Curtis dissimilarity, PCoA, PERMANOVA/PERMDISP, and depth structure.
16. Generate site-stratified bacterial taxon/geochemistry associations.
17. Compare bacterial-dominated 16S community turnover with the targeted mcrA community.
18. Generate depth/site/month-adjusted 16S taxon-mcrA lineage association tables.

## Start here

If you are new to bioinformatics, read these in order:

1. [Student guide](docs/00_student_guide.md)
2. [Project and data structure](docs/01_project_and_data.md)
3. [Environment setup](docs/02_environment_setup.md)
4. [Sample naming and metadata](docs/03_sample_naming_metadata.md)
5. [Primary full-length 99% OTU processing](docs/04_primary_sequence_processing.md)
6. [Taxonomy strategy](docs/05_taxonomy.md)
7. [GTDB and SILVA reference classifiers](docs/06_reference_classifiers.md)
8. [Master annotation and ecological filtering](docs/07_master_annotation_filtering.md)
9. [DADA2 comparison and Jan resequencing QC](docs/08_comparison_and_resequencing_qc.md)
10. [Ecology-ready analysis](docs/09_ecology.md)
11. [Troubleshooting](docs/10_troubleshooting.md)
12. [Analysis decisions and current QC](docs/11_analysis_decisions_qc.md)
13. [Copy-paste run recipe](docs/12_run_recipe.md)
14. [GitHub workflow](docs/13_github_workflow.md)
15. [Ecological analysis pipeline](docs/14_ecology_analysis_pipeline.md)
16. [16S-mcrA integration](docs/15_mcra_integration.md)

## Ecology analysis layer

After the final OTU table and taxonomy exports exist, run:

~~~bash
bash scripts/run_ecology_pipeline.sh config/config.sh
~~~

The ecology layer is documented in [docs/14_ecology_analysis_pipeline.md](docs/14_ecology_analysis_pipeline.md).

The repository documents methods, reasoning, inputs, outputs, and reproducible commands. Biological interpretation belongs in reports/manuscripts rather than hidden inside pipeline code.

## Main software

The completed workflow used:

- QIIME 2 amplicon 2026.1
- RESCRIPt
- Cutadapt
- VSEARCH
- SeqKit
- Python 3
- pandas
- NumPy
- SciPy
- statsmodels
- Matplotlib
- openpyxl

The QIIME environment used on the workstation was named:

~~~text
qiime2-amplicon-2026.1
~~~

## Primers

Biological full-length 16S primers:

~~~text
forward        AGRGTTYGATYMTGGCTCAG
reverse        RGYTACCTTGTTACGACTT
3' terminal    AAGTCGTAACAAGGTARCY
~~~

The Cutadapt primary workflow uses the forward primer and the forward-oriented reverse-terminal sequence with --revcomp so CCS reads in either orientation are standardized.

The forward primer is 27F-like and strongly bacterial-biased. Do not interpret the low archaeal fraction in this 16S dataset as the true archaeal fraction in sediment.

## Repository layout

~~~text
afeq-16s-ecology/
├── README.md
├── CONTRIBUTING.md
├── PROJECT_STATUS.md
├── config/
│   └── config.example.sh
├── docs/
├── metadata/
│   └── metadata_template.tsv
├── results/
│   ├── qc_summary.tsv
│   └── README.md
├── scripts/
├── tests/
└── .gitignore
~~~

## Reproducibility principle

Do not edit analysis outputs manually. If a filtering rule, taxonomic decision, prevalence threshold, rarefaction depth, or statistical design changes, change the script/configuration and regenerate the outputs.

## Data policy

This project is unpublished. Keep the GitHub repository **private** unless the PI explicitly decides to make the analysis public.

Do not commit:

- raw FASTQ files;
- full unpublished metadata workbooks;
- sample-level feature tables;
- QIIME .qza/.qzv files;
- GTDB/SILVA classifiers or databases;
- large FASTA/intermediate files;
- generated ecological tables or figures unless deliberately selected for release.

The supplied .gitignore prevents most accidental additions.

## Project management

- [Current project status](PROJECT_STATUS.md)
- [Contributing/version-control habits](CONTRIBUTING.md)
