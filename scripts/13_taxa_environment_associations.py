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


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--table", required=True)
    p.add_argument("--annotation", required=True)
    p.add_argument("--metadata", required=True)
    p.add_argument("--outdir", required=True)
    p.add_argument("--sample-id-col", default="sequencing_sample_id")
    p.add_argument("--site-col", default="Wetland name")
    p.add_argument("--rank", choices=["family", "genus"], required=True)
    p.add_argument(
        "--variables",
        default="Depth,Methane ,SO4 (mM),H2S (µM),Fe (µM),DIC (mM)",
    )
    p.add_argument("--min-prevalence", type=float, default=0.20)
    p.add_argument("--min-mean-ra", type=float, default=0.10)
    p.add_argument("--min-n", type=int, default=8)
    args = p.parse_args()

    table = pd.read_csv(args.table, sep="\t")
    table = table.rename(columns={table.columns[0]: "OTU_ID"})
    ann = pd.read_csv(args.annotation, sep="\t")
    meta = pd.read_csv(args.metadata, sep="\t")
    meta = meta.dropna(subset=[args.sample_id_col]).drop_duplicates(
        args.sample_id_col
    )
    meta = meta.set_index(args.sample_id_col)

    sample_cols = [
        x for x in table.columns[1:] if x in meta.index
    ]
    if not sample_cols:
        raise ValueError("No table samples match metadata")

    variables = [x for x in args.variables.split(",") if x]
    for var in variables:
        meta[var] = pd.to_numeric(meta[var], errors="coerce")

    profile = rank_profile(
        table,
        ann,
        sample_cols,
        args.rank,
    )

    rows = []

    for site, meta_site in meta.loc[sample_cols].groupby(args.site_col):
        site_samples = [
            s for s in profile.columns if s in meta_site.index
        ]

        for variable in variables:
            valid = meta_site.loc[site_samples, variable].notna()
            samples = list(meta_site.loc[site_samples].index[valid])

            if len(samples) < args.min_n:
                continue

            x = meta_site.loc[samples, variable].astype(float).to_numpy()
            sub = profile[samples]

            prevalence = (sub > 0).mean(axis=1)
            mean_ra = sub.mean(axis=1)

            taxa = sub.index[
                (prevalence >= args.min_prevalence)
                & (mean_ra >= args.min_mean_ra)
            ]

            for taxon in taxa:
                y = sub.loc[taxon, samples].to_numpy(dtype=float)
                if np.std(y) == 0 or np.std(x) == 0:
                    continue

                rho, pvalue = spearmanr(y, x)

                rows.append(
                    {
                        "rank": args.rank,
                        "site": site,
                        "variable": variable,
                        "taxon": taxon,
                        "n": len(samples),
                        "mean_ra_pct_site": float(mean_ra.loc[taxon]),
                        "prevalence_site": float(prevalence.loc[taxon]),
                        "rho": float(rho),
                        "p": float(pvalue),
                    }
                )

    out = pd.DataFrame(rows)
    if len(out):
        # Conservative FDR across all tests at the selected taxonomic rank.
        out["q"] = multipletests(out["p"], method="fdr_bh")[1]
        out = out.sort_values(["q", "site", "variable", "taxon"])

    outdir = Path(args.outdir)
    outdir.mkdir(parents=True, exist_ok=True)
    outfile = outdir / f"{args.rank}_environment_associations.tsv"
    out.to_csv(outfile, sep="\t", index=False)

    print(f"Samples with metadata: {len(sample_cols)}")
    print(f"Tests: {len(out)}")
    if len(out):
        print(f"FDR q<0.05: {(out['q'] < 0.05).sum()}")
    print(outfile)


if __name__ == "__main__":
    main()
