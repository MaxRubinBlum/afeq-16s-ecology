# Master annotation and ecological filtering

## Purpose

Taxonomic filtering should be applied once, transparently, before ecological scripts begin. Downstream scripts should all read the same approved working table.

## Inputs

~~~text
otu-table-99.tsv
GTDB taxonomy.tsv
SILVA taxonomy.tsv
~~~

The three files must contain exactly the same 26,300 OTU IDs.

## Master annotation

Run:

~~~bash
python3 scripts/08_build_master_annotation.py   --table "$OTU_TABLE"   --gtdb "$GTDB_TAXONOMY"   --silva "$SILVA_TAXONOMY"   --outdir "$ECOLOGY_OUT/prepared"
~~~

The script records the original GTDB/SILVA assignments and confidence values, then adds filtering flags.

## Exclusion rules

Before bacterial-dominated ecology, exclude an OTU if any of the following apply:

- SILVA calls it chloroplast;
- SILVA calls it mitochondrion;
- SILVA domain is Eukaryota;
- GTDB does not assign the sequence to Bacteria or Archaea.

The original taxonomy remains in master_taxonomy.tsv; the filtering flag does not erase the evidence.

## Current validated checkpoints

~~~text
final direct OTUs             26,300
working filtered OTUs         26,054
final direct mapped reads     12,355,927
working filtered reads        12,209,120
~~~

## Important interpretation note

The working table is called bacterial-dominated because the primer pair strongly underrepresents Archaea. Do not interpret the low archaeal read fraction quantitatively.
