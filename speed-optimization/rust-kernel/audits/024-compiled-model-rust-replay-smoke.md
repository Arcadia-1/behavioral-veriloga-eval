# 024 - Compiled Model Rust Replay Smoke

Status: `done`

Date: `2026-06-03`

Code commit: `EVAS 8930bb9`

Related paths:

- `EVAS/evas/simulator/backend.py`
- `EVAS/evas/simulator/engine.py`
- `EVAS/tests/test_engine.py`
- `EVAS/tests/test_netlist.py`

## One-Line Summary

用真实 parser/compiler/simulator/netlist 路径上的临时 static affine Verilog-A 模型验证 Rust replay，不再只停留在 toy prototype。

## What Changed

| Layer | Before | After | User-visible behavior |
|---|---|---|---|
| compiler metadata | 无 Rust eligibility | `_rust_static_affine_ops = (read, write, gain, bias)` | 默认仿真不变 |
| engine replay | Rust prototype 不接生产 engine | `Simulator.run(..., rust_static_eval=True)` 可调用 Rust | opt-in |
| netlist replay | 无 env/simopt 入口 | `EVAS_RUST_STATIC_EVAL=1` / `evas_rust_static_eval=true` | opt-in |

## Principle

这个改动属于 **降低每步成本** 的真实路径 smoke。

021 只证明 Rust 里可以跑 node/state id toy kernel。024 则验证完整路径：

```text
Verilog-A source -> parser -> compiler metadata -> Simulator.run -> indexed voltage array -> Rust ABI -> CSV/log
```

当前 eligibility 非常保守，只接受 literal affine:

```verilog
V(vout) <+ 2.0 * V(vin) + 0.125;
```

如果模型含有参数、状态变量、event、transition、dynamic index、function call 或 differential branch，就不进入 Rust replay。

## Before / After Evidence

| Metric | Before | After | Interpretation |
|---|---:|---:|---|
| real compiled model Rust replay | none | available opt-in | 从 toy 进入生产路径 |
| default Python result | baseline | unchanged | 关闭 opt-in 不变 |
| Rust opt-in parity | n/a | matches Python on gain model | 静态 affine 可等价 replay |
| vaBench release row replay | not run | not run | 不能声明 release-wide 效果 |

Validation commands:

```bash
python3 -m pytest tests/test_engine.py::TestSimulator::test_rust_static_eval_matches_default_for_static_affine_model -q
python3 -m pytest tests/test_netlist.py::TestIndexedMigrationHarness::test_evas_simulate_logs_rust_static_eval_when_opted_in -q
python3 -m pytest tests -q
```

Important output:

```text
engine Rust opt-in test: passed
netlist Rust opt-in log test: passed
full pytest: 456 passed
```

## Functional Safety

- Default backend changed: `no`
- CSV schema changed: `no`
- `strobe.txt` behavior changed: `no`
- Checker behavior changed: `no`
- Fallback path exists: `yes`

## Learning Notes

这里的“replay”意思是：模型表达式已经由 Python 编译器识别成很简单的数学形式，Rust 只是按同样的公式重新执行一遍。

这不是重新写完整 Verilog-A 编译器，也不是完整 Rust 仿真器。它只是把最简单的一类连续贡献先迁移到 Rust，用来验证 ABI、array、node-id、fallback 和日志入口。

## Risks And Rollback

| Risk | Signal | Rollback |
|---|---|---|
| 把临时 gain 模型误当 vaBench row | 文档或汇报出现 release-wide claim | 明确 024 只是 compiled-model smoke |
| eligibility 过宽 | 含状态/event 的模型进入 Rust 后 parity 失败 | 收窄 `_collect_rust_static_affine_ops()` |

## Next Step

- `025 - Production Opt-In Rust Backend Channel`
