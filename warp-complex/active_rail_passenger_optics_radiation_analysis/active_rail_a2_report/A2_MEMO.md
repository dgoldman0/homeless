# Phase A2 Optical/Radiation-Adjacent Screen Memo

## Executive read

Phase A2 was run to answer a narrow but important question: whether the large radial focusing spike seen in Phase A should be treated as a real viewport/radiation hazard or as a reduced one-dimensional artifact. The result favors the artifact interpretation. When the active-rail branch is tested with frozen-frame two-dimensional equatorial rays carrying impact parameter, the large Phase A radial focusing proxy collapses to much smaller values. The active branch still is not radiation-certified, because this test does not include full time-dependent 3D geodesics, RSET/semiclassical radiation, particle pickup, material transport, or source-side emission. But A2 does strengthen the larger architectural pattern: once the geometry is placed in the throat-supported, catch-rematched active-rail form, successive reduced probes tend to attack the comparison branches or reveal manageable diagnostics rather than force a redesign of the selected branch.

The surprising result is not that the model is “safe.” It is that the same frozen architecture continues to hold together under qualitatively different simplified tests. Across the project sequence, the design has been examined as a gated-shift geometry, a packet-service/catch-rematch system, a radial null-bundle/obstruction model, a local optical-energy screen, and now an off-axis impact-parameter artifact check. The selected branch has not required an unfreeze after these tests. That stability is meaningful, even though the large source-availability assumption and the reduced nature of the screens remain decisive caveats.

## What Phase A2 tested

Phase A produced a mixed result. Local photon energy gain in the protected active branch was mild, but the radial focusing proxy was extremely large. That created a serious ambiguity. In a purely radial screen, many neighboring rays can be artificially forced into the same one-dimensional channel. Such a setup can exaggerate focusing because it suppresses angular escape routes and impact-parameter structure. A real viewport does not receive only perfectly radial rays. It sees a cone of rays with angular momentum and off-axis structure.

Phase A2 therefore introduced a frozen-frame two-dimensional equatorial extension for the active branch. The test placed packet observers at three packet offsets and launched rays with impact angles from 5 to 85 degrees away from the radial direction. The Hamiltonian null condition was solved in the frozen metric, allowing rays to carry angular momentum through an approximate equatorial angular metric. The goal was not final safety certification; it was an artifact check on the Phase A radial spike.

The screen asked:

1. Do off-axis rays still show large photon energy gain?
2. Do off-axis rays still show extreme focusing?
3. Does the heuristic flux-risk proxy remain in the dangerous range?
4. Does the active-rail optical behavior look like a general viewport-killer, or did Phase A overstate the hazard by forcing rays into a radial channel?

## Numerical headline

The Phase A radial screen produced a very large focusing proxy:

| Quantity | Phase A radial result |
|---|---:|
| p99 focusing proxy | ~2,061 |
| max focusing proxy | ~79,682 |

Phase A2 reduced this sharply:

| Quantity | A2 all-angle result | A2 off-axis, theta >= 20 deg |
|---|---:|---:|
| energy-shift max | 0.830 | 0.830 |
| energy-shift p99 | 0.829 | 0.829 |
| focusing proxy max | 23.47 | 21.59 |
| focusing proxy p99 | 21.53 | 17.65 |
| risk proxy max | 3.71 | 3.71 |
| risk proxy p99 | 3.05 | 3.11 |

The important comparison is the focusing proxy. The p99 value drops by about two orders of magnitude, and the maximum drops by more than three orders of magnitude. The energy-shift result is also encouraging in this approximation: photons reaching the packet in A2 are redshifted rather than blueshifted, with energy-shift factor below 1.

## Interpretation

The Phase A radial focusing spike should not be treated as a general optical death sentence for the active-rail viewport. A2 suggests that the spike is largely a one-dimensional radial caustic artifact. Once rays carry impact parameter, the large radial compression is relieved.

This does not clear real transparent windows or raw viewports. It does support a narrower conclusion: there is no immediate classical optical evidence, at this reduced level, that the active branch produces unavoidable unshieldable photon amplification. The result keeps an honest sensor viewport branch alive.

The best current interpretation is:

> The active-rail geometry appears classically optically tame in local energy shift and does not preserve the Phase A radial focusing catastrophe once off-axis rays are allowed. Optical safety remains open but not presently defeated by the reduced screens.

## Why this matters for the active-rail architecture

The broader significance is architectural. The active rail is not being evaluated as a standalone warp bubble. It assigns the transport shift to the throat support envelope, while the passenger packet is serviced by the infrastructure. The selected branch’s doctrine is:

- the throat carries capacity, lapse/time-rate support, and transport shift;
- transport shift remains inside the throat-managed support profile;
- the passenger region is a packet/coupling object, not the source of the exotic geometry;
- the packet is caught/rematched before shift release and throat relaxation;
- release and reset are infrastructure operations, not passenger-vehicle propulsion events.

That division of labor has now survived several different reduced tests. The independent passenger-shift comparison failed lapse/shift balance checks. The no-catch and late-catch branches failed packet clearance. The active branch retained packet timelikeness in the reduced service screen. The Phase A optical screen did not show large local photon energy gain in the active branch. A2 then weakened the main remaining Phase A optical warning by showing that the radial focusing spike does not persist as a broad off-axis feature.

This is exactly the kind of behavior one would hope for if the architecture has identified the correct reduced branch. The design is not merely tuned to one metric diagnostic. It keeps preserving the same conceptual separation under different probes: support belongs to the plant, the packet remains the passenger object, and release timing matters.

## Literature placement

The active-rail result should be understood against known warp and wormhole hazards.

Alcubierre’s warp-drive construction introduced the ADM-style shift-based picture in which a local passenger region can be carried by surrounding spacetime distortion rather than by ordinary acceleration. That created the central attraction of warp geometries, but also moved the danger into the wall/shift structure.

Clark, Hiscock, and Larson numerically studied null geodesics in Alcubierre spacetime and found strong aberration, redshift/blueshift structure, and horizon-like regions for a superluminal bubble. Their work is directly relevant to visual viewport questions because it shows that what the crew sees is a null-geodesic mapping problem, not a simple external camera problem.

Finazzi, Liberati, and Barceló studied semiclassical instability in dynamical warp drives and found that an observer in a superluminal warp bubble would generically experience Hawking-like flux, while the RSET grows near the front wall. This is the reason the current active-rail optical tests cannot be considered final radiation safety results. Classical ray behavior can look manageable while semiclassical stress-energy still kills the geometry.

McMonigal, Lewis, and O’Byrne studied null and massive particles interacting with Alcubierre warp bubbles and found high-energy particle behavior and release hazards. That literature motivates future particle-pickup and release-burst screens for the active rail.

Everett and Roman’s Krasnikov-tube work is relevant because it shifts attention from a passenger-controlled moving bubble to prepared infrastructure. They noted that a bubble’s center cannot control the outer wall once causal separation appears, and they explored a prepared route that changes the control problem. The active rail follows the same broad infrastructure lesson, but localizes it into a throat-supported service architecture rather than a long physical tube.

Garattini and Zatrimaylov’s wormhole--warp-drive correspondence is especially relevant because it formalizes the interface between warp-drive structure and wormhole backgrounds. Their obstruction for localized Alcubierre bubbles in Morris--Thorne backgrounds helps explain why the active rail should not be framed as “a warp bubble passing through a throat.” The active rail instead moves the shift role into the throat support envelope and treats the passenger as a packet served by the plant.

Bobrick and Martire’s ADM framing is also important because it encourages separating lapse, shift, spatial geometry, capacity, and physical conditions into design handles. The active rail uses that separability as engineering doctrine: capacity, lapse/time-rate support, and shift are not passenger-vehicle features; they are infrastructure channels assigned to the throat plant.

## What is genuinely surprising

The surprising part is the stability of the selected branch. Under source availability, the active rail has behaved like a coherent reduced architecture rather than a single lucky ansatz.

A less robust design would likely have required repeated unfreezing: changing the release order, moving the shift, changing the passenger role, altering the support envelope, or abandoning the packet logic after new diagnostics. Instead, the same active-rail branch continues to answer the tests with the same division of labor. The failures remain informative rather than destructive: independent shift teaches that shift belongs inside support; no-catch and late-catch teach that catch must precede release; the Phase A radial focusing spike teaches that one-dimensional optical channels exaggerate hazards; A2 teaches that impact-parameter structure relieves the spike.

This is not proof of physical viability. It is stronger than a one-off numerical success. It is a pattern of architectural coherence.

## Safety implications

A2 weakens the case against honest visual viewports. It does not certify them.

A practical passenger-rated design should still use sensor viewports rather than transparent panes. The viewport should support:

- raw sensor mode;
- human-corrected spectral mode;
- diagnostic overlay mode;
- no-ray masking;
- caustic/focusing warnings;
- automatic shuttering or display suppression during unvalidated phases;
- separate radiation monitors tied to the packet and support edge.

The A2 result suggests that classical optical safety may be a manageable display/filtering problem rather than an immediate hard stop. The next optical rendering stage should use the A2 ray maps to produce a 2.5D viewport atlas and animation, with energy shift, focusing, no-ray masks, and visual reconstruction derived from the same data.

## What A2 does not settle

A2 remains simplified in several ways:

1. It is frozen-frame rather than fully time-dependent.
2. It uses a 2D equatorial approximation rather than full 3D geodesics.
3. It does not compute RSET or semiclassical radiation.
4. It does not include source-generated radiation from the support plant.
5. It does not model charged particles, dust, or plasma.
6. It does not run material transport through a shield/cabin model.
7. It does not compute absorbed dose or dose equivalent for passengers.

These are not minor details. They are the next places where the design could fail.

## Recommended next work

The next technical steps should be staged:

### Phase B: 2.5D viewport atlas

Use A2-style impact-parameter rays to build forward and side viewport frames during carry, catch, fade, and relaxation. Render:

- raw sensor image;
- energy-shift overlay;
- focusing/risk overlay;
- no-ray mask;
- corrected human-view mode.

This will show whether the optical behavior is localized into narrow bands or spread across the viewport.

### Phase C: time-dependent off-axis geodesics

Replace frozen frames with geodesic propagation through the time-dependent active-rail service sequence. This tests whether catch/fade dynamics create transient bursts that the frozen frame misses.

### Phase D: particle pickup and release

Trace massive and null test particles around the support envelope to check for snowplow, time-locking, and release-burst analogs.

### Phase E: semiclassical/RSET screen

Build a 1+1 radial conformal-field proxy first. If that is not pathological, consider a heavier semiclassical approximation. This is the most important radiation gate after classical optics.

### Phase F: material dose model

Feed incident spectra and particles into a shielding/cabin transport model, eventually with Geant4 or an equivalent particle-transport tool.

## Bottom line

Phase A2 does not prove the active rail safe. It does make the active rail harder to dismiss. The strongest conclusion is that the selected active-rail branch continues to behave like the right reduced architecture to test. The optical/radiation-adjacent probes do not currently force an unfreeze. They instead refine the next hazards to test: time-dependent off-axis behavior, particle pickup, RSET, and material dose.
