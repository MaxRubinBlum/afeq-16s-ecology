# Metadata

Do not commit sensitive or uncontrolled metadata workbooks here by default.

The first-year workbook used during development contained 107 metadata records and included fields such as sample identifier, month, depth, wetland/site, methane and porewater chemistry.

Use:

```bash
python3 scripts/07_harmonize_metadata.py \
  --metadata /path/to/metadata.xlsx \
  --table /path/to/otu-table-99-prokaryotes.tsv \
  --outdir analysis_ready
```

The harmonizer converts the workbook's sequencing labels to canonical sample IDs such as:

```text
Apr25-EA1-1
Jan25-EA2-3
Jul25-EA4-2
Sep24-EA3-5
```

Run-3408 Jan resequencing libraries remain separate and are not automatically assigned the same metadata row.
