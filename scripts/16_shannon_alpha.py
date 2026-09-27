#!/usr/bin/env python3

import argparse
from pathlib import Path
import numpy as np
import pandas as pd


def shannon_from_counts(counts):
    counts = np.asarray(counts, dtype=float)
    total = counts.sum()
    if total <= 0:
        return np.nan
    p = counts[counts > 0] / total
    return float(-(p * np.log(p)).sum())


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--table", required=True)
    p.add_argument("--out", required=True)
    p.add_argument("--rarefaction-depth", type=int, default=5000)
    p.add_argument("--iterations", type=int, default=50)
    p.add_argument("--seed", type=int, default=20260927)
    args = p.parse_args()

    table = pd.read_csv(args.table, sep="\t")
    table = table.rename(columns={table.columns[0]: "OTU_ID"})
    X = table.drop(columns="OTU_ID")

    rng = np.random.default_rng(args.seed)
    rows = []

    for sample in X.columns:
        counts = X[sample].to_numpy(dtype=np.int64)
        total = int(counts.sum())
        observed_raw = int(np.sum(counts > 0))
        shannon_raw = shannon_from_counts(counts)

        rec = {
            "sample_id": sample,
            "library_size": total,
            "observed_otu99_raw": observed_raw,
            "shannon_raw": shannon_raw,
            "rarefaction_depth": args.rarefaction_depth,
            "rarefaction_iterations": args.iterations,
            "included_rarefaction": total >= args.rarefaction_depth,
            "observed_otu99_rarefied_mean": np.nan,
            "observed_otu99_rarefied_sd": np.nan,
            "shannon_rarefied_mean": np.nan,
            "shannon_rarefied_sd": np.nan,
        }

        if total >= args.rarefaction_depth:
            richness = []
            shannon = []
            for _ in range(args.iterations):
                draw = rng.multivariate_hypergeometric(
                    counts, args.rarefaction_depth
                )
                richness.append(int(np.sum(draw > 0)))
                shannon.append(shannon_from_counts(draw))

            rec.update(
                {
                    "observed_otu99_rarefied_mean": float(np.mean(richness)),
                    "observed_otu99_rarefied_sd": float(np.std(richness, ddof=1)),
                    "shannon_rarefied_mean": float(np.mean(shannon)),
                    "shannon_rarefied_sd": float(np.std(shannon, ddof=1)),
                }
            )

        rows.append(rec)

    out = pd.DataFrame(rows)
    Path(args.out).parent.mkdir(parents=True, exist_ok=True)
    out.to_csv(args.out, sep="\t", index=False)

    print(f"Samples: {len(out)}")
    print(
        f"Rarefaction-eligible: "
        f"{int(out['included_rarefaction'].sum())}/{len(out)}"
    )
    print(
        out[
            [
                "library_size",
                "observed_otu99_raw",
                "shannon_raw",
                "observed_otu99_rarefied_mean",
                "shannon_rarefied_mean",
            ]
        ].describe().to_string()
    )


if __name__ == "__main__":
    main()
