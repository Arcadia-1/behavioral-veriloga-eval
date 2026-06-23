# 037 - Static Linear Evaluate IR B1-B4

Status: `done`

Date: `2026-06-03`

Code commit: `pending`

Related reports:

- `EVAS/evas/simulator/evaluate_ir.py`
- `EVAS/evas/simulator/backend.py`
- `EVAS/evas/simulator/engine.py`
- `EVAS/evas/simulator/rust_backend.py`
- `EVAS/evas/rust_core/src/lib.rs`

## One-Line Summary

把 Rust 原型从单输入 `static affine` 扩展为有明确 IR 边界的 `static linear evaluate`，覆盖 B1-B4 的静态节点、多输入表达式/contribution、简单 scalar state 读写。

## What Changed

| Layer | Before | After | User-visible behavior |
|---|---|---|---|
| compiler/backend | 只记录 `_rust_static_affine_ops`，形状限于 `V(out) <+ gain * V(in) + bias` | 新增 `_evaluate_ir_static_linear_ops`，可记录 `node/state` source 和 `node/state` target 的有序线性 op | 默认 Python evaluator 不变 |
| Python IR | 没有单独的 evaluate IR parity executor | 新增 `evaluate_ir.py`，提供 `normalize_linear_ops()` 和 Python array executor | 仅测试/诊断使用 |
| Rust ABI | `evas_rust_evaluate_static_affine(ops, values)` | 新增 `evas_rust_evaluate_static_linear(ops, terms, node_values, state_values)` | 旧 ABI 保留 |
| engine | opt-in Rust static eval 只执行 affine batch | opt-in Rust static eval 优先执行 static linear IR；stateful segment 单模型执行，node-only segment 仍可 batch | `EVAS_RUST_STATIC_EVAL=1` 下覆盖更多模型 |
| tests | 只验证 static affine | 新增 differential linear、state assignment/output、self-ref fallback、Rust node/state buffer、engine parity 测试 | 功能不删减 |

## Principle

这次不是继续做零散 Python helper 小修，而是建立一个可被 Rust 消费的 evaluate IR：

- **降低每步成本**：把 `V(node)` / `state["x"]` 这类热路径从字符串和 dict 访问，转为 node/state id + array index。
- **扩大 batch 粒度**：一个 Rust call 可以执行多个 ordered linear op，而不是每个表达式单独跨 FFI。
- **保留 fallback**：event、dynamic node、array、整数 state、自引用状态更新、非线性函数仍走 Python evaluator。

IR 目前只覆盖静态线性段，形式是：

```text
target = bias + sum(gain_i * source_i)
source_i = node[id] or state[id]
target = node[id] or state[id]
```

例子：

```verilog
sample = 2.0 * V(vin) + 0.1;
V(vout) <+ sample + 0.2;
```

会降成两个 ordered op：

```text
state(sample) = 0.1 + 2.0 * node(vin)
node(vout) = 0.2 + 1.0 * state(sample)
```

## Before / After Evidence

Targeted microbench, local-only, not paper-facing. Each case used median over repeated local runs.

| Case | Python wall | Rust wall | Python model eval | Rust eval segment | Interpretation |
|---|---:|---:|---:|---:|---|
| single static affine op | 0.459408 s | 1.282007 s | 0.053449 s | 0.234135 s | 单 op 不划算，FFI/indexed sync 开销盖过收益 |
| single differential linear op | 0.771650 s | 2.452090 s | 0.110277 s | 0.415195 s | 多 source 但 batch 太小，仍不划算 |
| single state linear model | 0.427202 s | 1.296274 s | 0.056236 s | 0.261791 s | B4 功能可行，但单模型不应 claim 加速 |
| 10-model affine chain | 1.370094 s | 1.439743 s | 0.320220 s | 0.193274 s | Rust eval 段已快，但 E2E 基本持平 |
| 100-model affine chain | 9.593462 s | 8.761598 s | 2.579396 s | 0.880682 s | batch 后 Rust eval 段 2.93x，E2E 1.10x |
| 500-model affine chain | 48.308435 s | 43.396182 s | 13.526968 s | 4.018397 s | batch 后 Rust eval 段 3.37x，E2E 1.11x |

Interpretation:

- Rust native loop 已经能降低 batched evaluate 段成本。
- 单 op/单模型 Rust 化不是正确方向，因为 ctypes FFI、indexed array sync、dirty validation、record/error-control 仍有固定成本。
- 下一步必须继续扩大 per-call work，并减少每步 sync/validation 开销。

## Functional Safety

- Default backend changed: `no`
- CSV schema changed: `no`
- `strobe.txt` behavior changed: `no`
- Checker behavior changed: `no`
- Fallback path exists: `yes`

Unsupported patterns that intentionally fallback:

- event statements and event-dependent operators
- dynamic bus/node indexes
- arrays
- integer state
- self-referential state update such as `x = x + 1`
- non-linear functions and comparisons
- child-model hierarchy
- models needing future node voltages or post-update events

## Validation

Commands run:

```bash
python3 -m pytest tests/test_indexed_backend.py::test_compiled_model_records_static_linear_evaluate_ir_for_differential_model tests/test_indexed_backend.py::test_static_linear_evaluate_ir_executes_state_assignment_then_output tests/test_indexed_backend.py::test_static_linear_evaluate_ir_rejects_self_referential_state_update -q
python3 -m pytest tests/test_rust_backend.py -q
python3 -m pytest tests/test_engine.py::TestSimulator::test_rust_static_eval_matches_default_for_static_affine_model tests/test_engine.py::TestSimulator::test_rust_static_eval_applies_runtime_parameter_overrides tests/test_engine.py::TestSimulator::test_rust_static_eval_batches_consecutive_affine_models_in_order tests/test_engine.py::TestSimulator::test_rust_static_eval_deferred_output_sync_preserves_unmapped_model tests/test_engine.py::TestSimulator::test_rust_static_eval_keeps_full_indexed_validation_for_mixed_models tests/test_engine.py::TestSimulator::test_rust_static_eval_handles_simple_state_linear_model -q
python3 -m pytest tests/test_netlist.py::TestIndexedMigrationHarness::test_evas_simulate_logs_rust_static_eval_when_opted_in tests/test_netlist.py::TestIndexedMigrationHarness::test_evas_simulate_rust_static_eval_uses_instance_parameter_overrides -q
cargo test
python3 -m pytest -q
```

Results:

```text
IR targeted: 3 passed
Rust backend targeted: 3 passed
Engine Rust/static targeted: 6 passed
Netlist Rust/static targeted: 2 passed
Rust core: 5 passed
Full EVAS pytest: 478 passed
```

## Learning Notes

这次的核心学习点是：Rust 快，不等于“只要进 Rust 就快”。

Python 当前的主要成本来自：

```text
self._get_voltage("vin", nv)
self.state["sample"]
self._set_output("vout", value, nv)
```

这些操作每次都涉及 Python 函数、字符串、dict、object。Rust 的理想路径是：

```text
node_values[vin_id]
state_values[sample_id]
node_values[vout_id] = value
```

但 Python 和 Rust 之间还有 FFI 边界。一次 FFI 调用如果只做一个乘加，收益会被固定调用成本吃掉；一次 FFI 调用如果做 100 个或 500 个模型 op，固定成本被摊薄，Rust loop 的优势才显出来。

所以后续优化重点不是“让更多小片段勉强 Rust 化”，而是：

```text
更大的 segment
更少的 Python/Rust 往返
更少的 indexed sync/dirty validation
更少的 Python lifecycle/post-processing
```

## Risks And Rollback

| Risk | Signal | Rollback |
|---|---|---|
| IR 误收不该 Rust 化的模型 | 新增 waveform/checker mismatch | revert `backend.py` IR collector and engine linear path |
| stateful segment 语义偏差 | state-linear parity test fail | fallback all state target/source ops |
| FFI 固定成本导致小模型慢 | single-op microbench slower | keep Rust path opt-in; only claim batched segment speed |
| indexed sync 仍限制 E2E | Rust eval faster but wall only small gain | optimize sync/validation/record boundary next |

## Next Step

下一篇审计建议：

- `038 - Static Linear Segment Sync Reduction`

目标：在 Rust static linear segment 成功后，减少每步 `node_voltages` dict sync、dirty validation 和 model output set 刷新，让 Rust eval 段收益更多反映到 E2E wall。
