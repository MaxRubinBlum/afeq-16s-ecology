# Results directory

This repository does not store large generated biological result files.

Large outputs remain on the analysis workstation, including:

- raw and trimmed FASTQs;
- pooled and dereplicated FASTA files;
- final OTU FASTA;
- full sample-level OTU count tables;
- QIIME 2 QZA/QZV artifacts;
- GTDB/SILVA classifier artifacts;
- generated ecology tables and manuscript figures.

Small non-interpretive QC summaries may be committed when they are useful for reproducibility and do not expose unpublished sample-level information.

The current committed example is:

~~~text
qc_summary.tsv
~~~

Biological interpretation belongs in reports/manuscripts. The repository should contain the code and methodological reasoning needed to reproduce those results.
