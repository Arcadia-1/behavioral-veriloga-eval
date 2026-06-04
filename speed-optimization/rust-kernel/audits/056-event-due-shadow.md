# 056 - Event Due Shadow

Status: `done`

Date: `2026-06-04`

Code commit: `pending`

Related documents:

- `051-timer-step-rust-primitives.md`
- `052-cross-above-detector-rust-primitives.md`
- `055-event-lifecycle-production-gate.md`
- `../behavior-coverage-map.v1.json`

## One-Line Summary

新增 opt-in `rust_event_due_shadow` 路径：Python 仍然执行生产事件检测和 event body，Rust 只用同一时刻输入和检查前状态复算 `cross()`、`above()`、periodic `timer()`、absolute `timer()` 是否 due，并把 match/mismatch/error 聚合进 simulator counters。

## Why This Cut Exists

050-052 已经有 transition/timer/cross/above 的 Rust typed-array primitives，但它们之前只在 primitive unit test 中和 Python oracle 对齐。056 把这些 primitive 接到真实 engine 检测入口旁边，回答一个更关键的问题：

```text
真实仿真过程中，Python 当前会检查的 event due 状态，Rust 是否能逐步复现？
```

这一步仍然不是加速。它是 production event queue Rust 化前的 correctness gate。

## Changed Code

| File | Change |
|---|---|
| `EVAS/evas/simulator/backend.py` | `CompiledModel` 增加 `_set_rust_event_due_shadow_backend()`，在 `_check_cross()`、`_check_above()`、`_check_timer_due()`、`_check_timer_at()` 后做 Rust shadow compare |
| `EVAS/evas/simulator/engine.py` | `Simulator.run(..., rust_event_due_shadow=False)` 增加 opt-in flag、Rust backend early load、shadow counter 聚合 |
| `EVAS/evas/netlist/runner.py` | 增加 `EVAS_RUST_EVENT_DUE_SHADOW=1` / `evas_rust_event_due_shadow=true` 入口和日志 |
| `EVAS/tests/test_engine.py` | hand-built model 覆盖 cross/above/periodic timer/absolute timer shadow parity |
| `EVAS/tests/test_netlist.py` | netlist runner smoke 验证环境变量、日志 counters、未强制 indexed arrays |

## Runtime Contract

打开方式：

```text
EVAS_RUST_EVENT_DUE_SHADOW=1
```

或 netlist simopt：

```text
evas_rust_event_due_shadow=true
```

新增 counters：

| Counter | Meaning |
|---|---|
| `rust_event_due_shadow_requested` | 用户是否请求该 shadow 路径 |
| `rust_event_due_shadow_available` | Rust backend 是否成功加载 |
| `rust_event_due_shadow_enabled` | 是否已安装到 model tree |
| `rust_event_due_shadow_cross_checks_total` | shadow 覆盖的 `_check_cross()` 次数 |
| `rust_event_due_shadow_above_checks_total` | shadow 覆盖的 `_check_above()` 次数 |
| `rust_event_due_shadow_timer_periodic_checks_total` | shadow 覆盖的 `_check_timer_due()` 次数 |
| `rust_event_due_shadow_timer_absolute_checks_total` | shadow 覆盖的 `_check_timer_at()` 次数 |
| `rust_event_due_shadow_matches_total` | Rust/Python due + detector/timer state 完全匹配次数 |
| `rust_event_due_shadow_mismatches_total` | Rust/Python 不一致次数 |
| `rust_event_due_shadow_errors_total` | Rust call 或 buffer compare 抛错次数 |
| `rust_event_due_shadow_max_time_diff_total` | crossing/timer state 时间字段最大差异 |

## Correctness Boundary

Shadow 比较的是：

- `cross()` / `above()` detector state update
- crossing triggered flag
- crossing time
- trigger direction / went-beyond flag for `cross()`
- periodic timer due / skipped / next-fire state before reschedule
- absolute timer due / expired / last-fired state

Shadow 不比较、也不替代：

- event body execution
- event body write-set
- event ordering queue
- event-context voltage interpolation side effects
- transition target execution after event body
- record / CSV / checker path

也就是说，056 证明的是“Rust 可以复算 event due 检测层”，不是“event system 已 Rust 化”。

## Verification

Fresh local checks:

```text
PYTHONPATH=EVAS python3 -m pytest EVAS/tests/test_engine.py EVAS/tests/test_netlist.py -q -k "rust_event_due_shadow"
2 passed, 300 deselected

PYTHONPATH=EVAS python3 -m pytest EVAS/tests/test_engine.py -q
225 passed

PYTHONPATH=EVAS python3 -m pytest EVAS/tests/test_netlist.py -q
77 passed

PYTHONPATH=EVAS python3 -m pytest EVAS/tests/test_rust_backend.py -q
18 passed

cargo test
25 passed
```

## Speed Impact

Expected speed impact in normal runs: none, because the flag defaults to off.

Expected speed impact when enabled: slower, because every event due check does an additional Rust FFI call and state comparison. This is intentional. The purpose is parity evidence, not acceleration.

## Learning Note

这里的“shadow”可以理解成旁边放一个审计员：

```text
Python: 真的开关灯、改状态、继续仿真
Rust:   用同样输入在草稿纸上算一次，告诉我们结果是否一致
```

只有 shadow 长期没有 mismatch，才适合把某一层从“审计员”升级为“真正执行者”。

## Next Step

057 应该做 event ordering shadow：当同一步存在多个 due event 时，Rust 生成稳定的 chronological/source-order trace，和 Python 当前 retrograde suppression / source-order fallback 对齐。只有 due + ordering 都能解释，后面才有资格审计 event body write-set。
