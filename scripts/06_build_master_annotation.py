#!/usr/bin/env python3

import argparse
from pathlib import Path
import pandas as pd


def read_taxonomy(path, prefix):
    df = pd.read_csv(path, sep="\t")
    required = {"Feature ID", "Taxon", "Confidence"}
    missing = required - set(df.columns)
    if missing:
        raise ValueError(f"{path}: missing columns {sorted(missing)}")

    df = df[["Feature ID", "Taxon", "Confidence"]].copy()
    df.columns = [
        "OTU_ID",
        f"{prefix}_taxonomy",
        f"{prefix}_confidence",
    ]

    if df["OTU_ID"].duplicated().any():
        dup = df.loc[df["OTU_ID"].duplicated(), "OTU_ID"].iloc[0]
        raise ValueError(f"{path}: duplicate taxonomy ID {dup}")

    return df


def gtdb_domain(taxon):
    if pd.isna(taxon):
        return ""
    for token in str(taxon).split(";"):
        token = token.strip()
        if token.startswith("d__"):
            return token[3:].strip()
    return ""


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--table", required=True, help="VSEARCH otu-table-99.tsv")
    p.add_argument("--gtdb", required=True, help="QIIME-exported GTDB taxonomy.tsv")
    p.add_argument("--silva", required=True, help="QIIME-exported SILVA taxonomy.tsv")
    p.add_argument("--outdir", required=True)
    args = p.parse_args()

    outdir = Path(args.outdir)
    outdir.mkdir(parents=True, exist_ok=True)

    table = pd.read_csv(args.table, sep="\t")
    otu_col = table.columns[0]
    table = table.rename(columns={otu_col: "OTU_ID"})

    if table["OTU_ID"].duplicated().any():
        raise ValueError("OTU table contains duplicate OTU IDs")

    count_ids = set(table["OTU_ID"])

    gtdb = read_taxonomy(args.gtdb, "GTDB")
    silva = read_taxonomy(args.silva, "SILVA")

    for name, tax in [("GTDB", gtdb), ("SILVA", silva)]:
        tax_ids = set(tax["OTU_ID"])
        missing = sorted(count_ids - tax_ids)
        extra = sorted(tax_ids - count_ids)
        if missing or extra:
            raise ValueError(
                f"{name} IDs do not match OTU table: "
                f"missing={len(missing)}, extra={len(extra)}"
            )

    ann = gtdb.merge(silva, on="OTU_ID", how="inner", validate="one_to_one")

    silva_text = ann["SILVA_taxonomy"].fillna("")
    ann["is_chloroplast"] = silva_text.str.contains(
        "Chloroplast", case=False, regex=False
    )
    ann["is_mitochondria"] = silva_text.str.contains(
        "Mitochondria", case=False, regex=False
    )
    ann["is_eukaryota"] = silva_text.str.contains(
        "d__Eukaryota", case=False, regex=False
    )

    ann["GTDB_domain"] = ann["GTDB_taxonomy"].map(gtdb_domain)
    ann["is_gtdb_unassigned_domain"] = ~ann["GTDB_domain"].isin(
        ["Bacteria", "Archaea"]
    )

    ann["exclude_from_prokaryotic_ecology"] = (
        ann["is_chloroplast"]
        | ann["is_mitochondria"]
        | ann["is_eukaryota"]
        | ann["is_gtdb_unassigned_domain"]
    )

    ann.to_csv(outdir / "master_taxonomy.tsv", sep="\t", index=False)

    keep_ids = set(
        ann.loc[~ann["exclude_from_prokaryotic_ecology"], "OTU_ID"]
    )
    prok = table.loc[table["OTU_ID"].isin(keep_ids)].copy()
    prok.to_csv(outdir / "otu-table-99-prokaryotes.tsv", sep="\t", index=False)

    sample_cols = [c for c in table.columns if c != "OTU_ID"]
    total_reads = table[sample_cols].to_numpy().sum()
    prok_reads = prok[sample_cols].to_numpy().sum()

    def reads_for_flag(flag):
        ids = set(ann.loc[ann[flag], "OTU_ID"])
        return table.loc[
            table["OTU_ID"].isin(ids), sample_cols
        ].to_numpy().sum()

    summary = pd.DataFrame(
        [
            ("OTUs_total", len(table)),
            ("OTUs_chloroplast", int(ann["is_chloroplast"].sum())),
            ("OTUs_mitochondria", int(ann["is_mitochondria"].sum())),
            ("OTUs_eukaryota", int(ann["is_eukaryota"].sum())),
            (
                "OTUs_GTDB_unassigned_domain",
                int(ann["is_gtdb_unassigned_domain"].sum()),
            ),
            (
                "OTUs_excluded_union",
                int(ann["exclude_from_prokaryotic_ecology"].sum()),
            ),
            ("OTUs_prokaryotic_working", len(prok)),
            ("reads_total", int(total_reads)),
            ("reads_chloroplast", int(reads_for_flag("is_chloroplast"))),
            ("reads_mitochondria", int(reads_for_flag("is_mitochondria"))),
            ("reads_eukaryota", int(reads_for_flag("is_eukaryota"))),
            (
                "reads_GTDB_unassigned_domain",
                int(reads_for_flag("is_gtdb_unassigned_domain")),
            ),
            ("reads_prokaryotic_working", int(prok_reads)),
            ("samples", len(sample_cols)),
        ],
        columns=["metric", "value"],
    )
    summary.to_csv(outdir / "master_qc_summary.tsv", sep="\t", index=False)

    print(summary.to_string(index=False))


if __name__ == "__main__":
    main()
