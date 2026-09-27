#!/usr/bin/env python3

import argparse
from pathlib import Path
import pandas as pd
import numpy as np


RANK_PREFIX = {
    "domain": "d__",
    "phylum": "p__",
    "class": "c__",
    "order": "o__",
    "family": "f__",
    "genus": "g__",
    "species": "s__",
}


def normalize(v):
    total = np.sum(v)
    return v / total if total > 0 else v


def bray_similarity(a, b):
    # Technical/resequencing comparison is performed on relative abundance
    # so differences in library size do not dominate Bray-Curtis.
    a = normalize(a.astype(float))
    b = normalize(b.astype(float))
    den = np.sum(a + b)
    if den == 0:
        return np.nan
    return 1.0 - np.sum(np.abs(a - b)) / den


def extract_rank(taxon, rank):
    prefix = RANK_PREFIX[rank]
    if pd.isna(taxon):
        return "Unassigned"
    for token in str(taxon).split(";"):
        token = token.strip()
        if token.startswith(prefix):
            value = token[len(prefix):].strip()
            return value if value else "Unassigned"
    return "Unassigned"


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--table", required=True)
    p.add_argument("--annotation")
    p.add_argument("--out", required=True)
    p.add_argument(
        "--ranks",
        default="phylum,family,genus",
        help="GTDB ranks to compare when --annotation is provided",
    )
    args = p.parse_args()

    table = pd.read_csv(args.table, sep="\t")
    table = table.rename(columns={table.columns[0]: "OTU_ID"})
    sample_cols = table.columns[1:].tolist()

    pairs = []
    for s in sample_cols:
        if s.endswith("-r3408"):
            original = s[:-6]
            if original in sample_cols:
                pairs.append((original, s))

    if not pairs:
        raise ValueError("No original / -r3408 Jan pairs found")

    layers = {"OTU": table.set_index("OTU_ID")}

    if args.annotation:
        ann = pd.read_csv(args.annotation, sep="\t")
        ranks = [x.strip() for x in args.ranks.split(",") if x.strip()]
        labels = ann.set_index("OTU_ID")["GTDB_taxonomy"]

        for rank in ranks:
            grouped = table[["OTU_ID"] + sample_cols].copy()
            grouped["rank"] = grouped["OTU_ID"].map(labels).map(
                lambda x: extract_rank(x, rank)
            )
            grouped = grouped.drop(columns="OTU_ID").groupby("rank").sum()
            layers[f"GTDB_{rank}"] = grouped

    rows = []
    for level, mat in layers.items():
        for original, resequenced in pairs:
            a = mat[original].to_numpy(dtype=float)
            b = mat[resequenced].to_numpy(dtype=float)

            rows.append(
                {
                    "level": level,
                    "original": original,
                    "resequenced": resequenced,
                    "reads_original": int(a.sum()),
                    "reads_resequenced": int(b.sum()),
                    "bray_curtis_similarity": bray_similarity(a, b),
                }
            )

    out = pd.DataFrame(rows)
    Path(args.out).parent.mkdir(parents=True, exist_ok=True)
    out.to_csv(args.out, sep="\t", index=False)

    print(
        out.groupby("level")["bray_curtis_similarity"]
        .agg(["count", "mean", "median", "min", "max"])
        .to_string()
    )


if __name__ == "__main__":
    main()
