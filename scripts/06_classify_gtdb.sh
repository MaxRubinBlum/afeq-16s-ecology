#!/usr/bin/env bash
set -euo pipefail

ANALYSIS_DIR="${ANALYSIS_DIR:-16S_analysis}"
DIRECT_DIR="${DIRECT_DIR:-$ANALYSIS_DIR/otu99_direct}"
QIIME_OUT="${QIIME_DIRECT_DIR:-$ANALYSIS_DIR/qiime/direct_otu99}"
GTDB_CLASSIFIER="${GTDB_CLASSIFIER:-$ANALYSIS_DIR/qiime/gtdb_r226/classifier/gtdb-r226-full-length-classifier.qza}"
JOBS="${CLASSIFIER_JOBS:-12}"

mkdir -p "$QIIME_OUT/taxonomy_gtdb226/export"

# Remove VSEARCH abundance annotations so feature IDs are exactly OTU_#.
sed -E 's/;size=[0-9]+$//'   "$DIRECT_DIR/results/otu99-nonchimeric.fasta"   > "$DIRECT_DIR/results/otu99-nonchimeric-clean.fasta"

qiime tools import   --type 'FeatureData[Sequence]'   --input-path "$DIRECT_DIR/results/otu99-nonchimeric-clean.fasta"   --output-path "$QIIME_OUT/rep-seqs-99.qza"

qiime feature-classifier classify-sklearn   --i-classifier "$GTDB_CLASSIFIER"   --i-reads "$QIIME_OUT/rep-seqs-99.qza"   --p-n-jobs "$JOBS"   --p-confidence 0.7   --p-read-orientation auto   --o-classification "$QIIME_OUT/taxonomy_gtdb226/taxonomy.qza"

qiime metadata tabulate   --m-input-file "$QIIME_OUT/taxonomy_gtdb226/taxonomy.qza"   --o-visualization "$QIIME_OUT/taxonomy_gtdb226/taxonomy.qzv"

qiime tools export   --input-path "$QIIME_OUT/taxonomy_gtdb226/taxonomy.qza"   --output-path "$QIIME_OUT/taxonomy_gtdb226/export"
