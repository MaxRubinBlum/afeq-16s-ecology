# Input QC and manifests

## Manifest construction

Canonical sample IDs are generated from FASTQ filenames by `scripts/00_make_manifests.py`.

Expected manifest sizes:

- run 2860: 62 samples
- run 3408: 126 samples

The generated TSV uses Unix line endings. This matters because a carriage return at the end of an absolute FASTQ path is interpreted as part of the filename by shell tools.

## Duplicate checks

Within each sequencing-run manifest, sample IDs must be unique.

The six copied `2860_*.fastq.gz` files in the second raw-data directory are deliberately ignored. The run-3408 manifest uses only `3408_*.fastq.gz`.

## Raw length QC

Observed read-length distribution:

### Run 2860

- total: 6,328,023
- <1000 bp: 45,515 (0.719%)
- 1000–1600 bp: 6,228,496 (98.427%)
- 1600–1800 bp: 50,758 (0.802%)
- >1800 bp: 3,254 (0.051%)

### Run 3408

- total: 19,067,541
- <1000 bp: 199,051 (1.044%)
- 1000–1600 bp: 18,777,185 (98.477%)
- 1600–1800 bp: 83,762 (0.439%)
- >1800 bp: 7,543 (0.040%)

## Length decision

The working sequence range is 1000–1800 bp.

The 1800-bp maximum removes only the extreme long tail while retaining potentially valid full-length reads between 1600 and 1800 bp.

## PacBio FASTQ quality encoding

VSEARCH defaults to a maximum FASTQ quality score of 41. PacBio HiFi/CCS FASTQs can contain higher Phred values. The direct workflow therefore explicitly uses:

```bash
--fastq_qmax 93
```

Without this option VSEARCH can terminate with:

```text
Fatal error: FASTQ quality value (...) above qmax (41)
```
