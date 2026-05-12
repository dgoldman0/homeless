# Compensated Flare-Gated Radial Stretch

This bundle screens positive-compensation mechanisms for the flare-gated radial-stretch protocol.

The tested sequence is:

```math
B	ext{-setup} ightarrow R	ext{-open} ightarrow 	ext{quiet hold} ightarrow R	ext{-close} ightarrow 	ext{compensation} ightarrow B	ext{-reset}.
```

Primary finding: explicit post-closure source compensation carries the core/support repayment ledger cleanly; shoulder `R` contributes shoulder-buffer compensation; lapse `N` supplies timing and matching co-control.

Files:

- `MEMO_compensation_branch_screen.md`: design memo and result interpretation.
- `run_compensation_branch_screen.py`: reproducible reduced screen.
- `compensation_case_summary.csv`: full case table.
- `compensation_compact_ranking.csv`: compact comparison table.
- `compensation_class_summary.csv`: actuator-family summary.
- `extracts.json`: selected machine-readable results.
- `manifest.json`: checksums.
