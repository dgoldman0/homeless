# HSC-1 Cross-Spectral Sensor Roadmap

**Document date:** May 3, 2026  
**Product concept:** A single-chip, one-lens, snapshot cross-spectral imaging module with a stacked visible-color anchor pixel inside a multispectral macrocell, producing a strong human-viewable RGB image and calibrated visible/NIR spectral outputs from the same exposure.

---

## 1. Executive summary

HSC-1 can be advanced meaningfully before any wafer run, camera module, optical bench, or laboratory test setup exists. The pure desk-work program can define the product, model the physics, select spectral bands, simulate macrocells, test reconstruction algorithms against public hyperspectral data, prepare the manufacturing inquiry package, map adjacent products, and establish the prototype test matrix.

The practical desk-work ceiling is **analytical TRL 3**: a proof-of-concept supported by modeling, simulation, prior art, requirements, and vendor-facing specifications. Physical TRL 4 begins once components or breadboards are built and measured in a lab. NASA describes TRLs as a nine-level maturity scale, with TRL 1 as the lowest and TRL 9 as the highest; it places active research/design and proof-of-concept work at TRL 3 and component/breadboard testing at TRL 4. [NASA — Technology Readiness Levels](https://www.nasa.gov/directorates/somd/space-communications-navigation-program/technology-readiness-levels/)

The goal of desk work is to reach this position:

> We know what to build, why it matters, what physics supports it, what the selected bands are, how the macrocell samples the scene, how raw data becomes RGB and spectral outputs, who can fabricate it, how it will be tested, and what results define success.

---

## 2. Roadmap structure

The roadmap has two tracks:

1. **Desk-work track:** concept to analytical proof-of-concept, with no build/test resources.
2. **Build/test track:** test chip, module, pilot system, field validation, production readiness.

The desk-work track is the immediate priority. It creates the package that lets a technical founder, investor, strategic partner, foundry, filter vendor, optics vendor, or government-grant reviewer evaluate the project without hand-waving.

---

## 3. TRL interpretation for HSC-1

| TRL | General meaning | HSC-1 interpretation | Desk work? |
|---:|---|---|---:|
| **1** | Basic principles observed and reported | Silicon absorption physics, stacked-pixel precedent, multispectral filter-array precedent, application needs collected | Yes |
| **2** | Technology concept and application formulated | HSC-1 architecture defined: stacked RGB anchor + surrounding spectral pixels + computational reconstruction | Yes |
| **3** | Analytical / experimental proof of concept | Radiometric model, macrocell simulation, synthetic reconstruction, IP map, vendor-feasible process concept | Yes, analytically |
| **4** | Component/breadboard validated in laboratory | Test pixels, filter coupons, surrogate optical bench, or first test chip measured | Requires build/test |
| **5** | Breadboard validated in relevant environment | Sensor/module tested under realistic illumination, optics, temperature, motion, and target scenes | Requires build/test |
| **6** | Prototype demonstrated in relevant environment | Integrated camera module with firmware, calibration, and application software demonstrated with target users | Requires build/test |
| **7** | Prototype demonstrated in operational environment | Field pilots in agriculture, inspection, robotics, conservation, or other target verticals | Requires build/test |
| **8** | System complete and qualified | Pre-production module qualified for reliability, calibration, supply chain, and manufacturing test flow | Requires build/test |
| **9** | System proven in operation | Production HSC-1 modules deployed by customers with support and yield data | Requires production |

**Desk-work ceiling:** HSC-1 can reach a strong analytical TRL 3. The first silicon, optical bench, or calibrated surrogate hardware moves the project into TRL 4 activity.

---

## 4. Pure desk-work scope

Pure desk work includes:

- requirements writing,
- literature review,
- source-verified competitive analysis,
- patent landscape and FTO preparation,
- silicon absorption and photon-budget modeling,
- macrocell sampling simulations,
- spectral band selection,
- use-case economics,
- public hyperspectral-dataset experiments,
- algorithm prototyping,
- calibration workflow design,
- manufacturing route planning,
- foundry/vendor inquiry package,
- prototype test matrix,
- investor/partner technical brief.

Pure desk work uses:

- spreadsheets,
- Python/Matlab/Julia simulations,
- optical and radiometric equations,
- public spectral datasets,
- public product specifications,
- public papers and patents,
- phone/email conversations with vendors,
- written design reviews.

Physical validation begins when the team purchases, builds, fabricates, modifies, or measures physical hardware for this project.

---

## 5. Desk-work roadmap

### D0 — Mission framing and product thesis

**TRL position:** pre-TRL / TRL 1 entry  
**Timebox:** 1–2 weeks  
**Main question:** What exact product is being created, and for whom?

**Work items**

- Define the product in one sentence.
- Define the target module form factor: bare sensor, board camera, enclosed module, or full instrument.
- Choose the first three application verticals.
- Define the “must be true” claims:
  - single exposure,
  - one optical path,
  - high-quality visible RGB output,
  - calibrated visible/NIR spectral outputs,
  - compact module,
  - application-ready software.
- Establish target sensor size, likely first format, and approximate pixel pitch range.
- Define the primary buyer: OEM, machine-vision integrator, research lab, agriculture platform, robotics company, conservation/forensics lab, or medical/life-science instrumentation company.

**Deliverables**

- Product one-pager.
- Target-user matrix.
- First use-case ranking.
- Initial price/margin assumptions.
- List of customer discovery questions.

**Exit criteria**

- A technically specific product statement.
- Three ranked applications.
- One target launch form factor.
- A short list of buyer types and pilot customers.

---

### D1 — Physics and precedent evidence pack

**TRL position:** TRL 1  
**Timebox:** 2–3 weeks  
**Main question:** Which proven physical effects and adjacent commercial designs support the architecture?

**Work items**

- Map silicon absorption versus wavelength from visible through NIR.
- Summarize stacked-color-pixel precedent.
- Summarize snapshot multispectral filter-array precedent.
- Summarize UV/violet package implications.
- Summarize NIR crosstalk and deep-trench-isolation implications.
- Summarize filter-stack and microlens integration precedent.
- Summarize adjacent commercial designs:
  - Sony IMX454-style multispectral sensor,
  - imec/XIMEA snapshot spectral cameras,
  - Canon RGB-NIR sensors,
  - Spectricity S1,
  - SILIOS CMS,
  - JAI Fusion prism cameras,
  - Sony stacked RGB/NIR ToF research.

**Evidence anchors**

- Sony’s multispectral image-sensor technology uses per-pixel multispectral filters and software to capture 41 wavelengths from 450 nm to 850 nm in one shot from 8 filter patterns. [Sony Semiconductor — Multispectral Image Sensor Technology](https://www.sony-semicon.com/en/technology/industry/multispectral.html)
- Imec has demonstrated integration of standard RGB filters, NIR-cut filters, NIR narrow band-pass filters, and on-chip microlenses down to small pixels around 5 µm. [imec — Snapshot RGB-NIR Multispectral Image Sensor](https://www.imec-int.com/en/articles/imec-introduces-new-snapshot-multispectral-image-sensor-that-combines-color-and-near-infrared-imaging)
- Silicon’s useful imaging response spans visible into near-IR, with absorption falling near the silicon bandgap around 1100 nm. [PVEducation — Optical Properties of Silicon](https://www.pveducation.org/pvcdrom/materials/optical-properties-of-silicon)
- NIR-enhanced CMOS work uses optical path engineering and deep trench isolation to improve 940 nm performance and reduce neighbor-pixel crosstalk. [Applied Optics — Near-IR absorption enhancement and crosstalk reduction](https://opg.optica.org/ao/abstract.cfm?uri=ao-61-22-6577)
- UV sensing changes packaging and microlens materials; Sony’s UV image-sensor technology uses quartz cover glass and UV-transmissive chip-on lens materials. [Sony Semiconductor — UV Image Sensor Technology](https://www.sony-semicon.com/en/technology/industry/uv.html)

**Deliverables**

- Physics memo.
- Adjacent-design comparison.
- Technology-prior map.
- Table of “proven,” “modeled,” and “to be measured” assumptions.

**Exit criteria**

- Every core claim has at least one source.
- All source claims are traceable to primary or highly credible sources.
- The architecture is grounded in known physics and known manufacturing categories.

---

### D2 — Requirements and success metrics

**TRL position:** TRL 2  
**Timebox:** 2–4 weeks  
**Main question:** What must HSC-1 do in measurable terms?

Requirements should be written in a structured way. ISO/IEC/IEEE 29148 provides guidance for requirements engineering and defines processes and information items for requirements-related activities. [IEEE — ISO/IEC/IEEE 29148-2018](https://standards.ieee.org/ieee/29148/6937/)

**Work items**

- Define product-level requirements:
  - spectral bands,
  - RGB output quality,
  - spatial resolution,
  - frame rate,
  - exposure range,
  - dynamic range,
  - raw bit depth,
  - calibration outputs,
  - operating temperature,
  - interface,
  - module size,
  - lens mount or fixed lens,
  - power budget,
  - software deliverables.
- Define sensor-level requirements:
  - pixel pitch target,
  - sensor format,
  - macrocell size,
  - stacked anchor density,
  - clear/panchromatic pixel density,
  - NIR pixel density,
  - read-noise target,
  - full-well target,
  - QE target by band,
  - crosstalk target by band.
- Define software-level requirements:
  - raw unpacking,
  - dark correction,
  - flat-field correction,
  - spectral response correction,
  - visible RGB reconstruction,
  - spectral-band cube reconstruction,
  - uncertainty map,
  - SDK/API.
- Define calibration requirements:
  - dark frames,
  - flat-field source,
  - spectral lamp/monochromator plan,
  - reflectance target plan,
  - module-specific calibration file.

**Deliverables**

- Product Requirements Document.
- Sensor Requirements Document.
- Module Requirements Document.
- Software Requirements Document.
- Calibration Requirements Document.
- Requirements traceability matrix.

**Exit criteria**

- Each requirement is measurable.
- Each requirement maps to a test method.
- Requirements are divided into target, threshold, and stretch values.
- The build team could use the requirements as the starting point for a real specification.

---

### D3 — Spectral band and radiometric model

**TRL position:** TRL 2 to analytical TRL 3  
**Timebox:** 3–5 weeks  
**Main question:** Do the selected bands collect enough photons to be useful?

**Baseline band set**

| Channel | Role |
|---|---|
| 405 nm violet | surface features, fluorescence-adjacent excitation/response workflows, cultural heritage, material contrast |
| 450 nm blue | visible reconstruction and pigment/material separation |
| 530–550 nm green | visible luminance, color anchor, vegetation/material features |
| 610–660 nm red/deep red | visible reconstruction, tissue/material/vegetation contrast |
| 700–740 nm red edge | vegetation and material-transition features |
| 810–850 nm NIR | vegetation, tissue, material contrast, active illumination compatibility |
| 940 nm NIR | active illumination, low-visible-light machine vision, material contrast |
| clear/panchromatic | high-resolution luminance and exposure robustness |
| stacked RGB anchor | local full-color visible reference |

**Work items**

- Estimate photon flux by application scene.
- Model spectral irradiance:
  - daylight,
  - LED illumination,
  - halogen/tungsten,
  - NIR LED,
  - fluorescence workflows if relevant.
- Model lens throughput, filter transmission, microlens efficiency, QE, full well, read noise, dark current, and shot noise.
- Calculate SNR by band and exposure.
- Identify active-illumination needs.
- Evaluate band widths and center wavelengths.
- Test alternative band packs for each application vertical.

**Deliverables**

- Radiometric spreadsheet/model.
- Band-selection memo.
- Assumption register.
- SNR-by-band tables.
- Exposure and illumination envelope.
- Recommendation for first product band set.

**Exit criteria**

- Each band has a stated reason to exist.
- Each band has an estimated SNR under target lighting.
- Bands with weak photon budgets have a defined illumination or exposure strategy.
- The spectral plan is tied to applications, not symmetry.

---

### D4 — Macrocell and reconstruction simulation

**TRL position:** analytical TRL 3  
**Timebox:** 4–8 weeks  
**Main question:** Can the sensor layout reconstruct useful RGB and spectral outputs?

**Candidate macrocell families**

```text
3×3 high-density concept
NIR850   Pan/Clear   NIR940
Violet   X3 RGB      RedEdge
Blue     Green/Pan   DeepRed
```

```text
4×4 higher-reconstruction concept
Pan/G    NIR850   Pan/G    RedEdge
Blue     X3 RGB   Clear    NIR940
Violet   Pan/G    DeepRed  NIR730
Clear    NIR850   Pan/G    Violet
```

**Work items**

- Simulate 3×3, 4×4, and 5×5 macrocells.
- Include stacked RGB anchor response curves.
- Include clear/panchromatic pixels for visible spatial detail.
- Include band-pass filter transmission curves.
- Include optical blur and sensor MTF assumptions.
- Include crosstalk models for deep red and NIR.
- Run synthetic captures using hyperspectral datasets.
- Reconstruct:
  - human-viewable RGB,
  - individual spectral bands,
  - application indices,
  - uncertainty maps.
- Compare against:
  - ordinary Bayer RGB,
  - RGB-NIR mosaic,
  - conventional snapshot MSI mosaic,
  - lower-resolution spectral cube with pan sharpening.

**Useful public datasets**

- Columbia CAVE Multispectral Image Database: visible 400–700 nm spectral scenes. [Columbia CAVE — Multispectral Images Database](https://cave.cs.columbia.edu/repository/Multispectral)
- Harvard Real-World Hyperspectral Images Database: indoor/outdoor scenes with 31 bands centered at 420–720 nm. [Harvard — Hyperspectral Images Database](https://vision.seas.harvard.edu/hyperspec/download.html)
- ICVL Hyperspectral Dataset: high-resolution natural hyperspectral imagery. [Yale HSI Open Ecosystem — ICVL Dataset](https://hsi.yale.edu/resource/675)
- Camera Spectral Sensitivity Database: measured spectral sensitivity functions for 28 cameras, useful for RGB-rendering comparisons. [Zenodo — Camera Spectral Sensitivity Database](https://zenodo.org/records/3245883)

**Deliverables**

- Macrocell simulation code.
- Synthetic raw generator.
- Reconstruction algorithm prototype.
- RGB quality report.
- Spectral-band quality report.
- Application-index quality report.
- Recommended macrocell layout.

**Exit criteria**

- At least two macrocell candidates are compared quantitatively.
- The chosen macrocell supports a strong visible image and useful spectral outputs.
- Reconstruction artifacts are characterized.
- Synthetic outputs can be shown to technical reviewers and target users.

---

### D5 — Manufacturing path and vendor package

**TRL position:** analytical TRL 3  
**Timebox:** 4–6 weeks  
**Main question:** Which manufacturing route can create HSC-1?

**Work items**

- Define the preferred process stack:
  - BSI CMOS image sensor,
  - deep trench isolation,
  - vertical stacked visible anchor pixel,
  - multispectral filter array,
  - microlens layer,
  - cover glass/window,
  - package,
  - test and calibration flow.
- Define the first die size and sensor format.
- Define the target pixel pitch.
- Define test structures:
  - standalone stacked visible pixels,
  - standalone spectral filter pixels,
  - NIR crosstalk structures,
  - DTI split lots if available,
  - dark-current structures,
  - filter-only coupons.
- Prepare an inquiry package for:
  - CIS foundries,
  - specialty multispectral filter vendors,
  - wafer-level optics vendors,
  - camera-module integrators,
  - calibration-equipment vendors,
  - lens vendors.

**Vendor questions**

- Can the foundry support a custom photodiode stack?
- Can DTI depth and geometry be tuned for NIR performance?
- Can the filter vendor pattern the required passbands at pixel scale?
- What passband shift occurs with chief-ray angle?
- What minimum pixel pitch supports the filter stack?
- What wafer-level microlens process is compatible?
- What package window supports violet/near-UV and NIR?
- What design rules affect the stacked center pixel?
- What test structures are recommended?
- What are MPW, engineering wafer, and production wafer options?
- What are expected NRE, mask, wafer, packaging, test, and calibration costs?

**Deliverables**

- Manufacturing concept memo.
- Test-chip proposal.
- Vendor RFI/RFQ package.
- Cost model.
- NRE model.
- Foundry/vendor shortlist.
- Package and lens assumptions.

**Exit criteria**

- The project has at least one plausible manufacturing route.
- Vendor questions are specific enough to produce actionable responses.
- The prototype run can be budgeted and scheduled.
- The build plan includes test structures, not only a full sensor.

---

### D6 — IP, positioning, and funding package

**TRL position:** analytical TRL 3 package complete  
**Timebox:** 4–8 weeks  
**Main question:** Is HSC-1 positioned as a protectable, fundable, build-ready product?

**Work items**

- Build an IP landscape:
  - Foveon/stacked visible color,
  - multispectral filter arrays,
  - stacked photodetectors,
  - RGB-NIR sensor architectures,
  - organic/stacked visible-NIR designs,
  - spectral reconstruction algorithms,
  - calibration workflows.
- Prepare provisional patent filing concepts.
- Prepare freedom-to-operate review package for counsel.
- Build investor/partner deck.
- Build grant proposal package if appropriate.
- Identify strategic partners:
  - industrial camera OEMs,
  - machine vision integrators,
  - agricultural imaging companies,
  - robotics platforms,
  - life-science instrumentation companies,
  - conservation/forensic imaging groups.

**Relevant precedent**

- Sigma’s full-frame Foveon effort illustrates the importance of mass-production feasibility in stacked-color sensors. Sigma stated in 2021 that the sensor then under development could not go into mass production due to a critical flaw, leading Sigma to halt that path and restart. [Sigma — Sensor development update](https://www.sigma-global.com/en/news/2021/02/19/12739/)
- Sony has demonstrated a stacked sensor concept using organic photoconductive-film RGB pixels over silicon NIR time-of-flight pixels, showing that visible/NIR stacking is an active architecture direction in advanced image-sensor research. [Sony — Organic RGB over NIR ToF stacked sensor](https://www.sony.com/en/SonyInfo/technology/publications/a-color-image-sensor-using-1.0-um-organic-photoconductive-film-pixels-stacked-on-4.0-um-si-pixels-for-near-infrared-time-of-flight-depth/)
- Patent literature includes multispectral imaging sensors with superpixels, spectral filters, and vertically stacked photodetectors. [Google Patents — Multispectral imaging sensors and systems](https://patents.google.com/patent/WO2018217770A2/en)

**Deliverables**

- IP landscape memo.
- Provisional patent claim themes.
- FTO counsel packet.
- Partner/investor technical brief.
- Budget and schedule for first physical prototype.
- Full desk-work data room.

**Exit criteria**

- The project is ready for counsel review.
- The technical package is ready for founders, investors, partners, and vendors.
- The next spend is tied to a specific test-chip/module plan.
- The desk-work evidence supports analytical TRL 3.

---

## 6. The desk-work data room

At the end of the desk-work track, the project should have a complete data room:

```text
01_Product
  Product thesis
  Target customer matrix
  Use-case economics
  Competitive landscape

02_Requirements
  Product requirements
  Sensor requirements
  Module requirements
  Software requirements
  Calibration requirements
  Requirements traceability matrix

03_Physics
  Silicon absorption model
  Radiometric model
  NIR crosstalk model
  UV/violet package notes
  Lens and illumination assumptions

04_Architecture
  Macrocell candidates
  Selected macrocell
  Pixel-function map
  Readout assumptions
  Raw data format

05_Simulation
  Synthetic raw generator
  Public dataset scripts
  Reconstruction algorithm
  RGB quality metrics
  Spectral quality metrics
  Sample outputs

06_Manufacturing
  Process stack concept
  Test structures
  Foundry RFI
  Filter-vendor RFI
  Optics-vendor RFI
  Package/test/calibration flow
  Cost and NRE model

07_IP
  Prior-art map
  Patent search notes
  Provisional filing themes
  Counsel packet

08_Build_Plan
  Test-chip plan
  Bench plan
  Calibration plan
  Prototype budget
  Prototype schedule
  Go/no-go gates
```

This package is the main output before any physical build or test resources are available.

---

## 7. Build/test roadmap after the desk-work package

### B1 — Test structures and filter coupons

**TRL target:** TRL 4 entry  
**Goal:** Validate the highest-risk components separately.

**Physical artifacts**

- stacked visible anchor test pixels,
- spectral filter coupons,
- NIR crosstalk structures,
- DTI split structures,
- dark-current and PRNU structures,
- microlens/filter alignment coupons.

**Measurements**

- spectral response,
- QE by wavelength,
- crosstalk by wavelength,
- filter passband center and FWHM,
- passband shift versus incident angle,
- dark current versus temperature,
- read noise,
- full well,
- defect maps.

**Exit criteria**

- Measured results support moving from test structures to a small imageable array.
- The highest-risk parameters have measured distributions.

---

### B2 — Small imageable test chip

**TRL target:** TRL 4  
**Goal:** Demonstrate that the macrocell forms images and supports reconstruction.

**Physical artifacts**

- small-format sensor array,
- evaluation board,
- raw capture software,
- first calibration flow.

**Measurements**

- raw capture by pixel type,
- visible reconstruction,
- spectral reconstruction,
- crosstalk,
- MTF,
- flat-field response,
- temperature behavior,
- calibration repeatability.

**Exit criteria**

- A lab-validated imageable sensor proves the macrocell concept.
- Calibration and reconstruction produce usable RGB and spectral outputs.

---

### B3 — Engineering camera module

**TRL target:** TRL 5  
**Goal:** Validate HSC-1 as a module under realistic conditions.

**Physical artifacts**

- camera board,
- matched VIS/NIR lens,
- package/window,
- firmware,
- SDK,
- calibration file format,
- enclosure or module frame.

**Measurements**

- spectral response through the lens,
- scene-level RGB rendering,
- scene-level spectral outputs,
- active illumination workflows,
- frame rate,
- thermal drift,
- mechanical stability,
- calibration persistence.

**Exit criteria**

- The integrated module performs under relevant lighting, optics, and scene conditions.

---

### B4 — Application prototypes

**TRL target:** TRL 6  
**Goal:** Demonstrate complete prototype systems for selected applications.

**Candidate pilots**

- vegetation/soil/leaf imaging,
- material sorting,
- surface inspection,
- cultural heritage/pigment analysis,
- robotics perception,
- life-science research imaging.

**Exit criteria**

- Prototype modules solve target tasks with repeatable workflows.
- Customers or partners can evaluate outputs without internal sensor expertise.

---

### B5 — Field demonstrations

**TRL target:** TRL 7  
**Goal:** Demonstrate HSC-1 in operational conditions.

**Work items**

- deploy modules with pilot customers,
- capture field data,
- measure performance against application-specific success criteria,
- compare to incumbent tools,
- collect workflow and software feedback,
- refine calibration and SDK.

**Exit criteria**

- Operational demonstrations prove value in target environments.
- Product requirements are updated with field evidence.

---

### B6 — Product qualification

**TRL target:** TRL 8  
**Goal:** Prepare HSC-1 for production and customer deployment.

**Work items**

- reliability testing,
- calibration-line design,
- yield monitoring,
- module QA process,
- supply-chain qualification,
- firmware/SDK release process,
- documentation,
- regulatory review where applicable.

**Exit criteria**

- HSC-1 is qualified as a shippable product.

---

### B7 — Production deployment

**TRL target:** TRL 9  
**Goal:** Deploy production modules and use field data to improve yield, calibration, and application software.

**Work items**

- production ramp,
- customer support,
- calibration database,
- yield learning,
- application-specific software packages,
- second-generation requirements.

**Exit criteria**

- HSC-1 operates reliably in customer workflows.

---

## 8. Domain map by stage

| Domain | D0 | D1 | D2 | D3 | D4 | D5 | D6 | Build/test |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Product/application science | Lead | Lead | Lead | Support | Support | Support | Lead | Lead |
| Image-sensor physics | Support | Lead | Lead | Lead | Support | Lead | Support | Lead |
| CMOS pixel design | Support | Support | Lead | Support | Support | Lead | Support | Lead |
| Semiconductor process | Support | Support | Support | Support | Support | Lead | Support | Lead |
| Optical thin films | Support | Lead | Lead | Lead | Lead | Lead | Support | Lead |
| Lens/optical engineering | Support | Support | Lead | Lead | Lead | Lead | Support | Lead |
| Radiometry | Support | Lead | Lead | Lead | Lead | Support | Support | Lead |
| Computational imaging | Support | Support | Lead | Lead | Lead | Support | Support | Lead |
| Color science | Support | Support | Lead | Support | Lead | Support | Support | Lead |
| Calibration/metrology | Support | Support | Lead | Lead | Lead | Lead | Support | Lead |
| Embedded/ISP/software | Support | Support | Lead | Support | Lead | Support | Support | Lead |
| IP counsel | Support | Support | Support | Support | Support | Support | Lead | Support |
| Manufacturing operations | Support | Support | Support | Support | Support | Lead | Lead | Lead |
| Business development | Lead | Support | Support | Support | Support | Support | Lead | Lead |

The first desk-work team can be lean:

- product/market lead,
- image-sensor physicist or senior imaging technologist,
- computational-imaging engineer,
- optical/radiometry advisor,
- semiconductor process advisor,
- IP counsel,
- business-development lead.

---

## 9. Key decision gates

### Gate A — Product clarity

**Passed when**

- the target customer is specific,
- the top applications are ranked,
- the module form factor is chosen,
- the product claim is concise and defensible.

### Gate B — Physics support

**Passed when**

- silicon wavelength limits are mapped,
- NIR crosstalk assumptions are stated,
- violet/UV packaging requirements are stated,
- stacked-pixel and multispectral-filter precedents are documented.

### Gate C — Virtual proof of concept

**Passed when**

- the radiometric model supports the band set,
- macrocell simulation produces strong RGB and useful spectral outputs,
- public dataset experiments show plausible reconstruction,
- failure modes are visible in simulation.

### Gate D — Manufacturing route

**Passed when**

- at least one plausible process route exists,
- test structures are defined,
- vendor questions are ready,
- first build cost range is credible.

### Gate E — IP and funding readiness

**Passed when**

- prior art is mapped,
- provisional filing themes are drafted,
- FTO review package is ready,
- first prototype budget and schedule are clear.

### Gate F — TRL 4 readiness

**Passed when**

- the desk-work data room is complete,
- requirements trace to tests,
- prototype plan is testable,
- build/test spending has precise learning goals.

---

## 10. Metrics to define during desk work

### Product metrics

- visible RGB output resolution,
- spectral output resolution,
- number of calibrated bands,
- frame rate,
- module size,
- power consumption,
- target selling price,
- target gross margin,
- calibration time per module,
- application-specific accuracy.

### Sensor metrics

- pixel pitch,
- full well,
- read noise,
- dark current,
- dynamic range,
- QE by band,
- crosstalk by band,
- PRNU/DSNU,
- defect density,
- passband center and FWHM,
- passband shift versus angle.

### Software metrics

- RGB color error,
- spectral reconstruction error,
- edge artifacts,
- aliasing artifacts,
- demosaic runtime,
- calibration-file size,
- SDK latency,
- uncertainty-map quality.

### Manufacturing metrics

- wafer cost,
- package/test cost,
- calibration cost,
- die yield,
- module yield,
- first-pass calibration yield,
- field return rate,
- supplier availability.

---

## 11. Competitive positioning to carry into the roadmap

HSC-1 should be positioned around this claim:

> A compact single-chip spectral imaging module that produces a strong human-viewable RGB image and calibrated cross-spectral outputs in the same exposure.

Adjacent products confirm demand and feasibility:

| Adjacent product/design | What it proves | HSC-1 distinction |
|---|---|---|
| Sony IMX454 multispectral sensor | One-shot visible/NIR spectral imaging from an on-sensor filter approach is commercially active | HSC-1 centers the visible RGB output as a first-class product outcome |
| imec/XIMEA snapshot spectral cameras | Compact snapshot spectral cameras and wafer-level filters are real | HSC-1 integrates the visible-color anchor into the macrocell concept |
| Canon RGB-NIR sensors | Single-sensor visible + NIR separation has industrial demand | HSC-1 expands from one NIR band to a calibrated multispectral band set |
| Spectricity S1 | Small CMOS-integrated spectral image sensors can target compact products | HSC-1 adds a higher-value imaging-module pathway with strong RGB context |
| SILIOS CMS | Custom Bayer-like mosaics on commercial CMOS support VIS/NIR spectral imaging | HSC-1 adds stacked visible anchoring and a tailored reconstruction architecture |
| JAI Fusion | Simultaneous visible/NIR imaging has value in precision applications | HSC-1 offers the single-chip, compact-module path |
| Sony organic RGB/NIR ToF research | Stacked visible/NIR architectures are a serious advanced-sensor direction | HSC-1 applies stacked anchoring to spectral imaging rather than ranging |

Source anchors:

- [Sony — Multispectral Image Sensor Technology](https://www.sony-semicon.com/en/technology/industry/multispectral.html)
- [imec — Snapshot RGB-NIR Multispectral Image Sensor](https://www.imec-int.com/en/articles/imec-introduces-new-snapshot-multispectral-image-sensor-that-combines-color-and-near-infrared-imaging)
- [Canon — RGB-NIR Color Filter Array for Research & Development](https://canon-cmos-sensors.com/industries/cmos-sensors-for-research-and-development/)
- [Spectricity — S1 Multispectral Image Sensor](https://spectricity.com/products/)
- [SILIOS — CMS Multispectral Cameras](https://www.silios.com/cms-series)
- [JAI — Fusion Series multispectral prism cameras](https://www.jai.com/products/product-lines/fusion-series-2-sensor-area-scan/)
- [Sony — Organic RGB over NIR ToF stacked sensor](https://www.sony.com/en/SonyInfo/technology/publications/a-color-image-sensor-using-1.0-um-organic-photoconductive-film-pixels-stacked-on-4.0-um-si-pixels-for-near-infrared-time-of-flight-depth/)

---

## 12. What to do first

The first practical desk-work sprint should produce five artifacts:

1. **Product Requirements Document**  
   Defines the target module, customers, bands, performance targets, and success metrics.

2. **Physics and Architecture Memo**  
   Maps silicon absorption, stacked RGB anchoring, NIR crosstalk, violet/UV constraints, and filter-array feasibility.

3. **Radiometric Model**  
   Calculates photon budget and SNR by band under target scenes.

4. **Macrocell Simulation Notebook**  
   Creates synthetic raw data from hyperspectral datasets and reconstructs RGB + spectral outputs.

5. **Build-Ready Test Matrix**  
   Specifies what the first test structures and prototype chip must measure.

The strongest near-term milestone is:

> Analytical TRL 3 package complete: requirements, physics evidence, simulated macrocell, radiometric model, manufacturing inquiry package, source-backed competitive map, IP counsel packet, and prototype test plan.

---

## 13. Source use map

| Source | Used for |
|---|---|
| [NASA — Technology Readiness Levels](https://www.nasa.gov/directorates/somd/space-communications-navigation-program/technology-readiness-levels/) | TRL scale, TRL 1–9 framing, TRL 3 and TRL 4 interpretation |
| [IEEE — ISO/IEC/IEEE 29148-2018](https://standards.ieee.org/ieee/29148/6937/) | Requirements-engineering structure |
| [Sony Semiconductor — Multispectral Image Sensor Technology](https://www.sony-semicon.com/en/technology/industry/multispectral.html) | One-shot 41-wavelength IMX454-style multispectral sensor technology and 8-filter-pattern approach |
| [imec — Snapshot RGB-NIR Multispectral Image Sensor](https://www.imec-int.com/en/articles/imec-introduces-new-snapshot-multispectral-image-sensor-that-combines-color-and-near-infrared-imaging) | Wafer-level RGB/NIR filter integration, NIR band-pass filters, microlens integration |
| [PVEducation — Optical Properties of Silicon](https://www.pveducation.org/pvcdrom/materials/optical-properties-of-silicon) | Silicon wavelength response and absorption coefficient reference |
| [Applied Optics — Near-IR absorption enhancement and crosstalk reduction](https://opg.optica.org/ao/abstract.cfm?uri=ao-61-22-6577) | 940 nm QE/crosstalk engineering, DTI example |
| [Sony Semiconductor — UV Image Sensor Technology](https://www.sony-semicon.com/en/technology/industry/uv.html) | UV package and material implications |
| [Sigma — Sensor development update](https://www.sigma-global.com/en/news/2021/02/19/12739/) | Stacked-color mass-production feasibility precedent |
| [Sony — Organic RGB over NIR ToF stacked sensor](https://www.sony.com/en/SonyInfo/technology/publications/a-color-image-sensor-using-1.0-um-organic-photoconductive-film-pixels-stacked-on-4.0-um-si-pixels-for-near-infrared-time-of-flight-depth/) | Advanced stacked visible/NIR sensor research precedent |
| [Google Patents — Multispectral imaging sensors and systems](https://patents.google.com/patent/WO2018217770A2/en) | Prior-art exploration for multispectral superpixels and vertically stacked photodetectors |
| [Canon — RGB-NIR Color Filter Array](https://canon-cmos-sensors.com/industries/cmos-sensors-for-research-and-development/) | Commercial single-sensor RGB/NIR precedent |
| [Spectricity — S1 Multispectral Image Sensor](https://spectricity.com/products/) | Compact CMOS-integrated spectral image sensor precedent |
| [imec/XIMEA — Snapshot VIS evaluation system](https://www.imechyperspectral.com/en/offering/evaluation-systems/snapshot-vis) | Snapshot spectral camera precedent and practical module characteristics |
| [SILIOS — CMS Multispectral Cameras](https://www.silios.com/cms-series) | Custom mosaic VIS/NIR spectral camera precedent |
| [JAI — Fusion Series](https://www.jai.com/products/product-lines/fusion-series-2-sensor-area-scan/) | Prism-based simultaneous visible/NIR multispectral camera precedent |
| [Columbia CAVE — Multispectral Images Database](https://cave.cs.columbia.edu/repository/Multispectral) | Public data source for desk-work macrocell simulation |
| [Harvard — Hyperspectral Images Database](https://vision.seas.harvard.edu/hyperspec/download.html) | Public data source for desk-work macrocell simulation |
| [Yale HSI Open Ecosystem — ICVL Dataset](https://hsi.yale.edu/resource/675) | Public high-resolution hyperspectral data source |
| [Zenodo — Camera Spectral Sensitivity Database](https://zenodo.org/records/3245883) | Public camera spectral-response comparison data |

---

## 14. Desk-work completion definition

The desk-work program is complete when the team can hand a reviewer a single package containing:

- product thesis,
- requirements,
- spectral band plan,
- macrocell layout,
- radiometric model,
- synthetic reconstruction evidence,
- competitive landscape,
- source-backed physics memo,
- IP/FTO review packet,
- manufacturing inquiry package,
- cost model,
- prototype budget,
- test-chip plan,
- calibration plan,
- go/no-go criteria.

That package represents the maximum useful progress before physical build and test activity. It makes the first physical prototype purposeful, bounded, and measurable.
