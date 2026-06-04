# 043 - Transition Target Executor And Timer Array Scan

Status: `done`

Date: `2026-06-03`

Code commit: `pending`

Related files:

- `EVAS/evas/simulator/evaluate_ir.py`
- `EVAS/evas/simulator/backend.py`
- `EVAS/evas/simulator/engine.py`
- `EVAS/evas/simulator/rust_backend.py`
- `EVAS/evas/rust_core/src/lib.rs`
- `EVAS/tests/test_indexed_backend.py`
- `EVAS/tests/test_rust_backend.py`
- `EVAS/tests/test_engine.py`

## One-Line Summary

043 把 042 记录的 `transition()` target IR 推进到可执行的 Python/Rust array executor，并把 timer breakpoint scan 接到 Rust C ABI 和 simulator hook；这仍是 event/evaluate Rust 化的内核前进步骤，不是最终速度 claim。

## What Changed

| Layer | Before | After | User-visible behavior |
|---|---|---|---|
| Transition target IR | 只有 `_transition_target_ir_ops` metadata | 新增 `TransitionTargetIR` 和 Python array executor，可按 node/state arrays 计算 target/delay/rise/fall buffers | 默认波形不变 |
| Rust transition target executor | Rust 只能执行 static-linear state/node write | 新增 `EvasRustTransitionTargetOp` 和 `evas_rust_evaluate_transition_targets` C ABI | 仅 opt-in/test path 使用 |
| ctypes wrapper | Python 不能批量调用 Rust transition target executor | 新增 `TransitionTargetOp` / `RustTransitionTargetBatch` / `evaluate_transition_targets()` | 默认 backend 不变 |
| Timer breakpoint scan | `_next_timer_breakpoint()` 每次 cache miss 遍历 Python dict | Rust core 新增 timer array scan C ABI；Rust array loop 下 model 可调用 scanner，异常回退 Python loop | event ordering 不变 |
| Simulator counters | 只统计 Python timer scan/cache | 新增 `rust_timer_breakpoint_*` model 和 simulator 汇总 counters | 便于后续 profile |

## Principle

这轮改动继续遵守一个原则：**先把 Python 对象路径拆成 typed array IR，再迁移执行循环；不要一次性搬整个事件系统。**

### 1. Transition target executor 为什么重要？

真实 event-heavy 模型里，`transition()` 常常写成：

```verilog
V(out) <+ transition(q ? 1.0 : 0.0, 0.0, tr, tf);
```

这里真正每步重复计算的是 target 表达式。042 已经能把它记录成 IR，043 进一步让这个 IR 变成可执行 array loop：

```text
target[id] = condition(state/node arrays) ? linear_true : linear_false
delay[id]  = delay
rise[id]   = rise
fall[id]   = fall
```

它和 static-linear evaluate IR 的数学结构一样，都是：

```text
y = bias + sum(gain_i * source_i)
```

区别只是 target 不直接写 `node_values` 或 `state_values`，而是写 transition state 所需的 target/delay/rise/fall buffers。这样后续才能把 `transition state update` 从 generated Python expression 迁到 Rust。

### 2. Timer scan 为什么先只搬“扫描”？

当前 `_next_timer_breakpoint()` 的语义很窄：

```text
在 timer_states 中找 nf > time 的最小 nf；
如果 timer_last_fired[key] == nf，则跳过这个已经触发过的 absolute timer。
```

Rust timer scan 不改变 timer reschedule，也不改变 `@(timer(...))` event body 执行。它只把“找最早下一触发点”的循环迁到 Rust array function：

```text
next_fire_times[] + last_fired_times[] + has_last_fired_flags[] -> earliest breakpoint
```

这一步的直接收益可能有限，因为目前 Python 仍需要把 dict 临时打包成 arrays；但它证明了 timer event queue 的 ABI 形状，下一步可以把 timer state 本身也改成 typed storage，避免每步 dict packing。

## Before / After Evidence

这轮没有跑新的 top-wall speed rerun，因此没有新增速度结论。验证目标是功能 parity 和 hook 可用性。

| Check | Result | Meaning |
|---|---:|---|
| `cargo test` | `15 passed` | Rust transition target executor、timer array scan、C ABI 均通过 |
| `tests/test_rust_backend.py` | `10 passed` | ctypes wrapper 可调用 transition target executor 和 timer scanner |
| `tests/test_indexed_backend.py -k 'transition_target or static_linear'` | `9 passed, 28 deselected` | Python IR executor/metadata 与 static-linear 相关测试通过 |
| `tests/test_engine.py -k 'rust_timer or rust_transition or timer_cache or next_breakpoint_includes_timer or ignores_consumed_absolute_timer'` | `8 passed, 205 deselected` | model hook、simulator install、timer cache 兼容性通过 |
| EVAS full regression | `504 passed` | 默认路径和已有 opt-in regression 未被破坏 |
| Rust release build | `passed` | release cdylib 可构建 |
| Diff whitespace check | `passed` | EVAS diff 和 rust-kernel 文档 diff 无 whitespace error |

Targeted commands:

```bash
cargo test
python3 -m pytest tests/test_rust_backend.py -q
python3 -m pytest tests/test_indexed_backend.py -k 'transition_target or static_linear' -q
python3 -m pytest tests/test_engine.py -k 'rust_timer or rust_transition or timer_cache or next_breakpoint_includes_timer or ignores_consumed_absolute_timer' -q
python3 -m pytest -q
cargo build --release
git diff --check
```

## Functional Safety

- Default backend changed: `no`
- CSV schema changed: `no`
- Checker behavior changed: `no`
- Event ordering changed: `no`
- `transition()` state update moved to Rust: `no`
- Generated Python `evaluate()` replaced: `no`
- Rust timer scanner default-on: `no`; only when Rust backend and indexed array loop already enabled
- Rust timer scanner fallback: `yes`; scanner exception falls back to original Python dict loop

Important boundary:

- Transition target executor is ready but not yet wired into production evaluate ordering.
- Timer scan currently still receives arrays built from Python dict state.
- Cross/above detector、source breakpoint、`$bound_step`、event body dispatch 仍在 Python 路径。

## Learning Notes

### 什么叫“可执行 IR”？

042 的 transition target IR 只是“记录了可以怎么算”。043 的 executor 是“真的能按数组算出结果”。这两者差别很关键：

- metadata 只能告诉我们某段代码可能 Rust 化；
- executor 才能证明同一段数学表达式能离开 Python object/dict 路径运行。

### 为什么现在还不能说 transition 已经 Rust 化？

因为完整 `transition()` 不只是 target 表达式，还包括：

1. 读取当前 transition state；
2. 判断 target 是否改变；
3. 设置 start time/start value/target value；
4. 生成 ramp 中间断点；
5. 在每个时间点 evaluate ramp 输出。

043 只覆盖第 1 步之前的 target 表达式 executor，以及第 4 步中的 breakpoint scan。它们是核心部件，但还没有串成完整 Rust transition pipeline。

### 为什么 timer scan 接了 Rust 但速度不一定立刻明显变快？

因为现在仍然有一段 Python 工作：

```text
dict timer_states -> array("d") next_fire_times
dict timer_last_fired -> array("d") last_fired_times + flags
Rust scan -> result
```

如果 timer 数量很少，FFI 和 array packing 可能比 Python 原循环还贵。真正大收益要等 timer state 本身变成 typed arrays，scan 才能做到“无 dict packing、无字符串 key lookup”。

## Risks And Rollback

| Risk | Signal | Rollback |
|---|---|---|
| Rust transition target ABI 布局错误 | `test_rust_backend.py` transition target test 失败 | revert `EvasRustTransitionTargetOp` 和 ctypes wrapper |
| Timer scan 漏掉已触发 absolute timer | `test_next_breakpoint_ignores_consumed_absolute_timer` 或 timer scanner test 失败 | disable `_set_rust_timer_breakpoint_scanner()` install path |
| Rust timer scanner 引入异常 | `rust_timer_breakpoint_fallbacks_total > 0` 或 waveform regression | 保留 ABI，但不在 simulator 中安装 scanner |
| 误把 executor 当成 production evaluate | top-wall waveform 或 parity 出现变化 | 回退 transition target executor wiring；metadata/executor test 可保留 |

## Next Step

044 建议继续做真正的 ordered transition pipeline 前置，而不是零散修 Python 小热点：

1. 给 transition target executor 加 coverage report：统计真实 top-wall 模型里 target 可 Rust 化/不可 Rust 化的原因。
2. 建立 ordered evaluate segment：把 `static-linear evaluate` 和 `transition target evaluate` 放进同一个 per-step Rust batch，但仍先只做 shadow/parity。
3. 把 timer state 从 dict sidecar 推到 typed arrays，减少当前 timer Rust scan 前的 dict packing。
4. 再迁移 transition state update/evaluate ramp；最后才处理 cross/above detector 和 event body dispatch。
