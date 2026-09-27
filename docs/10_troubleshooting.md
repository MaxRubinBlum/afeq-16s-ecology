# Troubleshooting

## VSEARCH says FASTQ quality is above qmax 41

PacBio HiFi/CCS FASTQs can contain quality values above VSEARCH's default maximum.

Use:

~~~bash
--fastq_qmax 93
~~~

This is required in the filtering step.

## QIIME cannot find a FASTQ path from the manifest

Inspect the end of the manifest line:

~~~bash
cat -A 16S_analysis/manifests/manifest_run2860.tsv | head
~~~

A visible ^M indicates Windows CRLF line endings. Regenerate the manifest with the supplied Python script, which explicitly writes Unix line endings.

## The second raw-data directory contains 2860 files

Do not include them in the run-3408 manifest. Six copied Jan files were confirmed byte-identical to originals. The manifest generator selects only 3408-prefixed files.

## DADA2 removes most reads

Check the DADA2 statistics by stage.

In this dataset primer removal and ordinary quality filtering were successful; the collapse occurred during denoising/inference. This is why DADA2 is retained as a sensitivity branch rather than the main ecological table.

Do not loosen parameters blindly until you know which stage removes the reads.

## The final OTU FASTA header contains ;size=...

QIIME feature import requires a clean feature identifier. Remove the terminal abundance annotation:

~~~bash
sed -E 's/;size=[0-9]+$//' otu99-nonchimeric.fasta   > otu99-nonchimeric-clean.fasta
~~~

## classify-sklearn uses a lot of memory

Parallel workers multiply memory use. Twelve classifier jobs is a conservative default:

~~~bash
--p-n-jobs 12
~~~

Use free -h, htop, or ps to monitor memory.

## SILVA and GTDB disagree on a name

This is expected. Keep both classifications. GTDB is the primary ecological nomenclature; SILVA is an independent classification and organelle/non-target screen.

Do not manually replace one name with the other.

## Archaea are almost absent from 16S

Do not interpret that as ecological absence. The 27F-like forward primer is bacterial-biased and underrepresents Archaea. Use mcrA for the targeted methane-cycling archaeal signal.

## A sample is missing from metadata-based analysis

Check whether it is:

- a P/EN sample without the full EA metadata framework;
- a -r3408 Jan resequencing library;
- a true metadata mismatch;
- an intentionally absent library.

Never silently fabricate or infer missing metadata.
