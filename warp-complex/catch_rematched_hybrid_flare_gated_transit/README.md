# Catch-Rematched Hybrid Flare-Gated Transit Bundle

This bundle contains a GitHub-flavored Markdown report evaluating how the Catch-rematched throat-loaded transit design changes the engineering complexity of the Hybrid Flare-Gated Reduced Reference Model v1.0.

## Main file

- `REPORT.md` — main report with GitHub-style math fences, results, citations, and design conclusions.

## Reproducibility

The code used for the reduced evaluations is in `code/`.

The generated results are in `data/`.

Compact derived tables used by the report are in `derived/`.

Rebuild the compact derived tables from the raw JSON:

```bash
python code/build_report_tables.py
```

## Folder layout

```text
code/       evaluation and table-generation scripts
data/       raw JSON outputs and markdown summaries from the evaluation passes
derived/    compact report metrics generated from data/*.json
sources/    repository source notes and literature references
```

## Scope

The report assumes source availability and evaluates engineering structure under that premise. It is a reduced screen rather than a full source construction, quantum-admissibility proof, or `3+1` constraint-quality initial-data solve.
