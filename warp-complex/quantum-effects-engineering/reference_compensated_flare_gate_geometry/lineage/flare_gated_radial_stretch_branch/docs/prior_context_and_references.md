# Prior Context and References

Relevant prior repository materials:

1. Engineering framework PDF/source:
   - `warp-complex/quantum-effects-engineering/wormhole_support_engineering_framework/pdf/wormhole_support_engineering_framework.pdf`
   - `warp-complex/quantum-effects-engineering/wormhole_support_engineering_framework/latex/main.tex`

2. Earlier adiabatic radial-stretch protocol:
   - `warp-complex/quantum-effects-engineering/adiabatic_radial_process/adiabatic_radial_process_memo.md`
   - `warp-complex/quantum-effects-engineering/adiabatic_radial_process/scripts/run_adiabatic_radial_protocol_eval.py`

3. Prior result:
   - `B(l,t)` adiabatic stretching makes peak dynamic costs scale down with ramp time and supplies a clean radial proper-length support-dilution actuator.
   - The fixed access profile `R(l)=sqrt(1+l^2)` keeps the areal flare active throughout setup, hold, and reset.

4. Current branch result:
   - `R(l,t)` participates as the flare/access-state actuator.
   - `B(l,t)` remains the radial support-dilution actuator.
   - The successful ordering is `B` prestretch, `R` flare-open, quiet hold, `R` flare-close, `B` reset.
