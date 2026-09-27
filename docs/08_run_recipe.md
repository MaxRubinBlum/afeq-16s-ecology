# Run recipe

This is the short operational recipe for reproducing the current primary dataset.

## 1. Generate manifests

```bash
python3 scripts/00_make_manifests.py
```

Check expected sizes:

- 62 run-2860 samples
- 126 run-3408 samples

## 2. Direct trimming and filtering

```bash
bash scripts/01_trim_filter.sh
```

Expected checkpoint:

```text
20,117,175 filtered reads
```

## 3. Direct 99% OTUs

```bash
bash scripts/02_build_otu99.sh
```

Expected validated output:

```text
26,300 non-chimeric OTUs
12,355,927 reads in final OTU table
```

## 4. GTDB

If a GTDB R226 classifier does not already exist:

```bash
bash scripts/04_train_gtdb_classifier.sh
```

Classify:

```bash
bash scripts/05_classify_gtdb.sh
```

## 5. SILVA

Point `SILVA_CLASSIFIER` to the compatible full-length SILVA Naive Bayes classifier, then:

```bash
bash scripts/05b_classify_silva.sh
```

## 6. Build analysis-ready taxonomy/table

```bash
python3 scripts/06_build_master_annotation.py \
  --table /path/to/otu-table-99.tsv \
  --gtdb /path/to/gtdb/taxonomy.tsv \
  --silva /path/to/silva/taxonomy.tsv \
  --outdir analysis_ready
```

## 7. QC and ecology

Run the downstream scripts in numerical order.

## Optional DADA2 comparison branch

```bash
bash scripts/03_qiime_dada2_comparison.sh
```

This branch is retained for sensitivity analysis and provenance, not as the primary ecological count table.
