# Active Rail 2.5D Viewport Atlas

This is a physics-informed visual atlas, not a full time-dependent 3D geodesic solver.

It uses the Phase A2 lesson: once rays carry impact parameter, the Phase A radial focusing spike does not persist as a broad off-axis viewport hazard. The renderer therefore keeps photon energy shift redshift-dominant, allows focusing in the low-tens range, and renders no-ray regions as low-confidence darkness rather than material walls.

Modes:
- Raw sensor: preserves redshift and dimming.
- Human-corrected: same ray map, color/brightness corrected for readability.
- Diagnostic: orange/red = focusing, cyan = no-ray/low confidence, blue = redshift.

Forward view emphasizes axial remapping around the rail/throat direction. Side view emphasizes laminar shearing across the support/shift envelope.

Safety note: this keeps honest viewports visually plausible, but it is not radiation certification. The next gates remain time-dependent off-axis geodesics, particle pickup/release, RSET/semiclassical radiation, and material dose modeling.
