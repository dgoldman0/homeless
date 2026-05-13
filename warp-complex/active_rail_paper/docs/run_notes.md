# Run notes

The generated data in this bundle were produced from the included self-contained script:

```bash
python code/obstruction_screen.py
```

The run regenerated 15 branch/width rows across five variants and three transition-width factors.

Confirmed in the included reduced screen:

- The active-rail branch preserves packet clearance in the stressed case tested.
- No-catch branches fail the packet-norm screen by large margins.
- The late-catch throat-gated branch fails the packet-norm screen by large margins.
- The reduced radial null-bundle screen remains finite and shows no bundle folding in the tested branches.

Scope boundary:

- This is a reduced radial ADM diagnostic screen.
- It is not a constraint-quality initial-data solve.
- It is not a full off-axis global causal analysis.
- It is not a semiclassical/RSET calculation.
