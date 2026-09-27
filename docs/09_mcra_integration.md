# 16S–mcrA integration analysis

This stage links the broad 16S community to the targeted mcrA community while avoiding a direct equivalence between 16S OTUs and mcrA lineages.

## Shared sample set

Use only exact sample IDs present in:

- the organelle/eukaryote-filtered 16S table
- corrected sediment metadata
- the retained mcrA ecological dataset

Jan run-3408 resequencing libraries remain excluded from this integration until their provenance is resolved.

## Community-level coupling

Use `scripts/12_mcra_16s_coupling.py` to compare 16S and mcrA Bray–Curtis distance matrices.

This asks whether samples that differ strongly in the whole prokaryotic community also differ strongly in the methane-cycling community.

## Taxon–environment associations

Use `scripts/13_taxa_environment_associations.py`.

Default environmental variables:

- depth
- methane
- sulfate
- sulfide
- dissolved Fe
- DIC

Associations are calculated separately within each wetland using Spearman correlation.

Taxa are tested only when they meet both:

- prevalence >= 20%
- mean relative abundance >= 0.1% within the tested site

Benjamini–Hochberg FDR is applied across all tests at a given taxonomic rank.

Family-level results are preferred for the primary interpretation because GTDB family assignment is more complete and stable than genus assignment. Genus-level results provide additional detail.

## Direct 16S–mcrA taxon coupling

Use `scripts/14_mcra_taxa_coupling.py`.

The method:

1. calculates 16S relative abundance at GTDB family or genus level
2. retains taxa with >=20% prevalence and >=0.1% mean abundance
3. Hellinger-transforms 16S taxa and mcrA lineage relative abundances
4. removes site, month and linear depth effects from each variable
5. correlates residuals with Spearman correlation
6. controls FDR across all taxon × mcrA-lineage tests

These are ecological co-variation tests. They do not demonstrate direct metabolic interaction.

## Interpretation rules

- Treat family-level associations as the primary taxonomic result.
- Use genus-level associations when they reinforce a family-level pattern or identify a biologically interpretable lineage.
- Do not interpret correlation as syntrophy, electron transfer or direct partnership without independent evidence.
- Site-specific geochemical associations with small n, especially sulfide/DIC measurements at EA3 or EA4, should be treated as provisional even when FDR-significant.
- Direct agreement between homologous 16S and mcrA names may be weak because universal 16S reads contain a very small archaeal fraction, whereas mcrA is a targeted functional marker.
