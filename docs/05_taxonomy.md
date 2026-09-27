# Taxonomy

Two independent full-length 16S taxonomies are retained.

## GTDB — primary taxonomy

GTDB is the primary taxonomy because the project's MAGs are classified with GTDB and direct 16S-versus-MAG comparisons require a common taxonomy.

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

## Organelle filtering

Before prokaryotic ecological analyses, flag and remove OTUs whose SILVA taxonomy contains:

- `Chloroplast`
- `Mitochondria`

In the validated 26,300-OTU dataset:

- 112 OTUs were labelled chloroplast
- 111 OTUs were labelled mitochondria

Together chloroplast and mitochondrial reads represented approximately 1.18% of the unfiltered table. The final prokaryotic working filter also removes low-abundance SILVA Eukaryota and GTDB-unassigned-domain OTUs.

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

Do not compare ASV/OTU counts directly with MAG species counts. For 16S-MAG comparisons, aggregate both datasets to common GTDB ranks such as genus, family or order.
