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

## Certified Batch 5

The fifth submitted batch adds five logic primitive tasks and brings the
certified source-import count to 30 tasks, the lower bound of the planned first
batch. These tasks are intentionally small but still useful as voltage-domain
truth-table fixtures: they exercise stable event-triggered logic updates,
multi-input logic contracts, and basic digital control blocks used around ADC
and timing behavioral models.

| Task | Source | Scenario | EVAS | Spectre | Parity |
|---|---|---|---|---|---|
| `137-source-two-input-nand-gate` | `tangxy/nand2.va` | voltage-domain two-input NAND logic | PASS | PASS | passed |
| `138-source-two-input-nor-gate` | `tangxy/nor2.va` | voltage-domain two-input NOR logic | PASS | PASS | passed |
| `139-source-three-input-and-gate` | `wangx/and3.va` | three-input AND control logic | PASS | PASS | passed |
| `140-source-three-input-or-gate` | `wangx/or3.va` | three-input OR control logic | PASS | PASS | passed |
| `141-source-three-input-xor-gate` | `wangx/xor3.va` | three-input parity/XOR logic | PASS | PASS | passed |

Evidence artifacts:

- `WORK/source-import-batch5-evas/summary.json`
- `WORK/source-import-batch5-spectre/summary.json`

## Certified Batch 6

The sixth submitted batch adds six continuous voltage-domain primitives from
the deduplicated source corpus. This extends the source-import coverage beyond
logic fixtures into reusable signal-conditioning blocks: dB attenuation,
single-ended and differential deadband extraction, hard clamping, smooth
comparison, and supply-referenced limiting.

| Task | Source | Scenario | EVAS | Spectre | Parity |
|---|---|---|---|---|---|
| `142-source-attenuator-gain` | `wangx/attenuator.va` | decibel-configured voltage attenuation | PASS | PASS | passed |
| `143-source-deadband-window` | `wangx/deadband.va` | windowed deadband error extraction | PASS | PASS | passed |
| `144-source-differential-deadband` | `wangx/deadband_diffamp.va` | differential deadband amplifier with leakage bias | PASS | PASS | passed |
| `145-source-hard-voltage-clamp` | `wangx/hard_voltage_clamp.va` | hard-limited voltage clamp | PASS | PASS | passed |
| `146-source-smooth-comparator-tanh` | `chenr/comparator_ideal.va` | continuous tanh comparator macro model | PASS | PASS | passed |
| `147-source-limiter-rails` | `zhangm/LIMITER.va` | supply-referenced limiter with programmable rail margins | PASS | PASS | passed |

Evidence artifacts:

- `WORK/source-import-batch6-evas/summary.json`
- `WORK/source-import-batch6-spectre/summary.json`

Batch timings:

- EVAS hidden: 6/6 PASS, wallclock 0.426 s.
- Spectre AX hidden plus EVAS/Spectre parity: 6/6 passed, wallclock 12.511 s
  with 6-way parallel submission.

## Certified Batch 7

The seventh submitted batch adds eight function-style voltage-domain behavioral
primitives. These cover arithmetic and signal-conditioning contracts that are
useful inside converter and mixed-signal macro models without requiring KCL,
device models, or current contributions.

One `amp.va`-derived candidate was repaired before certification: the original
parameterized offset form triggered an EVAS frontend compile failure, so the
submitted task fixes the gain and offset values directly in the task contract.
The certified task still checks the offset-gain behavior and passes EVAS,
Spectre AX, and parity.

| Task | Source | Scenario | EVAS | Spectre | Parity |
|---|---|---|---|---|---|
| `148-source-absolute-value` | `wangx/absolute_value.va` | absolute-value conditioning for bipolar voltages | PASS | PASS | passed |
| `149-source-offset-gain-amplifier` | `wangx/amp.va` | fixed offset-gain linear amplifier | PASS | PASS | passed |
| `150-source-safe-voltage-divider` | `wangx/divider.va` | bounded denominator division | PASS | PASS | passed |
| `151-source-polynomial-differential-vcvs` | `cuiyl/LI_VCVS_NLIN.va` | nonlinear differential VCVS with saturation | PASS | PASS | passed |
| `152-source-differential-gain-driver` | `wangx/diffdriver.va` | symmetric differential output driver | PASS | PASS | passed |
| `153-source-limiting-differential-amplifier` | `wangx/limiting_diffamp.va` | clamped differential gain block | PASS | PASS | passed |
| `154-source-analog-multiplier` | `wangx/multiplier.va` | two-input analog multiplier | PASS | PASS | passed |
| `155-source-three-way-threshold-mux` | `wangx/multiplexer.va` | three-way analog mux selected by differential thresholds | PASS | PASS | passed |

Evidence artifacts:

- `WORK/source-import-batch7-evas/summary.json`
- `WORK/source-import-batch7-spectre/summary.json`

Batch timings:

- EVAS hidden: 8/8 PASS, wallclock 0.510 s.
- Spectre AX hidden plus EVAS/Spectre parity: 8/8 passed, wallclock 14.712 s
  with 8-way parallel submission.

## Certified Batch 8

The eighth submitted batch adds six continuous mixed-signal primitives and
brings the certified source-import count to 50 tasks. These tasks emphasize
differential analog behavior and nonlinear signal conditioning while staying
inside EVAS's voltage-domain scope.

| Task | Source | Scenario | EVAS | Spectre | Parity |
|---|---|---|---|---|---|
| `156-source-differential-amplifier-core` | `wangx/diffamp.va` | single-ended output differential amplifier | PASS | PASS | passed |
| `157-source-logarithmic-amplifier` | `wangx/log_amp.va` | bounded logarithmic measurement | PASS | PASS | passed |
| `158-source-soft-voltage-clamp` | `wangx/soft_voltage_clamp.va` | smooth exponential voltage limiting | PASS | PASS | passed |
| `159-source-variable-gain-differential-amplifier` | `wangx/vargain_diffamp.va` | differential amplifier with differential gain control | PASS | PASS | passed |
| `160-source-voltage-controlled-gain-amplifier` | `wangx/vc_vg_diffamp.va` | voltage-controlled differential gain block | PASS | PASS | passed |
| `161-source-ideal-differential-opamp` | `taoy/OPAMP.va` | ideal differential output opamp around common-mode | PASS | PASS | passed |

Evidence artifacts:

- `WORK/source-import-batch8-evas/summary.json`
- `WORK/source-import-batch8-spectre/summary.json`

Batch timings:

- EVAS hidden: 6/6 PASS, wallclock 0.408 s.
- Spectre AX hidden plus EVAS/Spectre parity: 6/6 passed, wallclock 12.163 s
  with 6-way parallel submission.

## Certified Batch 9

The ninth submitted batch adds five voltage-domain digital arithmetic and state
primitives from the same source corpus. These tasks are intended to exercise
truth-table and latch-state behavior used around converter control logic, not
gate-delay characterization. Their parity policy therefore checks stable logic
and waveform mismatch while ignoring small simulator-dependent output edge
time deltas.

| Task | Source | Scenario | EVAS | Spectre | Parity |
|---|---|---|---|---|---|
| `162-source-half-adder-logic` | `wangx/half_adder.va` | one-bit half adder | PASS | PASS | passed |
| `163-source-full-adder-logic` | `wangx/full_adder.va` | one-bit full adder with carry-in | PASS | PASS | passed |
| `164-source-half-subtractor-logic` | `wangx/half_subtractor.va` | one-bit half subtractor | PASS | PASS | passed |
| `165-source-full-subtractor-logic` | `wangx/full_subtractor.va` | one-bit full subtractor with borrow-in | PASS | PASS | passed |
| `166-source-rs-latch-voltage` | `wangx/rs_ff.va` | set/reset voltage-domain latch | PASS | PASS | passed |

Evidence artifacts:

- `WORK/source-import-batch9-evas/summary.json`
- `WORK/source-import-batch9-spectre/summary.json`

Batch timings:

- EVAS hidden: 5/5 PASS, wallclock 1.171 s.
- Spectre AX hidden plus EVAS/Spectre parity: 5/5 passed, wallclock 12.526 s
  with 5-way parallel submission.

## Certified Batch 10

The tenth submitted batch adds six source-import tasks focused on converter
utility blocks and sampled state behavior. These are more integration-relevant
than another pure logic batch: differential ADC quantization, differential DAC
reconstruction, sampled analog delay, clocked muxing, clock division, and flash
thermometer post-processing. Their fairness contract is stable sampled state,
not exact solver edge placement.

| Task | Source | Scenario | EVAS | Spectre | Parity |
|---|---|---|---|---|---|
| `167-source-ideal-adc-4bit-quantizer` | `zhaoh/IDEAL_ADC.va` | rising-edge sampled 4-bit differential ADC quantizer | PASS | PASS | passed |
| `168-source-ideal-dac-4bit-differential` | `zhaoh/IDEAL_DAC_V.va` | falling-edge sampled 4-bit differential DAC reconstruction | PASS | PASS | passed |
| `169-source-two-period-sample-delay` | `zhangzixuan/_tool_delay_two_period.va` | one-sample delayed analog pipeline register | PASS | PASS | passed |
| `170-source-clocked-four-input-mux` | `zhangm/MUX4T1.va` | falling-edge latched four-input analog mux | PASS | PASS | passed |
| `171-source-divide-by-eight-clock` | `huangsy/DIV8.va` | divide-by-eight 50% duty-cycle clock model | PASS | PASS | passed |
| `172-source-flash-thermometer-centered-sum` | `zhaoty/TB_flash.va` | centered flash thermometer-code summary | PASS | PASS | passed |

Evidence artifacts:

- `WORK/source-import-batch10-evas/summary.json`
- `WORK/source-import-batch10-spectre/summary.json`

Batch timings:

- Visible smoke: 6/6 PASS.
- EVAS hidden: 6/6 PASS, wallclock 2.014 s.
- Spectre AX hidden plus EVAS/Spectre parity: 6/6 passed, wallclock 12.648 s
  with 6-way parallel submission after explicitly clearing
  `VAEVAS_SUI_PROXY_JUMP` for the direct `zhangz@101.6.68.147` host.

## Next Expansion

The next batch should extend the same SOP to SAR/CDAC/comparator/clock modules
from the candidate manifest. Modules with bus ports, same-name conflicts,
current contributions, model-device style code, or source/testbench behavior
should stay out of the release task tree until they have a dedicated contract
and parity evidence.
