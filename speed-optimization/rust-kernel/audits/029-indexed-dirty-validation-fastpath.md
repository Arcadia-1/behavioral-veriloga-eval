# 029 - Indexed Dirty Validation Fastpath

Status: `done`

Date: `2026-06-03`

Code commit: `EVAS 16cbe9d`

Related reports:

- `speed-optimization/rust-kernel/audits/028-rust-output-node-sync-deferral.md`
- `speed-optimization/rust-kernel/RUSTIFICATION_SLEEP_WORKLIST_20260603.md`

## One-Line Summary

在全 Rust static affine segment 场景下，用预计算 dirty node tuple 替代每步冗余全量 dict/array validation，减少 indexed validation 的 checked values。

## What Changed

| Layer | Before | After | User-visible behavior |
|---|---|---|---|
| indexed helper | 只能全量比较 mapping | 增加 `max_abs_diff_names()` 检查指定节点集合 | helper only |
| engine validation | indexed path 每步 snapshot 后全量 diff，model 后再全量 diff | 全 Rust static path 跳过 snapshot 后冗余 diff，model 后只查 source/output dirty tuple | opt-in only |
| mixed model guard | 无 dirty fastpath | 只要存在 Python model，就继续 full validation | safer mixed path |
| counters | 只有 checked values/syncs | 增加 dirty enabled/syncs/nodes checked/prev skips | opt-in diagnostics |

## Principle

028 后 Rust path 每步仍有两类 indexed validation：

```text
1. prev_nv = dict(node_voltages)
   compare indexed array vs prev_nv

2. after model eval
   compare indexed array vs node_voltages
```

对于全 Rust static affine segment，这两个检查里第一类是冗余的：上一轮 post-model validation 已经证明 dict/array 一致，中间没有新的写入。

029 因此只在很窄的条件启用 dirty validation：

```text
rust_static_eval=True
and all models are covered by Rust static segments
```

此时每步可能变化的节点集合可以在 run 开始时预计算：

```text
dirty_nodes = source_nodes + rust_segment_output_nodes
```

热路径不再维护 Python `set`，而是直接用固定 tuple 做 subset diff。

## Before / After Evidence

| Metric | 028 | 029 | Interpretation |
|---|---:|---:|---|
| local 64-model Rust median wall | `0.370936792 s` | `0.331407459 s` | Rust opt-in path 小幅改善 |
| indexed values checked | not recorded in 028 table | `65390` | 约为 indexed-only `130715` 的一半 |
| dirty validation enabled | n/a | `1` | 全 Rust static path 启用 |
| dirty syncs | n/a | `1005` | 每 accepted step 一次 dirty validation |
| dirty prev snapshot skips | n/a | `1005` | 每 accepted step 跳过一次冗余 full diff |
| indexed repairs | `0` | `0` | 没有依赖 repair 兜底 |
| full EVAS tests | `458 passed` | `460 passed` | 默认路径未回归 |

Local benchmark output:

```text
rust best 0.3271756670000001 median 0.33140745900000024 steps 1005 values_checked 65390 dirty_enabled 1 dirty_syncs 1005 dirty_checked 65325 dirty_prev_skips 1005 node_syncs 64320 output_syncs 64 deferred 64320 repairs 0 last 1.0070622219003786
```

For comparison, the same diagnostic shape without dirty validation showed:

```text
indexed best 0.5188790829999999 median 0.7100205420000001 steps 1005 values_checked 130715 dirty_enabled 0
```

Important rejected path:

```text
set-based dirty tracking: values_checked dropped, but Rust median regressed to about 0.532s
fixed dirty tuple: values_checked stays low and Rust median improves to about 0.331s
```

## Functional Safety

- Default backend changed: `no`
- CSV schema changed: `no`
- `strobe.txt` behavior changed: `no`
- Checker behavior changed: `no`
- Fallback path exists: `yes`
- Accuracy impact: `none expected`; dirty validation only enables when all models are Rust static segments

## Validation

Commands run:

```bash
cargo test --release
python3 -m pytest tests/test_rust_backend.py tests/test_indexed_backend.py tests/test_engine.py::TestSimulator::test_rust_static_eval_matches_default_for_static_affine_model tests/test_engine.py::TestSimulator::test_rust_static_eval_batches_consecutive_affine_models_in_order tests/test_engine.py::TestSimulator::test_rust_static_eval_deferred_output_sync_preserves_unmapped_model tests/test_engine.py::TestSimulator::test_rust_static_eval_keeps_full_indexed_validation_for_mixed_models tests/test_netlist.py::TestIndexedMigrationHarness::test_evas_simulate_logs_rust_static_eval_when_opted_in -q
python3 -m pytest tests -q
git diff --check
```

Results:

```text
cargo test --release: 3 passed
targeted pytest: 31 passed
full pytest: 460 passed
git diff --check: clean
```

## Learning Notes

“检查得少”不一定会更快。如果为了检查得少，每步先维护一个 Python `set`，这个 set 本身也有 hash/object 开销。

029 的经验是：

```text
bad:  每步构造/更新 dirty set
good: run 开始时预计算固定 dirty node tuple
```

这也说明 Rust 化前置 IR 的价值：只要我们能在编译/初始化阶段证明“哪些节点会被改”，热路径就能避免大量 Python 动态结构。

## Risks And Rollback

| Risk | Signal | Rollback |
|---|---|---|
| dirty validation 漏掉 Python model 写入 | mixed model test 或 full pytest failure | guard 保持 mixed path full validation |
| fixed dirty tuple 漏掉动态新增节点 | indexed repair/mismatch counter 非零 | 回退 `EVAS 16cbe9d` 或禁用 dirty fastpath |
| checked values 降低但 wall 变慢 | benchmark median 回退 | 已拒绝 set-based dirty tracking |

## Next Step

- `030 - Segment Lifecycle Fastpath`

030 应减少全 Rust static segment 中每个 model 仍然执行的 Python `_prepare_step()`、timer expire 和 post-update bookkeeping。
