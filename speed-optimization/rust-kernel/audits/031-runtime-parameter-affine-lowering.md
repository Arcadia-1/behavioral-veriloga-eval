# 031 - Runtime Parameter Affine Lowering

Status: `done`

Date: `2026-06-03`

Code commit: `1b5330a` (`EVAS`, branch `codex/evas-spectre-rulefix-20260529`)

Related reports:

- `speed-optimization/rust-kernel/audits/026-opt-in-static-continuous-model-rust-eval.md`
- `speed-optimization/rust-kernel/audits/027-rust-consecutive-model-segment-batch.md`
- `speed-optimization/rust-kernel/audits/030-segment-lifecycle-fastpath.md`

## One-Line Summary

把 `gain` / `bias` 来自 numeric parameters 的静态 affine model 纳入 Rust static eval 覆盖范围，并在每个 instance 已经应用 netlist parameter override 后再求最终 float 系数。

## What Changed

| Layer | Before | After | User-visible behavior |
|---|---|---|---|
| Compiler metadata | `_rust_static_affine_ops` 只接受 literal numeric coefficient | 支持 parameter-only scalar descriptor，例如 `("param", "gain")` 或 `("div", ("param", "a"), ("param", "b"))` | 默认 backend 不变 |
| Rust plan builder | 直接把 metadata 中的 `gain/bias` 转成 float | 对每个 model instance 用 `model.params` 求值，再生成 `StaticAffineOp` | instance parameter override 能影响 Rust path |
| Safety counters | 只能看到 Rust models/ops | 新增 `rust_static_eval_runtime_param_ops` 和 `rust_static_eval_coeff_eval_fallbacks` | 可审计 parameterized affine 是否进入 Rust |
| Tests | 只有 literal affine Rust lowering | 增加 compiler metadata、direct simulator override、netlist instance override 测试 | 输出 parity 保持 |

## Principle

这次主要属于 **扩大 Rust coverage**，不是减少同一个模型的每步成本。

之前 Rust static eval 的 eligible 形式是：

```text
V(out) <+ 2.0 * V(in) + 0.125
```

真实 Verilog-A 更常见的是：

```text
parameter real gain = 2.0;
parameter real offset = 0.125;
V(out) <+ gain * V(in) + offset;
```

如果 compiler 在 class 级别直接把参数默认值冻结成 float，Spectre netlist 里的 instance override 会被 Rust path 忽略，例如：

```text
I0 (vin vout) gain_param gain=3 offset=250m
```

所以 031 不在 compile 阶段算最终系数，而是保存一个很小的 parameter-only 表达式 descriptor。`Simulator.run()` 构建 Rust plan 时，每个 model 已经有自己的 `model.params`，这时再求出当前 instance 的 `gain/bias`，传给原来的 Rust ABI。

Rust ABI 没变：Rust 仍然只接收 `double gain` 和 `double bias`。

## Before / After Evidence

| Metric | Before | After | Interpretation |
|---|---:|---:|---|
| parameterized affine Rust metadata | rejected | accepted | `gain * V(vin) + offset` 现在能进入 `_rust_static_affine_ops` |
| netlist instance parameter override | Python only | Rust opt-in parity pass | `gain=3 offset=250m` 最终 `vout=2.5` |
| 64-model parameterized affine, default Python median | n/a | `0.1918 s` | 1001 steps, DC input |
| 64-model parameterized affine, Rust static eval median | n/a | `0.2322 s` | Rust still slower on fixed-step sample |
| Rust planned models / ops | `0` | `64 / 64` | coverage expansion works |
| `rust_static_eval_runtime_param_ops` | `0` | `64` | 每个 model 的 coefficient 都来自 runtime params |
| `rust_static_eval_coeff_eval_fallbacks` | n/a | `0` | 参数表达式求值未触发 fallback |
| lifecycle skips | `0` | `64064` | 1001 steps * 64 models |

解读：

- 031 的价值是把常见 parameterized affine model 从 Python-only coverage 推进到 Rust static segment coverage。
- 固定步数 microbenchmark 中 Rust 仍慢于默认 Python，说明当前瓶颈仍是 Python/Rust 边界、dict sync 和 validation，而不是 Rust 乘加本身。
- 这一步为后续更大表达式 IR 和真实 vaBench coverage audit 做准备。

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
python3 -m pytest tests/test_rust_backend.py tests/test_indexed_backend.py::test_compiled_model_records_rust_static_affine_ops_for_literal_linear_model tests/test_indexed_backend.py::test_compiled_model_records_rust_static_affine_ops_for_parameterized_linear_model tests/test_indexed_backend.py::test_compiled_model_rejects_rust_static_affine_ops_for_stateful_model tests/test_engine.py::TestSimulator::test_rust_static_eval_applies_runtime_parameter_overrides tests/test_engine.py::TestSimulator::test_rust_static_eval_matches_default_for_static_affine_model tests/test_netlist.py::TestIndexedMigrationHarness::test_evas_simulate_logs_rust_static_eval_when_opted_in tests/test_netlist.py::TestIndexedMigrationHarness::test_evas_simulate_rust_static_eval_uses_instance_parameter_overrides -q
python3 -m pytest tests/test_indexed_backend.py::test_compiled_model_records_rust_static_affine_ops_for_parameterized_linear_model tests/test_indexed_backend.py::test_compiled_model_records_rust_static_affine_ops_for_parameter_expression_model tests/test_engine.py::TestSimulator::test_rust_static_eval_applies_runtime_parameter_overrides tests/test_netlist.py::TestIndexedMigrationHarness::test_evas_simulate_rust_static_eval_uses_instance_parameter_overrides -q
python3 -m pytest tests -q
git diff --check
cargo clean
```

Results:

```text
cargo test --release: 3 passed
initial targeted pytest: 9 passed
parameter-expression targeted pytest: 4 passed
full pytest: 464 passed in 35.90s
git diff --check: clean
```

Microbenchmark:

```text
64-model parameterized affine DC fixed-step sample:
  python_default median = 0.191835834 s, steps = 1001
  rust_static median    = 0.232150334 s, steps = 1001
  rust models / ops     = 64 / 64
  runtime_param_ops     = 64
  coeff fallbacks       = 0
  lifecycle skips       = 64064
```

## Learning Notes

这里有一个容易误解的点：parameter 不是普通常数。

Verilog-A 文件里会写默认值：

```text
parameter real gain = 2.0;
```

但 Spectre netlist 可以对每个 instance 改它：

```text
I0 (...) gain_param gain=3
I1 (...) gain_param gain=4
```

所以 class-level metadata 不能直接把 `gain` 固定成 `2.0`。正确做法是：

1. compiler 只记录“这个 coefficient 来自参数 gain”；
2. netlist runner 创建每个 model instance，并把 override 写到 `model.params`；
3. simulator 开始 run 前构建 Rust plan，用当前 instance 的 `model.params` 算出 float；
4. Rust kernel 仍然只处理普通 `f64` 数组和 `gain/bias`。

这样既保留了 parameter override 语义，也不需要 Rust 先学会完整 Verilog-A 参数系统。

## Risks And Rollback

| Risk | Signal | Rollback |
|---|---|---|
| 参数在 compile 阶段被错误冻结 | netlist override test 中 `vout` 不等于 override 结果 | revert EVAS commit `1b5330a` |
| descriptor 误接受 state/function/string | stateful/string/function model 进入 Rust 并产生 parity mismatch | 保持 `_rust_scalar_expr()` 只接受 REAL/INTEGER parameter 和 arithmetic |
| runtime coeff 求值失败后误报 Rust coverage | `rust_static_eval_coeff_eval_fallbacks` 非零且 models/ops 计数异常 | 检查 engine plan builder fallback 逻辑 |

## Next Step

下一篇审计：

- `032-dynamic-bus-base-offset-lowering.md`：把简单 `V(bus[i])` / `V(bus[i][j])` 从字符串节点格式化推进到 base+offset node-id lowering。
