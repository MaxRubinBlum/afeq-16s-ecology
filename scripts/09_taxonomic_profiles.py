#!/usr/bin/env python3

import argparse
from pathlib import Path
import pandas as pd


RANKS = {
    "domain": ("d__", 0),
    "phylum": ("p__", 1),
    "class": ("c__", 2),
    "order": ("o__", 3),
    "family": ("f__", 4),
    "genus": ("g__", 5),
    "species": ("s__", 6),
}


def get_rank(taxon, rank):
    prefix, pos = RANKS[rank]
    if pd.isna(taxon):
        return "Unassigned"

    tokens = [x.strip() for x in str(taxon).split(";")]

    for token in tokens:
        if token.startswith(prefix):
            value = token[len(prefix):].strip()
            return value if value else "Unassigned"

    if pos < len(tokens):
        value = tokens[pos]
        if "__" in value:
            value = value.split("__", 1)[1]
        return value.strip() or "Unassigned"

    return "Unassigned"


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--table", required=True)
    p.add_argument("--annotation", required=True)
    p.add_argument("--source", choices=["GTDB", "SILVA"], default="GTDB")
    p.add_argument("--rank", choices=list(RANKS), default="phylum")
    p.add_argument("--out", required=True)
    args = p.parse_args()

    counts = pd.read_csv(args.table, sep="\t")
    counts = counts.rename(columns={counts.columns[0]: "OTU_ID"})
    ann = pd.read_csv(args.annotation, sep="\t")

    tax_col = f"{args.source}_taxonomy"
    labels = ann.set_index("OTU_ID")[tax_col].map(
        lambda x: get_rank(x, args.rank)
    )

    counts["taxon"] = counts["OTU_ID"].map(labels)
    grouped = counts.drop(columns="OTU_ID").groupby("taxon").sum()

    # samples x taxa
    grouped = grouped.T
    rel = grouped.div(grouped.sum(axis=1).replace(0, pd.NA), axis=0) * 100

    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    rel.to_csv(out, sep="\t", index_label="sample_id")

    print(f"Samples: {len(rel)}")
    print(f"{args.source} {args.rank} categories: {rel.shape[1]}")


if __name__ == "__main__":
    main()
