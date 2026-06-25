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

## Next Expansion

The next batch should extend the same SOP to SAR/CDAC/comparator/clock modules
from the candidate manifest. Modules with bus ports, same-name conflicts,
current contributions, model-device style code, or source/testbench behavior
should stay out of the release task tree until they have a dedicated contract
and parity evidence.
