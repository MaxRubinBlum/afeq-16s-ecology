#!/usr/bin/env python3

from pathlib import Path
import importlib.util


SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "01_make_manifests.py"

spec = importlib.util.spec_from_file_location("make_manifests", SCRIPT)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)


def main():
    p2860 = Path("2860_x_Sep_2416s_EA1-3_PacBKinnex.fastq.gz")
    p3408 = Path("3408_x_Apr25_16s_EA2-10.fastq.gz")
    p3408_jan = Path("3408_x_Jan25_16s_EA4-2.fastq.gz")

    assert mod.parse_2860(p2860) == "Sep24-EA1-3"
    assert mod.parse_3408(p3408) == "Apr25-EA2-10"
    assert mod.parse_3408(p3408_jan) == "Jan25-EA4-2-r3408"

    print("Manifest parser tests passed")


if __name__ == "__main__":
    main()
