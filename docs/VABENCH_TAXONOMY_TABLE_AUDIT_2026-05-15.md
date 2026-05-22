# vaBench Taxonomy Table Audit

Date: 2026-05-15

Scope:

- `docs/VABENCH_LEVEL_COVERAGE_TABLE.md`
- `docs/VABENCH_RELEASE_TAXONOMY.md`
- `docs/VABENCH_BASE_FUNCTION_REGISTRY.md`
- `docs/VABENCH_BASE_FUNCTION_REGISTRY.csv`

Question checked:

1. Whether the table has duplicated functions.
2. Whether each listed item deserves to be a benchmark function.
3. Whether naming matches analog/mixed-signal IC conventions.
4. Whether the category/function choices have external technical support.

## Verdict

The 9-category structure is usable, but the table needed naming cleanup and
stricter separation between:

- circuit functions,
- measurement/stimulus helper models,
- and EVAS/Spectre conformance semantics.

The table is now better framed as:

```text
current L1 seeds
  -> expansion L1 candidates
  -> L2 complete-circuit targets
  -> separate L0 conformance cases
```

Current scored seed count remains 28. The larger function list is an expansion
pool, not a release score.

## External Support Checked

| Source | What it supports |
| --- | --- |
| Accellera Verilog-AMS standard download page | Verilog-AMS is a behavioral language for analog and mixed-signal systems; this supports keeping the benchmark centered on behavioral AMS functions. |
| Cadence Analog Modeling with Verilog-A training page | Verilog-A is an analog-only subset used with Virtuoso/Spectre to model structures and behavior of analog systems/components; examples include DACs, voltage-controlled sources, and delay lines. |
| Cadence mixed-signal verification white paper | SPICE is the analog reference, while analog behavioral models are used for faster mixed-signal verification; this supports EVAS-as-fast-filter and Spectre-as-reference wording. |
| Kundert, "Modeling and Simulation of Jitter in Phase-Locked Loops" | PLLs are naturally modeled from behavioral blocks such as VCO/divider/PFD/loop-level abstractions for efficient high-level simulation. |
| Wang et al., "Thermo data-weighted average dynamic element matching encoder for current-steering DACs" | Supports DEM/DWA, thermometer encoding, unit-element DAC behavior, and INL/DNL/SFDR-oriented DAC coverage. |
| Li et al., "A 12-bit 30 MS/s SAR ADC with Foreground Digital Calibration Algorithm" | Supports SAR ADC, comparator offset, capacitor mismatch, and digital calibration as legitimate converter/calibration benchmark functions. |

Reference links:

- https://www.accellera.org/downloads/standards/v-ams
- https://www.cadence.com/en_US/home/training/all-courses/82086.html
- https://www.cadence.com/content/dam/cadence-www/global/en_US/documents/solutions/mixed-signal-verification-wp.pdf
- https://kenkundert.com/docs/aacd97.pdf
- https://www.jstage.jst.go.jp/article/elex/10/20/10_10.20130459/_pdf
- https://www.mdpi.com/2073-8994/12/1/165

## Audit Findings

| ID | Area | Issue | Decision |
| --- | --- | --- | --- |
| A001 | Data converter naming | "simple 4-bit binary-coded DAC", "ideal binary DAC", and "clocked binary DAC" could read as duplicate functions. | Keep the seed as "simple 4-bit binary-coded DAC" because it is a mathematical code/15 transfer model. Keep register-loaded or structural DAC variants only when their prompt/checker exercise distinct behavior. |
| A002 | Thermometer DAC naming | The historical `thermometer_dac` seed is not a true thermometer/unit-element DAC. | Keep it only after rename as binary-weighted DAC. Reserve "unit-element thermometer DAC" for a real thermometer-coded DAC. |
| A003 | Decoder naming | "analog-to-binary converter" was too broad for `d2b_4b`, which is actually a code-format generator. | Use "trim-code decoder for binary/one-hot/thermometer outputs". |
| A004 | Comparator naming | "strongarm-style behavior" was informal and inconsistent. | Use "StrongARM-style latch comparator behavior"; keep it explicitly behavioral, not transistor-level. |
| A005 | PFD naming | "PFD reset-race logic" sounded like a bug pattern rather than a circuit function. | Use "PFD UP/DN reset-race behavior" for the seed and "PFD UP/DN core" for expansion. |
| A006 | DEM/DWA duplication | Rotating selector, DWA pointer, no-overlap pointer, and wraparound can become duplicate rows if counted blindly. | Keep only behaviorally distinct pointer/selection rules. Treat pure wraparound boundary checks as conformance or checker cases unless the public task requires a full DEM encoder. |
| A007 | Measurement helper leakage | "metric artifact schema checker" is not a circuit function. | Remove it from L1 expansion candidates; keep it under L0 checker/artifact conformance. |
| A008 | Stimulus helper leakage | "bounded-step period guard source" is closer to conformance/source scheduling than a reusable source model. | Remove from L1 candidates unless rewritten as a source generator with a normal circuit contract. |
| A009 | Analog limiter duplication | "analog limiter" duplicated `voltage_clamp` unless it adds hysteresis, soft limiting, or different transfer behavior. | Rename expansion candidate to "hysteretic or soft limiter". |
| A010 | Differential output | "differential voltage output" is a topology/interface phrase, not enough by itself. | Rename to "differential output driver" if retained as a circuit function; otherwise demote to output-contract conformance. |
| A011 | Sample/hold duplication | `leaky_hold`, "sample-hold droop", and "held-value reset variant" overlapped. | Rename seed as "sample-and-hold with droop/leakage"; keep resettable S/H as a separate candidate only if reset behavior is central. |
| A012 | Basic logic necessity | Inverter/gates/DFF are valid voltage-domain event logic, but weak as paper-facing analog IC novelty. | Keep as low-priority expansion material or conformance/smoke support; do not let them dominate release coverage. |

## Edits Applied

| File | Applied change |
| --- | --- |
| `docs/VABENCH_LEVEL_COVERAGE_TABLE.md` | Renamed data-converter, comparator, PFD, DEM/DWA, measurement, stimulus, limiter, and sample/hold entries. Removed non-circuit helper wording from L1 candidates. |
| `docs/VABENCH_RELEASE_TAXONOMY.md` | Synced release names and expansion-pool wording with analog/mixed-signal IC terminology. |
| `docs/VABENCH_BASE_FUNCTION_REGISTRY.csv` | Updated release names for PFD, StrongARM comparator, binary-weighted DAC, and thermometer-code decoder. |
| `docs/VABENCH_BASE_FUNCTION_REGISTRY.md` | Updated high-risk thermometer-DAC wording. |

## Remaining Review Questions

| Question | Recommendation |
| --- | --- |
| Should basic gates count as benchmark functions? | Only if the release explicitly wants voltage-domain event-logic coverage. Otherwise keep them as smoke/conformance support. |
| Should threshold/window detectors be comparator or signal-conditioning tasks? | Put them in comparator/decision circuits when output is a binary decision; use signal conditioning only when output remains analog. |
| Should gain calibration be L1 or L2? | A standalone bounded trim controller is L1; gain estimator + amplifier + controller convergence is L2. |
| Should DWA wraparound be a task? | It should be L1 only if the task asks for a full pointer generator/encoder. A single wraparound edge case should be L0/conformance or a checker window. |
| Should ADPLL/CPPLL smoke tasks be release tasks? | Only after decomposition into clear components and a checker that verifies lock, ratio hop, or reacquisition behavior. |

## Promotion Criteria For New Functions

An expansion candidate should be promoted only when all are true:

1. The public prompt names a real circuit function, not just a simulator
   primitive or helper artifact.
2. The checker observes behavior unique to that function.
3. The name is standard enough for analog/mixed-signal IC readers.
4. It has gold Verilog-A/testbench assets and EVAS/Spectre certification.
5. It is not a near-duplicate of an existing seed unless the new variant adds
   a meaningful architecture dimension such as clocking, segmentation,
   unit-element selection, mismatch, hysteresis, leakage, or loop closure.
