#!/usr/bin/env python3

import argparse
from pathlib import Path

import numpy as np
import pandas as pd


def read_table(path):
    df = pd.read_csv(path, sep="\t", comment=None)
    if df.columns[0].startswith("#"):
        df = df.rename(columns={df.columns[0]: "feature_id"})
    else:
        df = df.rename(columns={df.columns[0]: "feature_id"})
    return df


def describe(df, label):
    sample_cols = df.columns[1:]
    depths = df[sample_cols].sum(axis=0)
    return {
        "dataset": label,
        "features": len(df),
        "samples": len(sample_cols),
        "total_reads": int(depths.sum()),
        "median_reads_per_sample": float(depths.median()),
        "min_reads_per_sample": int(depths.min()),
        "max_reads_per_sample": int(depths.max()),
    }, depths


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--direct-table", required=True)
    p.add_argument("--dada2-table", required=True)
    p.add_argument("--outdir", required=True)
    args = p.parse_args()

    direct = read_table(args.direct_table)
    dada2 = read_table(args.dada2_table)

    dsum, ddepth = describe(direct, "direct_99")
    asum, adepth = describe(dada2, "dada2_then_99")

    outdir = Path(args.outdir)
    outdir.mkdir(parents=True, exist_ok=True)

    pd.DataFrame([dsum, asum]).to_csv(
        outdir / "processing_branch_summary.tsv",
        sep="\t",
        index=False,
    )

    shared = sorted(set(ddepth.index) & set(adepth.index))
    per_sample = pd.DataFrame(
        {
            "sample_id": shared,
            "direct_reads": [int(ddepth[s]) for s in shared],
            "dada2_reads": [int(adepth[s]) for s in shared],
        }
    )
    per_sample["dada2_over_direct"] = (
        per_sample["dada2_reads"]
        / per_sample["direct_reads"].replace(0, np.nan)
    )
    per_sample.to_csv(
        outdir / "processing_branch_sample_depths.tsv",
        sep="\t",
        index=False,
    )

    print(pd.DataFrame([dsum, asum]).to_string(index=False))
    print(f"Shared samples: {len(shared)}")


if __name__ == "__main__":
    main()
