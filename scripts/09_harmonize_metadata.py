#!/usr/bin/env python3

import argparse
from pathlib import Path
import pandas as pd


MONTH_PREFIX = {
    "April": "Apr25",
    "July": "Jul25",
    "January": "Jan25",
    "September": "Sep24",
}


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--metadata", required=True, help="Metadata workbook (.xlsx)")
    p.add_argument("--table", required=True, help="OTU table TSV")
    p.add_argument("--outdir", required=True)
    p.add_argument("--sheet", default=0)
    args = p.parse_args()

    outdir = Path(args.outdir)
    outdir.mkdir(parents=True, exist_ok=True)

    meta = pd.read_excel(args.metadata, sheet_name=args.sheet)

    if "Month" not in meta.columns:
        raise ValueError("Metadata workbook lacks a 'Month' column")

    source_col = meta.columns[0]
    sample_ids = []

    for _, row in meta.iterrows():
        source = str(row[source_col])
        month = str(row["Month"])

        if month not in MONTH_PREFIX:
            sample_ids.append(None)
            continue

        if "16s_" not in source:
            sample_ids.append(None)
            continue

        suffix = source.split("16s_", 1)[1]
        sample_ids.append(f"{MONTH_PREFIX[month]}-{suffix}")

    meta.insert(0, "sequencing_sample_id", sample_ids)

    table = pd.read_csv(args.table, sep="\t", nrows=1)
    samples = set(table.columns[1:])

    meta["present_in_otu_table"] = meta["sequencing_sample_id"].isin(samples)
    meta.to_csv(outdir / "metadata_harmonized.tsv", sep="\t", index=False)

    matched = meta.loc[meta["present_in_otu_table"]].copy()
    matched.to_csv(outdir / "metadata_matched.tsv", sep="\t", index=False)

    unmatched = meta.loc[~meta["present_in_otu_table"]].copy()
    unmatched.to_csv(outdir / "metadata_unmatched.tsv", sep="\t", index=False)

    print(f"Metadata rows: {len(meta)}")
    print(f"Matched to OTU table: {len(matched)}")
    print(f"Unmatched metadata rows: {len(unmatched)}")

    if len(unmatched):
        print("\nUnmatched IDs:")
        for x in unmatched["sequencing_sample_id"].tolist():
            print(x)


if __name__ == "__main__":
    main()
