# 110 - Timer/Array RustSimProgram and Speed Smoke

Date: 2026-06-06

## What Changed

This round widened the strict EVAS2 RustSimProgram path in three general areas:

- Added `$abstime` / `$realtime` expression lowering to the Rust body-expression stack machine.
- Allowed state-owned absolute `timer(next_t)` events to run in Rust and re-arm from Rust after the event body updates `next_t = $abstime + period`.
- Flattened static state-array elements such as `bits[0]` into normal typed Rust state slots, so static array reads/writes can participate in ordered event/evaluate bodies and transition targets.

One routing guard was also added: periodic timer-static-linear models without transition targets continue to use the older specialized Rust timer path, because that path already matches the established Python trace de-duplication behavior.

## Verification

Local verification:

| Check | Result |
| --- | --- |
| Python compile for changed simulator files | PASS |
| `cargo build --release` in `EVAS/evas/rust_core` | PASS |
| `pytest EVAS/tests/test_engine.py -q -k "rust_sim_program"` | 9 passed |
| `pytest EVAS/tests/test_engine.py -q -k "timer_static_linear"` | 3 passed |
| `pytest EVAS/tests/test_engine.py -q` | 259 passed |

New regression coverage:

- `state_owned_timer`: `@(timer(next_t))` re-arms from `$abstime + period` in Rust and matches Python EVAS state/waveform.
- `state_array_transition_target`: static array writes inside `if/else`, array reads into a weighted code, and transition target evaluation all execute in Rust and sync back to `model.arrays`.

## Speed Smoke

Comparable 4-row smoke, same slice as 109b:

Report:
`speed-optimization/reports/rust_sim_program_110_release_checker_smoke_20260606.json`

| Mode | PASS | Non-PASS | Total wall s | Safe vs strict | Unsafe vs strict |
| --- | ---: | ---: | ---: | ---: | ---: |
| strict_current | 4 | 0 | 4.323 | 0 | 0 |
| profile_fast_evas2 | 4 | 0 | 2.677 | 4 | 0 |

Valid speed on this 4-row slice:

- Sum speedup: `4.323 / 2.677 = 1.61x`
- Median per-row speedup vs strict: `1.36x`
- Geomean per-row speedup vs strict: `1.50x`

Selected 12-row smoke:

Report:
`speed-optimization/reports/rust_sim_program_110_selected12_smoke_20260606.json`

| Mode | PASS | Non-PASS | Total wall s | Safe vs strict | Unsafe vs strict |
| --- | ---: | ---: | ---: | ---: | ---: |
| strict_current | 12 | 0 | 46.011 | 0 | 0 |
| profile_fast_evas2 | 6 | 6 | 5.407 | 6 | 6 |

Do not use the full 12-row aggregate as a claim, because 6 rows are unsafe. On the safe subset only:

| Entry | Strict wall s | EVAS2 wall s | Speedup | Main Rust path |
| --- | ---: | ---: | ---: | --- |
| vbr1_l1_binary_weighted_voltage_dac | 0.465 | 0.411 | 1.13x | RustSimProgram |
| vbr1_l1_dac_mismatch_unit_weighting_model | 0.361 | 0.362 | 1.00x | RustSimProgram |
| vbr1_l1_pipeline_adc_stage | 1.452 | 0.494 | 2.94x | RustSimProgram |
| vbr1_l1_propagation_delay_comparator | 18.586 | 0.528 | 35.21x | existing specialized Rust path |
| vbr1_l1_segmented_dac | 0.412 | 0.386 | 1.07x | RustSimProgram |
| vbr1_l2_cppll_tracking_and_frequency_step_reacquire_flow | 3.715 | 0.683 | 5.44x | existing specialized Rust path |

Safe-subset sum speedup:

`24.991 / 2.864 = 8.73x`

## Unsafe Rows

The unsafe rows are not valid speed evidence. Manual probing shows they mostly fail because strict EVAS2 cannot find a supported whole-segment Rust runtime, so no `tran.csv` is produced.

| Entry | Observed blocker |
| --- | --- |
| vbr1_l1_capacitive_weighted_sar_feedback_dac | `post_update_not_lowered` |
| vbr1_l1_clocked_adc_quantizer | `event_body_not_lowered` |
| vbr1_l1_edge_interval_timer | `post_update_not_lowered` |
| vbr1_l1_lfsr_prbs_generator | needs separate LFSR/event-body lowering audit |
| vbr1_l1_sar_logic | `event_body_not_lowered` |
| vbr1_l2_adpll_lock_ratio_hop_timer_flow | `bound_step_not_lowered` |

## Current Claim Boundary

What is now supported:

- Strict RustSimProgram can own complete source/record/no-model loops.
- It can own continuous ordered body writes for supported scalar/static-array expressions.
- It can own `initial_step`, `cross`, `above`, state-owned absolute `timer(next_t)`, simple event bodies, transition target evaluation, transition output, and sparse record for supported whole-segment programs.
- Static array elements with constant indices are mapped to typed state slots and sync back to Python arrays after the Rust run.

What is not yet claimable:

- Full release-wide Rust EVAS2 coverage.
- Speedup on unsupported rows.
- Paper-facing Spectre AX comparison, because this smoke is EVAS-only and not same-slice Spectre timing.

## Remaining Large Blocks

Priority order:

1. `post_update` ownership in Rust. This blocks CDAC and edge-interval timer style models.
2. General event-body lowering for multi-write / nested control-flow ADC and SAR logic bodies.
3. `$bound_step` and adaptive step ownership in Rust. This blocks ADPLL-style models.
4. LFSR/event-body state-array and bit-operation production path audit.
5. Dynamic bus/indexed port output lowering. Static state arrays are handled; dynamic output-node selection is not.

The practical completion level is therefore not full Rust EVAS2 yet. On this 12-row smoke, production-safe coverage is 6/12 rows; RustSimProgram itself safely covers 4/12 rows, while two additional safe rows are still covered by older specialized Rust paths.
