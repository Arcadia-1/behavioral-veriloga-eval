# 039 - Rust Coverage Expansion For Real Models

Status: `done`

Date: `2026-06-03`

Code commit: `pending`

Related reports:

- `EVAS/evas/simulator/evaluate_ir.py`
- `EVAS/evas/simulator/backend.py`
- `EVAS/evas/simulator/engine.py`
- `EVAS/evas/simulator/rust_backend.py`
- `EVAS/evas/rust_core/src/lib.rs`
- `EVAS/tests/test_indexed_backend.py`
- `EVAS/tests/test_rust_backend.py`
- `EVAS/tests/test_engine.py`
- `behavioral-veriloga-eval/speed-optimization/reports/e2e_wall_profile_20260603_r50_rust_coverage_current.json`

## One-Line Summary

把 static linear evaluate IR 从“只覆盖纯线性赋值”扩展到真实模型里出现的 timer-free 条件赋值和 initial-step no-op 场景；top-wall 10 中 `dither_adder` 和 `gain_amp_fixed` 现在能进入 Rust IR，但主耗时模型仍被 event/timer/cross、transition、integer/state array、dynamic bus 阻塞。

## What Changed

| Layer | Before | After | User-visible behavior |
|---|---|---|---|
| evaluate IR | 只支持 `target = bias + sum(gain * source)` | 支持单个 top-level ternary 条件选择：`cond ? linear_a : linear_b` | 默认 Python evaluator 不变 |
| compiler lowering | 任意 event statement 都阻止 IR | 仅 `@(initial_step)` / `@(final_step)` 中不影响 evaluate 的 `$strobe` 类 no-op 可跳过 | cross/timer/above 仍 fallback |
| Rust ABI | static linear op 只有一个 term slice | op 可携带 condition id、false branch term slice 和 false bias | opt-in Rust only |
| engine | 只映射 true branch node/state terms | 映射 condition/false branch 的 node/state ids，并计入 state reads | fallback 仍保留 |
| array loops | Rust 只能执行 evaluate op | 新增 Rust `copy_f64` 和 `max_err_ratio` primitives；engine 仅在大 node-count 时门控启用 | 小模型不因 FFI 固定成本变慢 |

新增覆盖的典型真实代码形态：

```verilog
@(initial_step) $strobe("...");
dither = (V(DPN) > vth) ? DITHER_AMP : -DITHER_AMP;
V(VOUT_P) <+ V(VRES_P) + 0.5 * dither;
V(VOUT_N) <+ V(VRES_N) - 0.5 * dither;
```

数学上降成 ordered IR：

```text
state(dither) = if node(DPN) > vth then +DITHER_AMP else -DITHER_AMP
node(VOUT_P) = node(VRES_P) + 0.5 * state(dither)
node(VOUT_N) = node(VRES_N) - 0.5 * state(dither)
```

## Top-Wall 10 Coverage Diagnosis

Row set: `e2e_wall_profile_20260603_r50_rust_coverage_current.json`, same top-wall 10 selection as 038 diagnostics. Candidate/ops come from the EVAS compiler's generated `_evaluate_ir_static_linear_ops`; blockers are explanatory source features.

| # | Entry/form | Model | Rust IR | Ops | Main blocker if not covered |
|---:|---|---|---:|---:|---|
| 1 | `vbr1_l1_gain_estimator/tb` | `gain_estimator.va` | no | 0 | timer sampling, transition output, integer valid flag, control flow |
| 2 | `vbr1_l2_gain_extraction_convergence_measurement_flow/tb` | `dither_adder.va` | yes | 3 | covered: initial-step no-op + conditional scalar state |
| 2 | same | `gain_amp_fixed.va` | yes | 3 | covered: linear scalar state + linear outputs |
| 2 | same | `lfsr.va` | no | 0 | cross event, state array, integer state, transition output |
| 2 | same | `vin_src.va` | no | 0 | timer/event behavior, random/sine source, transition output |
| 3 | `vbr1_l1_gain_estimator/e2e` | `gain_estimator.va` | no | 0 | same as row 1 |
| 4 | `vbr1_l2_gain_extraction_convergence_measurement_flow/e2e` | `dither_adder.va` | yes | 3 | covered |
| 4 | same | `gain_amp_fixed.va` | yes | 3 | covered |
| 4 | same | `lfsr.va` | no | 0 | same as row 2 |
| 4 | same | `vin_src.va` | no | 0 | same as row 2 |
| 5 | `vbr1_l1_pfd_up_dn_logic/bugfix` | `dut_buggy.va`, `dut_fixed.va` | no | 0 | cross event, integer state, transition output |
| 6 | `vbr1_l2_weighted_sar_adc_dac_loop/tb` | `dac_weighted_8b.va` | no | 0 | event/control flow, transition output |
| 6 | same | `sar_adc_weighted_8b.va` | no | 0 | cross event, state array, dynamic bus, integer state |
| 6 | same | `sh_ideal.va` | no | 0 | cross event sample-and-hold, transition output |
| 7 | `vbr1_l1_propagation_delay_comparator/dut` | `cmp_delay.va` | no | 0 | cross event, integer state, `ln/exp`, transition output |
| 7 | same | `edge_interval_timer.va` | no | 0 | cross event, integer state, transition output |
| 8 | `vbr1_l2_cppll_tracking.../e2e` | `cppll_timer_ref.va` | no | 0 | cross/timer, `$bound_step`, integer state, transition output |
| 8 | same | `ref_step_clk.va` | no | 0 | event/timer clock generation, transition output |
| 9 | `vbr1_l2_cppll_tracking.../tb` | `cppll_timer_ref.va`, `ref_step_clk.va` | no | 0 | same as row 8 |
| 10 | `vbr1_l1_lfsr_prbs_generator/dut` | `prbs7.va`, `prbs7_ref.va` | no | 0 | cross event, LFSR state/integer logic, transition output |

Unique-model interpretation:

| Category | Count |
|---|---:|
| newly Rust-covered unique real models | 2 |
| newly Rust-covered ops | 6 |
| still non-candidate unique models | 14 |
| dominant blockers | event/timer/cross, transition, integer state, state array, dynamic bus |
| child model blocker in this top-wall 10 | not observed as dominant blocker |

## Performance Evidence

### Top-Wall 10 Diagnostic

EVAS-only, profile mode, no Spectre reference gate. This is diagnostic evidence only.

| Report | Rows PASS | Total E2E wall | EVAS subprocess wall | Interpretation |
|---|---:|---:|---:|---|
| r48 fast-sync final | 10/10 | 18.117548 s | 14.270016 s | before 039, representative inspected row had `candidate_models=0` |
| r50 coverage current | 10/10 | 23.329653 s | 19.306166 s | after 039, measurement-flow rows get partial Rust coverage, but mixed Rust/Python path is slower |

Do not read r50 as a speed claim. It proves correctness/coverage on the top-wall diagnostic slice, and it exposes the next bottleneck: partial Rust coverage of two small helper models is not enough when the same run still pays Python event models, indexed sync, output sync, checker, and CSV costs.

### Direct Full-Log Measurement-Flow Check

Netlist:

```text
results/e2e-wall-profile-20260603-r49-rust-coverage-expanded/staged/vbr1_l2_gain_extraction_convergence_measurement_flow/tb/gold/vbr1_l2_gain_extraction_convergence_measurement_flow_tb/profile_fast_skip_source_error_control/gold/tb_gain_extraction_ref.scs
```

Current direct log:

```text
/private/tmp/evas-rust-coverage-gain-extraction-r49-039-threshold.log
rust_static_eval_candidate_models = 2
rust_static_eval_models = 2
rust_static_eval_ops = 6
rust_static_eval_calls = 32472
rust_static_eval_errors = 0
rust_array_loop_enabled = 0
```

Same netlist, diagnostic profile:

| Mode | Total elapsed | Key counters |
|---|---:|---|
| Python/no Rust | 1.2 s | `rust_static_eval_models=0` |
| Rust coverage, small-case threshold | 3.8 s | `rust_static_eval_models=2`, `rust_array_loop_enabled=0` |

Interpretation:

- The new IR coverage is functionally correct, but not yet a speed win on this mixed measurement-flow row.
- The remaining non-Rust models (`vin_src`, `lfsr`) are event/random/state-array heavy and dominate the practical value of this case.
- Rust array loops are threshold-gated because for 15-node small cases, per-step FFI calls for snapshot/err_ratio cost more than the Python loop.

## Functional Safety

- Default backend changed: `no`
- CSV schema changed: `no`
- Checker behavior changed: `no`
- Event ordering changed: `no`
- Rust path default: `off`
- Fallback path exists: `yes`

Safety boundaries:

- `cross`, `timer`, `above`, `$bound_step`, transition dynamics, dynamic bus access, arrays, integer-state logic, and child-model hierarchy still fallback to Python.
- Conditional IR supports one top-level ternary only. Nested conditions and nonlinear branches fallback.
- Differential conditional contribution is covered by regression: both true and false branch include the reference node term for `V(outp,outn)`.
- Rust array snapshot/err_ratio loops are enabled only for larger indexed arrays; small cases stay on the old Python/list path to avoid FFI overhead.

## Validation

Commands run:

```bash
python3 -m pytest tests/test_indexed_backend.py::test_static_linear_evaluate_ir_ignores_initial_step_event_body tests/test_indexed_backend.py::test_static_linear_evaluate_ir_lowers_top_level_ternary_state_assignment tests/test_indexed_backend.py::test_static_linear_evaluate_ir_lowers_ternary_differential_contribution tests/test_rust_backend.py::test_rust_backend_static_linear_batch_evaluates_conditional_select tests/test_engine.py::TestSimulator::test_rust_static_eval_handles_initial_step_and_conditional_state_model -q
python3 -m pytest tests/test_rust_backend.py -q
python3 -m pytest tests/test_engine.py -k 'rust_static_eval or rust_static_fast_sync' -q
cargo build --release
cargo test
python3 -m pytest -q
```

Results:

```text
targeted conditional/Rust IR: passed in repeated runs
Rust backend ctypes: 6 passed
engine Rust path: 9 passed
Rust core: 8 passed
full EVAS pytest: 488 passed
```

`cargo fmt --check` was attempted but this machine lacks the `rustfmt` component for `stable-aarch64-apple-darwin`.

## Learning Notes

这轮最重要的学习点是：**coverage expansion 和 speedup 是两件事**。

把 `dither_adder` 降到 Rust IR，说明我们已经能理解更多真实 Verilog-A evaluate 语义；但如果一个 testbench 里还有 `lfsr`、`vin_src` 这种 event/state-array/random 模型，仿真主循环仍然要执行大量 Python event logic。此时两个小模型进 Rust，反而可能因为 mixed sync 和 FFI 固定成本让 E2E 变慢。

所以后续优化顺序应该是：

1. 继续扩大 evaluate IR，但只优先覆盖真实 top-wall 中高调用、高占比、非事件的 model。
2. 对大 node-count 的 indexed array，迁移 `err_ratio`、snapshot、record/trace storage，而不是对小数组盲目 FFI。
3. 最后再做 event/timer/breakpoint queue Rust 化，因为那会触碰事件顺序和 Spectre parity，风险最高。

## Next Step

建议下一篇审计：

- `040 - Rust Transition/Event Boundary Profiling`

目标不是继续修 Python 小热点，而是把 top-wall 里真正挡住 Rust coverage 的几类语义拆清楚：

- `transition()` 是否能拆成 target update IR + waveform evaluation IR。
- integer scalar state 是否能映射到 typed Rust state slots。
- state array 和 dynamic bus 是否先做 indexed typed layout，再考虑 Rust loop。
- event/timer/cross queue 的最小可验证语义边界是什么。
