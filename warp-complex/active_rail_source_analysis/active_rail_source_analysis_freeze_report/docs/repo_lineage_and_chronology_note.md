# Repo Lineage and Chronology Note

The chronology in the freeze report is reconstructed primarily from repository artifact lineage and report contents, not from a complete commit-history audit.

A connector commit search surfaced a later cleanup commit:

```text
2026-05-14 07:03:38 - Delete warp-complex/active_rail_source_analysis_post_report directory
```

but it did not expose enough complete commit metadata to order every precursor precisely by timestamp. The scientific lineage is clearer from the directory/report chain:

1. `quantum-effects-engineering/adiabatic_radial_process/`
   - explicit adiabatic setup/hold/reset protocol.
2. `quantum-effects-engineering/dynamic_throat_gate/` and flare-gated support branches.
   - dynamic throat/support engineering screens.
3. `catch_rematched_hybrid_flare_gated_transit/`
   - packet-centered catch/rematch active rail and B/R/N infrastructure role map.
4. `active_rail_paper/`
   - standalone active-rail paper and reduced obstruction screen.
5. post-paper source-analysis bundles from this conversation.
   - source ledger, angular jacket, q(s) decompression, baseline subtraction, freeze.

This bundle records the current synthesis rather than trying to rewrite exact Git history.
