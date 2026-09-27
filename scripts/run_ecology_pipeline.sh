#!/usr/bin/env bash
set -euo pipefail

CONFIG="${1:-config/config.sh}"

if [[ ! -f "$CONFIG" ]]; then
    echo "Configuration file not found: $CONFIG" >&2
    echo "Copy config/config.example.sh to config/config.sh and edit paths." >&2
    exit 1
fi

# shellcheck disable=SC1090
source "$CONFIG"

: "${OTU_TABLE:?Set OTU_TABLE in config}"
: "${GTDB_TAXONOMY:?Set GTDB_TAXONOMY in config}"
: "${SILVA_TAXONOMY:?Set SILVA_TAXONOMY in config}"
: "${METADATA_XLSX:?Set METADATA_XLSX in config}"
: "${ECOLOGY_OUT:?Set ECOLOGY_OUT in config}"

RAREFACTION_DEPTH="${RAREFACTION_DEPTH:-5000}"
SHANNON_ITERATIONS="${SHANNON_ITERATIONS:-50}"
PERMUTATIONS="${PERMUTATIONS:-999}"
RANDOM_SEED="${RANDOM_SEED:-20260927}"

PREP="$ECOLOGY_OUT/prepared"
QC="$ECOLOGY_OUT/qc"
COMP="$ECOLOGY_OUT/composition"
SHANNON="$ECOLOGY_OUT/shannon"
ORD="$ECOLOGY_OUT/ordination"
GEO="$ECOLOGY_OUT/geochemistry"
MCRA="$ECOLOGY_OUT/mcra_integration"

mkdir -p "$PREP" "$QC" "$COMP" "$SHANNON" "$ORD" "$GEO" "$MCRA"

echo "=== 1. Build master taxonomy and filtered working table ==="
python3 scripts/06_build_master_annotation.py   --table "$OTU_TABLE"   --gtdb "$GTDB_TAXONOMY"   --silva "$SILVA_TAXONOMY"   --outdir "$PREP"

FILTERED_TABLE="$PREP/otu-table-99-prokaryotes.tsv"
MASTER="$PREP/master_taxonomy.tsv"

echo "=== 2. Harmonize metadata ==="
python3 scripts/07_harmonize_metadata.py   --metadata "$METADATA_XLSX"   --table "$FILTERED_TABLE"   --outdir "$PREP"

META="$PREP/metadata_matched.tsv"

echo "=== 3. Validate metadata/sample identity ==="
python3 scripts/00_validate_metadata.py   --metadata "$META"   --table "$FILTERED_TABLE"   --out "$QC/metadata_validation_summary.tsv"

echo "=== 4. Jan resequencing QC ==="
python3 scripts/08_compare_jan_resequencing.py   --table "$FILTERED_TABLE"   --annotation "$MASTER"   --out "$QC/jan_resequencing.tsv"

echo "=== 5. GTDB taxonomic profiles ==="
for rank in phylum family genus
do
  python3 scripts/09_taxonomic_profiles.py     --table "$FILTERED_TABLE"     --annotation "$MASTER"     --source GTDB     --rank "$rank"     --out "$COMP/GTDB_${rank}_relative_abundance_pct.tsv"
done

echo "=== 6. Repeated-rarefaction alpha diversity ==="
python3 scripts/10_alpha_diversity.py   --table "$FILTERED_TABLE"   --out "$SHANNON/alpha_diversity.tsv"   --rarefaction-depth "$RAREFACTION_DEPTH"   --iterations "$SHANNON_ITERATIONS"   --seed "$RANDOM_SEED"

echo "=== 7. Bray-Curtis / PCoA / community tests ==="
python3 scripts/11_bray_pcoa.py   --table "$FILTERED_TABLE"   --metadata "$META"   --outdir "$ORD"   --transform relative   --permutations "$PERMUTATIONS"   --seed "$RANDOM_SEED"

echo "=== 8. Site-stratified environment associations ==="
for rank in family genus
do
  python3 scripts/13_taxa_environment_associations.py     --table "$FILTERED_TABLE"     --annotation "$MASTER"     --metadata "$META"     --rank "$rank"     --outdir "$GEO"
done

if [[ -n "${MCRA_FEATURE_TABLE:-}" && -f "${MCRA_FEATURE_TABLE:-}" ]]; then
  echo "=== 9. 16S-mcrA community-distance coupling ==="
  python3 scripts/12_mcra_16s_coupling.py     --sixteen-table "$FILTERED_TABLE"     --mcra-table "$MCRA_FEATURE_TABLE"     --metadata "$META"     --out "$MCRA/community_distance_coupling.tsv"     --permutations "$PERMUTATIONS"     --seed "$RANDOM_SEED"
else
  echo "Skipping mcrA community coupling: MCRA_FEATURE_TABLE not configured."
fi

if [[ -n "${MCRA_LINEAGES:-}" && -f "${MCRA_LINEAGES:-}" ]]; then
  echo "=== 10. 16S taxon-mcrA lineage coupling ==="
  for rank in family genus
  do
    python3 scripts/14_mcra_taxa_coupling.py       --sixteen-table "$FILTERED_TABLE"       --annotation "$MASTER"       --mcra-lineages "$MCRA_LINEAGES"       --metadata "$META"       --rank "$rank"       --outdir "$MCRA"
  done
else
  echo "Skipping taxon-mcrA coupling: MCRA_LINEAGES not configured."
fi

echo "=== Ecology pipeline complete ==="
echo "Output: $ECOLOGY_OUT"
