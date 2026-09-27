#!/usr/bin/env python3

from pathlib import Path
import argparse
import csv
import re


def parse_2860(path: Path) -> str:
    m = re.search(
        r'_(Sep_24|Jan_25)16s_([A-Za-z0-9]+)-([A-Za-z0-9]+)_PacBKinnex',
        path.name,
    )
    if not m:
        raise ValueError(f"Cannot parse run-2860 filename: {path.name}")

    month_raw, site, sample = m.groups()
    month = {"Sep_24": "Sep24", "Jan_25": "Jan25"}[month_raw]
    return f"{month}-{site}-{sample}"


def parse_3408(path: Path) -> str:
    m = re.search(
        r'_(Apr25|Jul25|Jan25|Feb25|Mar25)_16s_'
        r'([A-Za-z0-9]+)-([A-Za-z0-9]+)\.',
        path.name,
    )
    if not m:
        raise ValueError(f"Cannot parse run-3408 filename: {path.name}")

    month, site, sample = m.groups()
    sample_id = f"{month}-{site}-{sample}"

    # Preserve Jan run-3408 libraries as separate resequencing libraries.
    if month == "Jan25":
        sample_id += "-r3408"

    return sample_id


def write_manifest(paths, parser, outfile: Path):
    records = []
    seen = set()

    for path in sorted(paths):
        sample_id = parser(path)
        if sample_id in seen:
            raise ValueError(f"Duplicate sample ID within manifest: {sample_id}")
        seen.add(sample_id)
        records.append((sample_id, str(path.resolve())))

    outfile.parent.mkdir(parents=True, exist_ok=True)

    # lineterminator='\n' prevents Windows CRLF from becoming part of FASTQ paths.
    with outfile.open("w", newline="") as handle:
        writer = csv.writer(handle, delimiter="\t", lineterminator="\n")
        writer.writerow(["sample-id", "absolute-filepath"])
        writer.writerows(records)

    return len(records)


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--run2860-dir", default="16S_Afeq_Sept_Jan")
    p.add_argument("--run3408-dir", default="16S_Afeq_Apr_Jul")
    p.add_argument("--outdir", default="16S_analysis/manifests")
    p.add_argument("--expected2860", type=int, default=62)
    p.add_argument("--expected3408", type=int, default=126)
    args = p.parse_args()

    run2860_dir = Path(args.run2860_dir)
    run3408_dir = Path(args.run3408_dir)
    outdir = Path(args.outdir)

    # Only genuine run-prefixed files are selected. This automatically ignores
    # the six copied 2860 Jan EA4 FASTQs in the second raw-data directory.
    run2860 = sorted(run2860_dir.glob("2860_*.fastq.gz"))
    run3408 = sorted(run3408_dir.glob("3408_*.fastq.gz"))

    n2860 = write_manifest(
        run2860, parse_2860, outdir / "manifest_run2860.tsv"
    )
    n3408 = write_manifest(
        run3408, parse_3408, outdir / "manifest_run3408.tsv"
    )

    print(f"{outdir / 'manifest_run2860.tsv'}: {n2860} samples")
    print(f"{outdir / 'manifest_run3408.tsv'}: {n3408} samples")

    if n2860 != args.expected2860:
        raise SystemExit(
            f"Unexpected run-2860 count: {n2860} != {args.expected2860}"
        )
    if n3408 != args.expected3408:
        raise SystemExit(
            f"Unexpected run-3408 count: {n3408} != {args.expected3408}"
        )


if __name__ == "__main__":
    main()
