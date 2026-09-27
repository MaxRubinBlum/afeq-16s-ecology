# 16S-mcrA integration

This analysis connects two deliberately different marker systems.

## Biological roles of the markers

### Full-length 16S

The 27F-like primer makes this dataset strongly bacterial-biased. Use it to describe the broader bacterial sediment community and its depth/geochemical structure.

### mcrA

mcrA directly targets methane-cycling archaea and resolves methanogens and anaerobic methane-oxidizing lineages much better than this 16S assay.

The two markers are therefore complementary, not redundant.

## Shared samples

Only exact sample IDs present in the filtered 16S table, corrected metadata, and retained mcrA ecology table enter cross-marker analyses.

The first integrated analysis contained 96 exact shared samples.

## Community-level coupling

Script:

~~~text
scripts/12_mcra_16s_coupling.py
~~~

The script calculates Bray-Curtis distances independently for 16S and mcrA and tests whether pairwise community differences covary.

This is the primary cross-marker test because it does not require direct taxonomic equivalence between the two marker systems.

## Taxon-to-lineage coupling

Script:

~~~text
scripts/14_mcra_taxa_coupling.py
~~~

The analysis:

1. aggregates 16S to GTDB family or genus;
2. filters to recurrent/abundant bacterial taxa;
3. Hellinger-transforms 16S and mcrA relative abundance;
4. removes broad site, month, and linear depth effects;
5. correlates residuals;
6. applies FDR correction.

## Interpretation limits

A significant taxon-to-mcrA association does not establish syntrophy, electron transfer, or direct physical interaction.

Use these associations to identify candidate bacterial community modules accompanying methane-cycling transitions.

## Future MAG layer

MAGs are still in progress and are not part of the current integrated interpretation. Once available, they can provide a genome-resolved bridge between taxonomic patterns and metabolic potential.
