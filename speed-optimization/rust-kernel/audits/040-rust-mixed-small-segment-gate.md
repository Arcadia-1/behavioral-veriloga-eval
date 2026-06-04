# 040 - Rust Mixed Small Segment Gate

Status: `done`

Date: `2026-06-03`

Code commit: `pending`

Related reports:

- `EVAS/evas/simulator/engine.py`
- `EVAS/tests/test_engine.py`
- `behavioral-veriloga-eval/speed-optimization/reports/e2e_wall_profile_20260603_r51_rust_mixed_small_gate.json`

## One-Line Summary

039 证明 partial Rust coverage 能识别真实 helper models，但小规模 mixed Rust/Python segment 会拖慢 benchmark；040 增加 fast-sync speed mode 的 small mixed-segment gate，让这类情况记录候选但回退 Python runtime。

## Follow-Up Plan

| Priority | Work item | Goal | Expected effect | Risk |
|---|---|---|---|---|
| P0 | Mixed small-segment gate | 避免 partial Rust coverage 把真实 speed mode 拖慢 | 消除 039 暴露的 measurement-flow regression | 低：只影响 opt-in Rust fast-sync path |
| P1 | Transition boundary profiling | 量化 `transition()` target update、evaluate、output write 的真实占比 | 找到 event-heavy models 的最大可 Rust 化子问题 | 中：transition 语义和延迟/边沿相关 |
| P1 | Integer scalar state IR | 把 `integer valid_q/state` 这类状态从 Python dict 降到 typed slots | 覆盖 gain estimator、PFD、PLL 中的控制状态 | 中：需要保证 Spectre integer coercion |
| P2 | State array and dynamic bus typed layout | 把 LFSR/SAR 里的 arrays/bus 变成 indexed typed layout | 为 LFSR/SAR Rust evaluate 做前置 | 中高：dynamic index 和 bus naming 容易出错 |
| P3 | Event/timer/breakpoint queue | 最后迁移 cross/timer/bound_step 扫描 | 减少 CPPLL/ADPLL/PFD 每步事件扫描 | 高：事件顺序和 missed breakpoint 风险最大 |

This round implements only P0. The later items should each get a separate audit document and parity regression.

## What Changed

Before 040:

```text
EVAS_RUST_STATIC_EVAL=1
EVAS_RUST_STATIC_FAST_SYNC=1
```

would execute any Rust static segment found, even if the run still contained Python event models. On `gain_extraction`, only `dither_adder` and `gain_amp_fixed` were Rust candidates; `vin_src` and `lfsr` stayed Python. The mixed path paid indexed array snapshot/sync costs every step and became slower.

After 040:

```text
if fast-sync requested
and Rust coverage is not full-model coverage
and planned Rust op count < 64:
    record gated candidate counters
    clear Rust segments
    if indexed arrays were only forced by Rust, disable them
    run the ordinary Python evaluator
```

New counters:

| Counter | Meaning |
|---|---|
| `rust_static_eval_mixed_small_fallbacks` | small mixed fast-sync gate fired |
| `rust_static_eval_gated_models` | candidate models intentionally not executed in Rust |
| `rust_static_eval_gated_ops` | candidate ops intentionally not executed in Rust |
| `rust_static_eval_gated_segments` | candidate segments removed by the gate |

Why threshold 64 ops:

- Full Rust coverage remains allowed even for tiny tests, because fast sync can remove per-step dict validation.
- Partial/mixed Rust coverage needs enough work per FFI/sync boundary to pay for itself.
- 039's real regression was 2 models / 6 ops / mixed Python event models, far below this threshold.
- The threshold is intentionally conservative and should be recalibrated after more real mixed slices are profiled.

## Evidence

### Direct Measurement-Flow Check

Netlist:

```text
results/e2e-wall-profile-20260603-r50-rust-coverage-current/staged/vbr1_l2_gain_extraction_convergence_measurement_flow/tb/gold/vbr1_l2_gain_extraction_convergence_measurement_flow_tb/profile_fast_skip_source_error_control/gold/tb_gain_extraction_ref.scs
```

Direct logs:

| Mode | Total elapsed | Rust candidates | Rust executed | Indexed snapshots/syncs | Interpretation |
|---|---:|---:|---:|---:|---|
| Python/no Rust | 1.2 s | 0 | 0 | 0 / 0 | baseline diagnostic |
| 039 partial Rust | 3.8 s | 2 models / 6 ops | 2 models / 6 ops | 16236 / 16236 | regression from mixed sync |
| 040 mixed gate | 1.6 s | 2 models / 6 ops | 0 models / 0 ops | 0 / 0 | regression removed |

040 log excerpt:

```text
rust_static_eval_candidate_models = 2
rust_static_eval_gated_models = 2
rust_static_eval_gated_ops = 6
rust_static_eval_mixed_small_fallbacks = 1
rust_static_eval_models = 0
rust_static_eval_no_segment_fallbacks = 1
indexed_array_snapshots = 0
indexed_array_syncs = 0
Total time: CPU = 1.6 s, elapsed = 1.6 s
```

### Top-Wall 10 Diagnostic

EVAS-only, no Spectre gate; diagnostic only.

| Report | Rows PASS | Total E2E wall | EVAS subprocess wall | Measurement-flow tb/e2e |
|---|---:|---:|---:|---:|
| r48 fast-sync final | 10/10 | 18.117548 s | 14.270016 s | 1.457929 s / 1.500118 s |
| r50 coverage current | 10/10 | 23.329653 s | 19.306166 s | 3.064029 s / 2.603997 s |
| r51 mixed-small gate | 10/10 | 18.337417 s | 14.704750 s | 1.474433 s / 1.442644 s |

Interpretation:

- 040 removes the partial-Rust regression introduced by 039 coverage expansion.
- It does not create a new top-wall speedup; it restores the fast-sync diagnostic path to roughly the pre-039 range.
- This is still not a paper-facing speed claim because the run is EVAS-only and Spectre-equivalence gates are blocked by missing references.

## Functional Safety

- Default backend changed: `no`
- CSV schema changed: `no`
- Checker behavior changed: `no`
- Event ordering changed: `no`
- Rust path default: `off`
- Fallback path exists: `yes`

Important boundary:

- Pure `rust_static_eval=True` still executes mixed Rust/Python segments for diagnostics.
- The new gate applies to fast-sync speed mode, where partial mixed coverage cannot actually enable fast sync.
- Full model coverage still runs Rust and can enable fast sync.

## Validation

Commands run:

```bash
git diff --check -- evas/simulator/engine.py tests/test_engine.py
git diff --check -- speed-optimization/rust-kernel/README.md speed-optimization/rust-kernel/audits/040-rust-mixed-small-segment-gate.md
python3 -m pytest tests/test_engine.py::TestSimulator::test_rust_static_eval_keeps_full_indexed_validation_for_mixed_models tests/test_engine.py::TestSimulator::test_rust_static_fast_sync_gates_small_mixed_segments_to_python tests/test_engine.py::TestSimulator::test_rust_static_fast_sync_skips_per_step_dict_validation tests/test_engine.py::TestSimulator::test_rust_static_fast_sync_no_segment_falls_back_to_python_runtime -q
python3 -m pytest tests/test_engine.py -k 'rust_static_eval or rust_static_fast_sync' -q
python3 -m pytest tests/test_rust_backend.py -q
python3 -m pytest -q
cargo test
cargo build --release
```

Results:

```text
diff checks: passed
engine targeted: 4 passed
engine rust-static selector: 10 passed
Rust backend ctypes: 6 passed
Rust core: 8 passed
EVAS full pytest: 489 passed
Rust release build: passed
```

## Next Step

The next useful optimization is not another Python micro-fix. It should be a read-only-to-implementation cycle around event-heavy models:

1. Profile `transition()` in `gain_estimator`, `PFD`, `SAR`, and `CPPLL` rows.
2. Split transition into target-state update and waveform evaluation boundaries.
3. Add typed integer state slots before attempting event/timer queue migration.
4. Only after those are stable, design the Rust event/timer/breakpoint queue.
