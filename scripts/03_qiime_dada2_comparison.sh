#!/usr/bin/env bash
set -euo pipefail

ANALYSIS_DIR="${ANALYSIS_DIR:-16S_analysis}"
MAN="$ANALYSIS_DIR/manifests"
Q="$ANALYSIS_DIR/qiime"
LOG="$ANALYSIS_DIR/logs"
THREADS="${DADA2_THREADS:-24}"

mkdir -p "$Q"/{run2860,run3408,merged} "$LOG"

for RUN in 2860 3408
do
    qiime tools import       --type 'SampleData[SequencesWithQuality]'       --input-path "$MAN/manifest_run${RUN}.tsv"       --output-path "$Q/run${RUN}/demux.qza"       --input-format SingleEndFastqManifestPhred33V2

    qiime demux summarize       --i-data "$Q/run${RUN}/demux.qza"       --o-visualization "$Q/run${RUN}/demux.qzv"

    qiime dada2 denoise-ccs       --i-demultiplexed-seqs "$Q/run${RUN}/demux.qza"       --p-front 'AGRGTTYGATYMTGGCTCAG'       --p-adapter 'RGYTACCTTGTTACGACTT'       --p-max-mismatch 2       --p-no-indels       --p-trunc-len 0       --p-trim-left 0       --p-max-ee 2       --p-trunc-q 2       --p-min-len 1000       --p-max-len 1800       --p-pooling-method pseudo       --p-chimera-method consensus       --p-min-fold-parent-over-abundance 3.5       --p-n-reads-learn 1000000       --p-hashed-feature-ids       --p-retain-all-samples       --p-n-threads "$THREADS"       --o-table "$Q/run${RUN}/table.qza"       --o-representative-sequences "$Q/run${RUN}/rep-seqs.qza"       --o-denoising-stats "$Q/run${RUN}/denoising-stats.qza"       --o-base-transition-stats "$Q/run${RUN}/base-transition-stats.qza"       --verbose       2>&1 | tee "$LOG/dada2_run${RUN}.log"

    qiime metadata tabulate       --m-input-file "$Q/run${RUN}/denoising-stats.qza"       --o-visualization "$Q/run${RUN}/denoising-stats.qzv"
done

qiime feature-table merge   --i-tables "$Q/run2860/table.qza" "$Q/run3408/table.qza"   --o-merged-table "$Q/merged/table.qza"

qiime feature-table merge-seqs   --i-data "$Q/run2860/rep-seqs.qza" "$Q/run3408/rep-seqs.qza"   --o-merged-data "$Q/merged/rep-seqs.qza"
