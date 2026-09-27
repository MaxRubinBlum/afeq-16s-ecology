#!/usr/bin/env python3

import argparse
from pathlib import Path
import numpy as np
import pandas as pd


def transform(X, method):
    X = X.astype(float)
    if method == "none":
        return X
    totals = X.sum(axis=1, keepdims=True)
    totals[totals == 0] = 1.0
    rel = X / totals
    if method == "relative":
        return rel
    if method == "hellinger":
        return np.sqrt(rel)
    raise ValueError(method)


def bray_curtis_matrix(X):
    n = X.shape[0]
    D = np.zeros((n, n), dtype=float)
    for i in range(n):
        for j in range(i + 1, n):
            den = np.sum(X[i] + X[j])
            d = np.sum(np.abs(X[i] - X[j])) / den if den else 0.0
            D[i, j] = D[j, i] = d
    return D


def pcoa(D):
    n = D.shape[0]
    J = np.eye(n) - np.ones((n, n)) / n
    B = -0.5 * J @ (D ** 2) @ J
    eigvals, eigvecs = np.linalg.eigh(B)
    order = np.argsort(eigvals)[::-1]
    eigvals = eigvals[order]
    eigvecs = eigvecs[:, order]

    positive = eigvals > 0
    coords = eigvecs[:, positive] * np.sqrt(eigvals[positive])
    return eigvals, coords


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--table", required=True)
    p.add_argument("--outdir", required=True)
    p.add_argument(
        "--transform",
        choices=["relative", "hellinger", "none"],
        default="relative",
    )
    args = p.parse_args()

    table = pd.read_csv(args.table, sep="\t")
    table = table.rename(columns={table.columns[0]: "OTU_ID"})

    samples = table.columns[1:].tolist()
    X = table[samples].T.to_numpy(dtype=float)
    X = transform(X, args.transform)

    D = bray_curtis_matrix(X)
    eigvals, coords = pcoa(D)

    outdir = Path(args.outdir)
    outdir.mkdir(parents=True, exist_ok=True)

    pd.DataFrame(D, index=samples, columns=samples).to_csv(
        outdir / "bray_curtis.tsv", sep="\t", index_label="sample_id"
    )

    n_axes = min(10, coords.shape[1])
    coord_df = pd.DataFrame(
        coords[:, :n_axes],
        index=samples,
        columns=[f"PCoA{i+1}" for i in range(n_axes)],
    )
    coord_df.to_csv(
        outdir / "pcoa_coordinates.tsv", sep="\t", index_label="sample_id"
    )

    positive = eigvals[eigvals > 0]
    explained = positive / positive.sum() if positive.sum() else positive
    eig_df = pd.DataFrame(
        {
            "axis": [f"PCoA{i+1}" for i in range(len(positive))],
            "eigenvalue": positive,
            "proportion_explained": explained,
        }
    )
    eig_df.to_csv(outdir / "pcoa_eigenvalues.tsv", sep="\t", index=False)

    print(coord_df.head().to_string())
    print("\nVariance explained by first axes:")
    print(eig_df.head(5).to_string(index=False))


if __name__ == "__main__":
    main()
