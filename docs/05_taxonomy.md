# Taxonomy

Two independent full-length 16S taxonomies are retained.

## GTDB — primary taxonomy

GTDB is the primary taxonomy because it provides a consistent bacterial/archaeal nomenclature and keeps the 16S dataset ready for later genome-resolved integration once the MAG analysis is complete.

Validated reference:

- GTDB release 226.0
- SSU species representatives
- Bacteria + Archaea
- full-length Naive Bayes classifier
- QIIME 2 / q2-feature-classifier

The local QIIME 2 Amplicon 2026.1 RESCRIPt plugin supports GTDB through R226.

Classifier parameters used for queries:

- confidence: 0.7
- read orientation: auto
- full-length query OTU representatives

## SILVA — secondary taxonomy

SILVA is retained as an independent 16S classification and for conventional taxonomic nomenclature.

It is also used to identify obvious non-prokaryotic organelle amplicons.

## Organelle and non-target filtering

Before bacterial-dominated ecological analyses, flag and remove:

- `Chloroplast`
- `Mitochondria`
- SILVA `d__Eukaryota`
- OTUs lacking a GTDB domain assignment to Bacteria or Archaea

In the validated 26,300-OTU dataset:

- 112 OTUs were labelled chloroplast
- 111 OTUs were labelled mitochondria

Together chloroplast and mitochondrial reads represented approximately 1.18% of the unfiltered table. The final working filter also removes low-abundance SILVA Eukaryota and GTDB-unassigned-domain OTUs.

## Primer-coverage note

The forward primer `AGRGTTYGATYMTGGCTCAG` is 27F-like and the dataset is strongly bacterial-biased. Archaeal relative abundance in this amplicon dataset must therefore **not** be interpreted as an estimate of total archaeal abundance in the sediment.

For the current integrated ecology:

- 16S = bacterial-dominated sediment-community structure
- mcrA = targeted methane-cycling archaeal community

## Master annotation table

The final annotation table should contain at minimum:

```text
OTU_ID
GTDB_taxonomy
GTDB_confidence
SILVA_taxonomy
SILVA_confidence
is_chloroplast
is_mitochondria
exclude_from_prokaryotic_ecology
```

Generate this table with `scripts/06_build_master_annotation.py`.

## Interpretation policy

GTDB and SILVA confidence values are classification confidence, not sequence identity.

MAG integration is a future analysis layer. Once MAGs are finalized, compare 16S and MAGs at common GTDB ranks such as genus, family, or order rather than equating 99% 16S OTUs with genome species.
