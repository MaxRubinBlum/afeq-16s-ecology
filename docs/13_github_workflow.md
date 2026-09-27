# GitHub workflow for this project

## Repository visibility

Keep the repository private during active unpublished analysis. A public release can be made later after data/publication decisions are explicit.

## What belongs in GitHub

Good to commit:

- scripts;
- documentation;
- configuration templates;
- small aggregate QC summaries;
- manuscript-independent plotting/statistics code;
- tests.

Do not commit by default:

- raw FASTQ files;
- full unpublished metadata workbooks;
- full sample-level OTU tables;
- GTDB/SILVA classifier artifacts or databases;
- QIIME artifacts/visualizations;
- large FASTA/intermediate files;
- generated ecological result tables or figures unless deliberately selected for release.

## Simple student workflow

~~~bash
git pull
git checkout -b depth-profiles

# edit scripts/docs
git status
git diff

python3 tests/validate_final_outputs.py --help

git add scripts docs results
git commit -m "Add depth-resolved 16S analysis"
git push -u origin depth-profiles
~~~

Then open a pull request. Even in a small lab project, pull requests create a useful record of why an analysis changed.

## Reproducible changes

If a filtering threshold changes, update:

1. the script/config value;
2. the QC documentation;
3. any result summary affected by the change.

Do not overwrite a result manually and leave the generating code unchanged.
