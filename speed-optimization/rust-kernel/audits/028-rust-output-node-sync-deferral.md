# 028 - Rust Output Node Sync Deferral

Status: `done`

Date: `2026-06-03`

Code commit: `EVAS 8782c11`

Related reports:

- `speed-optimization/rust-kernel/audits/027-rust-consecutive-model-segment-batch.md`
- `speed-optimization/rust-kernel/RUSTIFICATION_SLEEP_WORKLIST_20260603.md`

## One-Line Summary

在 opt-in Rust static affine path 中继续每步同步外部 `node_voltages`，但把 `model.output_nodes` 的值更新延迟到 `final_step` 前，减少 Python object/dict 写入。

## What Changed

| Layer | Before | After | User-visible behavior |
|---|---|---|---|
| Rust output sync | 每步写 `node_voltages` 和 `model.output_nodes` | 每步只写 `node_voltages`，`output_nodes` 在 final 前补齐 | opt-in only |
| counters | `rust_static_eval_output_syncs` 代表全部输出同步 | 新增 `node_voltage_syncs` / `deferred_output_syncs`，`output_syncs` 只表示真正写 `output_nodes` | opt-in only |
| tests | 只测 mapped affine 和 chain order | 增加 unmapped model parity，覆盖 error-control/output-node 边界 | no default change |

## Principle

027 之后的 Rust segment 已经把 FFI calls 降到每步一次，但仍然有大量 Python 侧写入：

```text
for each Rust op:
  node_voltages[external_node] = value
  model.output_nodes[local_node] = value
```

其中 `node_voltages` 仍然必须每步更新，因为后续 Python fallback model、record、event interpolation 和 error-control 都可能读它。

但 `model.output_nodes` 对 eligible static affine model 来说主要用于：

- 注册“这个 model 有哪些输出节点”；
- `final_step` 或 debug 状态读取最终输出；
- self-output fallback 读。

这些输出节点在 t=0 初始 Python evaluate 时已经注册，因此每一步都更新 `output_nodes` 的值不是必要的。028 改成：

```text
for each accepted step:
  Rust writes array slots
  sync external node_voltages only

before final_step:
  sync model.output_nodes once
```

这是一刀保守优化：不跳过 `node_voltages`，所以不会让后续仿真逻辑读到 stale dict。

## Before / After Evidence

| Metric | 027 diagnostic | 028 | Interpretation |
|---|---:|---:|---|
| local 64-model Rust median wall | `0.555189333 s` | `0.370936792 s` | Rust opt-in path 继续改善 |
| default Python median wall | `0.204989042 s` | `0.181447834 s` | Python 仍更快；不同 run 只作参考 |
| indexed-only median wall | `0.929563625 s` | `0.530767792 s` | 机器/噪声不同，不能当 028 claim |
| Rust FFI calls | `1001` | `1005` | 仍是 per-step segment call |
| Rust output_nodes writes | `64064` | `64` | 从每步每模型降到 final sync |
| Rust node_voltages writes | n/a | `64320` | 仍保留每步外部节点同步 |
| indexed repairs | `0` | `0` | dict/array 未发生 divergence |
| full EVAS tests | `457 passed` | `458 passed` | 默认路径未回归 |

028 的 benchmark 用 `1005` accepted steps，027 文档中的诊断样本是 `1001` steps，因此 wall time 只能作为方向性证据。最稳定的结论是 counter：

```text
output_syncs: 64
deferred_output_syncs: 64320
node_voltage_syncs: 64320
indexed_post_model_sync_repairs: 0
```

## Functional Safety

- Default backend changed: `no`
- CSV schema changed: `no`
- `strobe.txt` behavior changed: `no`
- Checker behavior changed: `no`
- Fallback path exists: `yes`
- Accuracy impact: `none expected`; mapped chain 和 unmapped model 均与 default Python waveform/step sizes 一致

## Validation

Commands run:

```bash
cargo test --release
python3 -m pytest tests/test_rust_backend.py tests/test_indexed_backend.py tests/test_engine.py::TestSimulator::test_rust_static_eval_matches_default_for_static_affine_model tests/test_engine.py::TestSimulator::test_rust_static_eval_batches_consecutive_affine_models_in_order tests/test_engine.py::TestSimulator::test_rust_static_eval_deferred_output_sync_preserves_unmapped_model tests/test_netlist.py::TestIndexedMigrationHarness::test_evas_simulate_logs_rust_static_eval_when_opted_in -q
python3 -m pytest tests -q
git diff --check
```

Results:

```text
cargo test --release: 3 passed
targeted pytest: 29 passed
full pytest: 458 passed
git diff --check: clean
```

Local microbenchmark output:

```text
python best 0.18049416699999998 median 0.18144783399999997 steps 1005 calls 0 segments 0 indexed_syncs 0 node_syncs 0 output_syncs 0 deferred 0 repairs 0 last 1.0070622219003786
indexed best 0.514948833 median 0.530767792 steps 1005 calls 0 segments 0 indexed_syncs 1005 node_syncs 0 output_syncs 0 deferred 0 repairs 0 last 1.0070622219003786
rust best 0.3227447090000002 median 0.3709367919999984 steps 1005 calls 1005 segments 1 indexed_syncs 1005 node_syncs 64320 output_syncs 64 deferred 64320 repairs 0 last 1.0070622219003786
```

## Learning Notes

这里要区分两个 Python 状态：

- `node_voltages`: 仿真全局节点电压，后续模型和 record 会读它。
- `model.output_nodes`: 某个模型对象自己的输出缓存，更多用于本模型输出注册、debug/final state。

如果直接两个都不写，Rust 会快一点，但 Python 模型可能读到旧值，仿真就不可信。

028 只延迟第二类写入，保留第一类写入。这就是“保守同步裁剪”：先砍掉证明不影响当前读路径的 Python object 写入，不急着让 Rust array 成为唯一状态源。

## Risks And Rollback

| Risk | Signal | Rollback |
|---|---|---|
| `output_nodes` 被某些 final/event 逻辑提前读取 | mapped/unmapped parity mismatch 或 final_step failure | 回退 `EVAS 8782c11` |
| 误以为可以跳过 `node_voltages` | 后续 Python model/record/event 读到 stale value | 继续保留 node sync，等 029/030 证明依赖后再动 |
| speed gain 被过度解释 | default Python 仍快于 Rust path | 文档保留 claim boundary |

## Next Step

- `029 - Indexed Dirty Validation Fastpath`

029 应减少每步全量 `indexed_array.max_abs_diff_mapping(self.node_voltages)` 的检查成本，但必须先有 mismatch injection test，证明 dirty validation 不会漏掉 array/dict divergence。
