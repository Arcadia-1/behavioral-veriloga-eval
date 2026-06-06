# 105 - EVAS2.0 Strict Rust Engine Gate

## Decision

EVAS1.0 remains the current Python simulator with optional Rust helpers and fallback.
EVAS2.0 is introduced as a stricter opt-in engine mode:

- `evas_engine=evas2`
- forces `evas_rust_full_model_fastpath=true`
- forces `evas_rust_full_model_required=true`
- forces `evas_rust_required=true`

If no supported whole-segment Rust runtime matches the design, EVAS2.0 fails with
an explicit unsupported error instead of silently falling back to Python EVAS.

This makes benchmark coverage honest: a benchmark only counts as EVAS2.0 runnable
when the Rust whole-segment path actually executes.

## Why This Replaces Small Per-Step Rust FFI as the Main Direction

The earlier phrase "event due + event body + transition + breakpoint + record in
one Rust batch" means Rust should own the contiguous simulation segment, not that
we should keep calling many tiny Rust functions from Python every timestep.

The useful EVAS2.0 shape is:

1. compile Verilog-A/testbench into typed node/state/source/record arrays;
2. select a whole-segment Rust runtime from semantic/dataflow candidate metadata;
3. run many timepoints/events inside Rust;
4. return only checker-visible trace data and counters.

The unhelpful shape is:

1. Python owns the timestep loop;
2. Python packs arrays every step;
3. Python calls Rust due/body/transition/breakpoint primitives separately;
4. Python syncs dict/object state every step.

The second shape can be slower than pure Python because FFI and state sync dominate
the tiny amount of work done per call.

## Current Release Coverage

Source: `speed-optimization/reports/current_release_rust_coverage_manifest_20260604.json`.

| Metric | Count |
|---|---:|
| Release benchmark entries | 79 |
| Release gold `.va` model rows | 357 |
| Compile-pass model rows in manifest | 357 |
| Static whole-segment candidate rows | 23 |
| Entries with at least one whole-segment candidate | 5 |
| Entry/form pairs with at least one whole-segment candidate | 12 |

Static whole-segment candidates:

| Candidate | Model rows | Entries | Entry/forms |
|---|---:|---:|---:|
| `cmp_delay_log_transition_v1` | 4 | 1 | 4 |
| `edge_interval_timer_v1` | 4 | 1 | 4 |
| `cross_scalar_lfsr_transition_bus_v1` | 3 | 1 | 2 |
| `weighted_dac_v1` | 2 | 1 | 2 |
| `weighted_sar_adc_v1` | 2 | 1 | 2 |
| `sample_hold_rising_v1` | 2 | 1 | 2 |
| `cppll_timer_v1` | 2 | 1 | 2 |
| `ref_step_clock_v1` | 2 | 1 | 2 |
| `gain_timer_reduction_v1` | 2 | 1 | 2 |

Candidate entries:

- `vbr1_l1_gain_estimator`: `e2e`, `tb`
- `vbr1_l1_lfsr_prbs_generator`: `bugfix`, `dut`
- `vbr1_l1_propagation_delay_comparator`: `bugfix`, `dut`, `e2e`, `tb`
- `vbr1_l2_cppll_tracking_and_frequency_step_reacquire_flow`: `e2e`, `tb`
- `vbr1_l2_weighted_sar_adc_dac_loop`: `e2e`, `tb`

These are static candidates, not full release Rustification. Runtime wiring,
sources, parameters, and saved signal contract still decide whether the EVAS2.0
runtime can execute.

## Runtime Smoke

Temporary smoke files were staged under `/private/tmp`; release sources were not
modified.

| Case | Expected | Result |
|---|---|---|
| `vbr1_l1_propagation_delay_comparator/e2e` | whole-segment candidate should run EVAS2.0 | PASS, `rust_full_model_fastpath_enabled=1`, `rust_full_model_whole_segment_points=1793` |
| `vbr1_l1_binary_weighted_voltage_dac/e2e` | non-candidate should not fall back | FAIL as unsupported, `EVAS2.0 Rust full-model path was required...` |

## Why Earlier Rust Speedups Do Not Automatically Apply Everywhere

Earlier speedups came from whole-model or whole-flow Rust traces such as PRBS7,
gain timer reduction, propagation delay, SAR, CPPLL, and gain measurement flow.
Those paths amortize Python/Rust boundary cost by doing many events/timepoints
inside Rust.

The 103/104 event-transition production experiment did not show speedup because
it still kept the Python outer loop and paid per-step array packing, FFI calls,
and dict/object state synchronization. In the smoke example there were only two
real events but thousands of Rust production calls, so the fixed overhead was
larger than the Python work being replaced.

## Implementation Anchors

- `EVAS/evas/simulator/engine.py`
  - adds `rust_full_model_required`
  - raises instead of falling back when whole-segment Rust does not match
- `EVAS/evas/netlist/runner.py`
  - maps `evas_engine=evas2` to strict full-model Rust mode
- `behavioral-veriloga-eval/runners/run_vabench_release_evas_speed_experiment.py`
  - adds `profile_fast_evas2`
- Tests:
  - `EVAS/tests/test_engine.py::test_rust_full_model_required_rejects_python_fallback`
  - `EVAS/tests/test_engine.py::test_rust_full_model_timer_static_linear_trace_matches_default`
  - `behavioral-veriloga-eval/tests/test_vabench_release_evas_speed_modes.py`

## Next Work

EVAS2.0 should now expand coverage by adding more whole-segment Rust runtimes,
not by adding more default-off per-step Rust helpers:

1. Convert high-frequency benchmark behaviors into semantic/dataflow whole-segment candidates.
2. Add Rust ABI/runtime for each candidate family.
3. Require EVAS2.0 runtime smoke and strict-EVAS parity before counting coverage.
4. Only after coverage expands, run same-slice EVAS2.0 vs EVAS1.0 vs Spectre AX/classic speed and accuracy tables.
