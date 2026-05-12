# Multi-Zone Phase-Cycled Throat Evaluation

Reduced wormhole-only evaluation of a multi-zone phase-cycled throat-support plant.

This bundle contains the report, scripts, CSV outputs, extracted sweep summaries, model summary JSON, and manifest checksums. It deliberately excludes transport/catch/passenger-network layers.

Run:

```bash
python run_multizone_phase_cycled_throat_eval.py
python run_multizone_parameter_sweep.py
```

Primary report:

- `multizone_phase_cycled_throat_report.md`

Primary outputs:

- `multizone_case_summary.csv`
- `multizone_zone_qi_summary.csv`
- `multizone_parameter_sweep.csv`
- `multizone_parameter_sweep_extracts.json`
