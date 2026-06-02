# 022 - Rust FFI Batch Evaluate Boundary

Status: `done`

Date: `2026-06-03`

Code commit: `EVAS 8930bb9`

Related paths:

- `EVAS/evas/rust_core/Cargo.toml`
- `EVAS/evas/rust_core/src/lib.rs`
- `EVAS/evas/simulator/rust_backend.py`
- `EVAS/tests/test_rust_backend.py`

## One-Line Summary

新增零依赖 Rust `cdylib` 和 Python `ctypes` loader，建立生产 runtime 可调用的 static affine batch ABI。

## What Changed

| Layer | Before | After | User-visible behavior |
|---|---|---|---|
| Rust runtime boundary | 只有 prototype toy crate | 新增 `evas/rust_core`，导出 C ABI | 默认 EVAS 不变 |
| Python bridge | 没有 Rust loader | 新增 `evas.simulator.rust_backend` | 仅 opt-in 使用 |
| ABI unit test | 无 | `tests/test_rust_backend.py` 编译并调用 Rust release lib | 只影响测试 |

## Principle

这个改动属于 **降低每步成本** 的前置边界。

Rust 侧只接受简单连续数组和整数 id：

```text
ops[i] = {read_node_id, write_node_id, gain, bias}
values[write_node_id] = bias + gain * values[read_node_id]
```

这样避开 Python `dict[str, float]`、字符串 hash、对象分派和 generated Python expression 的热循环开销。这里叫 batch，是因为一个 FFI 调用可以执行多个 affine op；但 022 只建立 ABI 和 loader，跨 model / 跨 step 的大 batch 还没有完成。

## Before / After Evidence

| Metric | Before | After | Interpretation |
|---|---:|---:|---|
| Rust production-callable ABI | none | `evas_rust_evaluate_static_affine` | 可以从 Python runtime 调用 |
| Rust ABI tests | n/a | 3 passed | ABI 越界和 batch 顺序被锁住 |
| Python bridge tests | n/a | included in targeted 27 passed | `array('d')` buffer 可被 Rust 原地更新 |
| default EVAS runtime | Python only | unchanged | 没打开 opt-in 时不加载 Rust |

Validation commands:

```bash
cargo test --release
python3 -m pytest tests/test_rust_backend.py tests/test_indexed_backend.py tests/test_engine.py::TestSimulator::test_rust_static_eval_matches_default_for_static_affine_model tests/test_netlist.py::TestIndexedMigrationHarness::test_evas_simulate_logs_rust_static_eval_when_opted_in -q
python3 -m pytest tests -q
git diff --check
```

Important output:

```text
cargo test --release: 3 passed; 0 failed
targeted pytest: 27 passed
full pytest: 456 passed
git diff --check: clean
```

## Functional Safety

- Default backend changed: `no`
- CSV schema changed: `no`
- `strobe.txt` behavior changed: `no`
- Checker behavior changed: `no`
- Fallback path exists: `yes`

## Learning Notes

`ctypes` 是 Python 标准库里的 C ABI 调用工具。它的优点是零额外依赖，适合当前没有 PyO3/maturin 依赖、网络受限的环境；缺点是类型和内存布局要自己写清楚。

`array('d')` 是 Python 标准库的连续 double 数组。Rust 通过 `ctypes.from_buffer()` 拿到它的内存地址后，可以原地修改值，不需要把整个电压表复制来复制去。

## Risks And Rollback

| Risk | Signal | Rollback |
|---|---|---|
| 每个 model 每步都跨 FFI | 026 microbenchmark 显示 Rust opt-in 反而更慢 | 保留 ABI，下一步做更大粒度 batch |
| ABI library 缺失 | `rust_static_eval_available = 0` | 自动回退 Python evaluate |
| ctypes layout 写错 | Rust/Python bridge test 失败 | 回退 `evas/simulator/rust_backend.py` 和 `evas/rust_core` |

## Next Step

- `023 - Dynamic Bus Runtime Codegen Fix`
