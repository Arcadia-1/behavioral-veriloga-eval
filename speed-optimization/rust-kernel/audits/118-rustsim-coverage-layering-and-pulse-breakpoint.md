# 118 - RustSimProgram Coverage Layering And Pulse Breakpoint Fix

Status: `done`

Date: `2026-06-06`

Code commit: `pending`

Related reports:

- `speed-optimization/reports/evas2_p1_bbpd_fixed_smoke_20260606.json`
- `speed-optimization/reports/evas2_p1_counter_smoke_20260606.json`
- `speed-optimization/reports/evas2_p1_current_topwall8_20260606.json`
- `speed-optimization/reports/evas2_p1_current_topwall8_worker_20260606.json`
- `speed-optimization/reports/evas2_p1_current_topwall8_worker_r2_20260606.json`

## One-Line Summary

把 Rust 覆盖率口径拆成静态 lowering / runtime 命中 / 速度证据三层，并修复 pulse source breakpoint 在浮点边界上重复返回当前时刻导致 RustSimProgram 卡死的问题；top-wall 8 当前样本全部命中 RustSimProgram，persistent worker 口径下相对旧 Python strict EVAS 样本总 wall 约 `133.4x`。

## What Changed

| Layer | Before | After | Why it matters |
|---|---|---|---|
| coverage report | legacy `30.4%` 容易被误读成真实 runtime Rust 覆盖 | 新增 layered summary：compile recognition、strict RustSimProgram lowering、whole-segment candidate、runtime coverage | 防止把 primitive/helper 状态误报成“全量 Rust 化” |
| runner staging | 每个 form 只复制本 form 的 `gold/*` | 缺失 include 时只在同一 release entry 的 sibling forms 中解析并复制 | 修复合法 sibling DUT 复用行，例如 bang-bang PD bugfix 的 `bbpd_ref.va` |
| perf counters | 只能知道 RustSimProgram 是否 enabled | 增加 lower / ABI build / time grid / runtime / replay / state sync / total 分段计时 | 能区分 Rust 内核时间和 Python runner/subprocess/checker 外层时间 |
| pulse source breakpoint | `time < delay` 会在 `time` 与 `delay` 只有浮点 eps 差异时重复返回同一个 breakpoint | 使用 `delay > time + eps`，并在 source loops 中跳过 `<= time + eps` 的旧 breakpoint | 修复 event-transition whole loop 的无限小步/卡死 |
| Rust loop safety | 若 future breakpoint 计算退化，可能长时间挂住 full rerun | source-only、source+linear、event+transition loops 加最大迭代 guard | 把无限循环变成显式 Rust error，便于定位 |

## Principle

这次修复的是通用 source scheduling 语义，不是某个 benchmark 特例。

对 pulse source 来说，delay、rise、fall、period 等 knee point 都是未来断点候选。Rust 主循环会反复跳过已经不在未来的 breakpoint：

```text
while next_breakpoint <= time + eps:
    recompute next_breakpoint after current time
```

如果 `rust_sim_source_next_breakpoint()` 在 `time ~= delay` 时仍返回 `delay`，外层循环会一直得到同一个“过去/当前”断点，仿真就卡住。正确规则是：

```text
candidate is future only if candidate > time + eps
```

这和 cross/timer/transition breakpoint 的处理原则一致：断点必须严格落在当前时间之后，`eps` 内的重复点应视为已消费。

## Evidence

Targeted smoke:

| Row | Status | RustSimProgram | Points | Rust core total | Runtime | Source BP | Event fires | Transition BP |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| `vbr1_l1_bang_bang_phase_detector/bugfix` | PASS | 1 | 2771 | 0.013s | 0.009s | 1693 | 271 | 801 |
| `vbr1_l1_propagation_delay_comparator/dut` | PASS | 1 | 1807 | 0.019s | 0.013s | 44 | 1874 | 270 |

Top-wall 8 EVAS2 sample with persistent worker:

| Entry | Form | Worker wall | Rust core | Old Python strict wall | Speedup vs old Python strict |
|---|---|---:|---:|---:|---:|
| `vbr1_l1_bang_bang_phase_detector` | bugfix | 0.043s | 0.012s | 18.297s | 423.0x |
| `vbr1_l1_bang_bang_phase_detector` | dut | 0.044s | 0.013s | 15.859s | 362.6x |
| `vbr1_l1_propagation_delay_comparator` | bugfix | 0.049s | 0.011s | 12.036s | 246.2x |
| `vbr1_l1_propagation_delay_comparator` | tb | 0.041s | 0.010s | 11.904s | 288.5x |
| `vbr1_l2_gain_extraction_convergence_measurement_flow` | e2e | 0.160s | 0.056s | 18.005s | 112.9x |
| `vbr1_l2_gain_extraction_convergence_measurement_flow` | tb | 0.163s | 0.057s | 17.332s | 106.1x |
| `vbr1_l2_weighted_sar_adc_dac_loop` | e2e | 0.914s | 0.385s | 79.022s | 86.5x |
| `vbr1_l2_weighted_sar_adc_dac_loop` | tb | 0.465s | 0.198s | 78.216s | 168.0x |
| **sum** |  | **1.879s** | **0.746s** | **250.671s** | **133.4x** |

The table uses the best of two persistent-worker repeats per row for wall time. It is EVAS-only evidence against the historical Python strict EVAS rows in `full_release_evas_py_rust_after_fixes_20260606.json`; it is not a Spectre AX speed claim.

## Current Interpretation

For these top-wall rows, RustSimProgram is no longer just a helper primitive. It owns the source scheduling, event due/body, transition output/breakpoint, record gather, and final state sync for the covered model segment.

The remaining wall gap is split by layer:

| Layer | Evidence | Next action |
|---|---|---|
| Rust core | 10 ms to 385 ms per row in the current top-wall 8 sample | Continue profiling SAR/gain runtime internals, especially event count and transition breakpoint density |
| subprocess / worker boundary | cold-start top-wall8 wall `4.742s`; persistent worker repeat best `1.879s` | Use persistent worker for E2E comparisons when the goal is simulator throughput rather than Python process startup |
| CSV / checker | SAR rows still spend about 0.06s CSV and 0.13s checker per run | Keep checker runtime and sparse trace improvements as E2E work, but separate them from kernel speed claims |
| Spectre comparison | not rerun in this step | Full same-slice four-way rerun is still required before claiming against Spectre AX/classic |

## Functional Safety

- Default Python EVAS path changed: `no`
- Strict EVAS2 behavior changed: `yes`, fixes a Rust-owned source breakpoint scheduling bug
- Benchmark-specific special case added: `no`
- Precision semantics changed: `no intended change`; the fix prevents duplicate current-time breakpoints and follows the existing `eps` future-breakpoint convention
- Fallback to Python added: `no`

## Validation

Commands run:

```bash
cargo fmt
cargo build --release
cargo test

PYTHONPYCACHEPREFIX=/private/tmp/vaevas_pycache python3 -m py_compile \
  EVAS/evas/simulator/engine.py \
  behavioral-veriloga-eval/runners/run_vabench_release_evas_speed_experiment.py \
  behavioral-veriloga-eval/runners/report_vabench_release_fourway_reference.py \
  behavioral-veriloga-eval/runners/report_vabench_release_rust_coverage_manifest.py

PYTHONPATH=runners python3 -m pytest \
  tests/test_vabench_release_evas_speed_modes.py \
  tests/test_vabench_release_fourway_reference.py \
  tests/test_vabench_release_rust_coverage_manifest.py -q
```

Results:

```text
cargo build --release: passed
cargo test: 38 passed
py_compile: passed
pytest: 11 passed
bbpd fixed smoke: 1/1 PASS, rust_sim_program_enabled=1
propdelay counter smoke: 1/1 PASS, rust_sim_program_enabled=1
top-wall8 cold EVAS2 smoke: 8/8 PASS
top-wall8 persistent-worker EVAS2 smoke: 8/8 PASS in both repeats
```
