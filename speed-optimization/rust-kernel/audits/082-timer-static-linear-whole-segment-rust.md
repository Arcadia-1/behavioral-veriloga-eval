# 082 Timer Static Linear Whole Segment Rust

## 核心结论

这一轮把一条保守但完整的仿真行为链迁到 Rust：

```text
periodic timer due/reschedule
-> event body static-linear state update
-> non-event static-linear output evaluate
-> explicit-record trace with timer breakpoints
```

也就是说，对命中 gate 的模型，Python 不再每个 record point 逐步执行 timer 检查、event body、output evaluate 和 record 读取，而是一次 FFI 调用把整条 fixed trace 交给 Rust 生成。

这不是全量 EVAS Rust 化。它是 B10/B11/B15/B18 的一个完整 segment executor，覆盖的是周期 timer + 简单 state event body + 简单输出贡献这一类行为。

## 改造原理

原来的 Python 路径按时间点循环：

```text
for t in times:
  update sources
  check timer due
  if due:
    execute event body
  evaluate model output
  record requested signals
```

这个循环慢的地方不是数学复杂，而是每步反复进 Python 对象系统：

- timer 状态在 Python dict/对象字段里检查和更新；
- event body 逐条 Python assignment 执行；
- output evaluate 读写 node/state dict 或 indexed sidecar；
- record 再按 signal name 查 node value。

本轮把这些动作降低为 Rust array loop：

```text
while t >= next_fire:
  state_values[...] = linear_expr(state_values, node_values)
node_values[source_id] = source(t)
node_values[out_id] = linear_expr(state_values, node_values)
out_trace[row, col] = node_values[record_id]
```

核心数学形式仍是有序线性表达：

```text
target = bias + sum(gain_i * source_i)
```

条件赋值会被 lowering 成：

```text
target = condition ? true_linear_expr : false_linear_expr
```

integer state 写入仍按 Verilog-A integer 语义做截断。由于 Rust 执行顺序和 Python event body statement 顺序一致，自依赖更新例如 `toggle = 1 - toggle` 和 `acc = acc + 2` 可以保持等价。

## Production Gate

当前 production Rust fastpath 只在以下条件同时满足时启用：

| Gate | 原因 |
|---|---|
| exactly one model | 避免跨 model order、parent/child node sync 和 hierarchy side effect |
| no child models | child model lifecycle/order 尚未进入 Rust segment |
| exactly one `timer(start, period)` | 多 timer 同步排序还没迁到 Rust event queue |
| explicit `record_step` | 当前 Rust trace 以用户记录点加周期 timer breakpoint 为边界；默认 EVAS 可能插入更多 adaptive/internal points |
| non-negative timer start | 负 start 的 pre-simulation firing 语义先保守 fallback |
| event body target 只写 state | event-owned output write 和 transition output 还没进入这条 generic path |
| event body 不读 node | 避免 event time source interpolation / crossing-time node value 语义错误 |
| evaluate target 只写 node | 输出贡献可以直接进入 `node_values` array |
| non-event evaluate 是 static-linear IR | 非线性、系统任务、动态数组、复杂 control flow 仍 fallback |

这些 gate 的目标是保守：宁可 fallback 到 Python，也不让 Rust 路径默默改变 waveform。

## 改动内容

| 文件 | 改动 |
|---|---|
| `EVAS/evas/simulator/backend.py` | 编译期记录 `_event_timer_static_linear_ir_ops`，并收集非 event 的 `_evaluate_ir_static_linear_non_event_ops` |
| `EVAS/evas/rust_core/src/lib.rs` | 新增 `timer_static_linear_trace_for_arrays()` 和 C ABI `evas_rust_timer_static_linear_trace()` |
| `EVAS/evas/simulator/rust_backend.py` | 新增 `RustBackend.timer_static_linear_trace()`，把 Python typed arrays 传给 Rust trace executor |
| `EVAS/evas/simulator/engine.py` | 新增 `_try_timer_static_linear_fastpath()`，命中 gate 时直接返回 Rust 生成的 `SimResult` |
| `EVAS/tests/test_engine.py` | 新增 timer counter parity regression，验证 Rust trace 与默认 EVAS fixed-record trace 一致 |

## 为什么要求 `record_step`

这里要特别小心：EVAS 默认 transient loop 不只输出用户关心的固定记录点。发生 output jump 或 error-control 触发时，它可能插入额外 internal/adaptive points。

本轮 Rust path 生成的是显式记录 trace：基础时间轴来自 `record_step`，再补上周期 timer 的 fire time。这样即使 `period=700ps`、`record_step=250ps` 这类不对齐情况，也会保留 `700ps`、`1.4ns` 等 timer breakpoint。

只有在用户明确给出 `record_step` 时，时间轴才有同一个可比较边界。没有 `record_step` 时，fastpath 会自动 fallback。

这不是精度降低，而是当前 fastpath 的 trace contract 更窄。后续如果要支持默认 adaptive trace，需要把 error-ratio scan、breakpoint/refine 和 internal-point emission 一起迁到 Rust。

## 验证结果

```text
PYTHONPYCACHEPREFIX=/private/tmp/vaevas_pycache PYTHONPATH=/Users/bucketsran/Documents/TsingProject/vaEvas/EVAS python3 -m py_compile \
  /Users/bucketsran/Documents/TsingProject/vaEvas/EVAS/evas/simulator/backend.py \
  /Users/bucketsran/Documents/TsingProject/vaEvas/EVAS/evas/simulator/engine.py \
  /Users/bucketsran/Documents/TsingProject/vaEvas/EVAS/evas/simulator/rust_backend.py
PASS
```

```text
cargo test --manifest-path /Users/bucketsran/Documents/TsingProject/vaEvas/EVAS/evas/rust_core/Cargo.toml timer_static_linear --release
PASS
```

```text
PYTHONPYCACHEPREFIX=/private/tmp/vaevas_pycache PYTHONPATH=/Users/bucketsran/Documents/TsingProject/vaEvas/EVAS python3 -m pytest \
  /Users/bucketsran/Documents/TsingProject/vaEvas/EVAS/tests/test_engine.py \
  -k "timer_static_linear or timer_event_batch_uses_rust or rust_full_model" -q
2 passed, 235 deselected
```

```text
PYTHONPYCACHEPREFIX=/private/tmp/vaevas_pycache PYTHONPATH=/Users/bucketsran/Documents/TsingProject/vaEvas/EVAS python3 -m pytest \
  /Users/bucketsran/Documents/TsingProject/vaEvas/EVAS/tests/test_rust_backend.py -q
31 passed
```

```text
PYTHONPYCACHEPREFIX=/private/tmp/vaevas_pycache PYTHONPATH=/Users/bucketsran/Documents/TsingProject/vaEvas/EVAS python3 -m pytest \
  /Users/bucketsran/Documents/TsingProject/vaEvas/EVAS/tests/test_engine.py \
  -k "timer or event_write or static_eval or whole_model" -q
47 passed, 190 deselected
```

## 速度影响判断

这条路径理论上会减少四类开销：

| 开销 | 原 Python 路径 | 新 Rust 路径 |
|---|---|---|
| timer due/reschedule | 每步 Python helper/dict 状态 | Rust scalar `next_fire` loop |
| event body | Python assignment/object dispatch | Rust `LinearOp` batch |
| output evaluate | Python generated method + node/state lookup | Rust array linear expression |
| record | Python signal name/node lookup | Rust record node-id copy |

但本轮还没有给出 release-wide speed claim。它只证明一类完整 segment 的迁移可行，并用 regression 锁住 parity。真正速度收益要看 top-wall 或 release runner 中有多少模型满足这个 gate。

## 仍未完成

| 未完成行为 | 为什么没迁 |
|---|---|
| multiple timers | 需要全局 event queue ordering，不能只按单 timer `next_fire` 推进 |
| `cross()` / `above()` production queue | 需要 crossing-time interpolation、prev/current/future node values 和 detector state 一起进 Rust |
| event body 读 node | timer body 读 source 时涉及 event-time source sampling；cross body 读 node 时涉及 interpolation |
| event-owned output write | 需要把离散 output write、continuous contribution、record/snapshot 的先后关系一起固化 |
| `transition()` output | 需要 target update、ramp state evolution、breakpoint/refine 和 record 一起迁 |
| default adaptive trace | 需要迁 error-ratio scan、breakpoint/refine 和 internal-point emission |
| dynamic arrays/buses | 需要 B17 offset primitive 与 state/node layout 在 production path 合并 |

## 下一步

下一步不应该继续做单点小 FFI。更有效的方向是把这个模式推广成 event queue 级 Rust segment：

1. 支持多个 timer 的 due mask 和 source-order event ordering。
2. 把 event body output write 和 continuous output contribution 合并到同一个 record trace executor。
3. 增加 cross/above detector + interpolation arrays，先 shadow parity，再 production gate。
4. 把 `transition()` target/state/record 合进同一段 typed-array loop。
