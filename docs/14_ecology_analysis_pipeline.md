# 16S ecological analysis pipeline

This chapter starts **after** the final direct 99% OTU table and GTDB/SILVA classifications exist. It explains how to turn those outputs into reproducible ecological tables, figures, alpha diversity, beta diversity, geochemical associations, and optional mcrA integration.

The structure intentionally parallels the Afeq mcrA repository so that the two projects can be learned and maintained in the same way.

The goal is methodological transparency. For every analysis, understand:

1. what biological question it asks;
2. which input table it uses;
3. which filtering decisions it inherits;
4. what statistical method it applies;
5. what output files it writes;
6. what the result does **not** prove.

## 1. Where this stage begins

Required 16S inputs:

~~~text
otu-table-99.tsv
GTDB taxonomy.tsv
SILVA taxonomy.tsv
corrected metadata workbook (.xlsx)
~~~

Optional mcrA inputs:

~~~text
mcrA feature-table.tsv
mcrA lineage_relative_abundance_long.tsv
~~~

### otu-table-99.tsv

Rows are the 26,300 direct non-chimeric 99% full-length 16S OTUs and columns are sequencing libraries.

### GTDB taxonomy.tsv

QIIME-exported GTDB R226 classification for the same OTU IDs.

### SILVA taxonomy.tsv

QIIME-exported SILVA classification for the same OTU IDs.

### Corrected metadata workbook

The workbook provides validated sample identity, month, site, measured sediment depth, and available geochemistry.

Do not substitute an older workbook without documenting the change.

## 2. Configuration

Copy:

~~~bash
cp config/config.example.sh config/config.sh
~~~

Edit the local paths and then:

~~~bash
source config/config.sh
~~~

Important ecology variables include:

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

Optional mcrA variables:

~~~text
MCRA_FEATURE_TABLE
MCRA_LINEAGES
~~~

Leave the mcrA paths empty if the cross-marker stage is not being run.

## 3. Run the complete ecology stage

From the repository root:

~~~bash
bash scripts/run_ecology_pipeline.sh config/config.sh
~~~

The runner executes the ecology scripts in numerical order.

Recommended output layout:

~~~text
ecology/
├── prepared/
├── qc/
├── composition/
├── depth_profiles/
├── shannon/
├── ordination/
├── geochemistry/
└── mcra_integration/
~~~

Generated sample-level results remain outside GitHub by default.

---

# 4. Step 13 - prepare ecology tables

Script:

~~~text
scripts/13_prepare_ecology_tables.sh
~~~

## Purpose

Create one transparent, reproducible input layer for every later ecological analysis.

This stage runs the lower-level preparation scripts:

~~~text
scripts/08_build_master_annotation.py
scripts/09_harmonize_metadata.py
scripts/00_validate_metadata.py
scripts/10_compare_jan_resequencing.py
~~~

## Operations

The preparation stage:

1. checks that GTDB and SILVA IDs match the final OTU table;
2. builds a combined master taxonomy table;
3. removes chloroplast, mitochondrial, SILVA-Eukaryota, and GTDB-unassigned-domain OTUs;
4. writes the bacterial-dominated working count table;
5. harmonizes the corrected metadata workbook to canonical sequence IDs;
6. reports metadata rows that do not match a 16S library;
7. validates month/site consistency;
8. compares Jan run-2860 and run-3408 repeated libraries without merging them.

## Outputs

In prepared/:

~~~text
master_taxonomy.tsv
otu-table-99-prokaryotes.tsv
master_qc_summary.tsv
metadata_harmonized.tsv
metadata_matched.tsv
metadata_unmatched.tsv
~~~

In qc/:

~~~text
metadata_validation_summary.tsv
metadata_validation_summary_problems.tsv
jan_resequencing.tsv
~~~

## Current validated checkpoint

~~~text
working OTUs   26,054
working reads  12,209,120
~~~

The filename otu-table-99-prokaryotes.tsv is retained for continuity, but biologically the table should be described as **bacterial-dominated** because the 27F-like primer underrepresents Archaea.

## Checkpoint before continuing

Confirm:

- OTU IDs are unique;
- all retained OTUs have GTDB and SILVA evidence;
- metadata sample IDs are unique;
- month/site checks pass;
- unmatched metadata rows are understood;
- -r3408 libraries remain separate.

---

# 5. Step 14 - taxonomic composition profiles

Script:

~~~text
scripts/14_composition_profiles.py
~~~

## Purpose

Aggregate the 99% OTU table to a requested taxonomic rank and calculate sample-level relative abundance.

The runner creates:

~~~text
GTDB_phylum_relative_abundance_pct.tsv
GTDB_family_relative_abundance_pct.tsv
GTDB_genus_relative_abundance_pct.tsv
~~~

## Why several ranks?

### Phylum

Useful for a broad overview of major community shifts.

### Family

Usually the best balance between ecological specificity and classification completeness. Family-level results should generally be the primary taxonomic layer for association analyses.

### Genus

Useful for focused interpretation, but classification completeness is lower and not every lineage is equally well resolved.

## Compositional rule

The script converts each sample to relative abundance after taxonomic aggregation.

When summarizing a site or month later, average the **sample-level percentages**. Do not simply pool all reads from all samples, because deep libraries would then contribute more weight.

---

# 6. Step 15 - depth-resolved taxonomic composition

Script:

~~~text
scripts/15_depth_taxonomy_plot.py
~~~

## Purpose

Show bacterial taxonomic composition and measured sediment depth simultaneously while retaining individual samples.

The default runner uses the GTDB phylum profile.

Visual encoding:

~~~text
facet row      = EA site
facet column   = sampling month
x position     = taxon
y position     = measured sediment depth
bubble area    = relative abundance
~~~

Depth increases downward and panels share a common depth scale.

## Taxon selection

By default, the ten most abundant phyla across the matched samples are displayed.

Values below 0.25% are not drawn but remain in the exact data table.

## Outputs

~~~text
depth_taxonomy_bubble.png
depth_taxonomy_bubble.pdf
depth_taxonomy_plot_data.tsv
depth_taxonomy_taxa.tsv
~~~

The TSV is the provenance layer for the figure.

---

# 7. Step 16 - Shannon alpha diversity

Script:

~~~text
scripts/16_shannon_alpha.py
~~~

## Purpose

Compare within-sample 99% OTU diversity at standardized sequencing effort.

## Why standardize read depth?

Alpha-diversity estimates change with library size because deeper sequencing detects more low-abundance OTUs.

The project therefore uses repeated rarefaction.

Default settings:

~~~text
rarefaction depth = 5,000 reads
iterations        = 50
random seed       = 20260927
~~~

## Repeated rarefaction

For each eligible sample:

1. draw exactly 5,000 reads without replacement;
2. calculate observed 99% OTU richness;
3. calculate Shannon diversity;
4. repeat 50 times;
5. report mean and standard deviation.

Samples below the rarefaction threshold remain in the output with included_rarefaction=False.

## Output

~~~text
alpha_diversity.tsv
~~~

The table also retains raw library size and unrarefied alpha-diversity values for QC.

## Interpretation

Shannon is a within-sample community diversity metric. It is not a measure of methane-cycling diversity and should not be compared directly with broad mcrA lineage counts.

---

# 8. Step 17 - Bray-Curtis, PCoA, PERMANOVA and PERMDISP

Script:

~~~text
scripts/17_bray_pcoa_permanova.py
~~~

## Purpose

Quantify sample-to-sample differences in the full bacterial-dominated 99% OTU community.

## Bray-Curtis

The script converts sample counts to the selected transformation and calculates pairwise Bray-Curtis dissimilarity.

The standard runner currently uses relative abundance.

## PCoA

Principal Coordinates Analysis represents the Bray-Curtis distance matrix in a small number of axes for visualization.

Outputs:

~~~text
bray_curtis.tsv
pcoa_coordinates.tsv
pcoa_eigenvalues.tsv
~~~

## PERMANOVA

Tests whether groups differ in multivariate community composition.

The current script tests site and month as one-factor analyses.

## PERMDISP

Tests whether groups differ in multivariate dispersion.

A significant PERMANOVA result should always be interpreted together with PERMDISP because differences in within-group heterogeneity can contribute to the apparent group separation.

## Depth structure

The script also compares Bray-Curtis distance with absolute difference in sediment depth, both across all metadata-matched samples and within individual sites.

Because site is a strong organizing factor, the within-site depth analyses are more biologically informative than a single pooled gradient.

## Output

~~~text
community_structure_tests.tsv
~~~

Use a fixed random seed and the documented permutation count for reproducibility.

---

# 9. Step 18 - site-stratified taxon/geochemistry associations

Script:

~~~text
scripts/18_geochemistry_associations.py
~~~

## Purpose

Identify recurrent bacterial families or genera whose relative abundance changes with depth or measured porewater chemistry within a wetland.

Default metadata variables include:

~~~text
Depth
Methane
SO4
H2S
Fe
DIC
~~~

## Why analyze within sites?

Pooled correlations can be driven by differences among wetlands rather than by a true environmental response within one sediment system.

The standard analysis therefore calculates correlations separately for each site.

## Taxon filtering

A taxon is tested only if it meets both default thresholds within the site:

~~~text
prevalence >= 20%
mean relative abundance >= 0.1%
~~~

This avoids large numbers of unstable tests on extremely rare taxa.

## Statistics

For each eligible site x variable x taxon combination:

- Spearman rank correlation;
- minimum sample count;
- Benjamini-Hochberg FDR correction.

The runner performs both family- and genus-level analyses.

## Outputs

~~~text
family_environment_associations.tsv
genus_environment_associations.tsv
~~~

## Interpretation

These are ecological co-variation tests.

A significant association does **not** by itself demonstrate substrate use, syntrophy, electron transfer, or direct interaction.

Small-n chemistry subsets should be labelled as provisional even if they survive FDR correction.

---

# 10. Step 19 - 16S-mcrA community coupling

Script:

~~~text
scripts/19_mcra_community_coupling.py
~~~

## Purpose

Test whether sample-to-sample turnover of the bacterial-dominated 16S community parallels turnover of the targeted mcrA community.

## Shared sample rule

Only exact sample IDs present in:

- the filtered 16S table;
- validated metadata;
- the retained mcrA feature table

are used.

## Method

The script:

1. converts each marker table to relative abundance;
2. calculates Bray-Curtis distances independently;
3. correlates the upper triangles of the two distance matrices;
4. permutes sample labels for significance testing;
5. repeats the comparison within individual wetlands when sample size allows.

This is the primary cross-marker analysis because it does not require direct taxonomic equivalence between bacterial 16S taxa and archaeal mcrA lineages.

## Output

~~~text
community_distance_coupling.tsv
~~~

---

# 11. Step 20 - 16S taxon to mcrA lineage coupling

Script:

~~~text
scripts/20_mcra_taxa_coupling.py
~~~

## Purpose

Identify bacterial families or genera whose abundance covaries with specific mcrA lineages after broad environmental structure is removed.

## Method

The script:

1. aggregates 16S to GTDB family or genus;
2. retains recurrent/abundant 16S taxa;
3. Hellinger-transforms 16S and mcrA relative abundances;
4. removes site, month, and linear depth effects;
5. correlates residuals with Spearman correlation;
6. applies Benjamini-Hochberg FDR.

## Outputs

~~~text
family_mcra_partial_associations.tsv
genus_mcra_partial_associations.tsv
~~~

## Interpretation

These associations identify bacterial community modules that accompany methane-cycling lineages.

They do not demonstrate direct physical or metabolic partnerships.

See docs/15_mcra_integration.md.

---

# 12. Reproducibility checklist

Before using an output in a report, thesis, or manuscript, record:

~~~text
Git commit SHA
metadata workbook version/date
final OTU table path
GTDB taxonomy export
SILVA taxonomy export
taxonomic filtering rules
rarefaction depth and iteration count
permutation count
random seed
exact command
~~~

For an important run, create a local RUN.txt containing the date and exact command.

Example:

~~~text
2026-09-27

bash scripts/run_ecology_pipeline.sh config/config.sh
~~~

## Student rule

Do not edit result tables or figures manually.

If a threshold, sample-selection rule, transformation, or statistical design changes:

1. change the script/configuration;
2. rerun the analysis;
3. compare the outputs;
4. update the QC/decision documentation;
5. commit the scientific change with a descriptive message.

## What this pipeline does not currently do

The current workflow intentionally does not:

~~~text
infer metabolic rates from 16S abundance
treat 16S archaeal read fraction as true archaeal abundance
fit causal ecological models
claim direct interactions from correlations
merge Jan resequencing libraries automatically
incorporate MAG results
~~~

MAGs are still in progress and should be added later as a new documented analysis layer rather than folded invisibly into the existing workflow.
