# Analysis decisions and QC log

This file records methodological decisions that materially affect the final dataset.

## 1. Single-end PacBio CCS treatment

The Kinnex libraries are single-FASTQ full-length 16S libraries. They are not processed as paired-end Illumina data.

## 2. Run separation in DADA2

Runs 2860 and 3408 were denoised separately because DADA2 error models are sequencing-run specific.

## 3. Duplicate raw files

Six run-2860 Jan EA4 FASTQs copied into the run-3408 directory were shown by `cmp` to be byte-identical to their originals. They were excluded from the second-run manifest.

## 4. Jan run-3408 sample IDs

Eleven Jan libraries in run 3408 are retained with suffix `-r3408`.

A preliminary comparison showed that these should not automatically be merged with their same-name run-2860 libraries. They remain separate until their biological/technical provenance is resolved.

## 5. Length limits

Use 1000–1800 bp.

Only approximately 0.04–0.05% of raw reads exceeded 1800 bp. The 1600–1800 bp interval was retained to avoid unnecessarily deleting potentially valid long full-length 16S amplicons.

## 6. PacBio FASTQ qmax

VSEARCH must use `--fastq_qmax 93` because PacBio CCS FASTQs can contain Phred values above the VSEARCH default qmax of 41.

## 7. DADA2 is not the primary ecological table

DADA2 successfully removed primers from approximately 98% of reads and ordinary quality filtering retained approximately 65–74%. The severe reduction occurred during DADA2 denoising.

This produced a final DADA2-derived 99% table with only approximately 0.64 million reads.

The direct workflow retained 20,117,175 reads after primer/quality filtering and 12,355,927 reads in the final non-chimeric 99% OTU table.

Therefore:

- direct 99% OTU table = primary ecological dataset
- DADA2-derived 99% table = stringent comparison / sensitivity dataset

## 8. Feature resolution

The project uses 99% full-length 16S OTUs as the main ecological units.

DADA2 ASVs are retained for provenance and sensitivity analysis, but raw ASV richness is not treated as equivalent to organismal or species richness.

## 9. Taxonomy

- GTDB R226 = primary taxonomy
- SILVA = secondary taxonomy and organelle flagging
- chloroplast and mitochondrial OTUs are removed before prokaryotic ecology

## 10. Validated primary-dataset checkpoints

- 188 libraries
- 25,395,564 raw reads
- 20,117,175 primer/quality/length-filtered reads
- 26,300 non-chimeric direct 99% OTUs
- 12,355,927 reads in final direct OTU table
- 26,300/26,300 OTU IDs matched GTDB taxonomy
- 26,300/26,300 OTU IDs matched SILVA taxonomy
