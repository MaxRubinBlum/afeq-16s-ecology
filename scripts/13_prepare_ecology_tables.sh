#!/usr/bin/env bash
set -euo pipefail

CONFIG="${1:-config/config.sh}"

if [[ ! -f "$CONFIG" ]]; then
    echo "Configuration file not found: $CONFIG" >&2
    exit 1
fi

# shellcheck disable=SC1090
source "$CONFIG"

: "${OTU_TABLE:?Set OTU_TABLE in config}"
: "${GTDB_TAXONOMY:?Set GTDB_TAXONOMY in config}"
: "${SILVA_TAXONOMY:?Set SILVA_TAXONOMY in config}"
: "${METADATA_XLSX:?Set METADATA_XLSX in config}"
: "${ECOLOGY_OUT:?Set ECOLOGY_OUT in config}"

PREP="$ECOLOGY_OUT/prepared"
QC="$ECOLOGY_OUT/qc"
mkdir -p "$PREP" "$QC"

echo "=== Build master taxonomy and filtered table ==="
python3 scripts/08_build_master_annotation.py   --table "$OTU_TABLE"   --gtdb "$GTDB_TAXONOMY"   --silva "$SILVA_TAXONOMY"   --outdir "$PREP"

FILTERED_TABLE="$PREP/otu-table-99-prokaryotes.tsv"
MASTER="$PREP/master_taxonomy.tsv"

echo "=== Summarize taxonomy QC ==="
python3 scripts/11_taxonomy_qc.py   --annotation "$MASTER"   --out "$QC/taxonomy_qc.tsv"

echo "=== Harmonize metadata ==="
python3 scripts/09_harmonize_metadata.py   --metadata "$METADATA_XLSX"   --table "$FILTERED_TABLE"   --outdir "$PREP"

META="$PREP/metadata_matched.tsv"

echo "=== Validate metadata ==="
python3 scripts/00_validate_metadata.py   --metadata "$META"   --table "$FILTERED_TABLE"   --out "$QC/metadata_validation_summary.tsv"

echo "=== Jan resequencing QC ==="
python3 scripts/10_compare_jan_resequencing.py   --table "$FILTERED_TABLE"   --annotation "$MASTER"   --out "$QC/jan_resequencing.tsv"

echo "Prepared ecology inputs:"
echo "  $FILTERED_TABLE"
echo "  $MASTER"
echo "  $META"
