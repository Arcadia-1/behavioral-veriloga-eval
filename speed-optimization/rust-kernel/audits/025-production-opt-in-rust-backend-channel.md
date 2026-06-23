# 025 - Production Opt-In Rust Backend Channel

Status: `done`

Date: `2026-06-03`

Code commit: `EVAS 8930bb9`

Related paths:

- `EVAS/evas/netlist/runner.py`
- `EVAS/evas/simulator/engine.py`
- `EVAS/evas/simulator/rust_backend.py`
- `EVAS/tests/test_netlist.py`

## One-Line Summary

把 Rust static affine backend 接入生产 runner 的显式开关和日志计数器，让 benchmark/harness 可以受控打开并观察 fallback。

## What Changed

| Layer | Before | After | User-visible behavior |
|---|---|---|---|
| env flag | 无 | `EVAS_RUST_STATIC_EVAL=1` | opt-in |
| simopt | 无 | `evas_rust_static_eval=true` | opt-in |
| indexed array dependency | 手动打开 `EVAS_INDEXED_ARRAYS` | Rust opt-in 自动启用 indexed arrays | 只影响 opt-in |
| log counters | 无 Rust runtime counters | `rust_static_eval_*` counters | 便于审计 |

## Principle

这个改动属于 **降低每步成本** 的生产通道准备，不是最终速度优化本身。

如果没有统一入口，后续 benchmark/harness 很难区分：

- 没打开 Rust；
- 打开了但库不存在；
- 库存在但没有 eligible model；
- eligible model 进入 Rust；
- Rust 出错后 fallback Python。

所以 025 增加这些计数器：

```text
rust_static_eval_requested
rust_static_eval_available
rust_static_eval_candidate_models
rust_static_eval_models
rust_static_eval_ops
rust_static_eval_calls
rust_static_eval_fallback_models
rust_static_eval_errors
```

## Before / After Evidence

| Metric | Before | After | Interpretation |
|---|---:|---:|---|
| runner opt-in flag | none | `EVAS_RUST_STATIC_EVAL=1` | harness 可打开 |
| missing Rust lib behavior | n/a | `available = 0`, fallback Python | 不破坏普通仿真 |
| available Rust lib behavior | n/a | `models = 1`, `ops = 1`, `errors = 0` in netlist test | 生产路径可调用 |
| default behavior | Python | unchanged | 默认不冒险 |

Validation commands:

```bash
python3 -m pytest tests/test_netlist.py::TestIndexedMigrationHarness::test_evas_simulate_logs_rust_static_eval_when_opted_in -q
python3 -m pytest tests -q
```

Important output:

```text
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

生产通道最重要的是“可观测”。如果只给一个开关但不写 counters，后续速度表很容易误判：看起来打开了 Rust，实际可能因为 dylib 缺失一直在 Python fallback。

因此 025 的重点不是速度数字，而是让每次实验都能回答：“到底有没有模型真正进入 Rust？”

## Risks And Rollback

| Risk | Signal | Rollback |
|---|---|---|
| opt-in flag 被误当默认加速 | logs 未显示 `evas_rust_static_eval = true` 却报告 Rust | 要求速度报告引用 counters |
| Rust lib 缺失导致实验误判 | `available = 0` 且 `models = 0` | 先 build Rust core，再 rerun |
| fallback 过多 | `candidate_models > models` | 检查 eligibility 和模型语义 |

## Next Step

- `026 - Opt-In Static Continuous Model Rust Eval`
