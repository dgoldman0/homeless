# HSC-1 Hybrid Cross-Spectral Sensor Product Design and Plan

**Working name:** HSC-1 — Hybrid Snapshot Cross-Spectral Sensor  
**Document date:** 2026-05-03  
**Product form:** calibrated one-lens camera module and OEM sensor engine

---

## 1. Executive Summary

HSC-1 is a **snapshot cross-spectral CMOS image sensor module** built around a distinctive pixel-level architecture:

1. a sparse **stacked visible-color anchor pixel** that captures depth-separated visible color at selected pixel sites,
2. a surrounding **multispectral filter-array mosaic** for visible, violet, red-edge, and near-infrared bands,
3. clear/panchromatic and visible-band samples that preserve spatial detail, and
4. a calibrated reconstruction pipeline that produces a human-viewable RGB image and a registered spectral data product from the same exposure.

The product position is direct:

> **A single-shot, single-lens spectral camera that produces a strong normal RGB image and simultaneous calibrated cross-spectral bands.**

The most attractive launch configuration is a **1-inch-type silicon CMOS module** covering approximately **405–940 nm**. That range aligns with practical silicon response, visible/NIR optics, LED illumination, agriculture indices, inspection contrast, robotics perception, conservation workflows, and medical-adjacent research instrumentation.

HSC-1 belongs in the compact spectral-imaging market alongside snapshot mosaic spectral cameras, RGB-NIR image sensors, mobile spectral sensors, and prism multispectral cameras. Its product distinction is the combination of **visible-image quality**, **spectral utility**, **single-chip alignment**, and **one-lens operation**.

---

## 2. Product Thesis

Current spectral imaging products usually optimize one of three outcomes:

| Market pattern | Established strength | HSC-1 expansion |
|---|---|---|
| Snapshot mosaic spectral cameras | compact spectral capture in one exposure | stronger human-viewable RGB output with a stacked visible anchor and visible/pan samples |
| RGB-NIR sensors | practical visible + 940 nm NIR capture at high volume | richer spectral sampling across violet, red-edge, 850 nm, and 940 nm bands |
| Prism multispectral cameras | simultaneous aligned multi-band capture with high per-band quality | smaller one-chip module architecture with straightforward OEM integration |
| Mobile spectral sensors | compact, low-power spectral sensing | higher image utility for robotics, inspection, research, and machine vision |
| Multi-camera rigs | flexible per-camera sensor/filter selection | one-lens registration and shared exposure timing |

HSC-1 addresses a product opening:

> **Calibrated spectral imaging with a real RGB image, rather than a spectral cube that merely includes a preview image.**

That distinction matters in field and industrial workflows because users need to inspect the scene as humans see it while also extracting band ratios, material signatures, vegetation indices, tissue/fluorophore-adjacent signals, or NIR contrast.

---

## 3. Launch Product Definition

### 3.1 Core module

| Parameter | Launch target |
|---|---:|
| Optical format | 1-inch type |
| Active area | ~13.2 mm × 8.8 mm class |
| Die area planning assumption | ~110–130 mm² |
| Pixel pitch | 4.5–6.0 µm |
| Native mosaic sites | 3–6 MP class |
| Reconstructed RGB output | 6–12 MP equivalent, application-dependent |
| Spectral data output | 6–10 bands at band-dependent effective spatial resolution |
| Shutter | global shutter preferred for industrial and robotics SKUs |
| Interface | MIPI CSI-2 at sensor/OEM level; USB3 or GigE at camera level |
| Raw precision | 12-bit minimum, 14-bit preferred |
| Spectral range | ~405–940 nm |
| Product form | calibrated camera module with SDK, lens profile, and spectral calibration file |

### 3.2 Product promise

HSC-1 delivers:

- a co-registered visible RGB image,
- red-edge and NIR spectral contrast,
- application-ready band-ratio products,
- one-exposure operation for moving subjects,
- one-lens geometry for simpler calibration,
- raw access for research users,
- embedded software support for OEM integration.

---

## 4. Target Customers and Applications

### 4.1 Primary segments

| Segment | Application | HSC-1 value |
|---|---|---|
| Precision agriculture | crop stress, NDVI-like indices, chlorophyll/red-edge monitoring | visible scene context plus red-edge/NIR indices |
| Industrial inspection | coating defects, contamination, adhesives, moisture proxies, sorting | visible inspection image plus band-ratio contrast |
| Robotics and autonomy | navigation, semantic scene understanding, active NIR illumination | aligned RGB and NIR features from one imaging path |
| Cultural heritage | pigment contrast, underdrawing visibility, varnish/retouching analysis | visible documentation plus violet/NIR channels |
| Medical-adjacent research | tissue reflectance and fluorescence-adjacent studies | calibrated visible/NIR capture under controlled illumination |
| Forensics and lab workflows | document, stain, residue, and material contrast | single-shot spectral comparison with RGB reference |

### 4.2 Buyer profiles

- machine-vision OEMs,
- agricultural robotics companies,
- precision-agriculture analytics companies,
- conservation labs and museums,
- medical-device research teams,
- inspection-camera manufacturers,
- research labs that currently use filter wheels, prism cameras, or multi-camera rigs.

---

## 5. Pixel and Macrocell Architecture

### 5.1 Architecture overview

The macrocell combines three sensing roles:

| Role | Pixel type | Purpose |
|---|---|---|
| Visible color anchor | sparse stacked visible RGB/X3-style pixel | stable local color reference and color transform anchor |
| Spatial detail | clear/panchromatic and green/pan pixels | luminance detail for RGB reconstruction and pan-sharpening |
| Spectral features | violet, red-edge, deep red, NIR filters | cross-spectral measurements for analysis |

### 5.2 Recommended 4×4 macrocell

```text
G/Pan      NIR850      G/Pan       RedEdge730
Blue450    X3-RGB      Clear       NIR940
Violet405  G/Pan       DeepRed660  NIR730
Clear      NIR850      G/Pan       Violet405
```

### 5.3 Compact 3×3 macrocell option

```text
NIR850     Clear/Pan     NIR940
Violet405  X3-RGB        RedEdge730
Blue450    Green/Pan     DeepRed660
```

### 5.4 Rationale

The central stacked pixel supplies high-confidence visible color at selected sites. The surrounding pan/green/clear pixels supply high-SNR spatial structure. The narrow and semi-narrow filtered pixels add the spectral contrast channels. This creates a reconstruction problem closer to **pan-sharpened multispectral demosaicing** than ordinary Bayer demosaicing.

The design treats RGB output as a first-class data product. The visible image is reconstructed from stacked-anchor color, visible filtered pixels, and high-SNR luminance samples, then exported alongside the spectral data cube.

---

## 6. Spectral Band Plan

| Channel | Approx. center/range | Function |
|---|---:|---|
| X3-B | depth-separated visible blue | visible color anchor |
| X3-G | depth-separated visible green | visible color anchor |
| X3-R | depth-separated visible red | visible color anchor |
| Violet | 405 nm | fluorescence-adjacent and material contrast |
| Blue | 450 nm | visible reconstruction and pigment/material contrast |
| Green/Pan | 530–560 nm or broad visible pan | luminance and RGB spatial detail |
| Deep red | 650–670 nm | vegetation, tissue, pigment, and coating contrast |
| Red-edge | 710–740 nm | vegetation and material indices |
| NIR1 | 810–850 nm | vegetation, active illumination, contrast enhancement |
| NIR2 | 930–950 nm | active illumination and material discrimination |

The launch spectral range of **405–940 nm** matches practical silicon imaging and available illumination. SWIR-class functionality becomes a separate material-stack product family using Ge, InGaAs, quantum-dot, organic, or hybrid-bonded detectors.

---

## 7. Physics Basis

### 7.1 Stacked visible sensing

The stacked visible pixel uses wavelength-dependent absorption depth in silicon. Shorter wavelengths are absorbed near the surface; longer wavelengths penetrate deeper. The governing intensity-depth relationship is:

```math
I(x,\lambda)=I_0(\lambda)e^{-\alpha(\lambda)x}
```

where `α(λ)` is the wavelength-dependent silicon absorption coefficient.

Foveon/X3 demonstrated the basic visible-silicon concept: vertically stacked photodiodes can create different spectral sensitivities within a single photosite. The HSC-1 implementation uses this concept selectively as a **sparse visible color anchor** inside a broader spectral macrocell.

### 7.2 Silicon range

Silicon is a strong match for visible through practical NIR imaging. Hamamatsu’s silicon/CCD detector discussion lists practical silicon photon interaction across roughly **400–1100 nm**, notes deeper penetration above 700–800 nm, and lists 90% absorption depth values from **0.19 µm at 400 nm** to **470 µm at 1000 nm** and **7600 µm at 1100 nm**. PVEducation’s optical-property reference similarly notes the sharp absorption drop near silicon’s band gap around **1100 nm**.

Design implications:

- 405–740 nm channels align naturally with visible and red-edge silicon response.
- 850 nm benefits from BSI and tuned optical stack.
- 940 nm benefits from NIR-enhanced pixel engineering and active illumination.
- 1000–1100 nm belongs in research characterization and high-exposure modes.
- SWIR-class use cases become a companion platform based on alternative absorber materials.

### 7.3 NIR crosstalk and pixel engineering

Longer wavelengths generate charge deeper in silicon. HSC-1 uses the following controls:

- backside illumination,
- deep trench isolation,
- backside AR coatings tuned for visible/NIR,
- NIR-enhanced silicon thickness and collection geometry,
- optional backside scattering or photon-trapping structures for 850–940 nm,
- per-band crosstalk calibration,
- macrocell layouts that place NIR and visible/pan samples deliberately.

Samsung/IISS work on backside scattering techniques reports a **1.5× improvement in 940 nm quantum efficiency** with acceptable inter-pixel crosstalk, supporting the practicality of NIR-focused pixel structures in BSI CMOS.

### 7.4 Violet/near-UV handling

405 nm is a practical launch band. It provides material and fluorescence-adjacent contrast while keeping the optical stack close to industrial VIS/NIR module practice. Deeper UV operation uses quartz windows, UV-transmissive microlenses or lensless choices, UV-pass optics, and dedicated safety/illumination controls. Sony’s UV image-sensor notes show the material-stack changes required for UV operation, including quartz cover glass and UV-transmissive chip-on lens material.

---

## 8. Optical System

HSC-1 is sold as a calibrated module because the lens, window, microlenses, filters, and reconstruction model work as one instrument.

### 8.1 Lens requirements

| Requirement | Target |
|---|---|
| Spectral transmission | 405–950 nm |
| Focus behavior | calibrated VIS/NIR focus model |
| Distortion | factory-calibrated geometric model |
| Chief-ray angle | matched to microlens/filter stack |
| Aperture | f/2.8–f/5.6 by SKU |
| Mount | C-mount for industrial/research; fixed lens or M12 for compact OEM modules |

### 8.2 Optical package

- spectral-grade cover glass,
- AR coatings for visible/NIR,
- optional SKU-specific band-limiting window,
- illuminator metadata support,
- factory lens profile and per-band flat-field files.

### 8.3 Illumination ecosystem

Recommended companion illuminators:

- broadband white LED,
- 405 nm violet LED,
- 660 nm deep red LED,
- 730 nm red-edge LED,
- 850 nm NIR LED,
- 940 nm NIR LED.

The camera records exposure, gain, temperature, illuminator state, and calibration profile in metadata.

---

## 9. Electronics and Readout

| Block | Target implementation |
|---|---|
| Pixel readout | 4T pinned photodiode CMOS for filtered pixels; custom multi-junction readout for stacked anchor pixels |
| Shutter | global shutter for industrial and robotics SKUs |
| ADC | column-parallel ADC |
| Precision | 12-bit minimum; 14-bit preferred |
| HDR | dual conversion gain or multi-exposure spectral mode |
| Frame rate | 30 fps full frame baseline; 60 fps target for machine vision |
| Interface | MIPI CSI-2 at sensor level; USB3/GigE at module level |
| Timing | trigger, strobe, and illuminator sync |
| Metadata | exposure, gain, temperature, lens profile, illuminator state, calibration ID |

---

## 10. Software Pipeline

The software is part of the product, with equal importance to the sensor.

### 10.1 Outputs

- raw mosaic frame,
- corrected mosaic planes,
- reconstructed RGB image,
- registered spectral cube,
- band-ratio/index maps,
- confidence/error maps,
- calibration metadata package.

### 10.2 Processing flow

```text
Raw mosaic
  -> black-level correction
  -> bad-pixel correction
  -> temperature-aware dark correction
  -> per-band flat-field correction
  -> lens-shading correction
  -> spectral crosstalk correction
  -> stacked-anchor RGB transform
  -> multispectral demosaicing
  -> pan/green/clear luminance fusion
  -> RGB image + spectral cube + indices + confidence maps
```

### 10.3 Calibration package

Each module ships with:

- dark-current map by temperature,
- per-band flat-field map,
- spectral response matrix,
- stacked-anchor visible transform,
- NIR crosstalk correction matrix,
- lens shading map,
- distortion model,
- illuminator profile compatibility table,
- serial-numbered calibration certificate.

---

## 11. Closest Existing Designs and Market Position

The field is active, which validates demand. HSC-1 occupies a differentiated position inside that field.

### 11.1 Sony IMX454 multispectral sensor

Sony’s IMX454 is a close single-chip snapshot reference. Sony states that the IMX454 uses **8 types of filters** and, with Sony signal-processing software, captures image data for **41 wavelengths from 450 nm to 850 nm in one shot**.

**HSC-1 position:** IMX454 validates one-shot filter-mosaic multispectral imaging. HSC-1 adds a product emphasis on a first-class reconstructed RGB image using stacked visible anchor samples plus visible/pan spatial samples.

### 11.2 imec / XIMEA snapshot spectral cameras

imec’s snapshot VIS evaluation system, integrated in a XIMEA USB camera, provides **2 MP**, **16 bands**, **460–600 nm**, and up to **120 cubes/second**. XIMEA/imec product materials also describe snapshot mosaic systems covering VIS, RedNIR, and NIR configurations, including NIR mosaic products around **665–960 nm**.

**HSC-1 position:** imec/XIMEA validates snapshot mosaic spectral imaging and complete camera-module delivery. HSC-1 extends the product promise toward one module that simultaneously prioritizes spectral data and a strong human-visible RGB output.

### 11.3 Spectricity S1

Spectricity’s S1 is a compact mobile spectral image sensor with **400–700 nm** range, **15 channels**, **34 nm average FWHM**, **864 × 648 SVGA** spatial format, **30 fps**, and CMOS integration.

**HSC-1 position:** Spectricity validates miniaturized spectral sensing. HSC-1 focuses on a larger industrial/research module with red-edge/NIR extension, 1-inch-class optics, and a calibrated RGB-plus-spectral product.

### 11.4 Canon RGB-NIR sensors

Canon’s LI3030SAI uses a specialized **RGB-NIR color filter array** and replaces one green filter with an NIR filter to separate visible and NIR wavelengths for simultaneous detection.

**HSC-1 position:** Canon validates single-sensor RGB/NIR workflows. HSC-1 expands the band plan from RGB+NIR to a broader spectral set with violet, deep red, red-edge, 850 nm, and 940 nm channels.

### 11.5 OMNIVISION and Sony RGB-IR automotive sensors

OMNIVISION’s OX05B1S is a **5 MP RGB-IR BSI global-shutter sensor** with **940 nm NIR sensitivity** for in-cabin applications. Sony announced the IMX775 RGB-IR sensor for in-cabin monitoring with approximately **5 effective megapixels**, **2.1 µm pixels**, visible RGB and **940 nm NIR** imaging on one chip, and planned mass-production shipment in **spring 2026**.

**HSC-1 position:** high-volume RGB-IR automotive sensors validate the value of co-registered RGB/NIR. HSC-1 targets richer spectral analysis and calibrated industrial/scientific outputs.

### 11.6 JAI Fusion prism multispectral cameras

JAI Fusion cameras use a prism architecture with two or three sensors, simultaneous capture, 10GigE output, up to **3.2 MP per channel**, and custom wavebands as narrow as **25 nm** anywhere from **405–1000 nm**.

**HSC-1 position:** JAI validates demand for simultaneous aligned multispectral imaging. HSC-1 creates a smaller single-chip, one-lens module option with direct OEM integration.

### 11.7 Stacked and hybrid research references

- Foveon/X3 demonstrates vertically stacked visible photodiodes using silicon’s natural color absorption depth.
- Sony’s organic photoconductive-film work demonstrates stacked visible RGB pixels over silicon NIR ToF pixels for high-resolution RGB and parallax-free NIR depth capture on one chip.
- University of Illinois work describes a bioinspired 9-band NIR camera with a visible filter for simultaneous RGB and a spectral filter array monolithically integrated with vertically stacked photodiodes.
- Patent publication WO2018217770A2 describes multispectral imaging sensors with superpixels, spectral filters, and vertically stacked photodetectors.

**HSC-1 position:** the research and patent landscape supports the architecture family. HSC-1’s product identity is the calibrated module implementation: sparse stacked visible anchor + multispectral mosaic + pan/visible spatial detail + RGB-first software pipeline.

### 11.8 Niche assessment

HSC-1 fits a clear product space:

> **Single-chip, one-lens, calibrated cross-spectral imaging with genuinely useful visible RGB output.**

Adjacent products validate the demand. HSC-1 packages a distinct combination as the product center: real RGB context, spectral bands, one exposure, one lens, and calibration-ready outputs.

---

## 12. Competitive Positioning

| Product category | Primary user benefit | HSC-1 product advantage |
|---|---|---|
| Bayer RGB cameras | high-resolution visible imaging | adds calibrated spectral channels while preserving RGB context |
| RGB-IR sensors | visible + 940 nm NIR in one chip | adds violet, deep red, red-edge, 850 nm, and richer spectral outputs |
| Snapshot mosaic spectral cameras | compact spectral cube capture | elevates visible RGB reconstruction as a primary output |
| Prism multispectral cameras | precise simultaneous multi-band capture | compresses the system into a smaller one-chip, one-lens module |
| Filter-wheel systems | flexible laboratory band selection | captures moving scenes with one exposure |
| Line-scan hyperspectral cameras | high spectral density | supports area snapshots for robotics, field work, and inspection |
| Mobile spectral sensors | miniaturized spectral sensing | provides industrial optics, NIR bands, and higher scene-imaging utility |

### Strategic positioning statement

> **HSC-1 is a calibrated RGB-plus-spectral imaging engine for customers who need spectral measurement and human-readable imagery in the same registered frame.**

---

## 13. Manufacturing Architecture

### 13.1 Fabrication stack

```text
microlens array
multispectral filter array / visible filters
planarization and passivation
backside AR coating
backside-illuminated silicon photodiode layer
stacked visible anchor photodiode structures
NIR-enhanced pixel structures
frontside/deep trench isolation
frontside readout circuitry
bond pads / wafer-level package
spectral-grade cover glass / optical window
```

### 13.2 Process dependencies

- BSI CMOS image-sensor process access,
- custom photodiode structure for sparse stacked visible anchors,
- multispectral filter-array lithography,
- deep trench isolation,
- backside thinning and passivation,
- NIR-enhanced pixel design for 850/940 nm,
- optical packaging with spectral-grade cover glass,
- automated spectral calibration and test.

### 13.3 Manufacturing plan

HSC-1 proceeds as a custom product-die program with these workstreams running in parallel:

| Workstream | Deliverable |
|---|---|
| Pixel architecture | stacked visible anchor test structures, NIR pixel variants, DTI layout variants |
| Macrocell design | 3×3 and 4×4 macrocell candidates, sampling simulation, reconstruction scoring |
| Filter fabrication | violet/visible/red-edge/NIR filter set, process-control coupons, transmission curves |
| Optics | matched VIS/NIR lens set, spectral window, chief-ray-angle model |
| Calibration | factory spectral calibration line, reference targets, automated certificate generation |
| SDK | raw reader, calibration engine, RGB reconstruction, spectral cube output, indices |
| Product integration | USB3/GigE/MIPI modules, illumination sync, industrial enclosure, OEM module design |

---

## 14. Cost Model

These are planning estimates for a 300 mm BSI CIS production context. Supplier quotes, foundry access, mask pricing, and yield-learning data set the final values.

### 14.1 Processed wafer assumptions

| Process class | Planning wafer cost |
|---|---:|
| mature 300 mm CMOS reference | ~$1.2k–$5k |
| standard BSI Bayer CIS | ~$4k–$8k |
| BSI multispectral mosaic CIS | ~$6k–$12k |
| HSC-1 hybrid stacked-visible + multispectral CIS | ~$10k–$25k |
| SWIR/hybrid compound-semiconductor product family | ~$30k–$100k+ equivalent |

AnySilicon summarizes the main wafer-cost drivers as node, process complexity, special options, and volume expectations. A CMOS cost lecture from MSOE gives a mature 300 mm wafer reference range of roughly **$1,200–$5,000/wafer** and ties die cost to wafer cost, die count, yield, packaging, and margin.

### 14.2 Die and package cost estimates

| Sensor size | Die area | Packaged/tested sensor cost estimate |
|---|---:|---:|
| Small industrial | 25–35 mm² | $15–$40 |
| 1-inch type | 110–130 mm² | $60–$140 |
| Micro Four Thirds / small APS-C | 220–370 mm² | $180–$650 |
| Full-frame class | ~864 mm² | $700–$2,000+ |

The best commercial target is:

> **1-inch-type packaged, tested, calibrated HSC-1 sensor: $60–$140 at mature volume, excluding NRE amortization.**

### 14.3 NRE planning range

| Program scope | NRE planning range |
|---|---:|
| HSC-1 hybrid stacked-visible + multispectral CIS | $30M–$100M |
| new stacked photodiode process development | $100M–$300M+ |
| SWIR/hybrid material-stack product family | $200M+ |

### 14.4 NRE amortization example

Assume $75M development cost.

| Lifetime units | NRE per unit |
|---:|---:|
| 100k | $750 |
| 1M | $75 |
| 5M | $15 |
| 10M | $7.50 |

### 14.5 Module COGS target

| Item | Cost target |
|---|---:|
| Sensor package/test/calibration | $60–$140 |
| VIS/NIR lens | $20–$200 |
| Optical window/filter | $5–$80 |
| Processing board | $30–$150 |
| Housing/thermal/interface | $30–$200 |
| Factory calibration automation allocation | $10–$100 |
| Total COGS target | $175–$870 |

### 14.6 ASP targets

| SKU | Target ASP |
|---|---:|
| OEM sensor engine | negotiated by volume |
| compact industrial module | $999–$1,999 |
| calibrated research/inspection module | $2,500–$5,000 |
| application-specific system with illumination and software | $5,000–$15,000+ |

---

## 15. Product SKUs

### HSC-1A — Agriculture and field robotics

- RGB anchor + visible/pan reconstruction,
- 660 nm, 730 nm, 850 nm, 940 nm,
- outdoor radiometric correction,
- NDVI-like and red-edge indices,
- rugged module package,
- drone/robot integration profile.

### HSC-1I — Industrial inspection

- RGB anchor + visible/pan reconstruction,
- 405 nm, 450 nm, 660 nm, 850 nm, 940 nm,
- global shutter,
- trigger/strobe support,
- GigE Vision / USB3 Vision,
- material and coating discrimination tools.

### HSC-1R — Research module

- raw access to all channels,
- calibration target,
- Python/C++ SDK,
- C-mount,
- spectral cube export,
- user-defined band ratios and calibration workflows.

### HSC-1M — Medical-adjacent research module

- controlled illumination profile,
- sterile-compatible housing option,
- 405/450/660/730/850/940 nm band emphasis,
- metadata-rich capture for research workflows,
- regulatory pathway handled by the customer application and end system.

---

## 16. Engineering Validation Plan

### 16.1 Pixel validation

| Metric | Target |
|---|---:|
| stacked-anchor visible color repeatability | stable transform under standard illuminants |
| 850 nm QE | commercially useful under passive or active illumination |
| 940 nm QE | useful with active illumination |
| per-band crosstalk after correction | <5–10% adjacent-band residual target |
| dark noise | suitable for 12–14 bit operation |
| bad-pixel density | correctable through calibration maps |

### 16.2 Image validation

| Metric | Target |
|---|---:|
| RGB image | sharp, usable, color-consistent output for human interpretation |
| spectral cube registration | sub-pixel alignment after calibration |
| flat-field repeatability | stable over operating temperature |
| frame rate | 30 fps product baseline; 60 fps target |
| calibration drift | managed by temperature metadata and reference target workflow |

### 16.3 Product validation

| Metric | Target |
|---|---:|
| module ASP / fully loaded COGS | >3× target |
| gross margin | >45% module-level target |
| pilot customers | 3–5 serious OEM/lab/industrial partners |
| lifetime volume for custom silicon | >500k units or premium-niche pricing support |
| SDK adoption | successful customer integration in Python/C++ and embedded pipeline |

---

## 17. Development Roadmap

### 17.1 Design sprint: 0–3 months

Deliverables:

- final target applications,
- selected band set,
- 3×3 and 4×4 macrocell simulations,
- synthetic raw mosaic generator,
- optical model for 405–940 nm,
- provisional patent filing package,
- target customer interview set.

### 17.2 Sensor and filter design: 3–12 months

Deliverables:

- stacked-anchor pixel design package,
- NIR-enhanced pixel variants,
- DTI and crosstalk layout variants,
- multispectral filter stack specification,
- filter transmission test plan,
- first SDK reconstruction prototype,
- calibration rig design.

### 17.3 Test chip and module engineering: 12–30 months

Deliverables:

- test chip containing macrocell variants,
- spectral response report,
- NIR QE and crosstalk report,
- visible RGB reconstruction quality report,
- lens and illuminator qualification,
- module EVT build,
- SDK beta.

### 17.4 Product silicon and launch: 30–60 months

Deliverables:

- production-intent 1-inch-type HSC-1 sensor,
- calibrated HSC-1A/HSC-1I/HSC-1R modules,
- factory spectral calibration line,
- SDK v1.0,
- application demos,
- OEM design-in documentation,
- launch customer deployments.

---

## 18. Data Products

### 18.1 Standard files

- `raw_mosaic.dng`
- `rgb_visible.tiff`
- `spectral_cube_405_940nm.tiff`
- `band_maps/`
- `confidence_map.tiff`
- `calibration.json`
- `indices.csv`
- `capture_metadata.json`

### 18.2 Built-in indices

Agriculture:

- 850/660 NDVI-like index,
- 730/660 red-edge index,
- NIR/green vegetation ratio,
- chlorophyll proxy map.

Industrial:

- 405/visible contrast,
- 850/visible contrast,
- 940/850 material discrimination,
- coating uniformity heat map.

Research:

- user-defined band ratios,
- spectral unmixing hooks,
- Python calibration API,
- raw per-band export.

---

## 19. IP and Patent Landscape

A formal freedom-to-operate review is part of the product program.

Priority review areas:

- Foveon/Sigma and Kodak stacked photodiode/color detector patents,
- multispectral filter-array fabrication patents,
- RGB-NIR CFA patents,
- vertically stacked photodetector multispectral patents,
- per-pixel spectral reconstruction and demosaicing patents,
- wafer-level filter integration patents,
- module-level spectral calibration and pan-spectral fusion patents.

Recommended IP focus:

1. sparse stacked visible anchor inside a multispectral macrocell,
2. macrocell layouts combining stacked RGB, pan/clear, visible, red-edge, and NIR samples,
3. RGB-first reconstruction from stacked-anchor + pan/visible + spectral samples,
4. module-level spectral calibration files linked to lens and illuminator profiles,
5. confidence-map generation for RGB and spectral outputs.

---

## 20. Business Plan

### 20.1 Revenue model

| Revenue stream | Description |
|---|---|
| camera modules | HSC-1A/I/R/M modules sold through direct and specialist channels |
| OEM sensor engine | sensor + module reference design + calibration SDK |
| software license | advanced reconstruction, indices, and application models |
| calibration services | annual recalibration and certified reference-target workflow |
| application kits | agriculture, inspection, conservation, and research bundles |

### 20.2 Differentiation claims

- one exposure captures RGB context and spectral information,
- one lens produces co-registered visible/NIR data,
- stacked visible anchor improves RGB confidence inside a spectral mosaic,
- 405–940 nm coverage serves practical field and industrial use cases,
- calibrated outputs reduce integration time for OEMs.

### 20.3 Launch channels

- industrial machine-vision distributors,
- direct OEM sales,
- research instrumentation channels,
- agriculture robotics partnerships,
- museum/conservation imaging specialists,
- medical-adjacent research integrators.

---

## 21. Immediate Actions

1. Finalize the 4×4 launch macrocell and one compact 3×3 alternative.
2. Simulate RGB and spectral reconstruction using public multispectral datasets.
3. Build the spectral response matrix model for 405, 450, 530/pan, 660, 730, 850, and 940 nm.
4. Model stacked-anchor visible responses using silicon absorption-depth data.
5. Build the first SDK pipeline around synthetic mosaics.
6. Identify BSI CIS foundry/service partners with custom photodiode and filter-array capability.
7. Request quotes for filter-array deposition and spectral calibration fixtures.
8. Define HSC-1A, HSC-1I, and HSC-1R lens/illumination kits.
9. Prepare a provisional patent filing around the macrocell and reconstruction pipeline.
10. Recruit pilot partners from agriculture robotics, industrial inspection, and conservation imaging.

---

## 22. Source Appendix

Links below were checked during preparation on 2026-05-03.

### Closest existing product designs

- [Sony Semiconductor Solutions — IMX454 multispectral image sensor](https://www.sony-semicon.com/en/products/is/industry/multispectral.html) — 8 filter types and software-derived 41 wavelengths from 450–850 nm in one shot.
- [Sony Semiconductor Solutions — multispectral image sensor technology](https://www.sony-semicon.com/en/technology/industry/multispectral.html) — snapshot multispectral architecture and filter/software design context.
- [imec hyperspectral — Snapshot VIS evaluation system](https://www.imechyperspectral.com/en/offering/evaluation-systems/snapshot-vis) — XIMEA/imec 2 MP, 16-band, 460–600 nm, up to 120 cubes/s system.
- [XIMEA — hyperspectral starter kit contents](https://www.ximea.com/support/wiki/standard-cameras/Contents_of_Hyperspectral_Starter_Kits) — snapshot mosaic VIS, RedNIR, and NIR configurations including 665–960 nm NIR.
- [Spectricity — S1 multispectral image sensor](https://spectricity.com/products/) — 400–700 nm, 15 channels, SVGA, 30 fps, mobile-focused CMOS integration.
- [Canon Industrial Sensors — LI3030SA/SAI RGB-NIR CMOS sensor](https://canon-cmos-sensors.com/canon-li3030sa-19um-cmos-sensor/) — specialized RGB-NIR CFA with simultaneous visible/NIR detection.
- [OMNIVISION — OX05B1S RGB-IR BSI global-shutter sensor](https://www.ovt.com/products/ox05b/) — 5 MP RGB-IR global-shutter sensor with 940 nm NIR sensitivity.
- [Sony Semiconductor Solutions — IMX775 RGB-IR image sensor announcement](https://www.sony-semicon.com/en/news/2025/2025100201.html) — 5 effective MP RGB-IR in-cabin sensor, 2.1 µm pixels, 940 nm NIR, spring 2026 planned mass shipment.
- [JAI — Fusion Series multispectral prism cameras](https://www.jai.com/products/product-lines/fusion-series-2-sensor-area-scan/) — two/three waveband prism cameras, custom 405–1000 nm bands as narrow as 25 nm.
- [SILIOS — CMS multispectral camera series](https://www.silios.com/cms-series) — compact mosaic multispectral cameras with 8 spectral bands plus B&W channel.

### Stacked and hybrid sensor references

- [IS&T paper — Foveon X3 image sensors](https://www.imaging.org/common/uploaded%20files/pdfs/Papers/2006/ICIS-0-736/33720.pdf) — X3 uses natural silicon color absorption properties and stacked pixels.
- [Sigma — official Foveon sensor development update](https://www.sigma-global.com/en/news/2021/02/19/12739/) — official manufacturing-status context for full-frame Foveon development.
- [Sony Group — organic photoconductive RGB film stacked over silicon NIR ToF pixels](https://www.sony.com/en/SonyInfo/technology/publications/a-color-image-sensor-using-1.0-um-organic-photoconductive-film-pixels-stacked-on-4.0-um-si-pixels-for-near-infrared-time-of-flight-depth/) — stacked RGB + NIR ToF concept on one chip.
- [University of Illinois IDEALS — Bioinspired 9-band NIR multispectral camera](https://www.ideals.illinois.edu/items/129464) — spectral filter array with nine NIR passbands, visible filter for RGB, and vertically stacked photodiodes.
- [Google Patents — WO2018217770A2 multispectral imaging sensors and systems](https://patents.google.com/patent/WO2018217770A2/en) — superpixels, spectral filters, and vertically stacked photodetectors.

### Sensor physics and optical constraints

- [Hamamatsu Learning Center — Quantum Efficiency](https://hamamatsu.magnet.fsu.edu/articles/quantumefficiency.html) — silicon spectral sensitivity, photon absorption depth table, and 400–1100 nm silicon interaction discussion.
- [PVEducation — Optical properties of silicon](https://www.pveducation.org/pvcdrom/materials/optical-properties-of-silicon) — silicon absorption coefficient and band-gap absorption drop near 1100 nm.
- [Sony Semiconductor Solutions — UV image sensor technology](https://www.sony-semicon.com/en/technology/industry/uv.html) — quartz cover glass and UV-transmissive chip-on lens material requirements.
- [Sony Semiconductor Solutions — IMX487 UV sensor](https://www.sony-semicon.com/en/products/is/industry/uv.html) — commercial UV sensor reference.
- [International Image Sensor Society / Samsung — backside scattering for 940 nm QE](https://imagesensors.org/papers/10.60928/jldx-htqc/) — 940 nm QE improvement with acceptable inter-pixel crosstalk.
- [Laser Focus World — crosstalk challenges CMOS sensor design](https://www.laserfocusworld.com/optics/article/16556196/crosstalk-challenges-cmos-sensor-design) — optical and electrical crosstalk mechanisms in CMOS image sensors.
- [MDPI Electronics — snapshot multispectral imaging review](https://www.mdpi.com/2079-9292/12/4/812) — snapshot MSI/HSI implementation context.

### Fabrication and cost references

- [AnySilicon — understanding wafer cost](https://anysilicon.com/wafer-cost/) — wafer-cost drivers: node, complexity, options, and volume expectations.
- [MSOE CMOS cost lecture](https://faculty-web.msoe.edu/johnsontimoj/EE4980/files4980/cmos_cost.pdf) — 300 mm wafer-cost reference, die count, yield, packaging, and margin concepts.
- [AnySilicon — die-per-wafer calculator and formula](https://anysilicon.com/die-per-wafer-formula-free-calculators/) — die count and wafer utilization estimation.
- [OMNIVISION — Nyxel NIR technology](https://www.ovt.com/technologies/nyxel-technology/) — NIR QE improvement in commercial CMOS image sensors.

---

## 23. Bottom-Line Product Evaluation

HSC-1 has a strong product identity:

> **A calibrated RGB-plus-cross-spectral imaging module that captures a human-readable visible image and targeted spectral bands in one registered exposure.**

The closest commercial systems validate the demand for snapshot spectral imaging, RGB-NIR sensing, and simultaneous multispectral capture. HSC-1 combines those validated directions into a focused product: **single-chip alignment, one-lens operation, stacked visible anchor samples, pan/visible spatial detail, and calibrated 405–940 nm spectral outputs.**

The resulting niche is solid: richer than RGB-IR, more RGB-useful than many spectral mosaic cameras, smaller than prism systems, and more instrument-like than mobile spectral sensors.
