# 109 - Continuous Body and Slot Remap

Status: `verified-smoke`

Date: `2026-06-06`

Code commit: `pending`

Related reports:

- `speed-optimization/reports/rust_sim_program_109b_release_checker_smoke_20260606.json`
- `speed-optimization/reports/rust_sim_program_109b_release_checker_smoke_20260606.md`

## One-Line Summary

把 transition target 前的连续条件赋值、integer state、bit/bus 权重计算迁进 RustSimProgram，并修正 node lowering 中“模型局部 port slot”和“全局 node id”混用导致的 bit 权重错位。

## What Changed

本轮新增一个 RustSim event kind：`always`。它不是 Verilog-A 事件，而是 Rust scheduler 每个仿真时间点都执行的连续 body segment：

```text
Rust loop per point:
    write sources
    execute supported event bodies
    execute always continuous body assignments
    evaluate continuous linear ops
    apply transition target/output
    record selected nodes
```

这覆盖了真实 DAC 类模型中的常见模式：

```verilog
code = (V(b0)>vth ? 1 : 0) + (V(b1)>vth ? 2 : 0) + ...;
y = vlo + (vhi - vlo) * code / 15.0;
V(out) <+ transition(y, 0, tr, tr);
```

## Correctness Fix

108 的首轮 release smoke 里，DAC 输出从全 0 变成错误码序列。原因不是 ternary 或 bit 权重公式错误，而是 lowering 时把全局 node id 当成模型局部 port slot 传给 body expression encoder，随后又做了一次 local-slot -> global-node remap。

修正后：

- expression IR 内只保存模型局部 port slot；
- RustSimProgram build 阶段统一 remap 到全局 node id；
- source 添加顺序可以和 Verilog-A module port 顺序不同；
- bit/bus 权重不再依赖端口名或 source insertion order。

## Smoke Result

本地 EVAS-only release checker smoke，比较 `strict_current` 和 `profile_fast_evas2`。这不是 Spectre/AX claim，只证明当前 Rust EVAS2 子集与 Python EVAS strict 在这 4 行上 checker-equivalent。

| Entry | Form | EVAS2 status | safe_vs_strict | Key Rust counters | Speedup vs strict |
|---|---|---|---:|---|---:|
| `vbr1_l1_binary_weighted_voltage_dac` | `tb` | PASS | 1 | `always=1`, `body_stmt_ops=2`, `transition=1`, `generic_executor_runs=0` | 0.503x |
| `vbr1_l1_dac_mismatch_unit_weighting_model` | `tb` | PASS | 1 | `always=1`, `body_stmt_ops=1`, `transition=1`, `generic_executor_runs=0` | 1.571x |
| `vbr1_l1_pipeline_adc_stage` | `tb` | PASS | 1 | `event=3`, `body_stmt_ops=13`, `transition=3`, `generic_executor_runs=0` | 2.923x |
| `vbr1_l1_segmented_dac` | `tb` | PASS | 1 | `always=1`, `body_stmt_ops=2`, `transition=1`, `generic_executor_runs=0` | 0.997x |

Aggregate for this smoke:

- `profile_fast_evas2`: `4/4 PASS`, `4/4 safe_vs_strict`
- total wall: strict `2.877s`, EVAS2 `2.260s`
- median speedup vs strict: `1.571x`
- geomean speedup vs strict: `1.232x`

## Interpretation

This is a real coverage improvement, not a benchmark-name fastpath:

- conditionals are lowered through generic `IfStatementIR` / ternary expression IR;
- integer state writes use the existing Rust body target integer rounding path;
- bus/bit weighting is represented as generic expression ops over node reads;
- transition target expressions read Rust-owned state updated earlier in the same timestep.

The speed result is mixed. Pipeline and mismatch DAC benefit; binary DAC is slower because the current Rust scheduler records many source/transition breakpoints and executes always body at every point. Correctness is now fixed, but sparse scheduling and target-change filtering are still needed before making a speed claim.

## Remaining Gaps

- `timer()` is still not part of the generic RustSimProgram event queue.
- Complex state arrays, dynamic bus indexing, file/final-step side effects, `$bound_step`, and global adaptive error-ratio ownership remain outside this path.
- Release-wide coverage must be measured as row-level strict Rust EVAS2 checker parity, not just static candidate count.
