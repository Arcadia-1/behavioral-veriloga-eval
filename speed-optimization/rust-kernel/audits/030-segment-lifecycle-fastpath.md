# 030 - Segment Lifecycle Fastpath

Status: `done`

Date: `2026-06-03`

Code commit: `3589841` (`EVAS`, branch `codex/evas-spectre-rulefix-20260529`)

Related reports:

- `speed-optimization/rust-kernel/audits/027-rust-consecutive-model-segment-batch.md`
- `speed-optimization/rust-kernel/audits/028-rust-output-node-sync-deferral.md`
- `speed-optimization/rust-kernel/audits/029-indexed-dirty-validation-fastpath.md`

## One-Line Summary

对已经由 compiler/Rust eligibility 证明为静态 affine 的 Rust segment，成功走 Rust batch 时跳过每个 model 的 Python `_prepare_step()`、timer expire 和 post-update bookkeeping；fallback 仍完整走原 Python 生命周期。

## What Changed

| Layer | Before | After | User-visible behavior |
|---|---|---|---|
| Simulator loop | Rust static segment 成功前仍逐 model 调 `_prepare_step()`，成功后仍逐 model 调 `_expire_absolute_timers()` 和 post-update 空检查 | Rust segment 成功时只做 Rust batch eval、必要 `node_voltages` sync 和计数；生命周期工作只在 Rust fallback 时执行 | 默认 backend 不变；`rust_static_eval=True` opt-in path 输出保持 parity |
| Perf counters | 没有区分 Rust segment lifecycle skip | 新增 `rust_static_eval_lifecycle_model_skips` | 方便审计每步到底跳过了多少 compiler-proven static model |
| Tests/logs | Rust log 只看 calls/sync/errors | Rust tests 和 netlist log 增加 lifecycle skip 断言 | runner 可见性增强，不改 CSV |

## Principle

这次属于 **降低每步成本**。

静态 affine Rust segment 的数学形式是：

```text
V(out) = gain * V(in) + bias
```

eligible segment 已经满足这些条件：

- analog body 只包含 unconditional voltage contribution；
- 没有 `cross/above/timer` post-update events；
- 没有 future-node read；
- 没有 child models；
- 没有 `$bound_step` 或动态 breakpoint；
- Rust batch 按 model 顺序执行，仍保留链式依赖顺序。

因此，Rust success path 每步真正需要做的是把 indexed voltage array 中的输入 slot 乘加写到输出 slot。以前保留的 `_prepare_step()`、timer expire 和 post-update 空检查，在这个子集里只是 Python bookkeeping，不参与数值计算。

重要边界：这不是全局跳过 lifecycle。只要 Rust call 失败或模型不属于 eligible segment，就走原 Python prepare/evaluate/post-update 路径。

## Before / After Evidence

| Metric | Before | After | Interpretation |
|---|---:|---:|---|
| 029 reference, 64-model static affine sample Rust median | `0.3314 s` | not directly rerun with identical pre-030 artifact | 029 的主要瓶颈已从 full validation 转到 lifecycle/sync/FFI |
| DC fixed-step sample, default Python median | n/a | `0.3336 s` | 1001 steps, 64 models, fixed input |
| DC fixed-step sample, Rust static eval median | n/a | `0.3959 s` | Rust 仍慢于 default Python；说明 FFI/sync/indexed validation 仍是剩余开销 |
| DC fixed-step sample, Rust lifecycle skips | `0` | `64064` | `1001 steps * 64 models`，计数精确命中 segment model-step |
| DC fixed-step sample, dirty checked values | n/a | `65130` | dirty validation 仍在，每步检查 source/output tuple |
| Ramp dynamic-step sample, default Python median | n/a | `12.3813 s` | 25048 steps，源 ramp 触发动态缩步，非 paper claim |
| Ramp dynamic-step sample, Rust static eval median | n/a | `6.1332 s` | 长步数压力下 Rust segment lifecycle skip 有明显收益 |
| Ramp dynamic-step sample, Rust lifecycle skips | `0` | `1603072` | `25048 steps * 64 models` |
| checker/result parity | pass | pass | 单测、netlist log、全量 pytest 均通过 |

解读：

- 030 的直接证明不是“Rust 已经总是更快”，而是“静态 segment 的 Python lifecycle bookkeeping 可以安全移出 hot loop”。
- 固定步数 DC 样本仍显示 Rust opt-in path 慢于 default Python，这说明后续还必须继续减少 `node_voltages` dict sync、dirty validation 和 FFI/ctypes 边界。
- 动态缩步 ramp 样本中 Rust 更快，但这个样本由误差控制产生 25k steps，不是 vaBench/Spectre/AX paper-facing speed claim。

## Functional Safety

- Default backend changed: `no`
- CSV schema changed: `no`
- `strobe.txt` behavior changed: `no`
- Checker behavior changed: `no`
- Fallback path exists: `yes`

## Validation

Commands run:

```bash
cargo test --release
python3 -m pytest tests/test_rust_backend.py tests/test_indexed_backend.py tests/test_engine.py::TestSimulator::test_rust_static_eval_matches_default_for_static_affine_model tests/test_engine.py::TestSimulator::test_rust_static_eval_batches_consecutive_affine_models_in_order tests/test_engine.py::TestSimulator::test_rust_static_eval_deferred_output_sync_preserves_unmapped_model tests/test_engine.py::TestSimulator::test_rust_static_eval_keeps_full_indexed_validation_for_mixed_models tests/test_netlist.py::TestIndexedMigrationHarness::test_evas_simulate_logs_rust_static_eval_when_opted_in -q
python3 -m pytest tests -q
git diff --check
cargo clean
```

Results:

```text
cargo test --release: 3 passed
targeted pytest: 31 passed
full pytest: 460 passed in 37.71s
git diff --check: clean
```

Microbenchmarks:

```text
64-model DC fixed-step sample:
  python_default median = 0.333597084 s, steps = 1001
  indexed_only median   = 1.225499584 s, steps = 1001
  rust_static median    = 0.395932084 s, steps = 1001
  rust lifecycle skips  = 64064

64-model ramp dynamic-step sample:
  python_default median = 12.381274625 s, steps = 25048
  indexed_only median   = 14.662830750 s, steps = 25048
  rust_static median    = 6.133186000 s, steps = 25048
  rust lifecycle skips  = 1603072
```

## Learning Notes

可以把每个 model 想成一个小函数。普通 Python 路径每一步会做三类事：

1. 先准备本步的上下文：上一拍电压、当前电压、未来源值等；
2. 执行 model 的电压计算；
3. 再检查有没有 timer/cross/above 之类的事件、是否需要刷新输出。

Rust static affine segment 是一个很窄但很干净的子集：它没有事件，也没有内部状态机，只是把输入电压做一次线性变换写到输出。因此第 1 和第 3 类工作在这个子集里是空转。

这也是为什么必须有 eligibility guard：如果一个模型有 timer 或 cross，跳过 lifecycle 就可能漏掉事件；如果一个模型只有 `V(out) <+ gain * V(in) + bias`，跳过 lifecycle 才是合理的。

## Risks And Rollback

| Risk | Signal | Rollback |
|---|---|---|
| eligibility guard 过宽，错误跳过动态模型 lifecycle | EVAS/Spectre parity 下降，或 Rust mixed-model test 中 Python model post-update call 数不对 | revert EVAS commit `3589841` |
| fallback path 漏掉 prepare/post-update | Rust backend error 后 waveform/test 失败 | revert `evas/simulator/engine.py` 的 segment fallback 移动 |
| perf counter 被误读为 speed claim | 报告宣称 Rust 已 paper-facing 快于 AX | 保持本审计的 claim boundary：这里只是 opt-in microbenchmark/engineering evidence |

## Next Step

下一篇审计：

- `031-runtime-parameter-affine-lowering.md`：让 Rust static affine 覆盖 `gain/bias` 来自 parameter override 的真实模型，而不是只覆盖 literal 常数。
