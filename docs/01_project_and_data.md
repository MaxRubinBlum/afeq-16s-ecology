# Project and data structure

## Biological project

The Afeq sediment project follows microbial-community structure across wetlands, seasons, and sediment depth, with methane and other porewater geochemistry available for a validated subset.

The current 16S analysis is intended to describe the bacterial-dominated community and later integrate it with the targeted mcrA methane-cycling community.

## Sequencing technology

The 16S libraries are PacBio Kinnex/CCS full-length amplicons. Each library is represented by one FASTQ file, not paired-end Illumina FASTQs.

## Sequencing runs

### Run 2860

- 62 libraries;
- Sep 2024 and Jan 2025.

### Run 3408

- 126 genuine run-3408 libraries;
- Jan, Feb, Mar, Apr and Jul 2025.

Six copied run-2860 FASTQs were present in the second raw-data directory and were confirmed byte-identical to originals. They are not separate biological observations.

## Total raw dataset

~~~text
libraries   188
raw reads   25,395,564
~~~

## Jan resequencing libraries

Eleven Jan sample identities occur again in run 3408.

These libraries receive the suffix:

~~~text
-r3408
~~~

They remain separate until their technical/biological provenance and statistical treatment are explicitly resolved.

## Primer pair

~~~text
forward  AGRGTTYGATYMTGGCTCAG
reverse  RGYTACCTTGTTACGACTT
~~~

For forward-oriented linked-adapter trimming, the reverse-terminal sequence is:

~~~text
AAGTCGTAACAAGGTARCY
~~~

## Expected read length

The vast majority of raw reads are approximately full-length bacterial 16S.

The working post-primer size range is:

~~~text
1000-1800 bp
~~~

## Analysis layers

The project keeps distinct layers:

1. raw FASTQs;
2. primer-trimmed/quality-filtered reads;
3. direct 99% OTU table;
4. DADA2 sensitivity branch;
5. GTDB + SILVA taxonomy;
6. filtered bacterial-dominated working table;
7. metadata-matched ecology;
8. 16S-mcrA integration.

Do not collapse these layers into one folder or overwrite earlier outputs.
