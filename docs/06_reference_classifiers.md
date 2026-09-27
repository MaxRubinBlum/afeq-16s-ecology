# Reference classifiers

## Why two taxonomies?

The project keeps two independent classifications for every final 99% OTU.

### GTDB R226

GTDB is the primary nomenclature used for ecological tables because it provides a consistent modern bacterial/archaeal taxonomy and will also be useful for later genome-resolved integration.

Reference setup:

~~~text
GTDB release 226.0
domain: Both
database type: SpeciesReps
full-length SSU sequences
~~~

A full-length Naive Bayes classifier was trained with QIIME 2 / RESCRIPt.

### SILVA

SILVA provides an independent 16S classification, conventional names, and useful explicit labels for chloroplast and mitochondrial sequences.

## Classification parameters

For both full-length classifiers:

~~~text
confidence       = 0.7
read orientation = auto
query sequences  = final direct 99% OTU centroids
~~~

## Student rule

Do not choose whichever database gives the taxonomic name you prefer. Keep both assignments and use the predefined project policy:

- GTDB = primary ecological taxonomy;
- SILVA = cross-check and organelle/non-target identification.

Confidence is classifier confidence, not percent sequence identity.

## Primer-coverage limitation

The forward primer is 27F-like and the resulting dataset is strongly bacterial-biased. The fraction of reads classified as Archaea is therefore not an estimate of the true archaeal fraction in the sediment.

The current cross-marker interpretation is:

- 16S = bacterial-dominated community;
- mcrA = targeted methane-cycling archaeal community.
