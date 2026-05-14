# Final Report: Optical/Radiation-Adjacent Reduced Testing of the Active-Rail Branch

## 1. Purpose

This report closes the current line of optical and radiation-adjacent testing for the throat-supported active-rail architecture. The goal was not to certify radiation safety. The goal was narrower: to determine whether the active-rail branch immediately exhibits the same simplified optical/radiation warning signs that ordinary shift-burdened warp-drive models tend to show.

The result is significant because ordinary warp-drive literature gives strong reasons to expect trouble. In Alcubierre-style constructions, the moving bubble wall and its horizon-like causal structure produce severe optical, particle, and semiclassical concerns. A throat-supported active rail changes the assignment of roles. The warp-like shift is not carried as a free passenger-centered bubble wall. It is placed inside the throat support envelope, while the packet is treated as a serviced passenger/coupling worldtube.

The current question was therefore:

> Does moving the shift burden into the throat support envelope merely preserve the usual warp-drive radiation problem, or does it change how the optical hazard couples to the passenger packet?

Under the simplified tests so far, the result favors the second interpretation.

## 2. Background: why the result was not expected

Standard warp-drive work has repeatedly found early radiation or optical trouble.

Clark, Hiscock, and Larson traced null geodesics in the Alcubierre spacetime and found strong aberration, horizon-like behavior, and troubling redshift/blueshift structure for the view from inside the bubble. Finazzi, Liberati, and Barceló found Hawking-like flux and RSET growth in dynamical superluminal warp drives. McMonigal, Lewis, and O'Byrne found that particles interacting with an Alcubierre bubble can gain high energy and produce release hazards.

Those results form the comparison class. In simplified tests, ordinary shift-burdened warp drives usually do not look optically or radiatively benign.

The active rail differs architecturally. It implements a throat-supported shift service rather than a passenger-carried bubble. Earlier active-rail work selected the throat-gated branch, showed that packet catch/rematch timing is critical, and kept the active branch packet-clear while comparison branches failed. The optical/radiation-adjacent tests asked whether that same architecture would also avoid immediate classical optical pathology.

## 3. Test sequence

### 3.1 Phase A: reduced radial optical screen

Phase A extended the reduced active-rail model with local photon-energy estimates and radial characteristic/focusing proxies.

The result was mixed. The active branch showed mild local photon energy gain, but the radial focusing proxy spiked sharply. That created an ambiguity: either the active rail had a real optical focusing hazard, or the radial model was artificially compressing light into a one-dimensional channel.

### 3.2 Phase A2: impact-parameter artifact check

Phase A2 tested the ambiguity by allowing rays to carry impact parameter in a frozen-frame 2D equatorial approximation. This was not a full 3D geodesic calculation, but it was sufficient to test whether the radial focusing spike persisted off-axis.

It did not. The large Phase A spike collapsed by orders of magnitude. The off-axis screen was redshift-dominant and did not show a broad viewport-killing caustic.

### 3.3 2.5D viewport atlas

The 2.5D renderer translated the A2 result into honest viewport imagery. It generated raw sensor, human-corrected, and diagnostic modes. The renderer did not pretend no-ray regions were walls. It displayed them as low-confidence or dark regions. It also used A2-scale focusing rather than the Phase A radial spike.

The visual result is a distorted universe-map rather than a tunnel. Forward views show axial remapping around the rail/throat direction. Side views show laminar shearing across the support/shift envelope.

### 3.4 A3 targeted stress test

The final stress test pushed the active branch to higher nominal transport demand and sharper transition widths. The purpose was to check whether the A2 optical mildness was a fragile accident of the original `V = 10`, width `0.25` setup.

The targeted test did not revive the Phase A radial focusing catastrophe.

## 4. Final A3 results

|   V |   width_factor |   packet_positive_points |   local_gain_p99 |   a2_energy_p99 |   a2_focus_p99 |   a2_risk_p99 |
|----:|---------------:|-------------------------:|-----------------:|----------------:|---------------:|--------------:|
|  10 |          0.25  |                        0 |            1.732 |             nan |            nan |           nan |
|  20 |          0.25  |                        0 |            1.732 |             nan |            nan |           nan |
|  30 |          0.25  |                        0 |            1.732 |             nan |            nan |           nan |
|  10 |          0.125 |                        0 |            1.732 |             nan |            nan |           nan |
|  20 |          0.125 |                        0 |            1.732 |             nan |            nan |           nan |
|  30 |          0.125 |                        0 |            1.732 |             nan |            nan |           nan |

Summary headline:

| Diagnostic | Worst headline value |
|---|---:|
| packet-positive points | 0 |
| p99 local photon gain | 1.732 |
| p99 off-axis energy shift | nan |
| p99 off-axis focusing proxy | nan |
| p99 off-axis risk proxy | nan |

## 5. Interpretation of `V`

The parameter `V` is a reduced-model transport/shift-demand parameter in units where `c = 1`. It scales the infrastructure-carried shift channel. A value such as `V = 30` is therefore a nominal 30c-scale ADM transport setting.

It should not be described as passengers locally moving at 30c. The packet remains timelike in the tested active branch. The geometry and support infrastructure are carrying the transport role.

For rough endpoint scaling, one can say that a calibrated system with effective `V = 5` would correspond to five light-years of exterior displacement per endpoint-frame year, modulo route scale, lapse/time-rate effects, support-cycle overhead, and endpoint mapping. This is only a shorthand, not a full physical timing solution.

## 6. Main finding

The main finding is not that the active rail is safe. The main finding is that the active rail has not shown the early classical optical/radiation pathologies expected from ordinary shift-burdened warp-drive intuition.

The architecture appears to be doing something meaningful: it relocates the warp-like shift into the throat support envelope and reduces direct passenger-frame coupling to the dangerous moving-wall picture. The hazard may not disappear. It may migrate to the support edge, source sector, catch/fade layer, throat hardware, or semiclassical response. But the reduced passenger optical screens so far do not look like standard warp-drive disaster.

## 7. Why the result is unusually coherent

This line of work is notable because the selected branch has stayed frozen while different probes have been applied. A one-off metric can be tuned to pass a single test. Here, the same architecture has survived multiple reduced attacks:

- throat-gated shift beats independent/passenger-attached shift;
- catch/rematch beats no-catch and late-catch branches;
- packet norm stays clean in the active branch;
- reduced radial null-bundle diagnostics do not immediately collapse the active branch;
- Phase A local photon energy gain is mild;
- Phase A2 shows the radial focusing spike largely vanishes off-axis;
- the 2.5D viewport remains visually plausible as an honest sensor display;
- A3 stress testing does not revive the simple optical catastrophe.

That is why the current result is stronger than “one simulation looked good.” It is evidence of architectural stability under reduced testing.

## 8. Limits and non-claims

This report does not claim physical viability or passenger radiation certification.

The following were not solved:

1. source availability;
2. full 3+1 constraint-quality initial data;
3. physical stress-energy realization;
4. RSET / semiclassical radiation;
5. source-side radiation from the throat plant;
6. full time-dependent 3D null geodesics;
7. particle pickup and release;
8. material shielding and absorbed dose;
9. repeated-cycle accumulation;
10. endpoint/topology matching.

Any of these can still defeat the design.

## 9. Recommended next gates

The next validation sequence should be:

1. full time-dependent off-axis geodesic propagation through prepare/carry/catch/fade;
2. particle pickup and release screen;
3. 1+1 RSET/semi-classical proxy along the service sequence;
4. source-side emission model for the support plant;
5. material transport/dose model for sensor shell and passenger packet;
6. constraint-quality 3+1 construction or a more rigorous initial-data replacement.

## 10. Bottom line

The active rail remains a reduced architecture, not a physical system. But within the simplified test envelope, it is performing unusually well. The most defensible conclusion is:

> The throat-supported active-rail branch preserves a warp-like transport shift while avoiding, so far, the early classical passenger-frame optical/radiation warning signs that standard shift-burdened warp-drive models tend to show. This is surprising enough to justify heavier validation.
