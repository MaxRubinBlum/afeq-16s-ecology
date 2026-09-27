#!/usr/bin/env python3

import argparse
from pathlib import Path
import numpy as np
import pandas as pd
from scipy.spatial.distance import pdist, squareform
from scipy.stats import spearmanr


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


def pcoa(D):
    n = D.shape[0]
    J = np.eye(n) - np.ones((n, n)) / n
    B = -0.5 * J @ (D ** 2) @ J
    eigvals, eigvecs = np.linalg.eigh(B)
    order = np.argsort(eigvals)[::-1]
    eigvals = eigvals[order]
    eigvecs = eigvecs[:, order]

    positive = eigvals > 1e-12
    coords = eigvecs[:, positive] * np.sqrt(eigvals[positive])
    return eigvals, coords


def permanova_oneway(D, labels, permutations, seed):
    labels = np.asarray(labels, dtype=object)
    n = len(labels)
    groups = np.unique(labels)
    k = len(groups)

    iu = np.triu_indices(n, 1)
    ss_total = np.sum(D[iu] ** 2) / n

    def statistic(lab):
        ss_within = 0.0
        for g in np.unique(lab):
            ids = np.where(lab == g)[0]
            ng = len(ids)
            if ng <= 1:
                continue
            sub = D[np.ix_(ids, ids)]
            ig = np.triu_indices(ng, 1)
            ss_within += np.sum(sub[ig] ** 2) / ng

        ss_between = ss_total - ss_within
        F = (ss_between / (k - 1)) / (ss_within / (n - k))
        R2 = ss_between / ss_total
        return float(F), float(R2)

    Fobs, R2 = statistic(labels)
    rng = np.random.default_rng(seed)
    ge = 0

    for _ in range(permutations):
        Fperm, _ = statistic(rng.permutation(labels))
        ge += Fperm >= Fobs - 1e-12

    p = (ge + 1) / (permutations + 1)
    return Fobs, R2, p


def permdisp(coords, labels, permutations, seed):
    labels = np.asarray(labels, dtype=object)
    groups = np.unique(labels)
    n = len(labels)
    k = len(groups)

    def distances_to_centroid(lab):
        d = np.zeros(n, dtype=float)
        for g in groups:
            ids = np.where(lab == g)[0]
            centroid = coords[ids].mean(axis=0)
            d[ids] = np.sqrt(((coords[ids] - centroid) ** 2).sum(axis=1))
        return d

    def F_from_distances(d, lab):
        grand = d.mean()
        ssb = sum(
            np.sum(lab == g) * (d[lab == g].mean() - grand) ** 2
            for g in groups
        )
        ssw = sum(
            ((d[lab == g] - d[lab == g].mean()) ** 2).sum()
            for g in groups
        )
        return float((ssb / (k - 1)) / (ssw / (n - k)))

    d = distances_to_centroid(labels)
    Fobs = F_from_distances(d, labels)

    rng = np.random.default_rng(seed)
    ge = 0
    for _ in range(permutations):
        perm = rng.permutation(labels)
        dp = distances_to_centroid(perm)
        Fp = F_from_distances(dp, perm)
        ge += Fp >= Fobs - 1e-12

    means = {
        str(g): float(d[labels == g].mean())
        for g in groups
    }
    return Fobs, (ge + 1) / (permutations + 1), means


def mantel_depth(D, depth, permutations, seed):
    depth = np.asarray(depth, dtype=float)
    depth_D = np.abs(depth[:, None] - depth[None, :])
    tri = np.triu_indices(len(depth), 1)

    rho = float(spearmanr(D[tri], depth_D[tri]).statistic)
    rng = np.random.default_rng(seed)
    ge = 0

    for _ in range(permutations):
        perm = rng.permutation(len(depth))
        dp = depth_D[np.ix_(perm, perm)]
        rp = float(spearmanr(D[tri], dp[tri]).statistic)
        ge += abs(rp) >= abs(rho) - 1e-12

    return rho, (ge + 1) / (permutations + 1)


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--table", required=True)
    p.add_argument("--outdir", required=True)
    p.add_argument("--metadata")
    p.add_argument("--sample-id-col", default="sequencing_sample_id")
    p.add_argument("--site-col", default="Wetland name")
    p.add_argument("--month-col", default="Month")
    p.add_argument("--depth-col", default="Depth")
    p.add_argument(
        "--transform",
        choices=["relative", "hellinger", "none"],
        default="relative",
    )
    p.add_argument("--permutations", type=int, default=999)
    p.add_argument("--seed", type=int, default=20260927)
    args = p.parse_args()

    table = pd.read_csv(args.table, sep="\t")
    table = table.rename(columns={table.columns[0]: "OTU_ID"})

    samples = table.columns[1:].tolist()

    if args.metadata:
        meta = pd.read_csv(args.metadata, sep="\t")
        meta = meta.dropna(subset=[args.sample_id_col]).copy()
        meta = meta.drop_duplicates(args.sample_id_col)
        meta = meta.set_index(args.sample_id_col)

        samples = [s for s in samples if s in meta.index]
        if not samples:
            raise ValueError("No OTU-table samples match metadata")

    X = table[samples].T.to_numpy(dtype=float)
    X = transform(X, args.transform)

    D = squareform(pdist(X, metric="braycurtis"))
    eigvals, coords = pcoa(D)

    outdir = Path(args.outdir)
    outdir.mkdir(parents=True, exist_ok=True)

    pd.DataFrame(D, index=samples, columns=samples).to_csv(
        outdir / "bray_curtis.tsv",
        sep="\t",
        index_label="sample_id",
    )

    n_axes = min(10, coords.shape[1])
    coord_df = pd.DataFrame(
        coords[:, :n_axes],
        index=samples,
        columns=[f"PCoA{i+1}" for i in range(n_axes)],
    )
    coord_df.to_csv(
        outdir / "pcoa_coordinates.tsv",
        sep="\t",
        index_label="sample_id",
    )

    positive = eigvals[eigvals > 1e-12]
    explained = positive / positive.sum()
    pd.DataFrame(
        {
            "axis": [f"PCoA{i+1}" for i in range(len(positive))],
            "eigenvalue": positive,
            "proportion_explained": explained,
        }
    ).to_csv(outdir / "pcoa_eigenvalues.tsv", sep="\t", index=False)

    if args.metadata:
        meta = meta.loc[samples].copy()
        tests = []

        for col, offset in [
            (args.site_col, 0),
            (args.month_col, 100),
        ]:
            keep = meta[col].notna().to_numpy()
            ids = np.where(keep)[0]

            if len(ids) < 3 or meta.iloc[ids][col].nunique() < 2:
                continue

            subD = D[np.ix_(ids, ids)]
            labels = meta.iloc[ids][col].astype(str).to_numpy()
            F, R2, pval = permanova_oneway(
                subD,
                labels,
                args.permutations,
                args.seed + offset,
            )

            _, subcoords = pcoa(subD)
            Fd, pdsp, means = permdisp(
                subcoords,
                labels,
                args.permutations,
                args.seed + offset + 1,
            )

            tests.append(
                {
                    "test": "PERMANOVA",
                    "variable": col,
                    "n": len(ids),
                    "statistic": F,
                    "R2": R2,
                    "p": pval,
                    "notes": "",
                }
            )
            tests.append(
                {
                    "test": "PERMDISP",
                    "variable": col,
                    "n": len(ids),
                    "statistic": Fd,
                    "R2": np.nan,
                    "p": pdsp,
                    "notes": "; ".join(
                        f"{k} mean_distance={v:.6f}"
                        for k, v in means.items()
                    ),
                }
            )

        depth_numeric = pd.to_numeric(meta[args.depth_col], errors="coerce")
        keep = depth_numeric.notna().to_numpy()
        ids = np.where(keep)[0]

        if len(ids) >= 5:
            rho, pval = mantel_depth(
                D[np.ix_(ids, ids)],
                depth_numeric.iloc[ids].to_numpy(),
                args.permutations,
                args.seed + 300,
            )
            tests.append(
                {
                    "test": "Mantel_Spearman",
                    "variable": args.depth_col,
                    "n": len(ids),
                    "statistic": rho,
                    "R2": np.nan,
                    "p": pval,
                    "notes": "Bray-Curtis versus absolute depth difference",
                }
            )

            for nsite, site in enumerate(sorted(meta[args.site_col].dropna().unique())):
                site_keep = (
                    (meta[args.site_col] == site)
                    & depth_numeric.notna()
                ).to_numpy()
                sids = np.where(site_keep)[0]
                if len(sids) < 5:
                    continue

                rho, pval = mantel_depth(
                    D[np.ix_(sids, sids)],
                    depth_numeric.iloc[sids].to_numpy(),
                    args.permutations,
                    args.seed + 400 + nsite,
                )
                tests.append(
                    {
                        "test": "Mantel_Spearman_within_site",
                        "variable": args.depth_col,
                        "n": len(sids),
                        "statistic": rho,
                        "R2": np.nan,
                        "p": pval,
                        "notes": f"site={site}",
                    }
                )

        pd.DataFrame(tests).to_csv(
            outdir / "community_structure_tests.tsv",
            sep="\t",
            index=False,
        )

    print(f"Samples analyzed: {len(samples)}")
    print("PCoA variance explained:")
    for i, x in enumerate(explained[:5], start=1):
        print(f"  PCoA{i}: {x:.4f}")


if __name__ == "__main__":
    main()
