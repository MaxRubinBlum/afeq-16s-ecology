#!/usr/bin/env python3

import argparse
from pathlib import Path
import numpy as np
import pandas as pd
from scipy.spatial.distance import pdist, squareform
from scipy.stats import spearmanr


def load_feature_table(path):
    # VSEARCH tables start directly with "#OTU ID". BIOM TSV exports often
    # contain one preceding "# Constructed from biom file" comment line.
    with open(path, "r", encoding="utf-8") as handle:
        first = handle.readline()

    skiprows = 1 if first.startswith("# Constructed") else 0
    df = pd.read_csv(path, sep="\t", skiprows=skiprows)
    df = df.rename(columns={df.columns[0]: "FeatureID"})
    return df


def relative_bray(table, samples):
    X = table[samples].T.to_numpy(dtype=float)
    totals = X.sum(axis=1, keepdims=True)
    if np.any(totals == 0):
        raise ValueError("Zero-count sample found")
    X = X / totals
    return squareform(pdist(X, metric="braycurtis"))


def matrix_coupling(D1, D2, permutations, seed):
    tri = np.triu_indices(D1.shape[0], 1)
    rho = float(spearmanr(D1[tri], D2[tri]).statistic)

    rng = np.random.default_rng(seed)
    ge = 0
    for _ in range(permutations):
        perm = rng.permutation(D2.shape[0])
        Dp = D2[np.ix_(perm, perm)]
        rp = float(spearmanr(D1[tri], Dp[tri]).statistic)
        ge += abs(rp) >= abs(rho) - 1e-12

    return rho, (ge + 1) / (permutations + 1)


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--sixteen-table", required=True)
    p.add_argument("--mcra-table", required=True)
    p.add_argument("--metadata", required=True)
    p.add_argument("--out", required=True)
    p.add_argument("--sample-id-col", default="sequencing_sample_id")
    p.add_argument("--site-col", default="Wetland name")
    p.add_argument("--mcra-min-reads", type=int, default=1000)
    p.add_argument("--permutations", type=int, default=999)
    p.add_argument("--seed", type=int, default=20260927)
    args = p.parse_args()

    s16 = load_feature_table(args.sixteen_table)
    mcra = load_feature_table(args.mcra_table)

    metadata = pd.read_csv(args.metadata, sep="\t")
    metadata = metadata.dropna(subset=[args.sample_id_col])
    metadata = metadata.drop_duplicates(args.sample_id_col)
    metadata = metadata.set_index(args.sample_id_col)

    s16_samples = set(s16.columns[1:])

    mcra_cols = list(mcra.columns[1:])
    mcra_totals = mcra[mcra_cols].sum(axis=0)
    mcra_samples = {
        s for s in mcra_cols
        if mcra_totals[s] >= args.mcra_min_reads
        and s in metadata.index
    }

    shared = [
        s for s in metadata.index
        if s in s16_samples and s in mcra_samples
    ]

    if len(shared) < 5:
        raise ValueError("Too few shared metadata-matched samples")

    D16 = relative_bray(s16, shared)
    Dm = relative_bray(mcra, shared)

    rows = []
    rho, pval = matrix_coupling(
        D16, Dm, args.permutations, args.seed
    )
    rows.append(
        {
            "scope": "all_shared",
            "n": len(shared),
            "spearman_distance_correlation": rho,
            "permutation_p": pval,
        }
    )

    meta = metadata.loc[shared]
    sites = meta[args.site_col]

    for i, site in enumerate(sorted(sites.dropna().unique())):
        ids = np.where((sites == site).to_numpy())[0]
        if len(ids) < 5:
            continue
        rho, pval = matrix_coupling(
            D16[np.ix_(ids, ids)],
            Dm[np.ix_(ids, ids)],
            args.permutations,
            args.seed + 100 + i,
        )
        rows.append(
            {
                "scope": f"site={site}",
                "n": len(ids),
                "spearman_distance_correlation": rho,
                "permutation_p": pval,
            }
        )

    out = pd.DataFrame(rows)
    Path(args.out).parent.mkdir(parents=True, exist_ok=True)
    out.to_csv(args.out, sep="\t", index=False)

    print(f"Shared samples: {len(shared)}")
    print(out.to_string(index=False))


if __name__ == "__main__":
    main()
