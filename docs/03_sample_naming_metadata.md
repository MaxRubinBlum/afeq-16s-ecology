# Sample naming and metadata validation

## Why sample naming matters

Most downstream failures in amplicon projects are not sophisticated bioinformatics failures; they are sample-identity failures. A correct OTU table linked to the wrong metadata is worse than no analysis.

## Canonical 16S IDs

Canonical IDs encode sampling period, site, and sample/depth identifier.

Examples:

~~~text
Sep24-EA1-7
Jan25-EA4-2
Apr25-EA1-3
Jul25-EA2-10
~~~

Run-3408 Jan libraries that repeat an existing Jan biological name are intentionally preserved as:

~~~text
Jan25-EA1-1-r3408
Jan25-EA2-2-r3408
~~~

Do not silently merge these libraries.

## Two sequencing runs

The dataset contains:

- run 2860: 62 libraries;
- run 3408: 126 genuine libraries.

The second raw-data directory also contained six copied 2860 FASTQ files. They were byte-identical to the original files and are excluded by selecting only genuine 3408-prefixed files for the second manifest.

## Metadata rules

For ecological analyses:

- the canonical sequence ID is the join key;
- month/site encoded in the sequence ID must agree with metadata;
- depth is a measured numeric variable, not inferred from the sample number;
- only samples with validated metadata enter depth/geochemistry tests;
- P/EN samples can remain useful compositionally even when the EA depth/geochemistry framework is incomplete;
- -r3408 Jan libraries remain separate until their provenance and appropriate treatment are resolved.

## Validation checklist

Before ecological analysis, confirm:

- no duplicate canonical sample IDs;
- no duplicate metadata join IDs;
- sequence month agrees with metadata month;
- EA/P/EN site code agrees;
- all sample IDs used in statistics are explicitly present in the metadata table;
- unmatched samples are reported rather than silently discarded.

Use scripts/00_validate_metadata.py for structural checks.
