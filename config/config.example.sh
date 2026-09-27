#!/usr/bin/env bash

# Copy this file to config/config.sh and edit local paths.
# config/config.sh is intentionally not required to be committed.

export PROJECT_ROOT="/media/bioinf/Data12/Maxim/16S/2026/2026_Keren_Julia"

export RUN2860_DIR="$PROJECT_ROOT/16S_Afeq_Sept_Jan"
export RUN3408_DIR="$PROJECT_ROOT/16S_Afeq_Apr_Jul"

export ANALYSIS_DIR="$PROJECT_ROOT/16S_analysis"

# Primary direct 99% OTU workflow
export DIRECT_DIR="$ANALYSIS_DIR/otu99_direct"

# QIIME 2 taxonomy resources
export GTDB_CLASSIFIER="$ANALYSIS_DIR/qiime/gtdb_r226/classifier/gtdb-r226-full-length-classifier.qza"

# Set this to the local full-length SILVA classifier used for the project.
export SILVA_CLASSIFIER="/path/to/silva-full-length-classifier.qza"

export THREADS=48
