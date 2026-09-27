#!/usr/bin/env python3

import argparse
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.stats import spearmanr
from statsmodels.stats.multitest import multipletests


RANK_PREFIX = {
    "family": "f__",
    "genus": "g__",
}


def extract_rank(taxon, prefix):
    if pd.isna(taxon):
        return None
    for token in str(taxon).split(";"):
        token = token.strip()
        if token.startswith(prefix):
            value = token[len(prefix):].strip()
            return value if value else None
    return None


def rank_profile(table, taxonomy, samples, rank):
    prefix = RANK_PREFIX[rank]
    tax = taxonomy.set_index("OTU_ID")["GTDB_taxonomy"].map(
        lambda x: extract_rank(x, prefix)
    )

    counts = table.set_index("OTU_ID")[samples].copy()
    rel = counts.div(counts.sum(axis=0), axis=1) * 100.0
    rel["taxon"] = rel.index.map(tax)
    rel = rel.dropna(subset=["taxon"])
    return rel.groupby("taxon")[samples].sum()


def residualize(v, design):
    beta = np.linalg.lstsq(design, v, rcond=None)[0]
    return v - design @ beta


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--sixteen-table", required=True)
    p.add_argument("--annotation", required=True)
    p.add_argument("--mcra-lineages", required=True)
    p.add_argument("--metadata", required=True)
    p.add_argument("--outdir", required=True)
    p.add_argument("--sample-id-col", default="sequencing_sample_id")
    p.add_argument("--site-col", default="Wetland name")
    p.add_argument("--month-col", default="Month")
    p.add_argument("--depth-col", default="Depth")
    p.add_argument("--rank", choices=["family", "genus"], required=True)
    p.add_argument("--min-prevalence", type=float, default=0.20)
    p.add_argument("--min-mean-ra", type=float, default=0.10)
    args = p.parse_args()

    table = pd.read_csv(args.sixteen_table, sep="\t")
    table = table.rename(columns={table.columns[0]: "OTU_ID"})
    ann = pd.read_csv(args.annotation, sep="\t")
    meta = pd.read_csv(args.metadata, sep="\t")
    lineage_long = pd.read_csv(args.mcra_lineages, sep="\t")

    meta = meta.dropna(subset=[args.sample_id_col]).drop_duplicates(
        args.sample_id_col
    )
    meta = meta.set_index(args.sample_id_col)

    lineage = lineage_long.pivot(
        index="lineage",
        columns="sample_id",
        values="relative_abundance_pct",
    ).fillna(0.0)

    table_samples = set(table.columns[1:])
    shared = [
        s for s in meta.index
        if s in table_samples and s in lineage.columns
    ]

    if len(shared) < 10:
        raise ValueError("Too few shared 16S/mcrA samples")

    profile = rank_profile(table, ann, shared, args.rank)
    prevalence = (profile > 0).mean(axis=1)
    mean_ra = profile.mean(axis=1)
    taxa = profile.index[
        (prevalence >= args.min_prevalence)
        & (mean_ra >= args.min_mean_ra)
    ]

    # Remove broad site, month and linear depth effects before testing
    # cross-marker associations.
    m = meta.loc[shared].copy()
    site_d = pd.get_dummies(
        m[args.site_col], drop_first=True, dtype=float
    )
    month_d = pd.get_dummies(
        m[args.month_col], drop_first=True, dtype=float
    )
    depth = pd.to_numeric(m[args.depth_col], errors="coerce")
    depth = (depth - depth.mean()) / depth.std()

    design = np.column_stack(
        [
            np.ones(len(shared)),
            site_d.to_numpy(),
            month_d.to_numpy(),
            depth.to_numpy(),
        ]
    )

    rows = []

    for taxon in taxa:
        # Hellinger transform before residualization.
        x = np.sqrt(
            np.clip(profile.loc[taxon, shared].to_numpy(dtype=float) / 100.0, 0, None)
        )
        rx = residualize(x, design)

        for mcr_lineage in lineage.index:
            y = np.sqrt(
                np.clip(
                    lineage.loc[mcr_lineage, shared].to_numpy(dtype=float) / 100.0,
                    0,
                    None,
                )
            )
            ry = residualize(y, design)

            rho, pvalue = spearmanr(rx, ry)

            rows.append(
                {
                    "rank": args.rank,
                    "taxon": taxon,
                    "mcra_lineage": mcr_lineage,
                    "mean_16s_ra_pct": float(mean_ra.loc[taxon]),
                    "prevalence_16s": float(prevalence.loc[taxon]),
                    "rho_partial": float(rho),
                    "p": float(pvalue),
                }
            )

    out = pd.DataFrame(rows)
    out["q"] = multipletests(out["p"], method="fdr_bh")[1]
    out = out.sort_values(["q", "mcra_lineage", "taxon"])

    outdir = Path(args.outdir)
    outdir.mkdir(parents=True, exist_ok=True)
    outfile = outdir / f"{args.rank}_mcra_partial_associations.tsv"
    out.to_csv(outfile, sep="\t", index=False)

    print(f"Shared samples: {len(shared)}")
    print(f"Eligible {args.rank} taxa: {len(taxa)}")
    print(f"Tests: {len(out)}")
    print(f"FDR q<0.05: {(out['q'] < 0.05).sum()}")
    print(outfile)


if __name__ == "__main__":
    main()
