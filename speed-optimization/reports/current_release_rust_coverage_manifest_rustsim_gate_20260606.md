# Release Rust Coverage Manifest

Created: `2026-06-06T17:40:57`
Paper speed claim allowed: `False`
Reason: This is compile-level Rust coverage evidence, not same-slice EVAS/Spectre timing.

## Scope

- Tasks root: `benchmark-vabench-release-v1/tasks`
- Model rows scanned: `357`
- Entry count: `79`
- Unique gold source hashes: `152`
- Duplicate gold source rows: `205`
- Whole-segment invalid candidates: `0`

## Rustification Estimate

- Engineering completion estimate: `30.4%`
- Basis: weighted B01-B18 seed status estimate; not a speed or correctness claim
- This number is deliberately conservative: shadow-only and partial helpers do not count as full Rust production.

## Compile Status

| Status | Model rows |
|---|---:|
| `pass` | 357 |

## Rust Signals

| Signal | Model rows |
|---|---:|
| `dynamic_bus_metadata` | 7 |
| `event_lfsr_batch` | 2 |
| `ordered_transition_shadow` | 262 |
| `state_owned_timer_fastpath` | 14 |
| `static_linear_ir` | 4 |
| `strict_rustsim_program` | 355 |
| `transition_target_ir` | 328 |
| `whole_segment_candidate` | 259 |

## Whole-Segment Candidates

| Candidate | Model rows |
|---|---:|
| `cmp_delay_log_transition_v1` | 4 |
| `cppll_timer_v1` | 2 |
| `cross_scalar_lfsr_transition_bus_v1` | 3 |
| `edge_interval_timer_v1` | 4 |
| `gain_timer_reduction_v1` | 2 |
| `generic_event_state_transition_v1` | 236 |
| `ref_step_clock_v1` | 2 |
| `sample_hold_rising_v1` | 2 |
| `weighted_dac_v1` | 2 |
| `weighted_sar_adc_v1` | 2 |

## Whole-Flow Fastpaths

| Candidate | Release forms |
|---|---:|
| `gain_measurement_flow_v1` | 2 |

| Candidate | Entry | Form | Production ABI |
|---|---|---|---|
| `gain_measurement_flow_v1` | `vbr1_l2_gain_extraction_convergence_measurement_flow` | `e2e` | `evas_rust_gain_measurement_flow_trace` |
| `gain_measurement_flow_v1` | `vbr1_l2_gain_extraction_convergence_measurement_flow` | `tb` | `evas_rust_gain_measurement_flow_trace` |

Note: whole-flow rows are source-shape candidates. The simulator runtime gate still validates wiring, sources, parameters, and recorded signals before enabling production Rust.

## Strict EVAS2 RustSimProgram Gate

This gate reuses the EVAS2 `RustSimProgram` lowering path and answers whether each compiled model can be represented by the Rust-owned program schema without Python `evaluate()` fallback. It is compile/lowering evidence, not waveform parity evidence.

| Gate status | Model rows |
|---|---:|
| `supported` | 355 |
| `unsupported` | 2 |

| Primary blocker | Model rows |
|---|---:|
| `event_body` | 2 |

| Blocker tag | Model rows |
|---|---:|
| `event_body` | 2 |

| Supported-program field | Total |
|---|---:|
| `body_expr_ops` | 29001 |
| `body_stmt_ops` | 8894 |
| `continuous_linear_ops` | 12 |
| `event_count` | 922 |
| `node_count` | 2644 |
| `param_count` | 1095 |
| `record_count` | 355 |
| `side_effect_count` | 12 |
| `source_count` | 0 |
| `state_count` | 1852 |
| `transition_count` | 924 |

## Behavior Coverage

| ID | Status | Present rows | Rust primitive |
|---|---|---:|---|
| `B01` | `partial` | 357 | `evas_rust_evaluate_static_linear` |
| `B02` | `partial` | 357 | `evas_rust_evaluate_static_linear + evas_rust_interpolate_event_values` |
| `B03` | `partial` | 354 | `evas_rust_evaluate_static_linear` |
| `B04` | `partial` | 12 | `evas_rust_evaluate_static_linear` |
| `B05` | `partial` | 281 | `evas_rust_evaluate_static_linear` |
| `B06` | `partial` | 357 | `evas_rust_evaluate_static_linear` |
| `B07` | `shadow_only` | 350 | `evas_rust_evaluate_transition_targets` |
| `B08` | `partial` | 350 | `evas_rust_transition_state_step` |
| `B09` | `partial` | 278 | `evas_rust_cross_detector_step + evas_rust_above_detector_step + evas_rust_interpolate_event_values` |
| `B10` | `partial` | 327 | `evas_rust_event_lfsr_shift_xor_step + evas_rust_event_static_linear_write + evas_rust_interpolate_event_values` |
| `B11` | `partial` | 70 | `evas_rust_next_timer_breakpoint + evas_rust_timer_periodic_step + evas_rust_timer_absolute_step + evas_rust_timer_static_linear_trace + evas_rust_timer_static_linear_queue_trace` |
| `B12` | `python_only` | 10 | `` |
| `B13` | `python_only` | 0 | `` |
| `B14` | `partial` | 0 | `evas_rust_max_err_ratio` |
| `B15` | `partial` | 0 | `evas_rust_record_values_for_node_ids` |
| `B16` | `python_only` | 90 | `` |
| `B17` | `partial` | 7 | `evas_rust_dynamic_bus_offsets` |
| `B18` | `partial` | 357 | `evas_rust_timer_static_linear_trace + evas_rust_timer_static_linear_queue_trace + model-specific whole-segment trace ABIs` |

## Top Blockers

| Blocker | Weighted model rows |
|---|---:|
| `B01:partial` | 357 |
| `B02:partial` | 357 |
| `B06:partial` | 357 |
| `B18:partial` | 357 |
| `B03:partial` | 354 |
| `B07:shadow_only` | 350 |
| `B08:partial` | 350 |
| `B10:partial` | 327 |
| `B05:partial` | 281 |
| `B09:partial` | 278 |
| `B16:python_only` | 90 |
| `B11:partial` | 70 |
| `B04:partial` | 12 |
| `B12:python_only` | 10 |
| `B17:partial` | 7 |

## Static Linear Rejections

| Rejection | Model rows |
|---|---:|
| `('event_statement', 1)` | 217 |
| `('event_cross', 1)` | 186 |
| `('contribution_non_static_linear_expr', 2)` | 151 |
| `('expr_function_transition', 2)` | 148 |
| `('contribution_non_static_linear_expr', 1)` | 123 |
| `('expr_function_transition', 1)` | 123 |
| `('event_statement', 2)` | 76 |
| `('assignment_self_dependent_state', 1)` | 72 |
| `('event_cross', 2)` | 69 |
| `('event_timer', 1)` | 68 |
| `('system_task', 1)` | 63 |
| `('assignment_non_static_linear_expr', 1)` | 62 |
| `('if_statement', 5)` | 61 |
| `('condition_non_static_linear_expr', 1)` | 55 |
| `('if_statement', 1)` | 53 |
| `('expr_non_static_linear_binary', 5)` | 50 |
| `('if_statement', 2)` | 45 |
| `('if_statement', 3)` | 45 |
| `('expr_unsupported_binary_op', 1)` | 42 |
| `('expr_non_static_linear_binary', 7)` | 41 |
| `('assignment_non_static_linear_expr', 2)` | 38 |
| `('assignment_self_dependent_state', 2)` | 38 |
| `('expr_non_static_linear_binary', 1)` | 35 |
| `('expr_non_static_linear_binary', 3)` | 32 |
| `('contribution_non_static_linear_expr', 4)` | 31 |

## Next Engineering Use

- Use `whole_segment_candidate_counts` to drive 068/069 Rust ABI work.
- Use `strict_rustsim_program_blocker_counts` to prioritize missing EVAS2 semantic lowering.
- Use `top_rust_blockers` to prioritize event/timer/transition/evaluate IR lowering.
- Do not use this artifact as EVAS-vs-Spectre speed evidence.
