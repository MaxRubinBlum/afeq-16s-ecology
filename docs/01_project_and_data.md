# Project and data

## Sequencing technology

The data are PacBio Kinnex full-length 16S rRNA gene libraries. Each library is represented by one FASTQ file rather than paired-end Illumina FASTQs.

## Sequencing runs

### Run 2860

- 62 FASTQ libraries
- Sep 2024 and Jan 2025 samples

### Run 3408

- 126 genuine run-3408 FASTQ libraries
- Jan, Feb, Mar, Apr and Jul 2025 samples

The directory containing run 3408 also contained six copied run-2860 Jan EA4 FASTQs. Byte-by-byte comparison showed that these six files were identical to the originals. They are excluded from run-3408 input by selecting only filenames beginning with `3408_`.

## Total dataset

- 188 sequencing libraries
- 25,395,564 raw reads

## Jan resequencing libraries

Eleven Jan 2025 sample identities occur again in run 3408. These are retained initially as separate libraries with IDs ending in `-r3408`.

They must not be merged merely because the sample names match. Technical reproducibility should be evaluated first.

## Primers

Biological full-length 16S primer sequences used in processing:

- forward: `AGRGTTYGATYMTGGCTCAG`
- reverse primer as supplied 5'→3': `RGYTACCTTGTTACGACTT`
- forward-oriented sequence expected at the 3' end: `AAGTCGTAACAAGGTARCY`

PacBio CCS reads occur in both orientations. The direct workflow uses Cutadapt `--revcomp` with a linked primer specification to orient and trim reads.
