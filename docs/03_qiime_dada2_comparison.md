# QIIME 2 DADA2 CCS comparison branch

This branch is preserved as a stringent comparison workflow. It is not the primary ecological table.

## Environment

Validated with QIIME 2 Amplicon 2026.1.

## Strategy

Runs 2860 and 3408 are imported and denoised separately so that each sequencing run learns its own DADA2 error model. Identical DADA2 parameters and hashed feature IDs permit sequence-identical features to be merged afterward.

## DADA2 CCS parameters

- front: `AGRGTTYGATYMTGGCTCAG`
- adapter: `RGYTACCTTGTTACGACTT`
- max mismatch: 2
- indels: false
- trunc len: 0
- trim left: 0
- max expected errors: 2
- trunc q: 2
- minimum length: 1000
- maximum length: 1800
- pooling: pseudo
- chimera method: consensus
- minimum parent abundance fold: 3.5
- reads for error learning: 1,000,000
- hashed feature IDs: true
- retain all samples: true

## Observed diagnostic pattern

Across both runs:

- primer removal: approximately 98%
- ordinary quality-filter retention: approximately 65–74%
- severe loss occurred during DADA2 denoising/inference
- subsequent chimera removal was small

The final DADA2-derived 99% table contained approximately 0.64 million reads, about 2.5% of the original raw-read total.

This diagnostic result motivated the direct 99% OTU branch.

The exact executable comparison pipeline is `scripts/03_qiime_dada2_comparison.sh`.
