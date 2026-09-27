#!/usr/bin/env python3

import argparse
import pandas as pd


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--table", required=True)
    p.add_argument("--gtdb", required=True)
    p.add_argument("--silva", required=True)
    p.add_argument("--expected-otus", type=int, default=26300)
    p.add_argument("--expected-samples", type=int, default=188)
    args = p.parse_args()

    table = pd.read_csv(args.table, sep="\t")
    otu_col = table.columns[0]
    otu_ids = set(table[otu_col])

    gtdb = pd.read_csv(args.gtdb, sep="\t")
    silva = pd.read_csv(args.silva, sep="\t")

    assert len(table) == args.expected_otus, (
        f"OTU count {len(table)} != {args.expected_otus}"
    )
    assert len(table.columns) - 1 == args.expected_samples, (
        f"Sample count {len(table.columns)-1} != {args.expected_samples}"
    )
    assert otu_ids == set(gtdb["Feature ID"]), "GTDB IDs do not match OTU table"
    assert otu_ids == set(silva["Feature ID"]), "SILVA IDs do not match OTU table"

    total_reads = int(table.iloc[:, 1:].to_numpy().sum())

    print(f"OTUs: {len(table)}")
    print(f"Samples: {len(table.columns)-1}")
    print(f"Mapped reads: {total_reads}")
    print("GTDB IDs: exact match")
    print("SILVA IDs: exact match")
    print("Validation passed")


if __name__ == "__main__":
    main()
