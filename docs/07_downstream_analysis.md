# Downstream analysis

The sequence-processing workflow ends with:

- direct non-chimeric 99% OTU FASTA
- sample-by-OTU count table
- GTDB taxonomy
- SILVA taxonomy
- metadata

## Preparation

Run:

```bash
python3 scripts/06_build_master_annotation.py \
  --table /path/to/otu-table-99.tsv \
  --gtdb /path/to/gtdb/taxonomy.tsv \
  --silva /path/to/silva/taxonomy.tsv \
  --outdir analysis_ready
```

This generates:

- a combined master taxonomy
- a filtered bacterial-dominated OTU count table
- QC summary

## Sequencing/resequencing QC

Use `scripts/08_compare_jan_resequencing.py` to compare same-name Jan run-2860 and run-3408 libraries without merging them.

The output reports Bray-Curtis similarity at OTU level and, when taxonomy is supplied, at selected taxonomic ranks.

## Taxonomic composition

Use `scripts/09_taxonomic_profiles.py` to aggregate the filtered table at a GTDB or SILVA taxonomic rank and calculate relative abundances.

## Alpha diversity

Use `scripts/10_alpha_diversity.py` for observed richness and Shannon diversity.

Sampling-depth dependence must be evaluated before interpreting richness.

## Beta diversity

Use `scripts/11_bray_pcoa.py` for Bray-Curtis dissimilarity and PCoA coordinates.

PERMANOVA and environmental models should be run only after metadata factors and repeated/technical samples are explicitly defined.

## Current cross-marker integration

The current integrated analysis combines:

- bacterial-dominated 16S community structure
- mcrA methane-cycling archaeal community structure

Use `scripts/12_mcra_16s_coupling.py`, `scripts/13_taxa_environment_associations.py`, and `scripts/14_mcra_taxa_coupling.py`.

## Future MAG integration

MAGs are still in progress and are not used in the current ecological interpretation.

Once the MAG dataset is finalized:

1. retain MAG taxonomy in GTDB
2. aggregate 16S counts to GTDB genus/family/order
3. convert MAG presence/abundance to the same rank
4. compare shared and unique lineages at the common rank

This avoids treating a 99% 16S cluster as equivalent to a GTDB genome species.
