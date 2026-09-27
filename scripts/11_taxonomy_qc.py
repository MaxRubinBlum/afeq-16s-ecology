#!/usr/bin/env python3

import argparse
from pathlib import Path

import pandas as pd


RANKS = {
    "domain": "d__",
    "phylum": "p__",
    "class": "c__",
    "order": "o__",
    "family": "f__",
    "genus": "g__",
    "species": "s__",
}


def rank_present(taxon, prefix):
    if pd.isna(taxon):
        return False
    for token in str(taxon).split(";"):
        token = token.strip()
        if token.startswith(prefix):
            return bool(token[len(prefix):].strip())
    return False


def summarize_source(df, source):
    tax_col = f"{source}_taxonomy"
    conf_col = f"{source}_confidence"
    rows = []

    for rank, prefix in RANKS.items():
        n = int(df[tax_col].map(lambda x: rank_present(x, prefix)).sum())
        rows.append(
            {
                "source": source,
                "metric": f"assigned_{rank}",
                "value": n,
                "fraction": n / len(df),
            }
        )

    conf = pd.to_numeric(df[conf_col], errors="coerce")
    for threshold in [0.7, 0.8, 0.9, 0.95]:
        n = int((conf >= threshold).sum())
        rows.append(
            {
                "source": source,
                "metric": f"confidence_ge_{threshold}",
                "value": n,
                "fraction": n / len(df),
            }
        )

    rows.append(
        {
            "source": source,
            "metric": "median_confidence",
            "value": float(conf.median()),
            "fraction": "",
        }
    )
    return rows


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--annotation", required=True)
    p.add_argument("--out", required=True)
    args = p.parse_args()

    ann = pd.read_csv(args.annotation, sep="\t")

    required = {
        "OTU_ID",
        "GTDB_taxonomy",
        "GTDB_confidence",
        "SILVA_taxonomy",
        "SILVA_confidence",
    }
    missing = required - set(ann.columns)
    if missing:
        raise ValueError(f"Missing columns: {sorted(missing)}")

    rows = [
        {
            "source": "all",
            "metric": "OTUs",
            "value": len(ann),
            "fraction": 1.0,
        }
    ]
    rows.extend(summarize_source(ann, "GTDB"))
    rows.extend(summarize_source(ann, "SILVA"))

    for flag in [
        "is_chloroplast",
        "is_mitochondria",
        "is_eukaryota",
        "is_gtdb_unassigned_domain",
        "exclude_from_prokaryotic_ecology",
    ]:
        if flag in ann.columns:
            n = int(ann[flag].astype(bool).sum())
            rows.append(
                {
                    "source": "filter",
                    "metric": flag,
                    "value": n,
                    "fraction": n / len(ann),
                }
            )

    out = pd.DataFrame(rows)
    path = Path(args.out)
    path.parent.mkdir(parents=True, exist_ok=True)
    out.to_csv(path, sep="\t", index=False)
    print(out.to_string(index=False))


if __name__ == "__main__":
    main()
