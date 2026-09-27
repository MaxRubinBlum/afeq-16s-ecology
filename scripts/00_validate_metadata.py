#!/usr/bin/env python3

import argparse
import re
from pathlib import Path

import pandas as pd


MONTH_MAP = {
    "Sep24": "September",
    "Jan25": "January",
    "Feb25": "February",
    "Mar25": "March",
    "Apr25": "April",
    "Jul25": "July",
}


def parse_id(sample_id):
    m = re.match(r"^(Sep24|Jan25|Feb25|Mar25|Apr25|Jul25)-([A-Za-z0-9]+)-(.+)$", str(sample_id))
    if not m:
        return None
    return m.groups()


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--metadata", required=True, help="Harmonized metadata TSV")
    p.add_argument("--table", help="Optional OTU table TSV")
    p.add_argument("--sample-id-col", default="sequencing_sample_id")
    p.add_argument("--month-col", default="Month")
    p.add_argument("--site-col", default="Wetland name")
    p.add_argument("--out")
    args = p.parse_args()

    meta = pd.read_csv(args.metadata, sep="\t")
    if args.sample_id_col not in meta.columns:
        raise ValueError(f"Missing metadata column: {args.sample_id_col}")

    meta = meta.dropna(subset=[args.sample_id_col]).copy()
    ids = meta[args.sample_id_col].astype(str)

    problems = []

    dup = ids[ids.duplicated(keep=False)]
    for sid in sorted(set(dup)):
        problems.append(("duplicate_metadata_id", sid, ""))

    for _, row in meta.iterrows():
        sid = str(row[args.sample_id_col])
        parsed = parse_id(sid)
        if parsed is None:
            problems.append(("noncanonical_sample_id", sid, ""))
            continue

        prefix, site, _ = parsed

        if args.month_col in meta.columns and pd.notna(row[args.month_col]):
            expected = MONTH_MAP[prefix]
            observed = str(row[args.month_col]).strip()
            if observed != expected:
                problems.append(
                    ("month_mismatch", sid, f"ID={expected}; metadata={observed}")
                )

        if args.site_col in meta.columns and pd.notna(row[args.site_col]):
            observed_site = str(row[args.site_col]).strip()
            if site != observed_site:
                problems.append(
                    ("site_mismatch", sid, f"ID={site}; metadata={observed_site}")
                )

    table_samples = set()
    if args.table:
        table = pd.read_csv(args.table, sep="\t", nrows=1)
        table_samples = set(table.columns[1:])
        for sid in ids:
            if sid not in table_samples:
                problems.append(("metadata_not_in_table", sid, ""))

    problem_df = pd.DataFrame(
        problems, columns=["problem", "sample_id", "detail"]
    )

    summary = pd.DataFrame(
        [
            ("metadata_rows_with_id", len(meta)),
            ("unique_metadata_ids", ids.nunique()),
            ("table_samples", len(table_samples) if args.table else ""),
            ("problems", len(problem_df)),
        ],
        columns=["metric", "value"],
    )

    if args.out:
        out = Path(args.out)
        out.parent.mkdir(parents=True, exist_ok=True)
        summary.to_csv(out, sep="\t", index=False)
        problem_df.to_csv(
            out.with_name(out.stem + "_problems.tsv"),
            sep="\t",
            index=False,
        )

    print(summary.to_string(index=False))
    if len(problem_df):
        print("\nProblems:")
        print(problem_df.to_string(index=False))

    severe = problem_df["problem"].isin(
        ["duplicate_metadata_id", "noncanonical_sample_id", "month_mismatch", "site_mismatch"]
    ).any()

    if severe:
        raise SystemExit("Metadata validation failed. Resolve identity problems before analysis.")


if __name__ == "__main__":
    main()
