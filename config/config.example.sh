#!/usr/bin/env bash

# Copy to config/config.sh and edit local paths.
# Do not commit config/config.sh.

export PROJECT_ROOT="/media/bioinf/Data12/Maxim/16S/2026/2026_Keren_Julia"

export RUN2860_DIR="$PROJECT_ROOT/16S_Afeq_Sept_Jan"
export RUN3408_DIR="$PROJECT_ROOT/16S_Afeq_Apr_Jul"

export ANALYSIS_DIR="$PROJECT_ROOT/16S_analysis"

# Primary direct 99% OTU workflow
export DIRECT_DIR="$ANALYSIS_DIR/otu99_direct"

# QIIME outputs
export QIIME_DIRECT_DIR="$ANALYSIS_DIR/qiime/direct_otu99"

# Final feature table
export OTU_TABLE="$DIRECT_DIR/results/otu-table-99.tsv"

# Taxonomy exports
export GTDB_CLASSIFIER="$ANALYSIS_DIR/qiime/gtdb_r226/classifier/gtdb-r226-full-length-classifier.qza"
export GTDB_TAXONOMY="$QIIME_DIRECT_DIR/taxonomy_gtdb226/export/taxonomy.tsv"

# Set to the local full-length SILVA classifier used for the project.
export SILVA_CLASSIFIER="/path/to/silva-full-length-classifier.qza"
export SILVA_TAXONOMY="$QIIME_DIRECT_DIR/taxonomy_silva/export/taxonomy.tsv"

# Corrected metadata workbook
export METADATA_XLSX="$PROJECT_ROOT/Metadata_1st_year (16S).xlsx"

# Post-taxonomy ecology output
export ECOLOGY_OUT="$ANALYSIS_DIR/ecology"

# Optional mcrA integration inputs.
# Leave empty to skip the cross-marker stage in run_ecology_pipeline.sh.
export MCRA_FEATURE_TABLE=""
export MCRA_LINEAGES=""

# Compute / classifier settings
export THREADS=48
export DADA2_THREADS=24
export CLASSIFIER_JOBS=12

# Ecology settings
export RAREFACTION_DEPTH=5000
export SHANNON_ITERATIONS=50
export PERMUTATIONS=999
export RANDOM_SEED=20260927
