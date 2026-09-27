#!/usr/bin/env python3

import argparse
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


MONTH_ORDER = ["September", "January", "April", "July"]
SITE_ORDER = ["EA1", "EA2", "EA3", "EA4"]


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--profile", required=True, help="Sample x taxon relative-abundance TSV")
    p.add_argument("--metadata", required=True)
    p.add_argument("--outdir", required=True)
    p.add_argument("--sample-id-col", default="sequencing_sample_id")
    p.add_argument("--site-col", default="Wetland name")
    p.add_argument("--month-col", default="Month")
    p.add_argument("--depth-col", default="Depth")
    p.add_argument("--top-n", type=int, default=10)
    p.add_argument("--min-percent", type=float, default=0.25)
    p.add_argument("--max-depth", type=float, default=40.0)
    args = p.parse_args()

    prof = pd.read_csv(args.profile, sep="\t")
    if prof.columns[0] != "sample_id":
        prof = prof.rename(columns={prof.columns[0]: "sample_id"})
    prof = prof.set_index("sample_id")

    meta = pd.read_csv(args.metadata, sep="\t")
    meta = meta.dropna(subset=[args.sample_id_col]).drop_duplicates(args.sample_id_col)
    meta = meta.set_index(args.sample_id_col)
    meta[args.depth_col] = pd.to_numeric(meta[args.depth_col], errors="coerce")

    samples = [s for s in prof.index if s in meta.index]
    if not samples:
        raise ValueError("No profile samples match metadata")

    prof = prof.loc[samples]
    meta = meta.loc[samples]

    mean_ab = prof.mean(axis=0).sort_values(ascending=False)
    taxa = list(mean_ab.head(args.top_n).index)

    long = (
        prof[taxa]
        .reset_index()
        .melt(id_vars="sample_id", var_name="taxon", value_name="relative_abundance_pct")
        .merge(
            meta[[args.site_col, args.month_col, args.depth_col]].reset_index(),
            left_on="sample_id",
            right_on=args.sample_id_col,
            how="left",
        )
    )
    long["plotted"] = long["relative_abundance_pct"] >= args.min_percent

    outdir = Path(args.outdir)
    outdir.mkdir(parents=True, exist_ok=True)
    long.to_csv(outdir / "depth_taxonomy_plot_data.tsv", sep="\t", index=False)
    pd.DataFrame({"taxon": taxa}).to_csv(
        outdir / "depth_taxonomy_taxa.tsv", sep="\t", index=False
    )

    sites = [s for s in SITE_ORDER if s in set(meta[args.site_col].dropna())]
    months = [m for m in MONTH_ORDER if m in set(meta[args.month_col].dropna())]

    fig, axes = plt.subplots(
        len(sites),
        len(months),
        figsize=(3.5 * len(months), 3.0 * len(sites)),
        squeeze=False,
        sharey=True,
    )

    xpos = {taxon: i for i, taxon in enumerate(taxa)}

    for i, site in enumerate(sites):
        for j, month in enumerate(months):
            ax = axes[i, j]
            sub = long[
                (long[args.site_col] == site)
                & (long[args.month_col] == month)
                & long[args.depth_col].notna()
                & long["plotted"]
            ].copy()

            if len(sub):
                x = sub["taxon"].map(xpos).to_numpy()
                y = sub[args.depth_col].to_numpy(dtype=float)
                a = sub["relative_abundance_pct"].to_numpy(dtype=float)
                ax.scatter(x, y, s=np.maximum(a, 0.1) * 8, alpha=0.7)

            ax.set_ylim(args.max_depth, 0)
            ax.set_xticks(range(len(taxa)))
            ax.set_xticklabels(taxa, rotation=60, ha="right", fontsize=7)
            if i == 0:
                ax.set_title(month)
            if j == 0:
                ax.set_ylabel(f"{site}\nSediment depth (cm)")

    fig.suptitle("Depth-resolved 16S taxonomic composition")
    fig.tight_layout()
    fig.savefig(outdir / "depth_taxonomy_bubble.png", dpi=300, bbox_inches="tight")
    fig.savefig(outdir / "depth_taxonomy_bubble.pdf", bbox_inches="tight")
    plt.close(fig)

    print(f"Samples: {len(samples)}")
    print(f"Taxa plotted: {len(taxa)}")
    print(outdir / "depth_taxonomy_bubble.png")


if __name__ == "__main__":
    main()
