# Copy-paste run recipe

This is the short operational version of the workflow. Read the preceding documentation before using it as a blind command list.

## 1. Configure paths

~~~bash
cp config/config.example.sh config/config.sh
nano config/config.sh
source config/config.sh
~~~

## 2. Activate the QIIME environment

~~~bash
conda activate qiime2-amplicon-2026.1
~~~

## 3. Generate manifests

~~~bash
python3 scripts/01_make_manifests.py   --run2860-dir "$RUN2860_DIR"   --run3408-dir "$RUN3408_DIR"   --outdir "$ANALYSIS_DIR/manifests"
~~~

Expected:

~~~text
run 2860 = 62 samples
run 3408 = 126 samples
~~~

## 4. Primary direct processing

~~~bash
bash scripts/02_trim_filter.sh
bash scripts/03_build_otu99.sh
~~~

Expected checkpoints:

~~~text
filtered reads = 20,117,175
final OTUs     = 26,300
mapped reads   = 12,355,927
~~~

## 5. Optional DADA2 sensitivity branch

~~~bash
bash scripts/04_qiime_dada2_comparison.sh
~~~

Do not substitute this table for the direct OTU table without revisiting the read-retention decision.

## 6. GTDB classifier

Train once if needed:

~~~bash
bash scripts/05_train_gtdb_classifier.sh
~~~

Classify:

~~~bash
bash scripts/06_classify_gtdb.sh
~~~

## 7. SILVA classifier

Set SILVA_CLASSIFIER in config/config.sh, then:

~~~bash
bash scripts/07_classify_silva.sh
~~~

## 8. Validate final IDs

~~~bash
python3 tests/validate_final_outputs.py   --table "$OTU_TABLE"   --gtdb "$GTDB_TAXONOMY"   --silva "$SILVA_TAXONOMY"
~~~

## 9. Run the ecology layer

Switch to the ecology environment if desired:

~~~bash
conda activate afeq16s-ecology
source config/config.sh
bash scripts/run_ecology_pipeline.sh config/config.sh
~~~

The runner creates the filtered taxonomy/table, harmonized metadata, QC, composition profiles, alpha diversity, beta diversity, and environment-association outputs.

If mcrA paths are configured, it also runs the cross-marker analyses.

## 10. Record provenance

For every analysis used in a report/manuscript, record:

~~~text
Git commit SHA
metadata workbook version/date
input OTU-table path
taxonomy export paths
random seed
rarefaction depth
permutation count
exact command
~~~

Do not edit generated result TSVs or figures manually.
