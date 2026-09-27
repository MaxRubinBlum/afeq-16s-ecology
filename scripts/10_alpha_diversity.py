#!/usr/bin/env python3

import argparse
from pathlib import Path
import numpy as np
import pandas as pd


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--table", required=True)
    p.add_argument("--out", required=True)
    args = p.parse_args()

    table = pd.read_csv(args.table, sep="\t")
    table = table.rename(columns={table.columns[0]: "OTU_ID"})
    X = table.drop(columns="OTU_ID")

    rows = []
    for sample in X.columns:
        counts = X[sample].to_numpy(dtype=float)
        total = counts.sum()
        observed = int(np.sum(counts > 0))

        if total > 0:
            pvec = counts[counts > 0] / total
            shannon = float(-np.sum(pvec * np.log(pvec)))
        else:
            shannon = np.nan

        rows.append(
            {
                "sample_id": sample,
                "library_size": int(total),
                "observed_otu99": observed,
                "shannon": shannon,
            }
        )

    out = pd.DataFrame(rows)
    Path(args.out).parent.mkdir(parents=True, exist_ok=True)
    out.to_csv(args.out, sep="\t", index=False)

    print(out[["library_size", "observed_otu99", "shannon"]].describe().to_string())


if __name__ == "__main__":
    main()
