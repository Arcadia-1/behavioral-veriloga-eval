# 027 - Rust Consecutive Model Segment Batch

Status: `done`

Date: `2026-06-03`

Code commit: `EVAS b9d5065`

Related reports:

- `speed-optimization/rust-kernel/audits/026-opt-in-static-continuous-model-rust-eval.md`
- `speed-optimization/rust-kernel/RUSTIFICATION_SLEEP_WORKLIST_20260603.md`

## One-Line Summary

把 026 的 Rust static affine path 从 `model x step` 小 FFI 调用改成每步一个 consecutive eligible segment 调用，显著降低跨 Python/Rust 边界开销，但还没有超过默认 Python backend。

## What Changed

| Layer | Before | After | User-visible behavior |
|---|---|---|---|
| engine Rust plan | 每个 eligible model 一个 Rust batch | 连续 eligible model 合并成一个 segment batch | opt-in only |
| evaluate loop | 每个 model 每步 `Python -> Rust -> Python` | segment 起点调用 Rust，segment 后续 model 跳过 | opt-in only |
| ordering guard | 单模型自然保持顺序 | 只 batch 连续 model index，按原模型顺序合并 ops | opt-in only |
| fallback | Rust 异常后单模型 Python fallback | Rust 异常后 segment 内模型按顺序 Python fallback，并同步 indexed array | opt-in only |
| counters | `models/ops/calls/errors/output_syncs` | 增加 `segments/max_segment_models` | opt-in only |

## Principle

026 证明 Rust 算术本身可以正确执行：

```text
values[vout_id] = gain * values[vin_id] + bias
```

但 026 的执行粒度太小：

```text
for step:
  for model:
    call Rust once
```

这会让每条很轻的乘加公式都付一次 `ctypes`/FFI 固定成本。027 改成：

```text
for step:
  prepare consecutive eligible models
  call Rust once for the whole segment
  sync segment outputs back to Python-visible state
```

数学上只要 segment 内 ops 按原模型顺序执行，就和 Python 逐模型执行等价。比如三个级联 gain：

```text
VIN -> N0 -> N1 -> VOUT
```

Rust batch 的 op 顺序是：

```text
N0 = f(VIN)
N1 = f(N0)
VOUT = f(N1)
```

第二条 op 读到的是第一条 op 刚写入的 array slot，因此级联语义保持不变。

## Before / After Evidence

| Metric | 026 | 027 | Interpretation |
|---|---:|---:|---|
| local 64-model Rust median wall | `0.852141417 s` | `0.325506250 s` | Rust opt-in path 约 `2.6x` 改善 |
| local Rust FFI calls | `64064` | `1001` | 从 `64 models x 1001 steps` 收成 `1 segment x 1001 steps` |
| Rust planned models | `64` | `64` | eligibility 不变 |
| Rust segments | n/a | `1` | 64 个连续 eligible model 合成一个 segment |
| max segment models | n/a | `64` | batch 覆盖完整级联 |
| full EVAS tests | `456 passed` | `457 passed` | 默认路径未回归 |

重要：027 不是最终速度胜利。更公平的 7-repeat local sample 显示：

| Mode | Median wall | Notes |
|---|---:|---|
| default Python | `0.204989042 s` | 当前仍最快 |
| Python indexed arrays | `0.929563625 s` | indexed sidecar 自身开销仍大 |
| Rust segment batch | `0.555189333 s` | 比 indexed path 快，但还慢于 default Python |

这说明 027 成功解决了 026 暴露的 FFI 小调用问题，但新的主要瓶颈变成：

- 每步 `indexed_array` 全量 sync/validate；
- 每步把 Rust output 同步回 Python dict/output_nodes；
- segment 内每个 model 仍然执行 Python `_prepare_step()`、timer expire 和 post-update bookkeeping；
- 当前只支持 literal static affine，真实 vaBench 里的复杂模型覆盖率还低。

## Functional Safety

- Default backend changed: `no`
- CSV schema changed: `no`
- `strobe.txt` behavior changed: `no`
- Checker behavior changed: `no`
- Fallback path exists: `yes`
- Accuracy impact: `none expected for eligible affine models`; targeted parity test 对比 default Python waveform

## Validation

Commands run:

```bash
cargo test --release
python3 -m pytest tests/test_rust_backend.py tests/test_indexed_backend.py tests/test_engine.py::TestSimulator::test_rust_static_eval_matches_default_for_static_affine_model tests/test_engine.py::TestSimulator::test_rust_static_eval_batches_consecutive_affine_models_in_order tests/test_netlist.py::TestIndexedMigrationHarness::test_evas_simulate_logs_rust_static_eval_when_opted_in -q
python3 -m pytest tests -q
git diff --check
```

Results:

```text
cargo test --release: 3 passed
targeted pytest: 28 passed
full pytest: 457 passed
git diff --check: clean
```

Local microbenchmark evidence:

```text
python best 0.17618145799999999 median 0.3138482909999999 steps 1001 rust_calls 0 rust_models 0 rust_ops 0 rust_segments 0 rust_max_segment 0
rust best 0.31479983300000036 median 0.3255062500000001 steps 1001 rust_calls 1001 rust_models 64 rust_ops 64 rust_segments 1 rust_max_segment 64
```

More diagnostic 7-repeat sample:

```text
python best 0.20088533399999997 median 0.204989042 calls 0 segments 0 sync_repairs 0 indexed_syncs 0 output_syncs 0
indexed best 0.6314419579999999 median 0.9295636249999997 calls 0 segments 0 sync_repairs 0 indexed_syncs 1001 output_syncs 0
rust best 0.4334367920000002 median 0.5551893329999995 calls 1001 segments 1 sync_repairs 0 indexed_syncs 1001 output_syncs 64064
```

## Learning Notes

Rust 并不会因为“语言更快”自动让程序变快。真正关键是让 Rust 一次处理足够多的连续数据。

可以把 FFI 理解成一次跨语言函数调用的门票成本。026 是：

```text
买 64064 次门票，每次只做一次很小的乘加
```

027 是：

```text
买 1001 次门票，每次做 64 个模型的乘加链
```

所以 Rust 路径明显变快。可它还慢于默认 Python，是因为我们仍然在每步做大量 Python 侧维护：

- array 和 dict 要互相校验；
- Rust 结果要写回 Python dict，方便后续 Python 模型、record、checker 使用；
- 每个模型仍走 Python 的 step prepare/post-update 框架；
- Rust 覆盖范围还只是极窄的 affine 模型。

这就是为什么 indexed 化不是终点，而是 Rust 化前置 IR：先把节点、状态、模型 IO 都编号，后面才能把更多 per-step 循环整体搬进 Rust，而不是只搬一条公式。

## Risks And Rollback

| Risk | Signal | Rollback |
|---|---|---|
| segment 破坏模型顺序 | 级联 affine test waveform mismatch | 回退 `EVAS b9d5065` 的 engine segment path |
| Python/Rust 状态不同步 | `indexed_post_model_sync_repairs > 0` 或 waveform mismatch | 保留单模型 fallback，收窄 segment eligibility |
| Rust opt-in 被误当 final speed claim | default Python 仍快于 Rust batch sample | 文档和 commit directive 明确禁止 claim |
| eligibility 过宽 | non-affine/event model 被 Rust path 接管 | 继续只允许 compiler-proven literal affine metadata |

## Next Step

- `028 - Rust Output Sync Gating`
- `029 - Indexed Dirty Sync / Validation Fastpath`
- `030 - Segment Lifecycle Fastpath`

这三步的共同目标是减少 027 后暴露出来的 Python side bookkeeping，而不是继续优化 Rust 里的乘加本身。
