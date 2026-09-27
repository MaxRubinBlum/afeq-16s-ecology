# Taxonomy

Two independent full-length 16S taxonomies are retained.

## GTDB - primary ecological taxonomy

GTDB R226 is the primary taxonomy used in ecological summaries.

Reasons:

- consistent modern bacterial/archaeal naming;
- useful family/genus hierarchy for environmental analysis;
- compatible with later genome-resolved work.

The project uses the GTDB R226 SpeciesReps full-length SSU reference set for Bacteria + Archaea.

## SILVA - secondary taxonomy

SILVA is retained as an independent 16S classification and for conventional nomenclature.

It is especially useful for explicit identification of:

- chloroplast;
- mitochondria;
- Eukaryota/non-target sequences.

## Why keep both?

No reference taxonomy is perfect.

Do not choose whichever assignment looks more familiar. Preserve both and keep the project rule stable:

~~~text
GTDB  = primary ecological nomenclature
SILVA = independent cross-check + organelle/non-target screen
~~~

## Classifier confidence

The QIIME classification output contains a confidence score.

This is **classifier confidence**, not percent sequence identity and not proof of species-level correctness.

## Taxonomic resolution

Family-level analysis is often the most stable ecological level in this dataset.

Genus-level analyses are useful but should be interpreted with awareness that many OTUs do not resolve equally well.

Species labels should be treated much more cautiously.

## Primer-coverage caveat

The forward primer is 27F-like and underrepresents Archaea.

Therefore, low archaeal relative abundance in the 16S table must not be interpreted as evidence that Archaea are rare in the sediment.

For methane-cycling archaea, use the mcrA marker as the targeted dataset.

See docs/06_reference_classifiers.md for the classifier construction and policy, and docs/07_master_annotation_filtering.md for the final filtering rules.
