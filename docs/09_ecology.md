# Ecology-ready analysis

This chapter defines the ecological questions and which data layer should be used for each.

## Start from the filtered OTU table

The primary ecological matrix is:

~~~text
otu-table-99-prokaryotes.tsv
~~~

Despite the filename, interpret it as a bacterial-dominated 16S table because the 27F-like forward primer underrepresents Archaea.

## Main ecological questions

### Community composition

Which bacterial lineages dominate each site, month, and sediment depth?

Use GTDB phylum/family/genus relative-abundance profiles.

### Alpha diversity

How does within-sample 99%-OTU diversity vary with site, season, and depth?

Use repeated rarefaction before comparing Shannon diversity across samples with unequal library sizes.

### Beta diversity

How strongly do site, month, and depth structure community composition?

Use Bray-Curtis dissimilarity, PCoA, PERMANOVA, PERMDISP, and site-stratified depth tests.

### Geochemical associations

Which recurrent bacterial families/genera covary with depth, methane, sulfate, sulfide, Fe, or DIC?

Use site-stratified Spearman correlations with prevalence/abundance filtering and FDR correction.

### mcrA integration

Do changes in the bacterial-dominated community track changes in the methane-cycling archaeal community?

Use shared sample IDs only. Community-level distance coupling is the first analysis; taxon-to-lineage correlations are secondary and must not be interpreted as direct metabolic interactions.

## Current metadata scope

EA1-EA4 have the validated depth/geochemistry framework used for inferential analyses. Additional P and EN samples can be retained for composition where appropriate but should not be silently mixed into analyses requiring missing metadata.
