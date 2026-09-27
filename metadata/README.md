# Metadata

Do not commit sensitive or uncontrolled metadata workbooks here by default.

The first-year workbook used during development contains sample identifiers, month, measured depth, wetland/site, methane, and other porewater chemistry.

The repository stores only a small metadata template and the code required to harmonize/validate the real workbook.

## Harmonization

Use:

~~~bash
python3 scripts/09_harmonize_metadata.py   --metadata /path/to/metadata.xlsx   --table /path/to/otu-table-99-prokaryotes.tsv   --outdir /path/to/ecology/prepared
~~~

The harmonizer converts workbook sequencing labels to canonical IDs such as:

~~~text
Apr25-EA1-1
Jan25-EA2-3
Jul25-EA4-2
Sep24-EA3-5
~~~

## Validation

Then run:

~~~bash
python3 scripts/00_validate_metadata.py   --metadata /path/to/ecology/prepared/metadata_matched.tsv   --table /path/to/otu-table-99-prokaryotes.tsv
~~~

Check month/site consistency and duplicate IDs before any ecological statistics.

Run-3408 Jan resequencing libraries remain separate and are not automatically assigned the same role as their original run-2860 libraries.
