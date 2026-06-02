# 026 - Opt-In Static Continuous Model Rust Eval

Status: `done`

Date: `2026-06-03`

Code commit: `EVAS 8930bb9`

Related paths:

- `EVAS/evas/simulator/backend.py`
- `EVAS/evas/simulator/engine.py`
- `EVAS/evas/rust_core/src/lib.rs`
- `EVAS/tests/test_engine.py`
- `EVAS/tests/test_netlist.py`

## One-Line Summary

完成 opt-in static affine continuous model 的 Rust evaluate 接入；功能正确，但本地 microbenchmark 显示当前 per-model FFI 粒度会让小模型场景变慢。

## What Changed

| Layer | Before | After | User-visible behavior |
|---|---|---|---|
| compiler eligibility | 无 | literal affine `V(out)<+a*V(in)+b` 会生成 `_rust_static_affine_ops` | 默认不变 |
| engine evaluate loop | 每个模型都 Python evaluate | opt-in eligible model 调 Rust，其他模型 Python fallback | opt-in |
| output sync | Python `_set_output()` 写 dict/array | Rust 写 array 后同步回 `output_nodes` 和 `node_voltages` | opt-in |
| profiler/counters | 无 Rust call 数 | 记录 models/ops/calls/errors/output syncs | opt-in |

## Principle

数学上，这个 lowering 是等价执行：

```verilog
V(vout) <+ 2.0 * V(vin) + 0.125;
```

Python 原路径每步做：

```text
read V(vin) -> compute -> _set_output(vout)
```

Rust opt-in 路径每步做：

```text
values[vout_id] = 0.125 + 2.0 * values[vin_id]
sync vout back to Python-visible dict/output_nodes
```

它不改变步长、event ordering、transition、timer、checker 或 CSV schema。当前只降低 eligible 模型内部表达式执行的对象开销；但因为仍然是每个 model 每步调用一次 Rust，FFI 固定成本会非常明显。

## Before / After Evidence

| Metric | Before | After | Interpretation |
|---|---:|---:|---|
| eligible static affine runtime | Python generated evaluate | opt-in Rust evaluate | 功能接入完成 |
| checker/result parity | Python baseline | Rust result matches on test model | 静态 affine 等价 |
| full EVAS tests | n/a | 456 passed | 默认路径未回归 |
| local 64-model median wall | `0.1788 s` | `0.8521 s` | 当前 FFI 粒度导致变慢 |
| local Rust FFI calls | `0` | `64064` | 64 models × 1001 steps |

Validation commands:

```bash
cargo test --release
python3 -m pytest tests/test_rust_backend.py tests/test_indexed_backend.py tests/test_engine.py::TestSimulator::test_rust_static_eval_matches_default_for_static_affine_model tests/test_netlist.py::TestIndexedMigrationHarness::test_evas_simulate_logs_rust_static_eval_when_opted_in -q
python3 -m pytest tests -q
git diff --check
```

Microbenchmark command shape:

```bash
cargo build --release
python3 -c '<64 static affine models, 1001 accepted steps, 5 repeats>'
```

Important output:

```text
cargo test --release: 3 passed; 0 failed
targeted pytest: 27 passed
full pytest: 456 passed
python best 0.176584333 median 0.178823208 steps 1001 rust_calls 0
rust best 0.453413708 median 0.852141417 steps 1001 rust_calls 64064 rust_models 64 rust_ops 64
```

Interpretation:

- 026 证明 Rust production path 可以正确接入。
- 026 也证明当前速度瓶颈不是 Rust 内部算术，而是 FFI 调用粒度。
- 不能用 026 声明 EVAS 变快；下一步必须把调用从 `model × step` 收成更大的 batch。

## Functional Safety

- Default backend changed: `no`
- CSV schema changed: `no`
- `strobe.txt` behavior changed: `no`
- Checker behavior changed: `no`
- Fallback path exists: `yes`
- Accuracy impact: `none expected for eligible affine models`; tests确认与 Python baseline 一致

## Learning Notes

Rust 快的前提是让它一次做足够多的工作。现在的结构是：

```text
for step:
  for model:
    Python -> Rust -> Python
```

这会产生很多跨语言小调用。每次调用都要准备 ctypes 参数、检查指针、进入动态库、返回 Python。对一个只有一条乘加公式的小模型来说，这个固定成本比 Rust 算术本身大得多。

更合理的下一步是：

```text
for step:
  prepare all models
  call Rust once for a consecutive eligible segment
  sync outputs once
```

或者更进一步：

```text
call Rust for many steps / many models
```

但跨 step batch 会碰到 source update、event、record、err_ratio 和 dynamic step adaptation，所以短期更现实的是 per-step consecutive segment batch。

## Risks And Rollback

| Risk | Signal | Rollback |
|---|---|---|
| 当前 Rust opt-in 被误报为速度优化成功 | microbenchmark 中 Rust median `0.8521 s` > Python `0.1788 s` | 文档保留 026 边界，下一步做 batch |
| eligibility 收得过宽 | Rust result 和 Python baseline 不一致 | 收窄 `_collect_rust_static_affine_ops()` |
| 输出同步遗漏 | `indexed_post_model_sync_repairs > 0` 或 waveform mismatch | 回退 engine Rust path |
| 默认路径被污染 | full pytest 失败或未开 env 时 counters 有 calls | 回退 `rust_static_eval` 入口 |

## Next Step

- `027 - Rust Consecutive Model Segment Batch`

027 应把当前 `64064` 次小 FFI 调用减少到接近 `1001` 次 per-step segment 调用。只有这个做完后，Rust static affine path 才有可能在真实 runtime 上体现速度优势。
