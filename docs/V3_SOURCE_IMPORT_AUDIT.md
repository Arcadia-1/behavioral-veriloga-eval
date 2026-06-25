# V3 Source Import Audit

This note records the first certified import from the deduplicated historical
Verilog-A corpus into `benchmark-vabench-release-v3`.

## Corpus Screen

- Original aggregate: 1663 module definitions.
- Exact-deduplicated aggregate: 1097 module definitions.
- Mechanical clean candidate pool: 292 modules under the current stricter
  source-import filter for voltage-only, scalar-port, non-device, non-testbench,
  non-conflicting modules.
- A broader manual-review pool remains available, but those modules need
  source-specific semantic contracts before they can be promoted.

## Import SOP

Each imported task must satisfy four gates before it is considered submit-ready:

- Useful scenario: the primitive is reusable in converter, timing, or
  mixed-signal behavioral flows.
- Reasonable task: the DUT is scoped to one public module with fixed port order
  and a clear waveform contract.
- Complete tests: visible smoke plus hidden EVAS and Spectre runs on the same
  deterministic testbench.
- Fair evaluation: stable-window or event-level behavior checks; no raw
  simulator timestep equality requirement.

## Certified Pilot Batch

The first submitted batch intentionally contains four tasks, not the larger
30-50 candidate batch. A generated 40-task scaffold was rejected during audit
because it did not yet provide semantic evaluation strong enough for release.

| Task | Source | Scenario | EVAS | Spectre | Parity |
|---|---|---|---|---|---|
| `112-source-clocked-sar-comparator` | `caiyizeng25/L3_SAR_comparator_ideal.va` | clocked SAR comparator decision/reset | PASS | PASS | passed |
| `113-source-clocked-dac-restore-4b` | `wangxy/DAC_restore_4bit.va` | clocked 4-bit mid-rise DAC reconstruction | PASS | PASS | passed |
| `114-source-sample-and-hold-ideal` | `wangx/sah_ideal.va` | rising-edge sample-and-hold | PASS | PASS | passed |
| `115-source-single-shot-pulse` | `wangx/single_shot.va` | fixed-width one-shot pulse generator | PASS | PASS | passed |

Evidence artifacts:

- `WORK/source-import-pilot-evas/summary.json`
- `WORK/source-import-pilot-spectre/summary.json`

Spectre was run with the SUI direct backend on `zhangz@101.6.68.147` in AX mode.
No EVAS/Spectre behavioral discrepancy was observed in this pilot batch, so no
EVAS issue was filed.


## Certified Batch 2

The second submitted batch adds six more tasks under the same SOP. One candidate (`117-source-bipolar-dac-4b-continuous`) initially failed EVAS semantic checking because the raw continuous ternary source did not update under EVAS as written; it was repaired into an event-updated equivalent before certification. Spectre and EVAS then agreed, so no EVAS issue was filed.

| Task | Source | Scenario | EVAS | Spectre | Parity |
|---|---|---|---|---|---|
| `116-source-clocked-comparator-reset-low` | `caiyizeng25/comp_ideal.va` | clocked comparator with falling-clock reset low | PASS | PASS | passed |
| `117-source-bipolar-dac-4b-continuous` | `shigao/DAC4bit_1.va` | 4-bit bipolar DAC level reconstruction | PASS | PASS | passed |
| `118-source-clocked-dac-restore-7b` | `wangxy/DAC_restore_7bit.va` | clocked 7-bit mid-rise DAC reconstruction | PASS | PASS | passed |
| `119-source-crossing-pulse-detector` | `zhangm/crossing_detector.va` | pulse generation after either input crossing | PASS | PASS | passed |
| `120-source-not-gate-voltage` | `wangx/not_gate.va` | voltage-domain inverter | PASS | PASS | passed |
| `121-source-dff-reset-voltage` | `hexy/dff_rst.va` | DFF sample-on-clock with reset behavior | PASS | PASS | passed |

Evidence artifacts:

- `WORK/source-import-batch2-evas/summary.json`
- `WORK/source-import-batch2-spectre/summary.json`

## Certified Batch 3

The third submitted batch adds six more source-import tasks. A low-power
comparator-ready candidate was screened out before submission: its stable logic
matched in EVAS and Spectre, but the generic edge-parity gate exposed a 50 ps
`transition()` timing difference on `RDY`. It remains only as scratch evidence
under `WORK/`; the submitted batch below has full checker and parity pass.

| Task | Source | Scenario | EVAS | Spectre | Parity |
|---|---|---|---|---|---|
| `122-source-offset-search-comparator` | `caiyizeng25/V_comp_offset.va` | comparator-offset binary search stimulus | PASS | PASS | passed |
| `123-source-start-gated-offset-search` | `shigao/V_comparator_offset.va` | start-gated comparator-offset search | PASS | PASS | passed |
| `124-source-comp-os-detect` | `guoxy/ideal_COMP_OS_DETECT.va` | successive-approximation comparator offset detect | PASS | PASS | passed |
| `125-source-clocked-dac-4b-binary` | `wangxy/DAC_4b.va` | clocked 4-bit binary-weighted DAC reconstruction | PASS | PASS | passed |
| `126-source-latched-comparator-delay` | `jielu/L2_comp.va` | supply-referenced latched comparator with output delay | PASS | PASS | passed |
| `127-source-sar-weighted-sum` | `shigao/V_SAR_sum.va` | SAR non-binary weighted residue/code reconstruction | PASS | PASS | passed |

Evidence artifacts:

- `WORK/source-import-batch3-evas/summary.json`
- `WORK/source-import-batch3-spectre/summary.json`

## Certified Batch 4

The fourth submitted batch adds nine more tasks and broadens the source-import
coverage beyond DAC/comparator primitives into logic, selection, timing,
differential buffering, peak holding, and SAR residue update behavior.

Two candidates were screened out before submission: `gaoya/L4_DELAY_VA.va` and
`huangsy/PD_XOR.va` both passed stable semantic checks, but the generic digital
edge parity gate exposed tens of picoseconds of `transition()` edge timing
difference. They remain scratch evidence only under `WORK/`. The submitted
`132-source-max-detector-hold` task also avoids the source model's dynamic
`cross(V(in)-maxin)` trigger because that form is not a stable EVAS/Spectre
parity contract; it preserves the max-hold behavior with continuous state
update instead.

| Task | Source | Scenario | EVAS | Spectre | Parity |
|---|---|---|---|---|---|
| `128-source-two-input-and-gate` | `tangxy/and2.va` | voltage-domain two-input AND logic | PASS | PASS | passed |
| `129-source-two-input-xor-gate` | `tangxy/xor2.va` | voltage-domain two-input XOR logic | PASS | PASS | passed |
| `130-source-analog-mux-threshold` | `wangx/analog_mux.va` | threshold-controlled analog mux | PASS | PASS | passed |
| `131-source-two-bit-counter-marker` | `zengsy/Counter_2b_VA.va` | marker emitted every fourth clock edge | PASS | PASS | passed |
| `132-source-max-detector-hold` | `hexy/maxDetector.va` | monotonic peak/max voltage hold | PASS | PASS | passed |
| `133-source-time-diff-detector` | `yangqihan/ideal_TIME_DIFF_DETECTOR.va` | edge time-difference to bounded voltage | PASS | PASS | passed |
| `134-source-differential-buffer` | `liudongyang/TOOL_buffer.va` | differential analog pass-through buffer | PASS | PASS | passed |
| `135-source-two-input-or-gate` | `tangxy/or2.va` | voltage-domain two-input OR logic | PASS | PASS | passed |
| `136-source-sar-cdac-residue` | `caiyizeng25/L3_SAR2_cdac_7b_ideal.va` | sample-and-step SAR CDAC residue update | PASS | PASS | passed |

Evidence artifacts:

- `WORK/source-import-batch4-evas/summary.json`
- `WORK/source-import-batch4-spectre/summary.json`

## Next Expansion

The next batch should extend the same SOP to SAR/CDAC/comparator/clock modules
from the candidate manifest. Modules with bus ports, same-name conflicts,
current contributions, model-device style code, or source/testbench behavior
should stay out of the release task tree until they have a dedicated contract
and parity evidence.
