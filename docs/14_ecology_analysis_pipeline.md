# 16S ecological analysis pipeline

This chapter starts after the final direct 99% OTU table and GTDB/SILVA taxonomies exist. It explains how to turn those outputs into reproducible ecological tables, alpha diversity, beta diversity, geochemical associations, and optional mcrA integration.

The goal is methodological transparency. For every step, the student should understand what the analysis asks, which input it uses, which filtering decisions it inherits, and which files it writes.

## 1. Where this stage begins

Required 16S inputs:

~~~text
otu-table-99.tsv
GTDB taxonomy.tsv
SILVA taxonomy.tsv
corrected metadata workbook
~~~

Optional cross-marker inputs:

~~~text
mcrA feature-table.tsv
mcrA lineage_relative_abundance_long.tsv
~~~

### otu-table-99.tsv

Rows are direct non-chimeric 99% full-length 16S OTUs and columns are sequencing libraries. This is the primary feature table.

### GTDB taxonomy.tsv

QIIME-exported GTDB R226 classifications for the same OTU IDs.

### SILVA taxonomy.tsv

QIIME-exported SILVA classifications for the same OTU IDs.

### Corrected metadata workbook

The workbook supplies sample identity, month, site, measured sediment depth, and available chemistry. Do not substitute an older workbook without documenting the change.

## 2. Configuration

Copy the template:

~~~bash
cp config/config.example.sh config/config.sh
source config/config.sh
~~~

The ecology layer uses variables such as:

~~~text
OTU_TABLE
GTDB_TAXONOMY
SILVA_TAXONOMY
METADATA_XLSX
ECOLOGY_OUT
RAREFACTION_DEPTH
SHANNON_ITERATIONS
PERMUTATIONS
RANDOM_SEED
~~~

Optional mcrA variables are described in docs/15_mcra_integration.md.

## 3. Run the complete ecology stage

From the repository root:

~~~bash
bash scripts/run_ecology_pipeline.sh config/config.sh
~~~

Recommended output layout:

~~~text
ecology/
├── prepared/
├── qc/
├── composition/
├── shannon/
├── ordination/
├── geochemistry/
└── mcra_integration/
~~~

Generated sample-level results remain outside GitHub by default.

---

# 4. Master taxonomy and bacterial-dominated working table

Script:

~~~text
scripts/06_build_master_annotation.py
~~~

## Purpose

Create one transparent annotation table and one approved working count table so that every downstream analysis uses the same taxonomic exclusions.

## Filtering

Exclude:

- chloroplast;
- mitochondria;
- SILVA Eukaryota;
- OTUs without a GTDB Bacteria/Archaea domain.

Do not manually delete rows from the feature table.

## Outputs

~~~text
master_taxonomy.tsv
otu-table-99-prokaryotes.tsv
master_qc_summary.tsv
~~~

The filename "prokaryotes" is historical shorthand; because of primer bias, interpret the working table as bacterial-dominated.

## Checkpoint

Current validated result:

~~~text
26,054 retained OTUs
12,209,120 retained reads
~~~

---

# 5. Metadata harmonization and validation

Scripts:

~~~text
scripts/07_harmonize_metadata.py
scripts/00_validate_metadata.py
~~~

## Purpose

Convert workbook labels into canonical sequencing IDs and stop the analysis if sample identity is ambiguous.

## Outputs

~~~text
metadata_harmonized.tsv
metadata_matched.tsv
metadata_unmatched.tsv
metadata_validation_summary.tsv
~~~

## Checkpoint

The current first-year EA framework matches 106 16S samples with depth/site metadata.

A metadata row that lacks a sequencing library is not automatically an error; it must be reported and understood.

---

# 6. Jan resequencing QC

Script:

~~~text
scripts/08_compare_jan_resequencing.py
~~~

## Purpose

Compare same-name run-2860 and run-3408 Jan libraries without assuming they can be merged.

The script uses relative abundance before Bray-Curtis comparison.

## Output

~~~text
jan_resequencing.tsv
~~~

Keep the -r3408 libraries separate unless a documented decision changes their treatment.

---

# 7. Taxonomic composition

Script:

~~~text
scripts/09_taxonomic_profiles.py
~~~

## Purpose

Aggregate OTU counts to a requested taxonomic rank and calculate sample-level relative abundance.

Recommended outputs:

~~~text
GTDB phylum
GTDB family
GTDB genus
~~~

## Why several ranks?

Phylum gives the broad community overview. Family often provides the best balance between ecological specificity and classification completeness. Genus is useful for focused interpretation but should not be treated as uniformly resolved across all OTUs.

## Rule

Calculate sample relative abundance first. When producing site/month summaries, average sample-level percentages rather than pooling all reads across samples.

---

# 8. Shannon alpha diversity

Script:

~~~text
scripts/10_alpha_diversity.py
~~~

## Purpose

Compare within-sample 99%-OTU diversity while controlling for unequal sequencing effort.

Default settings:

~~~text
rarefaction depth = 5,000
iterations        = 50
fixed random seed
~~~

For every eligible sample:

1. subsample exactly 5,000 reads without replacement;
2. calculate observed 99% OTU richness and Shannon diversity;
3. repeat 50 times;
4. report mean and standard deviation.

The script also retains raw library size and unrarefied metrics for QC.

## Important

Do not interpret richness without checking library-depth dependence. Shannon is less sensitive than raw richness but still benefits from standardized effort.

---

# 9. Bray-Curtis, PCoA, PERMANOVA, PERMDISP, and depth structure

Script:

~~~text
scripts/11_bray_pcoa.py
~~~

## Purpose

Describe and test whole-community compositional differences.

## Main outputs

~~~text
bray_curtis.tsv
pcoa_coordinates.tsv
pcoa_eigenvalues.tsv
community_structure_tests.tsv
~~~

## Statistical roles

### Bray-Curtis

Measures pairwise compositional dissimilarity.

### PCoA

Provides a low-dimensional visualization of the distance matrix.

### PERMANOVA

Tests whether group centroids differ in multivariate space.

### PERMDISP

Tests whether groups differ in multivariate dispersion.

Always interpret PERMANOVA together with PERMDISP.

### Depth Mantel tests

The current script compares Bray-Curtis dissimilarity with absolute depth difference and also performs site-specific depth tests.

Because site is a strong organizing factor, within-site depth tests are more informative than one pooled depth correlation.

## Permutations

Use a fixed seed and at least the documented 999 permutations for reproducible project analyses.

---

# 10. Site-stratified taxon-environment associations

Script:

~~~text
scripts/13_taxa_environment_associations.py
~~~

## Purpose

Identify recurrent bacterial families or genera whose abundance changes with depth or measured chemistry within a wetland.

Default variables include:

~~~text
Depth
Methane
SO4
H2S
Fe
DIC
~~~

## Taxon filtering

By default a taxon is tested within a site only if:

~~~text
prevalence >= 20%
mean relative abundance >= 0.1%
~~~

This avoids thousands of unstable tests on extremely rare taxa.

## Statistics

- Spearman rank correlation;
- minimum sample count;
- Benjamini-Hochberg FDR correction.

Family-level results are the preferred primary interpretation. Genus-level results are a more detailed second layer.

## Important limitation

A significant correlation is an ecological association, not evidence of a direct metabolic interaction.

---

# 11. mcrA integration

Scripts:

~~~text
scripts/12_mcra_16s_coupling.py
scripts/14_mcra_taxa_coupling.py
~~~

See docs/15_mcra_integration.md for the full rationale.

### Community-distance coupling

Tests whether samples that are different in the bacterial-dominated 16S community are also different in their mcrA community.

### Taxon-lineage coupling

Tests whether recurrent 16S families/genera covary with mcrA lineages after removing broad site, month, and linear depth effects.

Do not interpret cross-marker correlations as direct syntrophy.

---

# 12. Reproducibility checklist

Before using an output in a report, thesis, or manuscript, record:

~~~text
Git commit SHA
metadata workbook version/date
feature-table path
GTDB and SILVA taxonomy paths
filtering thresholds
rarefaction depth and iteration count
permutation count
random seed
script command
~~~

For an important run, create a small RUN.txt in the local output directory with the exact command and date.

## Do not

- manually edit result TSVs;
- manually relabel taxa in a final table;
- silently remove samples;
- merge Jan resequencing libraries by name;
- infer archaeal abundance from this 16S primer pair;
- mix P/EN samples into EA depth/geochemistry tests without matched metadata.

If a rule changes, change the code/configuration, rerun the analysis, and document the decision.
