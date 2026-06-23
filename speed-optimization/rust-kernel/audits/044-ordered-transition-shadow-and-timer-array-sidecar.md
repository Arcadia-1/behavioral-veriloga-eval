# 044 - Ordered Transition Shadow And Timer Array Sidecar

Status: `done`

Date: `2026-06-03`

Code commit: `pending`

Related files:

- `EVAS/evas/simulator/evaluate_ir.py`
- `EVAS/evas/simulator/backend.py`
- `EVAS/evas/simulator/engine.py`
- `EVAS/evas/simulator/rust_backend.py`
- `EVAS/evas/netlist/runner.py`
- `EVAS/evas/rust_core/src/lib.rs`
- `EVAS/tests/test_indexed_backend.py`
- `EVAS/tests/test_rust_backend.py`
- `EVAS/tests/test_engine.py`
- `EVAS/tests/test_netlist.py`

## One-Line Summary

044 把 static-linear evaluate 和 transition target evaluate 放进同一个 Rust ordered batch 做 shadow/parity，同时把 timer scan 前的状态从每次 dict 打包改成模型维护的 typed array sidecar；默认仿真结果不变，这仍是 Rust 化前置验证，不是最终速度 claim。

## What Changed

| Layer | Before | After | User-visible behavior |
|---|---|---|---|
| Ordered transition segment | static-linear evaluate 和 transition target executor 是两段独立能力 | 新增 ordered segment metadata：先执行 static-linear writes，再执行 transition target evaluate | 仅 shadow/parity 使用 |
| Rust core | Rust 可分别执行 static-linear 和 transition target | 新增 `evaluate_ordered_transition_segment` 和 C ABI | 仅 opt-in/test path 使用 |
| Simulator engine | 没有验证 Rust batch 是否能复现 Python transition target ordering | 新增 `rust_transition_shadow`：Python evaluate 后用 Rust batch replay，并比较 `target/delay/rise/fall` | 默认关闭，不写回真实状态 |
| Netlist runner | 只能打开 Rust static eval / fast sync | 新增 `EVAS_RUST_TRANSITION_SHADOW=1` 和 `evas_rust_transition_shadow=true` | 只增加日志和 perf counters |
| Timer state | Rust timer scan 前每次从 `timer_states` / `timer_last_fired` dict 组 arrays | `_set_timer_state()` / `_set_timer_last_fired()` 维护 `array("d")` / `array("B")` sidecar，scan 直接读数组 | timer 语义不变 |
| ctypes timer flags | timer flag 每次转换成 ctypes `uint8` array | 对 `array("B")` 走 from-buffer zero-copy path | 只影响 opt-in Rust timer scanner |

## Principle

这轮做的是两个“前置但已经接近核心”的改造。

第一，`transition()` 的正确性不只取决于 target 表达式，还取决于 evaluate 中前面的 state/node write 是否已经按顺序发生。例如：

```verilog
q = V(inp) > 0.45 ? 1 : 0;
V(out) <+ transition(q ? 1.0 : 0.0, 0.0, 1n, 2n);
```

如果 Rust 只单独计算 transition target，它必须读到 Python 已经更新后的 `q`。更稳的方式是把“写 q”和“读 q 生成 transition target”放进同一个 ordered Rust batch：

```text
state[q] = condition(node[inp]) ? 1 : 0
target[trans_0] = condition(state[q]) ? 1.0 : 0.0
delay/rise/fall = constants/parameters
```

这就是本轮 shadow/parity 的数学含义：同一个 Rust batch 能复现 Python generated evaluate 的顺序语义。

第二，timer scan 真正想优化的是每步找最早 timer breakpoint 的 hot loop。043 已经把 scan 本身接到 Rust，但 scan 前仍然需要：

```text
timer_states dict -> next_fire_times array
timer_last_fired dict -> last_fired_times array + flags
```

044 把这段打包工作从“每次 scan”挪到“timer 状态变化时”。timer dict 仍是权威状态，typed arrays 是 sidecar；因此语义风险低，但能减少 Rust scan 前的 Python dict/object/string key 开销。

## Before / After Evidence

这轮没有跑 top-wall 或 vaBench full speed rerun，因此没有新增真实 benchmark 速度结论。验证目标是功能 parity、FFI 可用性和 timer sidecar 行为。

| Check | Result | Meaning |
|---|---:|---|
| `cargo test` | `17 passed` | Rust ordered segment、transition target、timer scan、C ABI 均通过 |
| `cargo build --release` | `passed` | release cdylib 可构建，Python ctypes 可加载新增 ABI |
| `tests/test_rust_backend.py -q` | `11 passed` | ctypes wrapper 可调用 ordered transition segment 和 timer array scan |
| `tests/test_indexed_backend.py -k "transition_target or ordered_transition or static_linear"` | `10 passed, 28 deselected` | transition key metadata、ordered segment metadata、Python IR parity 通过 |
| `tests/test_engine.py -k "rust_transition_shadow or rust_timer or timer_sidecar or timer_scanner"` | `3 passed, 212 deselected` | simulator shadow counters、timer sidecar rebuild/update path 通过 |
| `tests/test_netlist.py -k "rust_transition_shadow or rust_static"` | `4 passed, 72 deselected` | netlist/env option 和 log counters 通过 |
| EVAS full regression | `509 passed` | 默认路径和已有 opt-in regression 未被破坏 |

Targeted commands:

```bash
cargo test
cargo build --release
python3 -m pytest tests/test_rust_backend.py -q
python3 -m pytest tests/test_indexed_backend.py -k "transition_target or ordered_transition or static_linear" -q
python3 -m pytest tests/test_engine.py -k "rust_transition_shadow or rust_timer or timer_sidecar or timer_scanner" -q
python3 -m pytest tests/test_netlist.py -k "rust_transition_shadow or rust_static" -q
python3 -m pytest -q
```

## Functional Safety

- Default backend changed: `no`
- CSV schema changed: `no`
- Checker behavior changed: `no`
- Event ordering changed: `no`
- Production `transition()` state update moved to Rust: `no`
- Production generated `evaluate()` replaced by ordered Rust segment: `no`
- Timer dict removed: `no`; dict remains authoritative
- Rust transition shadow default-on: `no`
- Timer sidecar affects non-Rust timer path: `no`; Python fallback loop still reads dict

Important boundary:

- `rust_transition_shadow` only compares Rust replay against Python `TransitionState`; it does not write Rust target values back.
- transition key parity currently depends on metadata collection and generated code using the same AST traversal order (`trans_0`, `trans_1`, ...).
- timer sidecar assumes timer mutation goes through `_set_timer_state()` / `_set_timer_last_fired()`; direct dict mutation is still tolerated for first scan by rebuilding the sidecar, but it is not the intended hot path.

## Learning Notes

### 什么叫 shadow/parity？

shadow 的意思是“旁路执行”。真实仿真仍然走 Python：

```text
Python evaluate -> 更新 model.transitions
Rust ordered batch -> 在数组副本上重放同一段逻辑
compare Rust target/delay/rise/fall vs Python TransitionState
```

Rust 结果不参与真实波形输出。这样我们可以先证明 Rust 语义正确，再决定是否把这段切成 production fast path。

### 为什么要把 static-linear 和 transition target 放在同一个 batch？

因为 transition target 往往依赖前面刚写的 state。单独 Rust 化 target 会遇到一个问题：它读到的是“Python 已经写过的 state”，还是“这一步开始前的 state”？ordered batch 把这个问题消掉：

```text
同一个 node/state array 副本
按 evaluate 顺序执行所有可 lower 的 static-linear write
再计算 transition target
```

这和未来完全 Rust 化的模型 evaluate 更接近。

### timer typed array sidecar 为什么能减少开销？

Python dict 适合表达 `timer_states["timer_0"] = 1e-9` 这种语义，但每步扫描时不适合高频循环：

- dict 需要 hash/string key lookup；
- 每次 Rust scan 前都要新建 array；
- flags 还要从 Python list 转 ctypes buffer。

typed array sidecar 把 timer 状态维护成连续内存：

```text
keys_by_id[i] -> timer key
next_fire_values[i] -> next fire time
last_fired_values[i] -> last fired target
has_last_fired_flags[i] -> 0/1
```

scan 时 Rust 可以直接读这些连续数组。这里减少的是“每步 Python 打包成本”，不是减少仿真步数。

## Risks And Rollback

| Risk | Signal | Rollback |
|---|---|---|
| ordered segment 误判可 Rust 化 | `rust_transition_shadow_mismatches > 0` | 保留 metadata，关闭/回退 shadow plan builder |
| transition key 与 Python generated code 不一致 | `rust_transition_shadow_skips` 增加，找不到 `model.transitions[key]` | 回退 transition key metadata，或改为 generated code 显式导出 key map |
| timer sidecar 与 dict 不一致 | timer breakpoint regression 失败，或 sidecar rebuild/update counters 异常 | 回退 `_next_timer_breakpoint()` 到 043 的每次 dict packing |
| Rust timer scan ABI flags 错误 | consumed absolute timer 被重新触发 | 回退 `_uint8_buffer()` zero-copy path 或 Rust timer scanner install |

## Next Step

045 应该从 shadow 走向真正的 production fast path，但仍然分阶段：

1. 把 ordered transition segment coverage 跑到真实 top-wall transition models，统计可覆盖/不可覆盖原因。
2. 对 shadow mismatch/skip 做诊断报告，确认 transition key 和默认 rise/fall 语义在真实模型上稳定。
3. 选择低风险模型，把 ordered batch 从 shadow 改成 opt-in production target update，但仍让 transition state update/evaluate ramp 保持 Python。
4. 再迁移 transition state update 和 ramp evaluate 到 Rust typed arrays。
5. 最后才处理 event/timer queue、cross/above detector 和 event body dispatch。
