#!/usr/bin/env bash
set -euo pipefail

ANALYSIS_DIR="${ANALYSIS_DIR:-16S_analysis}"
BASE="${DIRECT_DIR:-$ANALYSIS_DIR/otu99_direct}"
FILTERED="$BASE/filtered"
WORK="$BASE/work"
RESULTS="$BASE/results"
LOGS="$BASE/logs"
THREADS="${THREADS:-48}"

mkdir -p "$WORK" "$RESULTS" "$LOGS"

echo "======================================"
echo "1. Combine filtered reads"
echo "======================================"

cat "$FILTERED"/*.fasta > "$WORK/all-filtered.fasta"

FILTERED_READS=$(grep -c '^>' "$WORK/all-filtered.fasta")
echo "Filtered reads: $FILTERED_READS"

echo "======================================"
echo "2. Global exact dereplication"
echo "======================================"

vsearch   --derep_fulllength "$WORK/all-filtered.fasta"   --output "$WORK/uniques.fasta"   --sizeout   --minuniquesize 2   --relabel Uniq_   --fasta_width 0   2>&1 | tee "$LOGS/derep.log"

UNIQUES=$(grep -c '^>' "$WORK/uniques.fasta")
echo "Exact non-singleton sequences: $UNIQUES"

echo "======================================"
echo "3. Cluster at 99% identity"
echo "======================================"

vsearch   --cluster_size "$WORK/uniques.fasta"   --id 0.99   --strand plus   --sizein   --sizeout   --qmask none   --centroids "$WORK/otu99-raw.fasta"   --uc "$WORK/otu99-clusters.uc"   --relabel OTU_   --fasta_width 0   --threads "$THREADS"   2>&1 | tee "$LOGS/cluster99.log"

RAW_OTUS=$(grep -c '^>' "$WORK/otu99-raw.fasta")
echo "Raw 99% OTUs: $RAW_OTUS"

echo "======================================"
echo "4. Map all filtered reads to raw OTUs"
echo "======================================"

vsearch   --usearch_global "$WORK/all-filtered.fasta"   --db "$WORK/otu99-raw.fasta"   --id 0.99   --strand plus   --qmask none   --dbmask none   --threads "$THREADS"   --otutabout "$WORK/otu-table-prechim.tsv"   2>&1 | tee "$LOGS/map_prechim.log"

echo "======================================"
echo "5. Add total OTU abundances"
echo "======================================"

python3 - "$WORK/otu-table-prechim.tsv"           "$WORK/otu99-raw.fasta"           "$WORK/otu99-abundance.fasta" <<'PY'
import csv
import sys

table_file, fasta_in, fasta_out = sys.argv[1:]
sizes = {}

with open(table_file) as handle:
    reader = csv.reader(handle, delimiter="\t")
    next(reader)
    for row in reader:
        otu = row[0]
        sizes[otu] = sum(int(x) for x in row[1:] if x)

with open(fasta_in) as inp, open(fasta_out, "w") as out:
    for line in inp:
        if line.startswith(">"):
            otu = line[1:].split(";")[0].split()[0]
            if otu not in sizes:
                raise RuntimeError(f"No mapped abundance found for {otu}")
            out.write(f">{otu};size={sizes[otu]};\n")
        else:
            out.write(line)

print(f"Wrote abundance information for {len(sizes)} OTUs")
PY

echo "======================================"
echo "6. De novo chimera detection"
echo "======================================"

vsearch   --uchime_denovo "$WORK/otu99-abundance.fasta"   --sizein   --sizeout   --qmask none   --nonchimeras "$RESULTS/otu99-nonchimeric.fasta"   --chimeras "$RESULTS/otu99-chimeras.fasta"   --uchimeout "$RESULTS/uchime.tsv"   2>&1 | tee "$LOGS/uchime.log"

NONCHIMERIC=$(grep -c '^>' "$RESULTS/otu99-nonchimeric.fasta" || true)
CHIMERIC=$(grep -c '^>' "$RESULTS/otu99-chimeras.fasta" || true)

echo "Non-chimeric OTUs: $NONCHIMERIC"
echo "Chimeric OTUs: $CHIMERIC"

echo "======================================"
echo "7. Final mapping and OTU table"
echo "======================================"

vsearch   --usearch_global "$WORK/all-filtered.fasta"   --db "$RESULTS/otu99-nonchimeric.fasta"   --id 0.99   --strand plus   --qmask none   --dbmask none   --threads "$THREADS"   --otutabout "$RESULTS/otu-table-99.tsv"   2>&1 | tee "$LOGS/map_final.log"

MAPPED=$(awk 'NR>1{for(i=2;i<=NF;i++) s+=$i} END{print s+0}'   "$RESULTS/otu-table-99.tsv")

cat > "$RESULTS/pipeline_summary.tsv" <<EOF
metric\tvalue
filtered_reads\t$FILTERED_READS
exact_non_singleton_sequences\t$UNIQUES
raw_otu99\t$RAW_OTUS
nonchimeric_otu99\t$NONCHIMERIC
chimeric_otu99\t$CHIMERIC
final_mapped_reads\t$MAPPED
EOF

echo "======================================"
echo "DONE"
echo "======================================"
cat "$RESULTS/pipeline_summary.tsv"
