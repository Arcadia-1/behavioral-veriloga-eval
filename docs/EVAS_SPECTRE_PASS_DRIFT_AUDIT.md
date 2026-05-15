# EVAS/Spectre PASS Drift Audit

Date: 2026-05-14

## Scope

- EVAS root: `/Users/bucketsran/Documents/TsingProject/vaEvas/behavioral-veriloga-eval/results/vabench-main-v1-main120-gold-evas-2026-05-08`
- Spectre root: `/Users/bucketsran/Documents/TsingProject/vaEvas/behavioral-veriloga-eval/results/vabench-main-v1-main120-gold-spectre-jin-2026-05-08`
- Only tasks where both backends report `PASS` are included.
- Drift means the public checker passed on both backends, but `checker_result.notes` differ.

## Summary

- Drifted task forms: 52
- Deduplicated circuit groups: 14
- Priority counts by task form: {'P0-resolved': 4, 'P1-resolved-benchmark': 3, 'P1-resolved-checker': 12, 'P2-checker': 12, 'P2-tolerance': 13, 'P2-watch': 4, 'P3-noop': 4}
- Class counts by task form: {'comparator_reset_window_numeric_drift': 1, 'continuous_decay_numeric_drift': 4, 'continuous_integration_numeric_drift': 4, 'continuous_response_numeric_drift': 4, 'event_timing_quantization_drift': 4, 'float_format_only': 4, 'resolved_evas_startup_semantics': 4, 'stable_decision_checker_and_stop_time_repair': 3, 'stable_sequence_checker_repair': 12, 'time_fraction_sampling_drift': 12}

## Deduplicated Drift Table

| Base ID | Forms | Priority | Class | Stable check | EVAS note | Spectre note | Action |
| --- | --- | --- | --- | --- | --- | --- | --- |
| vbm1_barrel_pointer_window | bugfix,dut,e2e,tb | P1-resolved-checker | stable_sequence_checker_repair | match | count_range=(1, 2) | count_range=(2, 2) | materialize checks.yaml with fixed-time state-sequence checks instead of raw sample counts |
| vbm1_edge_detector | bugfix,dut,e2e,tb | P2-checker | time_fraction_sampling_drift | - | pulse_edges=4 high_frac=0.159 | pulse_edges=4 high_frac=0.141 | prefer time-weighted pulse width over row-fraction summaries |
| vbm1_element_shuffler | bugfix,dut,e2e,tb | P1-resolved-checker | stable_sequence_checker_repair | match | highs={'out0': 69, 'out1': 90, 'out2': 88, 'out3': 45} | highs={'out0': 81, 'out1': 92, 'out2': 90, 'out3': 46} | materialize checks.yaml with fixed-time state-sequence checks instead of raw sample counts |
| vbm1_first_order_lowpass | bugfix,dut,e2e,tb | P2-tolerance | continuous_response_numeric_drift | - | early=0.450 late=0.798 | early=0.449 late=0.798 | keep analog-value tolerances; no EVAS fix unless drift grows across more analog kernels |
| vbm1_leaky_hold | bugfix,dut,e2e,tb | P2-watch | continuous_decay_numeric_drift | - | high=0.655 decayed=0.265 rst=0.000 | high=0.659 decayed=0.263 rst=0.000 | keep tolerance checks and reuse the $abstime/decay conformance regression for sharper coverage |
| vbm1_lock_detector | bugfix,dut,e2e,tb | P2-checker | time_fraction_sampling_drift | - | early_high=0.000 late_high=0.789 | early_high=0.000 late_high=0.753 | use time-weighted late-lock duration or lock edge time instead of row fraction |
| vbm1_one_shot_timer | bugfix,dut,e2e,tb | P2-checker | time_fraction_sampling_drift | - | trig_edges=5 pulse_edges=5 pulse_frac=0.1517 | trig_edges=5 pulse_edges=5 pulse_frac=0.1519 | prefer time-weighted pulse width over row-fraction summaries |
| vbm1_pfd_reset_race | bugfix,dut,e2e,tb | P2-tolerance | event_timing_quantization_drift | - | up_first=0.0100 dn_first=0.0000 up_second=0.0000 dn_second=0.0100 up_pulses_first=5 dn_pulses_second=5 overlap_frac=0.0000 | up_first=0.0101 dn_first=0.0000 up_second=0.0000 dn_second=0.0102 up_pulses_first=5 dn_pulses_second=5 overlap_frac=0.0000 | keep tolerance-based timing checks; add atomic regression only if pulse counts diverge |
| vbm1_resettable_integrator | bugfix,dut,e2e,tb | P2-tolerance | continuous_integration_numeric_drift | - | reset=0.000 mid1=0.126 mid2=0.326 late=0.056 | reset=0.000 mid1=0.129 mid2=0.328 late=0.059 | keep analog-value tolerances; consider a dedicated integrator regression if future candidates flip pass/fail |
| vbm1_rotating_element_selector | bugfix,dut,e2e,tb | P1-resolved-checker | stable_sequence_checker_repair | match | highs={'sel0': 69, 'sel1': 90, 'sel2': 88, 'sel3': 45} | highs={'sel0': 81, 'sel1': 92, 'sel2': 90, 'sel3': 46} | materialize checks.yaml with fixed-time state-sequence checks instead of raw sample counts |
| vbm1_strongarm_comparator_behavior | dut,e2e,tb | P1-resolved-benchmark | stable_decision_checker_and_stop_time_repair | match | pre_high_frac=0.622 post_low_frac=1.000 | pre_high_frac=0.643 post_low_frac=1.000 | use fixed decision sample points and keep the source testbench stop time away from source edges |
| vbm1_strongarm_comparator_behavior | bugfix | P2-tolerance | comparator_reset_window_numeric_drift | - | reset_outp_max=0.000 reset_outn_max=0.000 high_outp=1.000 high_outn=1.000 low_outp=0.984 low_outn=0.984 | reset_outp_max=0.000 reset_outn_max=0.000 high_outp=1.000 high_outn=1.000 low_outp=0.985 low_outn=0.985 | keep reset-window numeric tolerance; no EVAS fix unless reset/decision classification changes |
| vbm1_thermometer_dac | bugfix,dut,e2e,tb | P3-noop | float_format_only | - | samples=[(0, 0.0), (2, 0.12), (4, 0.24), (6, 0.36), (8, 0.48), (10, 0.6), (12, 0.72), (15, 0.9)] span=0.900 max_err=0.000 mono=True | samples=[(0, 0.0), (2, 0.12), (4, 0.24), (6, 0.36), (8, 0.48), (10, 0.6), (12, 0.7200000000000001), (15, 0.9)] span=0.900 max_err=0.000 mono=True | normalize numeric formatting in reports if desired |
| vbm1_vco_phase_integrator | bugfix,dut,e2e,tb | P0-resolved | resolved_evas_startup_semantics | - | early_edges=2 late_edges=4 phase_span=0.995 | early_edges=2 late_edges=4 phase_span=0.992 | keep EVAS timer(0)+transition regression; regenerate gold EVAS evidence |

## Root-Cause Notes

### `vbm1_barrel_pointer_window`

- Priority/class: `P1-resolved-checker` / `stable_sequence_checker_repair`
- Cause: The repaired stable checker gives identical EVAS/Spectre state sequences; only the historical row-count notes drift.
- Action: materialize checks.yaml with fixed-time state-sequence checks instead of raw sample counts
- Numeric delta: `1.0`
- CSV summary: rows 298 vs 309; stop 1.3000012207e-07 vs 1.3e-07; max_feature_delta=0.0251
- Waveform flags: -
- Stable checker: `match`
- Stable EVAS note: window_sequence=12,23,03,01,12,23 expected=12,23,03,01,12,23
- Stable Spectre note: window_sequence=12,23,03,01,12,23 expected=12,23,03,01,12,23

### `vbm1_edge_detector`

- Priority/class: `P2-checker` / `time_fraction_sampling_drift`
- Cause: Pulse count matches; high fraction differs because EVAS and Spectre save different points around transitions.
- Action: prefer time-weighted pulse width over row-fraction summaries
- Numeric delta: `0.018000000000000016`
- CSV summary: rows 402 vs 396; stop 1.8e-07 vs 1.8e-07; max_feature_delta=0.03792
- Waveform flags: sig hi_frac 0.331 vs 0.293
- Stable checker: `-`
- Stable EVAS note: -
- Stable Spectre note: -

### `vbm1_element_shuffler`

- Priority/class: `P1-resolved-checker` / `stable_sequence_checker_repair`
- Cause: The repaired stable checker gives identical EVAS/Spectre state sequences; only the historical row-count notes drift.
- Action: materialize checks.yaml with fixed-time state-sequence checks instead of raw sample counts
- Numeric delta: `12.0`
- CSV summary: rows 298 vs 309; stop 1.3000012207e-07 vs 1.3e-07; max_feature_delta=0.03059
- Waveform flags: out0 hi_frac 0.232 vs 0.262
- Stable checker: `match`
- Stable EVAS note: active_sequence=1,2,3,0,1,2 expected=1,2,3,0,1,2
- Stable Spectre note: active_sequence=1,2,3,0,1,2 expected=1,2,3,0,1,2

### `vbm1_first_order_lowpass`

- Priority/class: `P2-tolerance` / `continuous_response_numeric_drift`
- Cause: Lowpass sample values differ by about 1 mV, consistent with solver/sample-grid differences.
- Action: keep analog-value tolerances; no EVAS fix unless drift grows across more analog kernels
- Numeric delta: `0.0010000000000000009`
- CSV summary: rows 1437 vs 614; stop 1.6e-07 vs 1.6e-07; max_feature_delta=0.05389
- Waveform flags: vin hi_frac 0.971 vs 0.919; vout hi_frac 0.875 vs 0.821
- Stable checker: `-`
- Stable EVAS note: -
- Stable Spectre note: -

### `vbm1_leaky_hold`

- Priority/class: `P2-watch` / `continuous_decay_numeric_drift`
- Cause: Hold/decay values differ by a few mV; related to continuous decay sampling but not a binary mismatch here.
- Action: keep tolerance checks and reuse the $abstime/decay conformance regression for sharper coverage
- Numeric delta: `0.0040000000000000036`
- CSV summary: rows 621 vs 373; stop 1.7000012207e-07 vs 1.7e-07; max_feature_delta=0.1178
- Waveform flags: rst hi_frac 0.069 vs 0.137; vout hi_frac 0.375 vs 0.257
- Stable checker: `-`
- Stable EVAS note: -
- Stable Spectre note: -

### `vbm1_lock_detector`

- Priority/class: `P2-checker` / `time_fraction_sampling_drift`
- Cause: Lock assertion behavior matches; late_high differs with accepted-point density.
- Action: use time-weighted late-lock duration or lock edge time instead of row fraction
- Numeric delta: `0.03600000000000003`
- CSV summary: rows 647 vs 845; stop 3.2000012207e-07 vs 3.2e-07; max_feature_delta=0.05336
- Waveform flags: ref_clk hi_frac 0.439 vs 0.492
- Stable checker: `-`
- Stable EVAS note: -
- Stable Spectre note: -

### `vbm1_one_shot_timer`

- Priority/class: `P2-checker` / `time_fraction_sampling_drift`
- Cause: Trigger and pulse edge counts match; only sampled high fraction differs slightly.
- Action: prefer time-weighted pulse width over row-fraction summaries
- Numeric delta: `0.00020000000000000573`
- CSV summary: rows 573 vs 553; stop 2.6e-07 vs 2.6e-07; max_feature_delta=0.0132
- Waveform flags: -
- Stable checker: `-`
- Stable EVAS note: -
- Stable Spectre note: -

### `vbm1_pfd_reset_race`

- Priority/class: `P2-tolerance` / `event_timing_quantization_drift`
- Cause: Pulse counts and overlap classification match; timing fractions differ at the fourth decimal place.
- Action: keep tolerance-based timing checks; add atomic regression only if pulse counts diverge
- Numeric delta: `0.00020000000000000052`
- CSV summary: rows 30132 vs 30125; stop 3e-07 vs 3e-07; max_feature_delta=0.001094
- Waveform flags: -
- Stable checker: `-`
- Stable EVAS note: -
- Stable Spectre note: -

### `vbm1_resettable_integrator`

- Priority/class: `P2-tolerance` / `continuous_integration_numeric_drift`
- Cause: Windowed analog means differ by a few mV while reset and trend semantics agree.
- Action: keep analog-value tolerances; consider a dedicated integrator regression if future candidates flip pass/fail
- Numeric delta: `0.0030000000000000027`
- CSV summary: rows 1431 vs 682; stop 3.2000012207e-07 vs 3.2e-07; max_feature_delta=0.1095
- Waveform flags: rst hi_frac 0.080 vs 0.189; vout hi_frac 0.341 vs 0.302
- Stable checker: `-`
- Stable EVAS note: -
- Stable Spectre note: -

### `vbm1_rotating_element_selector`

- Priority/class: `P1-resolved-checker` / `stable_sequence_checker_repair`
- Cause: The repaired stable checker gives identical EVAS/Spectre state sequences; only the historical row-count notes drift.
- Action: materialize checks.yaml with fixed-time state-sequence checks instead of raw sample counts
- Numeric delta: `12.0`
- CSV summary: rows 298 vs 309; stop 1.3000012207e-07 vs 1.3e-07; max_feature_delta=0.03059
- Waveform flags: sel0 hi_frac 0.232 vs 0.262
- Stable checker: `match`
- Stable EVAS note: active_sequence=1,2,3,0,1,2 expected=1,2,3,0,1,2
- Stable Spectre note: active_sequence=1,2,3,0,1,2 expected=1,2,3,0,1,2

### `vbm1_strongarm_comparator_behavior`

- Priority/class: `P1-resolved-benchmark` / `stable_decision_checker_and_stop_time_repair`
- Cause: The repaired stable checker gives identical EVAS/Spectre decisions; the source-controlled testbench now avoids ending on the 4 ns source boundary.
- Action: use fixed decision sample points and keep the source testbench stop time away from source edges
- Numeric delta: `0.02100000000000002`
- CSV summary: rows 839 vs 842; stop 4.00000099461e-09 vs 4e-09; max_feature_delta=0.9
- Waveform flags: clk final 0 vs 0.9 hi_frac 0.477 vs 0.507; out_n final 0.45 vs 0.9
- Stable checker: `match`
- Stable EVAS note: decision_samples=PPNN expected=PPNN
- Stable Spectre note: decision_samples=PPNN expected=PPNN

### `vbm1_strongarm_comparator_behavior`

- Priority/class: `P2-tolerance` / `comparator_reset_window_numeric_drift`
- Cause: The bugfix-form reset and decision windows agree; only low-level analog maxima differ by about 1 mV.
- Action: keep reset-window numeric tolerance; no EVAS fix unless reset/decision classification changes
- Numeric delta: `0.0010000000000000009`
- CSV summary: rows 4011 vs 4031; stop 8.00000048828e-08 vs 8e-08; max_feature_delta=0.006941
- Waveform flags: -
- Stable checker: `-`
- Stable EVAS note: -
- Stable Spectre note: -

### `vbm1_thermometer_dac`

- Priority/class: `P3-noop` / `float_format_only`
- Cause: The only difference is Python/Spectre float rendering such as 0.72 vs 0.7200000000000001.
- Action: normalize numeric formatting in reports if desired
- Numeric delta: `1.1102230246251565e-16`
- CSV summary: rows 345 vs 432; stop 1.65e-07 vs 1.65e-07; max_feature_delta=0.01709
- Waveform flags: -
- Stable checker: `-`
- Stable EVAS note: -
- Stable Spectre note: -

### `vbm1_vco_phase_integrator`

- Priority/class: `P0-resolved` / `resolved_evas_startup_semantics`
- Cause: EVAS historically saved an artificial t=0 transition ramp; fixed by initial-condition transition semantics.
- Action: keep EVAS timer(0)+transition regression; regenerate gold EVAS evidence
- Numeric delta: `0.0030000000000000027`
- CSV summary: rows 1082 vs 554; stop 1.8000012207e-07 vs 1.8e-07; max_feature_delta=0.0194
- Waveform flags: -
- Stable checker: `-`
- Stable EVAS note: -
- Stable Spectre note: -

## Interpretation

- `P0-resolved` means the drift exposed an EVAS conformance bug that has already been fixed and should remain covered by an atomic regression.
- `P1-checker` or `P1-benchmark` means the historical benchmark/checker can still pass while measuring a simulator-grid artifact. These should be corrected before publishing main120 as audited benchmark material.
- `P1-resolved-checker` means a source-controlled stable checker now exists for materialization; regenerate result evidence when those tasks are promoted.
- `P1-resolved-benchmark` means the source-controlled benchmark/checker path has been hardened; regenerate result evidence when the task is rerun.
- `P2-*` means the current evidence looks like tolerable sampling or analog numeric drift, but the checker should encode explicit tolerances rather than exact note strings.
- `P3-noop` is formatting-only drift.

## P2 Handling Examples

| Class | Examples | Why this is not an EVAS-kernel fix by default | Checker policy |
| --- | --- | --- | --- |
| `time_fraction_sampling_drift` | `edge_detector`, `one_shot_timer`, `lock_detector` | Edge counts and qualitative states match; row fractions move because the two simulators save different transient points. | Prefer edge counts, edge times, or time-weighted high duration over `high rows / total rows`. |
| `event_timing_quantization_drift` | `pfd_reset_race` | UP/DN pulse counts and no-overlap classification match; only small timing fractions differ at accepted-step precision. | Keep explicit timing tolerances and add an atomic regression only if pulse counts or overlap classification diverge. |
| `continuous_response_numeric_drift` | `first_order_lowpass` | Values differ by about 1 mV while trend and final behavior agree; forcing EVAS to match Spectre point-for-point would overfit solver sampling. | Score sampled windows with voltage tolerances and monotonic/trend assertions. |
| `continuous_decay_numeric_drift` | `leaky_hold` | Decay values differ by a few mV; the important behavior is hold, exponential decay direction, and reset recovery. | Keep value tolerances and cover `$abstime` decay with a separate conformance regression. |
| `continuous_integration_numeric_drift` | `resettable_integrator` | Reset and integration trend agree; window means differ by a few mV due to integration/sampling granularity. | Use reset-level, sign/trend, and bounded mean tolerances instead of exact waveform equality. |
