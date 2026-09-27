#!/usr/bin/env bash
set -euo pipefail

ANALYSIS_DIR="${ANALYSIS_DIR:-16S_analysis}"
OUT="${GTDB_DIR:-$ANALYSIS_DIR/qiime/gtdb_r226}"

mkdir -p "$OUT/classifier"

qiime rescript get-gtdb-data   --p-version 226.0   --p-domain Both   --p-db-type SpeciesReps   --o-gtdb-taxonomy "$OUT/gtdb-r226-taxonomy.qza"   --o-gtdb-sequences "$OUT/gtdb-r226-sequences.qza"   --verbose

qiime feature-classifier fit-classifier-naive-bayes   --i-reference-reads "$OUT/gtdb-r226-sequences.qza"   --i-reference-taxonomy "$OUT/gtdb-r226-taxonomy.qza"   --o-classifier "$OUT/classifier/gtdb-r226-full-length-classifier.qza"

qiime tools peek "$OUT/classifier/gtdb-r226-full-length-classifier.qza"
