#!/usr/bin/env bash
set -euo pipefail

ANALYSIS_DIR="${ANALYSIS_DIR:-16S_analysis}"
QIIME_OUT="${QIIME_DIRECT_DIR:-$ANALYSIS_DIR/qiime/direct_otu99}"
SILVA_CLASSIFIER="${SILVA_CLASSIFIER:?Set SILVA_CLASSIFIER to the full-length SILVA classifier .qza}"
JOBS="${CLASSIFIER_JOBS:-12}"

mkdir -p "$QIIME_OUT/taxonomy_silva/export"

qiime feature-classifier classify-sklearn   --i-classifier "$SILVA_CLASSIFIER"   --i-reads "$QIIME_OUT/rep-seqs-99.qza"   --p-n-jobs "$JOBS"   --p-confidence 0.7   --p-read-orientation auto   --o-classification "$QIIME_OUT/taxonomy_silva/taxonomy.qza"

qiime metadata tabulate   --m-input-file "$QIIME_OUT/taxonomy_silva/taxonomy.qza"   --o-visualization "$QIIME_OUT/taxonomy_silva/taxonomy.qzv"

qiime tools export   --input-path "$QIIME_OUT/taxonomy_silva/taxonomy.qza"   --output-path "$QIIME_OUT/taxonomy_silva/export"
