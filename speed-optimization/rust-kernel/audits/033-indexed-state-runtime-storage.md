# 033 - Indexed State Runtime Storage

Status: `done`

Date: `2026-06-03`

Code commit: `09f9ef5` (`EVAS`, branch `codex/evas-spectre-rulefix-20260529`)

Related reports:

- `speed-optimization/rust-kernel/audits/020-indexed-model-state-arrays.md`
- `speed-optimization/rust-kernel/audits/021-rust-model-evaluate-abi-prototype.md`
- `speed-optimization/rust-kernel/audits/032-dynamic-bus-base-offset-lowering.md`

## One-Line Summary

新增 opt-in indexed state runtime mirror，让 scalar、integer 和 array state 写入在保留 `self.state` / `self.arrays` 语义的同时，同步到连续 slot storage；这不是当前 Python 加速，而是 Rust state ABI 前置验证。

## What Changed

| Layer | Before | After | User-visible behavior |
|---|---|---|---|
| Scalar state write | generated code 直接 `self.state[name] = value` | 普通 assignment 走 `self._state_set(name, value)` | 默认结果不变 |
| Array state write | `_array_set()` 只写 `self.arrays` | opt-in 时同步写 `_indexed_state_array_values` | 默认结果不变 |
| Runtime switch | 无 state mirror 开关 | 新增 `indexed_state_storage=True` 和 `EVAS_INDEXED_STATE_STORAGE=1` | 显式 opt-in |
| Integer coercion | generated assignment 已对 integer state 调 `_to_integer()` | mirror 也按 integer state / integer array 规则存 float slot | Rust ABI 可区分 integer state |
| Counters | 只有 metadata count | 新增 state storage slots 和 write counters | 可量化 mirror 覆盖和开销 |

## Principle

这一步属于 **Rust 化前置数据结构准备**，不是直接速度优化。

Python 当前的 state 形状是：

```text
self.state["x"] = 1.25
self.arrays["accum"][3] = 0.7
```

Rust 更适合的形状是：

```text
state_values[0] = 1.25
array_values["accum"][3 - lo] = 0.7
```

033 先不让 Rust 接管 state，也不改变 state read。它只是新增一个 opt-in mirror：

```text
Python source of truth:
  self.state / self.arrays

Opt-in mirror:
  _indexed_state_values
  _indexed_state_array_values
```

这样后续 Rust model state ABI 可以先验证：

- scalar state 名字能稳定映射到 slot；
- integer state 能按 Verilog-A integer 规则存储；
- array state 能按 declared range 转成连续 slots；
- Python path 和 indexed mirror 的写入次数、slot 数量可观测。

## Before / After Evidence

| Metric | Default | Indexed state opt-in | Interpretation |
|---|---:|---:|---|
| stateful sample median wall | `0.007966792 s` | `0.010790875 s` | mirror 增加 Python 当前开销 |
| scalar writes mirrored | `0` | `2004` | 1001 steps 中 scalar state 写入被统计 |
| array writes mirrored | `0` | `3009` | array state 写入被统计 |
| out-of-bound array mirror writes | `0` | `0` | sample 没有越界写 |
| models with indexed state storage | `0` | `1` | opt-in 安装成功 |
| scalar slots | `0` | `2` | `x` 和 `code` |
| array slots | `0` | `8` | `accum[0:3]` + `bins[0:3]` |
| waveform parity | pass | pass | opt-in 不改变输出 |

解读：

- 033 短期在 Python 中会变慢，因为每次 state write 多了一次 mirror write。
- 这不是失败，而是预期成本：mirror 的价值是让后续 Rust 可以用连续数组接管 state read/write。
- 如果后续 Rust 能在 native loop 内读写这些 slots，当前 Python mirror overhead 会被替换掉，而不是保留下来。

## Functional Safety

- Default backend changed: `yes, generated scalar assignment now calls _state_set`, but `_state_set()` falls through to the old `self.state` behavior when mirror is disabled
- Opt-in required for mirror storage: `yes`
- CSV schema changed: `no`
- `strobe.txt` behavior changed: `no`
- Checker behavior changed: `no`
- Event ordering changed: `no`
- Rust ABI changed: `no`

## Validation

Commands run:

```bash
python3 -m pytest tests/test_indexed_backend.py::test_indexed_state_storage_mirrors_scalar_and_array_writes tests/test_engine.py::TestSimulator::test_indexed_state_storage_preserves_stateful_waveform_and_counts_writes tests/test_netlist.py::TestIndexedMigrationHarness::test_evas_simulate_logs_indexed_state_storage_when_opted_in -q
python3 -m pytest tests/test_indexed_backend.py tests/test_engine.py::TestSimulator tests/test_netlist.py::TestIndexedMigrationHarness -q
python3 -m pytest tests -q
cargo test --release
git diff --check
cargo clean
```

Results:

```text
targeted pytest: 3 passed
indexed/engine/netlist wider pytest: 59 passed
full pytest: 468 passed in 33.25s
cargo test --release: 3 passed
git diff --check: clean
```

Microbenchmark:

```text
default       median 0.007966792 best 0.007765833 scalar_writes 0    array_writes 0    oob 0 models 0 scalar_slots 0 array_slots 0 steps 1001
indexed_state median 0.010790875 best 0.010451292 scalar_writes 2004 array_writes 3009 oob 0 models 1 scalar_slots 2 array_slots 8 steps 1001
```

## Learning Notes

### 为什么这一步会变慢？

因为当前还是 Python 在跑：

```text
self.state["x"] = value
mirror[slot_of_x] = float(value)
```

这比只写 `self.state` 多做了一次 Python list 写入、一次 slot lookup 和一次计数器更新。所以在 Python 里短期变慢是合理的。

### 那为什么还要做？

Rust 化不能直接吃 Python dict：

```text
Rust cannot efficiently loop over self.state["x"]
```

Rust 想要的是：

```text
Vec<f64> state_values
Vec<f64> array_values
```

033 先把 state 的 runtime 形状准备出来，证明 slot 编号、integer coercion、array range 和写入生命周期是可观察、可测试的。后续 Rust 接管时，目标不是在 Python 旁边再写 mirror，而是让 Rust 成为主要执行 loop。

### 为什么不直接替换 state read？

state read 比 write 更危险。比如：

- `self.state` 里可能有 string parameter-like value；
- integer state 和 real state 有不同 coercion；
- event body、initial_step、final_step 可能依赖 state 更新顺序；
- loop variable 需要 `_loop_i` local variable 替换，不能简单全局改成 array read。

所以 033 只改 write mirror，不改 read source。后续要把 read 也 indexed/Rust 化，需要更细的 expression IR 和 state lifecycle 测试。

## Risks And Rollback

| Risk | Signal | Rollback |
|---|---|---|
| `_state_set()` 改变默认 assignment 行为 | full pytest 或 waveform parity 失败 | revert EVAS commit `09f9ef5` |
| loop variable 替换被破坏 | for-loop / dynamic bus / array tests 失败 | 检查 `_in_loop_var` guard 和 loop scaffolding |
| integer state mirror 与 Python state 不一致 | direct sidecar test 中 integer slot 不匹配 | 检查 `_to_integer()` use |
| 被误报为速度优化 | microbench 显示 opt-in path 变慢仍被写成 speedup | 引用本审计 claim boundary |

## Next Step

下一篇审计：

- `034-vabench-rust-coverage-smoke.md`：统计当前 vaBench/release 可仿任务中，哪些模型已具备 Rust/static/indexed lowering 条件，哪些仍卡在 event/state/dynamic bus/operator。
