# Student guide: how to use this project

## First: what is this dataset?

This project uses PacBio Kinnex/CCS full-length 16S rRNA gene amplicons from Afeq wetland sediment samples.

The final ecological units are **99% full-length OTUs**. An OTU here is a cluster of closely related full-length 16S sequences defined at 99% sequence identity.

This is different from the mcrA project, where DADA2 ASVs are the main sequence units.

## What the 16S marker tells us

The 16S data describe the broader sediment microbial community, but the primer pair is strongly bacterial-biased because the forward primer is 27F-like.

Therefore:

- use 16S primarily to describe the **bacterial-dominated community**;
- do not estimate total archaeal abundance from the 16S read fractions;
- use the mcrA dataset for the targeted methane-cycling archaeal community.

## What you are expected to understand before running anything

You do not need to be a bioinformatician, but you should be able to answer:

1. Which sample does each FASTQ file represent?
2. Which sequencing run produced the file?
3. Which files are genuine run-3408 files and which are copied run-2860 files?
4. Which primers were used?
5. Why are reads expected to be roughly full-length 16S size?
6. What output should each step produce?
7. What QC result would make you stop rather than continue?
8. Which samples have validated depth/geochemistry metadata?
9. Why are the Jan -r3408 libraries kept separate?

If any of these are unclear, resolve them before starting a long analysis.

## Recommended working habits

- Never modify raw FASTQ files.
- Never rename raw files without recording the original name.
- Use canonical biological IDs such as Jan25-EA1-4.
- Save commands in scripts rather than relying on shell history.
- Run each major step only after checking the previous step.
- Do not manually edit OTU tables or taxonomy outputs.
- Keep GTDB and SILVA classifications side by side.
- Keep the DADA2 branch as a sensitivity analysis rather than quietly deleting it.
- Use tmux for long classifier jobs.
- Keep sample-level unpublished results outside GitHub.

## Workflow in plain language

### Step 1 - identify samples

The two sequencing deliveries use different filename formats. scripts/01_make_manifests.py converts them into canonical IDs and manifests.

The second raw-data directory also contains copied 2860 files. The script deliberately selects only the real 3408-prefixed FASTQs.

### Step 2 - orient and trim full-length reads

PacBio CCS reads can appear in either orientation. Cutadapt identifies the expected linked full-length primer structure, reverses reads when necessary, and removes the primers.

### Step 3 - filter by quality and size

VSEARCH removes reads with excessive expected errors and sequences outside the 1000-1800 bp working range.

PacBio quality scores require fastq_qmax 93.

### Step 4 - build direct 99% OTUs

Filtered reads are pooled, exactly dereplicated, clustered at 99%, screened for chimeras, and then all filtered reads are mapped back to the accepted non-chimeric centroids.

This is the primary ecological feature table.

### Step 5 - keep DADA2 as a comparison

We also tested QIIME 2 DADA2 CCS. Primer removal and ordinary filtering worked, but most reads were lost during ASV inference.

Do not interpret that branch as the main dataset without revisiting the documented QC decision.

### Step 6 - classify every final OTU twice

GTDB R226 is the primary ecological taxonomy.

SILVA is retained as an independent classification and helps identify chloroplast, mitochondrial, and other non-target sequences.

### Step 7 - build one filtered working table

The master annotation combines both taxonomies and applies the project filtering rules once.

All later ecological analyses should use the same approved working table.

### Step 8 - validate metadata

Sample identity comes before statistics. Harmonize workbook labels, report unmatched samples, and check month/site agreement.

### Step 9 - describe ecology before testing mechanisms

Start with:

- taxonomic composition;
- depth profiles;
- Shannon diversity;
- Bray-Curtis/PCoA.

Only then move to geochemical association tests.

### Step 10 - integrate with mcrA

Use exact shared sample IDs.

The strongest first question is whether pairwise 16S community differences track pairwise mcrA community differences.

Taxon-to-lineage correlations are a second layer and do not prove direct interaction.

## Where to stop and ask for help

Stop if:

- expected sample counts are wrong;
- many primer-trimmed reads disappear unexpectedly;
- VSEARCH reports invalid PacBio quality values;
- the final OTU count changes unexpectedly;
- GTDB/SILVA feature IDs do not exactly match the OTU table;
- metadata month/site conflicts with the sequence ID;
- a result depends on silently dropping samples;
- a taxonomic conclusion is more specific than the classifier output supports;
- you are about to interpret the low 16S archaeal fraction as biological abundance.
