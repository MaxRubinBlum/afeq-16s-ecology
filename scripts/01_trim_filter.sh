#!/usr/bin/env bash
set -euo pipefail

ANALYSIS_DIR="${ANALYSIS_DIR:-16S_analysis}"
MANIFEST_DIR="${MANIFEST_DIR:-$ANALYSIS_DIR/manifests}"
OUT="${DIRECT_DIR:-$ANALYSIS_DIR/otu99_direct}"
THREADS="${THREADS:-24}"

mkdir -p "$OUT"/{trimmed,filtered,work,results,logs}

for MANIFEST in     "$MANIFEST_DIR/manifest_run2860.tsv"     "$MANIFEST_DIR/manifest_run3408.tsv"
do
    tail -n +2 "$MANIFEST" |
    while IFS=$'\t' read -r SAMPLE FASTQ
    do
        # Defensive removal of a carriage return if an externally edited
        # manifest has Windows CRLF line endings.
        FASTQ="${FASTQ%$'\r'}"

        echo "=== $SAMPLE ==="

        cutadapt           -g 'AGRGTTYGATYMTGGCTCAG...AAGTCGTAACAAGGTARCY'           "$FASTQ"           -o "$OUT/trimmed/${SAMPLE}.fastq.gz"           --trimmed-only           --revcomp           -e 0.1           -j "$THREADS"           > "$OUT/logs/${SAMPLE}.cutadapt.log"

        # VSEARCH fastq_filter is single-threaded. PacBio CCS quality scores
        # can exceed the VSEARCH default qmax=41, so qmax=93 is explicit.
        vsearch           --fastq_filter "$OUT/trimmed/${SAMPLE}.fastq.gz"           --fastq_qmax 93           --fastq_maxee 2           --fastq_minlen 1000           --fastq_maxlen 1800           --fastaout "$OUT/filtered/${SAMPLE}.fasta"           --relabel "${SAMPLE}_"           --sample "$SAMPLE"
    done
done

{
    printf "sample_id\tfiltered_reads\n"
    for f in "$OUT"/filtered/*.fasta
    do
        n=$(grep -c '^>' "$f")
        s=$(basename "$f" .fasta)
        printf "%s\t%s\n" "$s" "$n"
    done | sort
} > "$OUT/results/filtered_read_counts.tsv"

awk 'NR>1{s+=$2} END{print "Total filtered reads:",s}'   "$OUT/results/filtered_read_counts.tsv"
