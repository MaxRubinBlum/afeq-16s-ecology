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

: "${ECOLOGY_OUT:?Set ECOLOGY_OUT in config}"

RAREFACTION_DEPTH="${RAREFACTION_DEPTH:-5000}"
SHANNON_ITERATIONS="${SHANNON_ITERATIONS:-50}"
PERMUTATIONS="${PERMUTATIONS:-999}"
RANDOM_SEED="${RANDOM_SEED:-20260927}"

PREP="$ECOLOGY_OUT/prepared"
COMP="$ECOLOGY_OUT/composition"
DEPTH="$ECOLOGY_OUT/depth_profiles"
SHANNON="$ECOLOGY_OUT/shannon"
ORD="$ECOLOGY_OUT/ordination"
GEO="$ECOLOGY_OUT/geochemistry"
MCRA="$ECOLOGY_OUT/mcra_integration"

mkdir -p "$COMP" "$DEPTH" "$SHANNON" "$ORD" "$GEO" "$MCRA"

echo "=== Step 13. Prepare ecology tables and QC ==="
bash scripts/13_prepare_ecology_tables.sh "$CONFIG"

FILTERED_TABLE="$PREP/otu-table-99-prokaryotes.tsv"
MASTER="$PREP/master_taxonomy.tsv"
META="$PREP/metadata_matched.tsv"

echo "=== Step 14. GTDB taxonomic profiles ==="
for rank in phylum family genus
do
  python3 scripts/14_composition_profiles.py     --table "$FILTERED_TABLE"     --annotation "$MASTER"     --source GTDB     --rank "$rank"     --out "$COMP/GTDB_${rank}_relative_abundance_pct.tsv"
done

echo "=== Step 15. Depth-resolved phylum composition ==="
python3 scripts/15_depth_taxonomy_plot.py   --profile "$COMP/GTDB_phylum_relative_abundance_pct.tsv"   --metadata "$META"   --outdir "$DEPTH"   --top-n 10   --min-percent 0.25   --max-depth 40

echo "=== Step 16. Repeated-rarefaction alpha diversity ==="
python3 scripts/16_shannon_alpha.py   --table "$FILTERED_TABLE"   --out "$SHANNON/alpha_diversity.tsv"   --rarefaction-depth "$RAREFACTION_DEPTH"   --iterations "$SHANNON_ITERATIONS"   --seed "$RANDOM_SEED"

echo "=== Step 17. Bray-Curtis / PCoA / community tests ==="
python3 scripts/17_bray_pcoa_permanova.py   --table "$FILTERED_TABLE"   --metadata "$META"   --outdir "$ORD"   --transform relative   --permutations "$PERMUTATIONS"   --seed "$RANDOM_SEED"

echo "=== Step 18. Site-stratified environment associations ==="
for rank in family genus
do
  python3 scripts/18_geochemistry_associations.py     --table "$FILTERED_TABLE"     --annotation "$MASTER"     --metadata "$META"     --rank "$rank"     --outdir "$GEO"
done

if [[ -n "${MCRA_FEATURE_TABLE:-}" && -f "${MCRA_FEATURE_TABLE:-}" ]]; then
  echo "=== Step 19. 16S-mcrA community-distance coupling ==="
  python3 scripts/19_mcra_community_coupling.py     --sixteen-table "$FILTERED_TABLE"     --mcra-table "$MCRA_FEATURE_TABLE"     --metadata "$META"     --out "$MCRA/community_distance_coupling.tsv"     --permutations "$PERMUTATIONS"     --seed "$RANDOM_SEED"
else
  echo "Skipping step 19: MCRA_FEATURE_TABLE not configured."
fi

if [[ -n "${MCRA_LINEAGES:-}" && -f "${MCRA_LINEAGES:-}" ]]; then
  echo "=== Step 20. 16S taxon-mcrA lineage coupling ==="
  for rank in family genus
  do
    python3 scripts/20_mcra_taxa_coupling.py       --sixteen-table "$FILTERED_TABLE"       --annotation "$MASTER"       --mcra-lineages "$MCRA_LINEAGES"       --metadata "$META"       --rank "$rank"       --outdir "$MCRA"
  done
else
  echo "Skipping step 20: MCRA_LINEAGES not configured."
fi

echo "=== Ecology pipeline complete ==="
echo "Output: $ECOLOGY_OUT"
